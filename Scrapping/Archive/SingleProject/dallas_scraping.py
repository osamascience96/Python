from itertools import count
from numpy import amin
import pandas as pd
from gspread_dataframe import set_with_dataframe
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
from helper import ReadDallasCount, WriteDallasCount

from loader import initChromeDriver

# member variables
final_data = []

def separate_name(sample:list):
    keys_array = ['Address:', 'Property Site Address:', 'Current Tax Levy: \xa0 ', 
        'Current Amount Due: \xa0 ', 'Market Value:', 'Legal Description:', 'Prior Year Amount Due: \xa0 ',
        'Total Amount Due: \xa0 ', 'Land Value:', 'Improvement Value:', 'Capped Value:', 'Agricultural Value:', 'Exemptions:',
        'Current Tax Statement', 'Summary Tax Statement', 'Taxes Due Detail by Year and Jurisdiction', 'Payment Information',
        'Composite Receipt', '(pending payments are not included) ', 'Request an Address Correction']
    data = [i for i in sample if (i!='' and i!=" ")]
    
    name = ""
    address = ""
    PropertySiteAddress = ""
    TaxLevy = ""
    AmountDue = ""
    MarketVal = ""

    for value in data:
        if(value in keys_array):
            index = data.index(value) + 1
            if(index < len(data)):
                while(data[index] not in keys_array):
                    if value == keys_array[0]:
                        address += (data[index] + " ")
                    elif value == keys_array[1]:
                        name += (data[index] + " ")
                        PropertySiteAddress += (data[index] + " ")
                    elif value == keys_array[2]:
                        TaxLevy += data[index]
                    elif value == keys_array[7]:
                        AmountDue += data[index]
                    elif value == keys_array[4]:
                        MarketVal += data[index]
                    index +=1
    
    MarketVal = MarketVal.replace(' \xa0', '')

    return [name.strip(), address.strip(), PropertySiteAddress.strip(), TaxLevy.strip(), AmountDue.strip(), MarketVal.strip()]

def FinalWritingProcedure(driver, soup, street_name):
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
            if values.text.replace('\t', '').replace('\n', ''): 
                storage.append(values.text.replace('\t', '').replace('\n', ''))
            
            for value in values:
                temp = value.text.replace('\t', '').replace('\n', '')
                storage2.append(temp)
    
    seperated_value = separate_name(storage2)

    address_owner = seperated_value[0]
    address = seperated_value[1]
    PropertySiteAddress = seperated_value[2]
    TaxLevy = seperated_value[3]
    AmountDue = seperated_value[4]
    MarketVal = seperated_value[5]


    final_data.append([address_owner, address, PropertySiteAddress, TaxLevy, AmountDue, MarketVal])
    print(f"|| {address_owner} || Scrapped from {street_name}")
        

def ContinueWriteProcedure(driver, street_name):

    HypToClick = '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div[3]/table/tbody/tr/td[1]/a'
    
    while True:
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, HypToClick)))
            break
        except: 
            driver.refresh()
    
    driver.find_element(By.XPATH, HypToClick).click()
    time.sleep(1)

    # Get the searched Results
    soup = BeautifulSoup(driver.page_source, 'lxml')
    if(soup is not None):
        FinalWritingProcedure(driver, soup, street_name)

def run(list_df, output):
    print("=============Dallas Scrapping Started=============")
    df = list_df
    driver = initChromeDriver()

    continueCount = ReadDallasCount()

    # minimum search results
    minimumSearchCount = 0
    minimumSearch = input("Enter Minimum Search Results in Number: ")
    if minimumSearch is not None:
        minimumSearch = int(minimumSearch)

    for street_obj in df.values:
        if(minimumSearchCount >= minimumSearch):
            break
        while True:
            driver.set_page_load_timeout(10)
            try:
                driver.get('https://www.dallasact.com/act_webdev/dallas/searchbyproperty.jsp')            
                street_num = int(street_obj[0])
                street_name = street_obj[1]

                driver.find_element(By.XPATH,'/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td/center/form/table/tbody/tr[2]/td[2]/h3/input').send_keys(street_num)
                driver.find_element(By.XPATH,'/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td/center/form/table/tbody/tr[3]/td[2]/h3/input').send_keys(street_name)
                time.sleep(0.5)
                driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td/center/form/table/tbody/tr[5]/td/center/input').click()
                time.sleep(0.5)

                try:
                    # Get the searched Results
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    # Get the size of the data received
                    size = soup.find('span', id="mySize")
                    if(size is not None):
                        size = int(size.get_text())
                        if(size > 0):
                            ContinueWriteProcedure(driver, street_name)
                            break
                except Exception as e:
                    print(e)
                    time.sleep(1)
            except TimeoutException:
                driver.execute_script("window.stop();")
        
        minimumSearchCount +=1
        continueCount +=1
    
    # Write last count 
    WriteDallasCount(continueCount)

    fileName = f"Dallas Scrapping {str(minimumSearch)} Searches";

    final_dataframe = pd.DataFrame(final_data, columns=["Owner", "Address", "Property Site Address", "Current Tax Levy", "Total Amount due", "Market Value"])
    output.add_worksheet(rows=final_dataframe.shape[0], cols=final_dataframe.shape[1], title=fileName)  # Creat a new sheet
    work_sheet_instance = output.worksheet(fileName) # get that newly created sheet
    set_with_dataframe(work_sheet_instance, final_dataframe) # Set collected data to sheet
    driver.close() # Close the driver

    print("=============Dallas Scrapping finished=============")