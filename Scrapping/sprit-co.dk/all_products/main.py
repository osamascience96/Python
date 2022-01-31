import requests
from bs4 import BeautifulSoup
from get_all_products import AllProducts
from read_from_excel import Excel

url = "https://sprit-co.dk/shop"

# get the html
r = requests.get(url)
htmlcontent = r.content

# parse the html content using beautiful soap
soup = BeautifulSoup(htmlcontent, 'html.parser')

# create a new Excel Obj
excelObj = Excel('provided_data.xlsx')
sku_list = excelObj.GetPreSKUList()

all_categories = soup.find('ul', class_='products').find_all('li')

all_cat_products = dict()

for category in all_categories:
    title = category.find('h2').get_text().strip()
    link = category.find('a').get('href');
    print("Get Products from " + title + " ....")
    
    allprods = AllProducts(title, link)
    allprods.GetRemainingProducts()

    all_cat_products[title] = allprods.GetWebsiteProductsList()


for key in all_cat_products:
    allprods = all_cat_products.get(key)
    # excelObj.WritetoExcelFile(allprods, sku_list)
    excelObj.WriteAlltoExcelFile(allprods)

# close the book
excelObj.closeWorkBook()