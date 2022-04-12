import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import os

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException, ElementNotInteractableException
from selenium import webdriver
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

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


def get_stars_input():
    print("Enter number of stars for hotel: ")
    stars = int(input())
    if stars == 1:
        stars = "1 stars"
        return stars
    if stars == 2:
        stars = "2 stars"
        return stars
    if stars == 3:
        stars = "3 stars"
        return stars
    if stars == 4:
        stars = "4 stars"
        return stars
    if stars == 5:
        stars = "5 stars"
        return stars
    else:
        print("Wrong Input for Stars! Execution Stopped!\n")
        exit(-1)
    return ""


def get_review_language():
    print("Enter review language (1 for English / 2 for French): ")
    language = int(input())
    if language == 1:
        language = "English"
        return language
    if language == 2:
        language = "French"
        return language
    else:
        print("Wrong Input for Language! Execution Stopped!\n")
        exit(-1)
    return ""


def get_hotel_city():
    print("Enter city name: ")
    city_name = ""
    city_name = input()
    city_name = city_name.strip().lower().capitalize()
    return city_name + " Hotels"


hotel_stars = get_stars_input()

hotel_review_language = get_review_language()

hotel_city = get_hotel_city()

l_language = ["Language1"]
l_t_rating = ["Total Rating2"]
l_t_type = ["Traveller Type2"]
l_review = ["Review2"]
l_cleanliness = ["Cleanliness2"]
l_sleep_quality = ["Sleep Quality2"]
l_service = ["Service2"]
l_date = ["Date2"]
l_user_from = ["User From2"]
l_location = ["Location2"]
l_value = ["Value2"]
l_rooms = ["Rooms2"]

dict = {"Language": l_language, "Total Rating": l_t_rating, "Traveller Type": l_t_type, "Review": l_review,
        "Cleanliness": l_cleanliness,
        "Sleep Quality": l_sleep_quality, "Service": l_service, "Date": l_date, "User From": l_user_from,
        "Location": l_location, "Value": l_value, "Rooms": l_rooms}

df = pd.DataFrame(dict)
df.to_csv('review_file.csv')

total_pages = 5;

url = "https://www.tripadvisor.com/Hotels-g293730-Morocco-Hotels.html"

# create a new Chrome session
driver = initChromeDriver()
driver.implicitly_wait(30)
driver.get(url)

city_found = False;

total_city_pages = 0

# pagination_info_div = driver.find_elements_by_xpath("//div[@class='unified ui_pagination leaf_geo_pagination']")
pagination_info_div = driver.find_elements(By.XPATH,"(//div[@class='unified ui_pagination leaf_geo_pagination'])")

total_city_pages = pagination_info_div[0].get_attribute("data-numpages")

total_pages = int(total_city_pages)

current_page = 1

page_offset = 0

next_page_builder = "https://www.tripadvisor.com/Hotels-g293730-oa" + str(
    page_offset) + "-Morocco-Hotels.html#LEAF_GEO_LIST"

while city_found is not True:
    driver.implicitly_wait(60)
    current_page_cities = driver.find_elements_by_xpath("//a[contains(text(), '" + hotel_city + "')]")
     #current_page_cities = driver.find_elements(By.XPATH,"//a[contains(text(), '" + hotel_city + "')]")
    
    if len(current_page_cities) > 0:
        city_found = True
        city_url = current_page_cities[0].get_attribute("href")
        driver.get(city_url)
        break
    else:
        current_page = current_page + 1
        if current_page > total_pages:
            print("City Not Found\n")
            driver.stop_client()
            driver.quit()
            exit(0)
        page_offset = page_offset + 20
        next_page_builder = "https://www.tripadvisor.com/Hotels-g293730-oa" + str(
            page_offset) + "-Morocco-Hotels.html#LEAF_GEO_LIST"
        print(next_page_builder)
        driver.implicitly_wait(0)
        driver.get(next_page_builder)

driver.implicitly_wait(100)

blank_clc = driver.find_element_by_xpath("//*[contains(text(), '" + hotel_stars + "')]")
 #blank_clc = driver.find_elements(By.XPATH,"(//*[contains(text(), '" + hotel_stars + "')])")

if blank_clc is None:
    print("Hotels with " + hotel_stars + " not found!")
    driver.stop_client()
    driver.quit()
    exit(0)

try:
    blank_clc.click()
except StaleElementReferenceException:
    print("")

# filter added to the page
next_Hotel_page = True
next_page_link = ""

while next_Hotel_page is True:
    try:
        driver.implicitly_wait(100)
        all_links_on_current_page = driver.find_elements_by_xpath("//*[@data-clicksource='HotelName']")

        # got all hotel elements. Now extract hotel links from them.

        hotels_hrefs = []
        try:
            for hotel_hrf in all_links_on_current_page:
                hrf = hotel_hrf.get_attribute("href")
                hotels_hrefs.append(hrf)

            print(hotels_hrefs)

            driver.implicitly_wait(50)
            next_hotel_pagination = driver.find_element_by_class_name("standard_pagination")
            next_hotel_page = next_hotel_pagination.find_element_by_class_name("next")

            if next_hotel_page.is_enabled():
                link1 = next_hotel_page.get_attribute("href")
                next_page_link = link1
            else:
                next_Hotel_page = False

            reviews_pages = 1;
            doneFlag = False

            for hotel_link in hotels_hrefs:
                next_link = hotel_link

                while doneFlag is False:
                    driver.get(next_link)
                    driver.implicitly_wait(100)
                    language_french_filter = driver.find_elements_by_xpath("//span[@class='fwSIg q']")
                    driver.implicitly_wait(100)
                    found = False
                    for lang in language_french_filter:
                        if lang.get_attribute("innerText") == hotel_review_language:
                            lang.click()
                            time.sleep(1)
                            found = True
                            break
                    if found is False:
                        print("Language not Found!\n")
                        driver.stop_client()
                        driver.quit()
                        exit(0)




                    # Time to get Review Data
                    driver.implicitly_wait(100)
                    review_Tabs = driver.find_elements_by_xpath("//div[@class='cWwQK MC R2 Gi z Z BB dXjiy']")



                    review_ind = 0
                    first_up = False
                    for review_tab in review_Tabs:
                        driver.implicitly_wait(100)
                        rating_div = review_tab.find_element_by_xpath("//div[@class='elFlG f O']")
                        rating_span = review_tab.find_element_by_class_name("ui_bubble_rating")
                        total_rating1 = str(rating_span.get_attribute("class"))[-2]
                        review_text_tab = review_tab.find_element_by_class_name("XllAv")
                        review_text = review_text_tab.find_element_by_tag_name("span")
                        review1 = review_text.get_attribute("innerText")
                        date_span = review_tab.find_element_by_class_name("euPKI")
                        date1 = str(date_span.get_attribute("innerText"))
                        date1 = date1.split(":")[1].strip()



                        if first_up is False:
                            driver.implicitly_wait(90)
                            caret_clc = review_tab.find_element_by_class_name("eljVo")

                            try:
                                if caret_clc:
                                    caret_clc.click()
                                    time.sleep(1)

                            except StaleElementReferenceException as Exception:
                                first_up = True

                        driver.implicitly_wait(50)
                        review_tab = driver.find_elements_by_xpath("//div[@class='cWwQK MC R2 Gi z Z BB dXjiy']")[review_ind]

                        trip_type = ""
                        user_from = ""



                        try:
                            driver.implicitly_wait(0)
                            type_tab = review_tab.find_elements_by_class_name("eHSjO")
                            driver.implicitly_wait(0)

                            if (len(type_tab) > 0):
                                trip_type = str(type_tab[0].get_attribute("innerText")).split(":")[1].strip()

                        except NoSuchElementException:
                            trip_type = ""

                        try:
                            driver.implicitly_wait(0)
                            type_tab = review_tab.find_elements_by_class_name("ShLyt")
                            driver.implicitly_wait(0)

                            if (len(type_tab) > 0):
                                user_from = str(type_tab[0].get_attribute("innerText")).strip().encode()
                        except NoSuchElementException:
                            user_from = ""

                        value_r = ""
                        rooms_r = ""

                        sleep_r = ""
                        service_r = ""
                        cleanliness_r = ""
                        location_r = ""

                        driver.implicitly_wait(0)
                        main_div = review_tab.find_elements_by_class_name("cnFkU")
                        driver.implicitly_wait(0)
                        lop = 0
                        if len(main_div) > 0:
                            all_ratings = main_div[0].find_elements_by_class_name("fFwef")

                            rate_len = len(all_ratings)
                            rind = 0
                            while rind < rate_len:
                                sub_rating1 = all_ratings[rind]
                                text1 = str(sub_rating1.get_attribute("innerText"))
                                text1 = text1.strip()

                                sub_rating = sub_rating1.find_element_by_class_name("ui_bubble_rating")
                                val = ""
                                if (sub_rating):

                                    val = str(sub_rating.get_attribute("class"))[-2]
                                    if text1 == "Value":
                                        value_r = val
                                    if text1 == "Service":
                                        service_r = val
                                    if text1 == "Sleep Quality":
                                        sleep_r = val
                                    if text1 == "Location":
                                        location_r = val
                                    if text1 == "Rooms":
                                        rooms_r = val
                                    if text1 == "Cleanliness":
                                        cleanliness_r = val
                                rind = rind + 1
                                lop = lop + 1

                        print("Value Rating:" + value_r)
                        print("Cleanliness Rating:" + cleanliness_r)
                        print("Rooms Rating:" + rooms_r)
                        print("Location Rating:" + location_r)
                        print("Service Rating:" + service_r)
                        print("Sleep Quality:" + sleep_r)
                        print("User From:" + user_from)
                        print("Traveller Type: " + trip_type)
                        print("Date: " + date1)
                        print("Language: " + hotel_review_language)
                        print("Total Rating: " + total_rating1)
                        print("Review: " + review1)

                        temp = date1[-4:]
                        if temp <= "2014":
                            doneFlag = True
                            break

                        l_value.append(value_r)
                        l_rooms.append(rooms_r)
                        l_sleep_quality.append(sleep_r)
                        l_service.append(service_r)
                        l_cleanliness.append(cleanliness_r)
                        l_location.append(location_r)
                        l_review.append(review1)
                        l_t_rating.append(total_rating1)
                        l_language.append(hotel_review_language)
                        l_date.append(date1)
                        l_t_type.append(trip_type)
                        l_user_from.append(user_from)

                        review_ind = review_ind + 1
                        dict = {"Language": l_language, "Total Rating": l_t_rating, "Traveller Type": l_t_type,
                                "Review": l_review,
                                "Cleanliness": l_cleanliness,
                                "Sleep Quality": l_sleep_quality, "Service": l_service, "Date": l_date,
                                "User From": l_user_from,
                                "Location": l_location, "Value": l_value, "Rooms": l_rooms}

                        df = pd.DataFrame(dict)
                        df.to_csv('review_file.csv', mode='a', header=False, encoding='utf-8-sig')

                        del l_value[:]
                        del l_rooms[:]
                        del l_sleep_quality[:]
                        del l_service[:]
                        del l_cleanliness[:]
                        del l_location[:]
                        del l_review[:]
                        del l_t_rating[:]
                        del l_language[:]
                        del l_date[:]
                        del l_t_type[:]
                        del l_user_from[:]

                    if doneFlag:
                        doneFlag = False
                        break

                    reviews_pagination = driver.find_element_by_class_name("ClYTS")

                    next_review_page = reviews_pagination.find_element_by_class_name("next")
                    if next_review_page.is_enabled():
                        link = next_review_page.get_attribute("href")
                        next_link = link
                    else:
                        doneFlag = True
            if next_Hotel_page:
                driver.get(next_hotel_page)
                
        except (ElementClickInterceptedException, WebDriverException):
       
        
            reviews_pagination = driver.find_element_by_class_name("ClYTS")
            

            next_review_page = reviews_pagination.find_element_by_class_name("next")
            if next_review_page.is_enabled():
                link = next_review_page.get_attribute("href")
                next_link = link
            else:
                doneFlag = True
               

    except (ElementClickInterceptedException,ElementNotInteractableException):
        if next_Hotel_page:
            driver.implicitly_wait(100)
            driver.get(next_page_link)


driver.close()
driver.quit()
exit(0)
    # In[5]:
