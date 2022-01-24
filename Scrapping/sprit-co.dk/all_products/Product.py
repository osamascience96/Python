class Product:
    
    def __init__(self, title, link):
        self.title = title
        self.link = link
    
    def __init__(self, title, link, sku):
        self.title = title
        self.link = link
        self.sku = sku

    def setTitle(self, title):
        self.title = title
    
    def getTitle(self):
        return self.title
    
    def setLink(self, link):
        self.link = link
    
    def getLink(self):
        return self.link
    
    def setSKU(self, sku):
        self.sku = sku
    
    def getSKU(self):
        return self.sku