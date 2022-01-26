class Product:
    
    def __init__(self, title, link):
        self.title = title
        self.link = link
    
    def __init__(self, category, title, link, sku, price, description, imagelink, specs):
        self.category = category
        self.title = title
        self.link = link
        self.sku = sku
        self.price = price
        self.description = description
        self.imagelink = imagelink
        self.specs = specs

    def setCategory(self, category):
        self.category = category
    
    def getCategory(self):
        return self.category
    
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
    
    def setPrice(self, price):
        self.price = price
    
    def getPrice(self):
        return self.price
    
    def setDescription(self, description):
        self.description = description
    
    def getDescription(self):
        return self.description
    
    def setImageLink(self, imageLink):
        self.imagelink = imageLink
    
    def getImageLink(self):
        return self.imagelink
    
    def setSpecifications(self, specs):
        self.specs = specs
    
    def getSpecifications(self):
        return self.specs