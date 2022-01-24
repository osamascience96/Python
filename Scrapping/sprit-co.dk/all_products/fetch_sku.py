import requests
from Product import Product
from bs4 import BeautifulSoup

class SKU:

    def __init__(self, link):
        self.r = requests.get(link)
        self.htmlContent = self.r.content
        self.soup = BeautifulSoup(self.htmlContent, 'html.parser')

        self.link = link
    
    
    def GetProduct(self):
        # get the title and sku
        title = self.soup.find('h1', class_='product_title').get_text()
        sku = self.soup.find('tr', class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_sku')

        if sku is not None:
            sku = sku.find('td').get_text()
        else:
            sku = "Not Available"
        
        return Product(title, self.link, sku)


if __name__ == "__main__":
    sku = SKU('https://sprit-co.dk/shop/tequila-agave-spiritus/tequila/calle-23-blanco-100')
    print(sku.GetProduct())