import requests
from Product import Product
from bs4 import BeautifulSoup

class SKU:

    def __init__(self, category, link):
        self.r = requests.get(link)
        self.htmlContent = self.r.content
        self.soup = BeautifulSoup(self.htmlContent, 'html.parser')

        self.link = link
        self.category = category
    
    
    def GetProduct(self):
        # get the title and sku
        title = self.soup.find('h1', class_='product_title')
        if title is not None:
            title = title.get_text()
        else:
            title = 'Not Available'
        
        specs = self.soup.find('div', class_='product-info-attributes')
        if specs is not None:
            specs = specs.get_text()
            specs = specs.replace('\n', '')
        else:
            specs = 'Not Available'
        
        sku = self.soup.find('tr', class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_sku')
        
        price = self.soup.find('span', class_='woocommerce-Price-amount amount')
        if price is not None:
            price = price.find('bdi').get_text()
            price = price.replace('\xa0', " ")
        else:
            price = 'Not Available'
        
        description = self.soup.find('div', class_='woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab')
        if description is not None:
            if description.find('p') is not None:
                description = description.find('p').get_text()
            else:
                description = 'Not Available'
        else:
            description = 'Not Available'
        imageLink = self.soup.find('img', class_='wp-post-image')
        
        if imageLink is not None:
            imageLink = imageLink.get('src')
        else:
            imageLink = 'Not Available'

        if sku is not None:
            sku = sku.find('td').get_text()
        else:
            sku = "Not Available"
        
        return Product(self.category, title, self.link, sku, price, description, imageLink, specs)


if __name__ == "__main__":
    sku = SKU('Hedvin', 'https://sprit-co.dk/shop/hedvin/dessert-vin/dutschke-old-codger-tawny')
    print(sku.GetProduct())