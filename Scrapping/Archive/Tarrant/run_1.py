import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def initChromeDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=1")
    options.add_argument('--start-maximized')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
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

def get_pagination(pagination, url):
    pagination = [i.text.replace("\t", '').replace("\n", '') for i in pagination]
    pagination = [i for i in pagination if i!='']
    pagination_list = []
    if len(pagination)>2:
        pagination = pagination[:-3]
        for page in range(int(pagination[-1])):
            pagination_list.append(url+f"?pg={page+1}")
    return pagination_list

def get_table(soup):
    soup = soup.find("table")
    rows = soup.find_all("tr", class_="view_more_summary")
    table = []
    for row in rows:
        temp_row = []
        for col in row:
            temp_row.append(col.text.replace("\t", '').replace("\n", ""))
        temp_row = [i for i in temp_row if i!='']
        table.append(temp_row)
    return pd.DataFrame(table, columns=["Account", "Property Address", "Property City", "Primary Owner Name", "Market Value"])

def fake_input(driver):
    driver.get("https://www.tad.org/property-search/")
    time.sleep(1)
    driver.find_element(By.XPATH, 
                        "/html/body/div[3]/div[3]/div[2]/div[2]/form/div/div/div/span[4]/label").click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, 
                        "/html/body/div[3]/div[3]/div[3]/form/div/div[3]/div[1]/div[1]/div[1]/input").clear()
    time.sleep(0.5)
    driver.find_element(By.XPATH, 
                        "/html/body/div[3]/div[3]/div[3]/form/div/div[3]/div[1]/div[1]/div[1]/input").send_keys("wilson")
    time.sleep(0.5)
    driver.find_element(By.XPATH, 
                        "/html/body/div[3]/div[3]/div[3]/form/div/div[3]/div[1]/div[5]/input").click()
    time.sleep(1)
    driver.find_element(By.XPATH, 
                        "/html/body/div[3]/div[8]/div[1]/form/div[1]/div[4]/label").click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, 
                        "/html/body/div[3]/div[8]/div[1]/form/div[1]/input").click()
    time.sleep(1)

if __name__=='__main__':
    print("Getting Google SpreadSheets...")
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    # Get input file
    creds = ServiceAccountCredentials.from_json_keyfile_name('input.json', scope)
    streets_client = gspread.authorize(creds)
    # Get output File
    out_creds = ServiceAccountCredentials.from_json_keyfile_name('output.json', scope)
    output_client = gspread.authorize(out_creds)
    #Clear Output spreadsheet
    out_sheet = output_client.open('Street Output')
    out_sheets_list = out_sheet.worksheets()
    out_sheets_list.reverse()
    for o_sheet in out_sheets_list[:-1]:
        out_sheet.del_worksheet(o_sheet)
    # Open input spreadsheet and get all the input streets
    sheet = streets_client.open('Streets')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)
    input_streets = records_df["Streets"].tolist()
    
    driver = initChromeDriver()
    driver.implicitly_wait(10)
    driver.refresh()
    fake_input(driver)
    
    for street in input_streets:
        print(f"Scrapping {street} ..... ")
        driver.get("https://www.tad.org/property-search/")
        time.sleep(1)
        time.sleep(0.5)
        driver.find_element(By.XPATH, 
                            "/html/body/div[3]/div[3]/div[3]/form/div/div[3]/div[1]/div[1]/div[1]/input").clear()
        time.sleep(0.5)
        driver.find_element(By.XPATH, 
                            "/html/body/div[3]/div[3]/div[3]/form/div/div[3]/div[1]/div[1]/div[1]/input").send_keys(street)
        time.sleep(0.5)
        driver.find_element(By.XPATH, 
                            "/html/body/div[3]/div[3]/div[3]/form/div/div[3]/div[1]/div[5]/input").click()
        time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        pagination = soup.find('div', class_ = "itemPagination property-search-pagination")
        pagination_list = get_pagination(pagination=pagination, url= driver.current_url)
        all_tables = []
        if pagination_list!=[]:
            for page in pagination_list:
                time.sleep(1)
                driver.get(page)
                soup = BeautifulSoup(driver.page_source, 'lxml')
                all_tables.append(get_table(soup=soup))
        else:
            all_tables.append(get_table(soup=soup))
        
        final_dataframe = pd.concat(all_tables)
        final_dataframe.to_csv("oo.CSV", index=False)
        
        out_sheet.add_worksheet(rows=final_dataframe.shape[0], cols=final_dataframe.shape[1], title=street)  # Creat a new sheet
        work_sheet_instance = out_sheet.worksheet(street) # get that newly created sheet
        
        set_with_dataframe(work_sheet_instance, final_dataframe) # Set collected data to sheet
        
    driver.close() # Close the driver
    print("================== Program is Finished ====================")