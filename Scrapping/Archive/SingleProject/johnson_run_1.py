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
from loader import initChromeDriver
import time

final_data = []

def do_scraping(driver):
    driver_url = driver.current_url
    soup = BeautifulSoup(driver.page_source, "lxml")
    pagination = soup.find("ul", class_ = "justify-content-end mt-n3 pagination")
    if pagination:
        pages = [i.text for i in pagination.find_all("a")]
        for page in range(int(pages[-2])):
            driver.get(driver_url+f"&Query.PageNumber={page+1}")
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "lxml")
            cards = soup.find_all("div", class_ = "account-card card")
            for card in cards:
                strong_items = [i.text.replace("\t", "").replace("\n", "") for i in card.find_all("strong")]
                if len(strong_items) > 0:
                    strong_items.append(card.find("h4").text)
                final_data.append(strong_items)
    else:
        cards = soup.find_all("div", class_ = "account-card card")
        for card in cards:
            strong_items = [i.text.replace("\t", "").replace("\n", "") for i in card.find_all("strong")]
            if len(strong_items) > 0:
                strong_items.append(card.find("h4").text)
            final_data.append(strong_items)
    
    return final_data

def run(input_sheet, output):
    print("=="*30)
    print("Johnson Scrapping Started.")
    print("=="*30)

    driver = initChromeDriver()
    driver.implicitly_wait(10)
    driver.refresh()
    
    count = 0
    for street in input_sheet:
        if count == 15:
            break
        print(f"Scrapping {street} ......")
        driver.get(f"https://www.johnsoncountytaxoffice.org/Search/Results?Query.SearchField=5&Query.SearchText={street}&Query.SearchAction=&Query.PropertyType=&Query.PayStatus=Both")
        time.sleep(2)
        do_scraping(driver=driver)
        count+=1

    final_dataframe = pd.DataFrame(final_data, columns=["Account", "Name", "Amount"])
    output.add_worksheet(rows=final_dataframe.shape[0], cols=final_dataframe.shape[1], title="Johnson")  # Creat a new sheet
    work_sheet_instance = output.worksheet("Johnson") # get that newly created sheet
    set_with_dataframe(work_sheet_instance, final_dataframe) # Set collected data to sheet
    
    print("=="*30)
    print("Johnson Scrapping Ended.")
    print("=="*30)
        
        
        
        