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


def do_scraping(driver):
    driver_url = driver.current_url
    soup = BeautifulSoup(driver.page_source, "lxml")
    pagination = soup.find("ul", class_ = "justify-content-end mt-n3 pagination")
    if pagination:
        pages = [i.text for i in pagination.find_all("a")]
        final_data = []
        for page in range(int(pages[-2])):
            driver.get(driver_url+f"&Query.PageNumber={page+1}")
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "lxml")
            cards = soup.find_all("div", class_ = "account-card card")
            data = []
            for card in cards:
                strong_items = [i.text.replace("\t", "").replace("\n", "") for i in card.find_all("strong")]
                strong_items.append(card.find("h4").text)
                data.append(strong_items)
            final_data.append(pd.DataFrame(data, columns=["Account", "Name", "Amount"]))
        return pd.concat(final_data)
    else:
        cards = soup.find_all("div", class_ = "account-card card")
        data = []
        for card in cards:
            strong_items = [i.text.replace("\t", "").replace("\n", "") for i in card.find_all("strong")]
            strong_items.append(card.find("h4").text)
            data.append(strong_items)
        if data==[]:
            return pd.DataFrame([["", "", ""]], columns=["Account", "Name", "Amount"])
        return pd.DataFrame(data, columns=["Account", "Name", "Amount"])

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
    for street in input_streets:
        print(f"Scrapping {street} ......")
        driver.get(f"https://www.johnsoncountytaxoffice.org/Search/Results?Query.SearchField=5&Query.SearchText={street}&Query.SearchAction=&Query.PropertyType=&Query.PayStatus=Both")
        time.sleep(2)
        final_dataframe = do_scraping(driver=driver)
        out_sheet.add_worksheet(rows=final_dataframe.shape[0], cols=final_dataframe.shape[1], title=street)  # Creat a new sheet
        work_sheet_instance = out_sheet.worksheet(street) # get that newly created sheet
        set_with_dataframe(work_sheet_instance, final_dataframe) # Set collected data to sheet
    
    print("=="*30)
    print("Prgrame is Finished.")
    print("=="*30)
    exit()
        
        
        
        