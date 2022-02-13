from bs4 import BeautifulSoup
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from loader import initChromeDriver
import time

def run(input_sheets, output):
    
    print("=="*30)
    print("Denton Scrapping Second Instance Starting")
    print("=="*30)

    driver = initChromeDriver()
    driver.implicitly_wait(10)
    driver.refresh()
    time.sleep(40)

    address = []
    cities = []
    names = []
    mailing_addresses = []
    mailing_cities = []
    assessed_value_list = []

    input_data = input_sheets.get_all_records()
    input_df = pd.DataFrame.from_dict(input_data)
    account_list = input_df["Account"].tolist()

    for account in account_list:
        account = str(int(account))
        print(account)
        driver.get(f"https://propaccess.trueautomation.com/clientdb/Property.aspx?cid=19&prop_id={account}")
        time.sleep(1)
        data = []
        try:
            driver.find_element(By.XPATH, 
                                    "/html/body/form/div/div[5]/div[1]/span/input").click()
            assert_details = driver.find_element(By.XPATH, 
                                                    "/html/body/form/div/div[5]/div[5]").get_property("innerHTML")
            assert_soup = BeautifulSoup(assert_details, "lxml")
            assessed_value_list.append([i.text for i in assert_soup.find_all("td", class_ = "currency")][-1])
            
            property_details = driver.find_element(By.XPATH, 
                                                        "/html/body/form/div/div[5]/div[3]").get_property("innerHTML")
            property_soup = BeautifulSoup(property_details, "lxml")
            property_data = []
            for i in property_soup.find_all("tr"):
                for j in i.find_all("td"):
                    property_data.append([s.text.replace("\n", "") for s in j if s.text.replace("\n", "")!=""])
            
            for n, data in enumerate(property_data):
                if data == ['Address:']:
                    address.append(property_data[n+1][0])
                    temp = " ".join(property_data[n+1][1].split(" ")[:-1])
                    cities.append(temp)
                elif data == ['Name:']:
                    names.append(property_data[n+1][0])
                elif data == ['Mailing Address:']:
                    mailing_addresses.append(property_data[n+1][0])
                    mailing_cities.append(property_data[n+1][1])
        except:
            address.append("")
            cities.append("")
            names.append("")
            mailing_addresses.append("")
            mailing_cities.append("")
            assessed_value_list.append("")
        print(address)
        print(cities)
        print(names)
        print(mailing_addresses)
        print(mailing_cities)
        print(assessed_value_list)
        print("===="*20)
    
            
        
    input_df["Address"] = address
    input_df["City"] = cities
    input_df["Owner(From 2nd Web)"] = names
    input_df["Mailing Address"] = mailing_addresses
    input_df["Mialing City"] = mailing_cities
    input_df["Assessed Value"] = assessed_value_list
    
    output.add_worksheet(rows=input_df.shape[0], cols=input_df.shape[1], title="Denton")  # Creat a new sheet
    work_sheet_instance = output.worksheet(title="Denton") # get that newly created sheet
    set_with_dataframe(work_sheet_instance, input_df) # Set collected data to sheet
            
    print("=="*30)
    print("Denton Scrapping Second Instance Ended")
    print("=="*30)