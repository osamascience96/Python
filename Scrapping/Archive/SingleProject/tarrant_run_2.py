import pandas as pd
from gspread_dataframe import set_with_dataframe
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests, os, pydub
import speech_recognition as sr

from loader import initChromeDriver

new_data = []

def start_driver(account):
    try:
        driver = initChromeDriver()
        driver.implicitly_wait(10)
        driver.get("https://taxonline.tarrantcounty.com/taxweb/accountsearch.asp?linklocation=Iwantto&linkname=Property%20Account")
        time.sleep(1)
        driver.find_element(By.XPATH, 
                                "/html/body/table[1]/tbody/tr[3]/td/table/tbody/tr[1]/td/font/table/tbody/tr/td/table/tbody/tr[2]/td/form/input[1]").send_keys(account)
        return driver
    except:
        print("=="*30)
        print("Server is Down, Try it latter!")
        print("=="*30)
        exit()

def start_driver2(account):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("https://taxonline.tarrantcounty.com/taxweb/accountsearch.asp?linklocation=Iwantto&linkname=Property%20Account")
    driver.find_element(By.XPATH, 
                            "/html/body/table[1]/tbody/tr[3]/td/table/tbody/tr[1]/td/font/table/tbody/tr/td/table/tbody/tr[2]/td/form/input[1]").send_keys(account)
    return driver

def bypass_rechaptcha(account):
    for i in range(1):
        driver = start_driver(account=account)
        try:
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]"))).click()
            driver.switch_to.default_content()
            time.sleep(2)
            driver.find_element(By.XPATH, 
                                "/html/body/table[1]/tbody/tr[3]/td/table/tbody/tr[1]/td/font/table/tbody/tr/td/table/tbody/tr[2]/td/form/input[2]").click()
            return driver
        except:
            driver.quit()
    else:
        return None

def recognize_text():
    try:
        path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "audio.mp3"))
        path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "audio.wav"))
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")
        sample_audio = sr.AudioFile(path_to_wav)
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        return r.recognize_google(audio, language="en-US")
    except:
        return "speach is recognized"

def bypass_audio(account):
    driver = start_driver(account=account)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]"))).click()
    time.sleep(1)
    driver.switch_to.default_content()
    try:
        driver.find_element(By.XPATH, 
                                "/html/body/table[1]/tbody/tr[3]/td/table/tbody/tr[1]/td/font/table/tbody/tr/td/table/tbody/tr[2]/td/form/input[2]").click()
    except: pass
    if driver.current_url=="https://taxonline.tarrantcounty.com/taxweb/accountsearch.asp?linklocation=Iwantto&linkname=Property%20Account":
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,
                                                                                "/html/body/div[2]/div[4]/iframe")))
        driver.find_element(By.XPATH, 
                                "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button").click()
        audio_source = driver.find_element(By.XPATH, 
                                        "/html/body/div/div/div[7]/a").get_attribute("href")
        doc = requests.get(audio_source)
        with open('audio.mp3', 'wb') as f:
            f.write(doc.content)
        text = recognize_text()
        driver.find_element(By.XPATH, 
                            "/html/body/div/div/div[6]/input").send_keys(text)
        driver.find_element(By.XPATH, 
                            "/html/body/div/div/div[8]/div[2]/div[1]/div[2]/button").click()
        time.sleep(0.5)
        try:
            driver.switch_to.default_content()
            time.sleep(2)
            driver.find_element(By.XPATH, 
                                "/html/body/table[1]/tbody/tr[3]/td/table/tbody/tr[1]/td/font/table/tbody/tr/td/table/tbody/tr[2]/td/form/input[2]").click()
            return driver
        except:
            return None
    else:
        return driver

def do_scraping(driver):
    driver.find_element(By.XPATH,
                    "/html/body/table[1]/tbody/tr[2]/td/div/table[3]/tbody/tr[2]/td[1]/a").click()
    owner = driver.find_element(By.XPATH, 
                                "/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td/table[1]/tbody/tr/td[1]/table/tbody/tr[5]/td[2]").get_property('innerHTML')
    owner_soup = BeautifulSoup(owner, 'lxml')
    owner_details = [i.text for i in owner_soup.find_all("font")]
    city = owner_details[2].split("\xa0")[:2]
    owner_details[2] = " ".join(city)
    
    tax_table = driver.find_element(By.XPATH, 
                                    "/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td/div[5]/table").get_property("innerHTML")
    
    table_soup = BeautifulSoup(tax_table, 'lxml')
    row = table_soup.find_all("tr")[-1]
    total_value = row.find_all("td")[-2].text
    owner_details.append(total_value)
    if owner_details==[None]:
        new_data.append(["", "", "", ""])
    else:
        new_data.append(owner_details)

def run(input_sheet, final_client):
    print("============== Tarrant Second Instance is Started ===============")
    input_data = input_sheet.get_all_records()
    input_df = pd.DataFrame.from_dict(input_data)
    account_list = input_df["Account"].tolist()
    
    for account in account_list: 
        time.sleep(30)
        temp_driver = bypass_rechaptcha(account=account)
        if temp_driver:
            driver = temp_driver
            if driver.current_url!="https://taxonline.tarrantcounty.com/taxweb/accountsearch.asp?linklocation=Iwantto&linkname=Property%20Account":
                do_scraping(driver=driver)
            else:
                new_data.append(["", "", "", ""])
        else:
            new_data.append(["", "", "", ""])
        
    owners = [i[0] for i in new_data]
    addresses = [i[1] for i in new_data]
    cities = [i[2] for i in new_data]
    total_amount = [i[3] for i in new_data]

    input_df["Owner"] = owners
    input_df["Address"] = addresses
    input_df["City"] = cities
    input_df["Total"] = total_amount
    
    final_client.add_worksheet(rows=input_df.shape[0], cols=input_df.shape[1], title="Tarrant")  # Creat a new sheet
    work_sheet_instance = final_client.worksheet("Tarrant") # get that newly created sheet
    set_with_dataframe(work_sheet_instance, input_df) # Set collected data to sheet

    print("============== Tarrant Second Instance is Finished ===============")