import requests
from bs4 import BeautifulSoup
from fetch_sku import SKU

class AllProducts:
    
    def __init__(self, link):
        print('Fetching Products data from ' + link + " ......")
        self.link = link
        self.pagelinklist = set()

        self.products_list = list()

        self.r = requests.get(link)
        self.htmlContent = self.r.content
        self.soup = BeautifulSoup(self.htmlContent, 'html.parser')

        self.paginationLinks = self.soup.find('ul', class_='page-numbers')
        if(self.paginationLinks is not None):
            self.paginationLinks = self.paginationLinks.find_all('li')
            for pagination in self.paginationLinks:
                link = pagination.find('a')
                if(link is not None):
                    self.pagelinklist.add(link.get('href'))
        
        self.__getInitialProds()

    def __getInitialProds(self):
        
        listlinks = self.soup.find('ul', class_='products').find_all('li')
        for link in listlinks:
            fetched_link = link.find('a').get('href')
            sku = SKU(fetched_link)
            self.products_list.append(sku.GetProduct())
    
    def GetRemainingProducts(self):
        for link in self.pagelinklist:
            self.r = requests.get(link)
            self.htmlContent = self.r.content
            self.soup = BeautifulSoup(self.htmlContent, 'html.parser')

            listlinks = self.soup.find('ul', class_='products').find_all('li')
            for link in listlinks:
                fetched_link = link.find('a').get('href')
                sku = SKU(fetched_link)
                self.products_list.append(sku.GetProduct())
                    
        
    
    def GetWebsiteProductsList(self):
        return self.products_list
        

if __name__ == "__main__":
    prod = AllProducts('https://sprit-co.dk/kategori/whisky')
    prod.GetRemainingProducts()
    print(prod.GetRemainingProducts())
    
    