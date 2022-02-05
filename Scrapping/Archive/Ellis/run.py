import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
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


if __name__=="__main__":
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
    out_sheet = output_client.open('EllisCounty')
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
    
    for street in input_streets:
        print(f"Scrapping {street} ......")
        driver.get("https://actweb.acttax.com/act_webdev/ellis/index.jsp")
        time.sleep(1)
        driver.find_element(By.XPATH, 
                            "/html/body/div[1]/div/div[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/center/form/table/tbody/tr[3]/td[2]/h3[4]/b/input[2]").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, 
                            "/html/body/div[1]/div/div[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/center/form/table/tbody/tr[3]/td[2]/h3[2]/input").send_keys(street)
        time.sleep(0.5)
        driver.find_element(By.XPATH, 
                            "/html/body/div[1]/div/div[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/center/form/table/tbody/tr[5]/td[2]/h3[2]/input").click()
        time.sleep(1)
        try:
            table = driver.find_element(By.XPATH, 
                                        "/html/body/div/div/div[2]/table/tbody/tr[1]/td/form/div").get_property("innerHTML")
            df = pd.read_html(table)[0]
            accounts = list(df["Account Number"])[2:]
            accounts_list = []
            owners = []
            addresses = []
            cities = []
            property_address = []
            total_due = []
            gross_value = []
            for account in accounts:
                try:
                    driver.get(f"https://actweb.acttax.com/act_webdev/ellis/showdetail2.jsp?can={account}")
                    time.sleep(0.5)
                    table_data = driver.find_element(By.XPATH, 
                                                    "/html/body/div/div/div[2]/table/tbody/tr[2]/td/table[2]/tbody/tr").get_property("innerHTML")
                    soup = BeautifulSoup(table_data, "lxml")
                    table_text = [i for i in soup.find_all("h3")]
                    address_detail = [i.text.replace("\t", "").replace("\n", "") for i in table_text[1] if i.text.replace("\t", "").replace("\n", "")!=""]
                    accounts_list.append(account)
                    owners.append(address_detail[2].replace("  ", ""))
                    addresses.append(address_detail[3])
                    cities.append(address_detail[-1].split("  ")[0])
                    property_address.append([i.text.replace("\t", "").replace("\n", "") for i in table_text[2]][2].replace("  ", ""))
                    table_text_list = [i.text for i in table_text]
                    for i in table_text_list:
                        if "Total Amount Due" in i:
                            total_due.append(i.split("\xa0")[1])
                        elif "Gross Value" in i:
                            gross_value.append(i.split("\xa0")[1])
                except:
                    accounts_list.append(account)
                    owners.append("")
                    addresses.append("")
                    cities.append("")
                    property_address.append("")
                    total_due.append("")
                    gross_value.append("")
            
            final_dataframe = pd.DataFrame(zip(accounts_list, owners, addresses, cities, property_address, total_due, gross_value), 
                                        columns=["Account", "Owner", "Address", "City", "Property Site Address", "Total Amount Due", "Gross Value"])
        except:
            final_dataframe = pd.DataFrame([["", "", "", "", "", "", ""]], 
                                           columns=["Account", "Owner", "Address", "City", "Property Site Address", "Total Amount Due", "Gross Value"])
            
        out_sheet.add_worksheet(rows=final_dataframe.shape[0], cols=final_dataframe.shape[1], title=street)  # Creat a new sheet
        work_sheet_instance = out_sheet.worksheet(street) # get that newly created sheet
        set_with_dataframe(work_sheet_instance, final_dataframe) # Set collected data to sheet
    
    print("=="*30)
    print("Prgrame is Finished.")
    print("=="*30)
    exit()