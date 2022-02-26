import pandas as pd
from gspread_dataframe import set_with_dataframe
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from loader import initChromeDriver
import time

def run(input_sheet, output):
    print("=="*30)
    print("Ellis Scrapping is Started")
    print("=="*30)

    driver = initChromeDriver()
    driver.implicitly_wait(10)
    driver.refresh()

    accounts_list = []
    owners = []
    addresses = []
    cities = []
    property_address = []
    total_due = []
    gross_value = []

    for street in input_sheet:
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
        except:
            pass
    
    final_dataframe = pd.DataFrame(zip(accounts_list, owners, addresses, cities, property_address, total_due, gross_value), columns=["Account", "Owner", "Address", "City", "Property Site Address", "Total Amount Due", "Gross Value"])
            
    output.add_worksheet(rows=final_dataframe.shape[0], cols=final_dataframe.shape[1], title="Ellis Scrapping")  # Creat a new sheet
    work_sheet_instance = output.worksheet("Ellis Scrapping") # get that newly created sheet
    set_with_dataframe(work_sheet_instance, final_dataframe) # Set collected data to sheet
    
    print("=="*30)
    print("Ellis Scrapping is Finished")
    print("=="*30)