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
    print("Johnson Scrapping Second Instance Started")
    print("=="*30)

    driver = initChromeDriver()
    driver.implicitly_wait(10)
    driver.refresh()

    
    input_data = input_sheets.get_all_records()
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
    
    output.add_worksheet(rows=input_df.shape[0], cols=input_df.shape[1], title="Johnson")  # Creat a new sheet
    work_sheet_instance = output.worksheet("Johnson") # get that newly created sheet
    set_with_dataframe(work_sheet_instance, input_df) # Set collected data to sheet
            
    print("=="*30)
    print("Johnson Scrapping Second Instance Ended")
    print("=="*30)