import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def initChromeDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument('--start-maximized')
    options.add_argument('--headless')
    options.add_argument('--incognito')
    options.add_argument('ignore-certificate-errors')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver

def separate_name(sample:list):
    sample = [i for i in sample if (i!='' and i!=" ")]
    sample = sample[2:]
    if sample[0][-1]=="&" and sample[1][-1]!="&":
        name = " ".join(sample[:2])
        address = sample[2]
        #city = " ".join([i for i in sample[3].split(" ") if any(map(str.isdigit, i))==False])
        city = sample[3].split("  ")[0]
    elif sample[1][-1]=="&" and sample[2][-1]!="&":
        name = " ".join(sample[:3])
        address = sample[3]
        city = sample[4].split("  ")[0]
    elif sample[2][-1]=="&":
        name = " ".join(sample[:4])
        address = sample[4]
        city = sample[5].split("  ")[0]
    else:
        name = sample[0]
        address = sample[1]
        city = sample[2].split("  ")[0]
    return [name, address, city]

if __name__=='__main__':
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    # Get input file
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    # Get output File
    out_creds = ServiceAccountCredentials.from_json_keyfile_name('out_credential.json', scope)
    out_client = gspread.authorize(out_creds)
    #Clear Output spreadsheet
    out_sheet = out_client.open('Output')
    out_sheets_list = out_sheet.worksheets()
    out_sheets_list.reverse()
    for o_sheet in out_sheets_list[:-1]:
        out_sheet.del_worksheet(o_sheet)
    # Open input spreadsheet and get all the input streets
    sheet = client.open('Input')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)
    input_streets = records_df["Streets"].tolist()
    # Initialize the chrome
    # Get the dallas country link
    for street in input_streets:
        driver = initChromeDriver()
        # Click and apply input streets
        while True:
            driver.get('https://www.dallasact.com/act_webdev/dallas/searchbyproperty.jsp')
            try:
                WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div[1]/a[2]')))
                break
            except: 
                driver.refresh()
        driver.find_element(By.XPATH, 
                            '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div[1]/a[2]').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, 
                            '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td/center/form/table/tbody/tr[3]/td[2]/h3/input').send_keys(street)
        time.sleep(0.5)
        driver.find_element(By.XPATH, 
                            '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td/center/form/table/tbody/tr[5]/td/center/input').click()
        time.sleep(0.5)
        # Get the pegmentations
        soup = BeautifulSoup(driver.page_source, 'lxml')
        soup = soup.find('div', class_ = 'pagination')
        data_list = []
        pegmentations = []
        if soup:
            for pegment in soup:
                try: pegmentations.append(int(pegment.text))
                except: pass
        # Parse the table accross each pengemtation
        if pegmentations!=[]:
            for pegemnt in pegmentations:
                xpath = f'/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div[3]/div/form/div/a[{pegemnt}]'
                try:
                    driver.find_element(By.XPATH, xpath).click()
                    table = BeautifulSoup(driver.page_source, 'lxml')
                    df = pd.read_html(str(table.find("table", class_= 'tablesorter')))[0]
                    data_list.append(df)
                    time.sleep(2)
                except:
                    print("No Element Exists to click like: ")
                    print(xpath) 
        else:
            table = BeautifulSoup(driver.page_source, 'lxml')
            try:
                df = pd.read_html(str(table.find("table", class_= 'tablesorter')))[0]
                data_list.append(df)
                time.sleep(2)
            except:
                df = pd.DataFrame()
                data_list.append(df)
                time.sleep(2)
        
        data_df = pd.concat(data_list) # merge all the data
        data = data_df.values.tolist()
        final_data = []
        for addresses in data:
            time.sleep(1)
            try:
                account = addresses[0]
                new_link = f"https://www.dallasact.com/act_webdev/dallas/showdetail2.jsp?can={account}&ownerno=0"
                driver.get(new_link)
                while True:
                    try:
                        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table[2]')))
                        break
                    except: 
                        driver.refresh()
                
                table = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table[2]').get_property("innerHTML")
                soup = BeautifulSoup(table, 'lxml')
                soup = soup.find_all('h3')
                storage = []
                storage2 = []
                for values in soup:
                    if values.find('b'):
                        if values.text.replace('\t', '').replace('\n', ''): storage.append(values.text.replace('\t', '').replace('\n', ''))
                        for value in values:
                            temp = value.text.replace('\t', '').replace('\n', '')
                            storage2.append(temp)
                if "Total Amount Due: \xa0     $0.00" in storage[0]: continue
                else:
                    person_name = separate_name(storage2)[0]
                    final_data.append(separate_name(storage2) +
                                      [addresses[2]] + 
                                      [storage[0].split("\xa0")[-1].replace(" ", ''), storage[1].split("\xa0")[1].split(" ")[0]])
                    print(f"|| {person_name} || Scrapped from {street}")
            except: pass
        
        final_dataframe = pd.DataFrame(final_data, columns=["Name", "Address", "City", "Property Site Address","Total Amount due", "Market Value"])
            
        out_sheet.add_worksheet(rows=final_dataframe.shape[0], cols=final_dataframe.shape[1], title=street)  # Creat a new sheet
        work_sheet_instance = out_sheet.worksheet(street) # get that newly created sheet
        
        set_with_dataframe(work_sheet_instance, final_dataframe) # Set collected data to sheet
        
        driver.close() # Close the driver
    print("=============Program is Finised Successfully=============")
    exit() # End the programm
