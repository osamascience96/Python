import gspread
import pandas as pd
from loader import initChromeDriver
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

all_tables = []

def get_pagination(pagination, url):
    if pagination is not None:
        pagination = [i.text.replace("\t", '').replace("\n", '') for i in pagination]
        pagination = [i for i in pagination if i!='']
        pagination_list = []
        if len(pagination)>2:
            pagination = pagination[:-3]
            for page in range(int(pagination[-1])):
                pagination_list.append(url+f"?pg={page+1}")
        return pagination_list
    else:
        return []

def get_table(soup):
    soup = soup.find("table")
    if soup is not None:
        rows = soup.find_all("tr", class_="view_more_summary")
        for row in rows:
            temp_row = []
            for col in row:
                temp_row.append(col.text.replace("\t", '').replace("\n", ""))
            temp_row = [i for i in temp_row if i!='']
            all_tables.append(temp_row)

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


def run(input_streets, output):
    print("================== Tarrant First Instance Started ====================")
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

        if pagination_list!=[]:
            for page in pagination_list:
                time.sleep(1)
                driver.get(page)
                soup = BeautifulSoup(driver.page_source, 'lxml')
                get_table(soup=soup)
        else:
            get_table(soup=soup)
    driver.close() # Close the driver

    # final_dataframe = pd.concat(all_tables)
    final_dataframe = pd.DataFrame(all_tables, columns=["Account", "Property Address", "Property City", "Primary Owner Name", "Market Value"])
    final_dataframe.to_csv("oo.CSV", index=False)

    output.add_worksheet(rows=final_dataframe.shape[0], cols=final_dataframe.shape[1], title="Tarrant")  # Creat a new sheet
    work_sheet_instance = output.worksheet("Tarrant") # get that newly created sheet
    set_with_dataframe(work_sheet_instance, final_dataframe) # Set collected data to sheet

    print("================== Tarrant First Instance Finished ====================")