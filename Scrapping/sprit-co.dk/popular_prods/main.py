from traceback import print_tb
import requests
from bs4 import BeautifulSoup

url = "https://sprit-co.dk/";

class Product:
    
    def __init__(self, title, link):
        self.title = title
        self.link = link
    
    def setTitle(self, title):
        self.title = title
    
    def getTitle(self):
        return self.title
    
    def setLink(self, link):
        self.link = link
    
    def getLink(self):
        return self.link

# get the html
r = requests.get(url)
htmlContent = r.content

# parse the html content using beauitful soap
soup = BeautifulSoup(htmlContent, 'html.parser') 

# get the title
title = soup.title.get_text()

# get the popular products class
popular_prods_ul = soup.find('ul', class_='products')

popular_prods_list = popular_prods_ul.find_all('li')
final_popular_prods_list = list()

for popular_product in popular_prods_list:
    anchor = popular_product.find('a')
    
    title = anchor.find('h2').get_text()
    link = anchor.get('href')
    
    product = Product(title, link)

    final_popular_prods_list.append(product)


for product in final_popular_prods_list:
    print(product.getTitle())
    print(product.getLink())
    print("---------------------------------------------------------")

