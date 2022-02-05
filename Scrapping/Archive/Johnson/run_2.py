import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
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

if __name__=='__main__':
    print("Getting SpreadSheets .....")
    scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
    # Get input file
    creds = ServiceAccountCredentials.from_json_keyfile_name('output.json', scope)
    client = gspread.authorize(creds)
    # Get output File
    out_creds = ServiceAccountCredentials.from_json_keyfile_name('final.json', scope)
    out_client = gspread.authorize(out_creds)
    #Clear Output spreadsheet
    out_sheet = out_client.open('Johnson')
    out_sheets_list = out_sheet.worksheets()
    out_sheets_list.reverse()
    for o_sheet in out_sheets_list[:-1]:
        try :out_sheet.del_worksheet(o_sheet)
        except: pass
    # Open input spreadsheet and get all the input streets
    sheet = client.open('Street Output')
    all_input_sheets = sheet.worksheets()
    
    driver = initChromeDriver()
    driver.implicitly_wait(10)
    driver.refresh()

    for input_sheet in all_input_sheets[1:]:
        street = input_sheet.title
        print(f"Working on {street} .....")
        input_data = input_sheet.get_all_records()
        input_df = pd.DataFrame.from_dict(input_data)
        account_list = input_df["Account"].tolist()
        owners = []
        owner_address = []
        property_address = []
        land_state = []
        improve_value = []
        land_value = []
        for account in account_list:
            try:
                driver.get(f"http://search.johnson.manatron.com/search.php?searchStr={account}&searchType=account")
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/div[3]/table/tbody/tr[2]/td[1]/a").click()
                table = driver.find_element(By.XPATH, "/html/body/div[3]").get_property("innerHTML")
                df = pd.read_html(table)[0]
                data_list = df.values.tolist()
                for data in data_list:
                    if data[0]=="Owner Name:":
                        owners.append(data[1])
                    elif data[0]=="Owner Address:":
                        owner_address.append(data[1])
                    elif data[0]=="Property Location:":
                        property_address.append(data[1])
                    elif data[0]=="Land State Code:":
                        land_state.append(data[1])
                    elif data[0]=="Improvement Value":
                        improve_value.append(data[1])
                    elif data[0]=="Land Market Value:":
                        land_value.append(data[1])
            except:
                owners.append("")
                owner_address.append("")
                property_address.append("")
                land_state.append("")
                improve_value.append("")
                land_value.append("")
                
        input_df["Owner Name(From 2nd Web)"] = owners
        input_df["Owner Address"] = owner_address
        input_df["Property Location"] = property_address
        input_df["Land State Code"] = land_state
        input_df["Improvement Value"] = improve_value
        input_df["Land Market Value"] = land_value
        
        out_sheet.add_worksheet(rows=input_df.shape[0], cols=input_df.shape[1], title=street)  # Creat a new sheet
        work_sheet_instance = out_sheet.worksheet(street) # get that newly created sheet
        set_with_dataframe(work_sheet_instance, input_df) # Set collected data to sheet
            
    print("=="*30)
    print("Prgrame is Finished.")
    print("=="*30)
    exit() 