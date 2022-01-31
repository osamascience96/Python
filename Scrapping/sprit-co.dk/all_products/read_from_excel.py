from numpy import NaN
import pandas
import xlsxwriter

class Excel:

    def __init__(self, loc):
        data = pandas.read_excel(loc)
        
        self.row = 1

        self.sku_list = list()
        self.exceldata = data.to_dict()

        self.workbook = xlsxwriter.Workbook('sku_products.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        # write headings
        self.worksheet.write(0, 0, 'Name', self.workbook.add_format({'bold': True}))
        self.worksheet.write(0, 1, 'Item No', self.workbook.add_format({'bold': True}))
        self.worksheet.write(0, 2, 'Category', self.workbook.add_format({'bold': True}))
        self.worksheet.write(0, 3, 'Price', self.workbook.add_format({'bold': True}))
        self.worksheet.write(0, 4, 'Description', self.workbook.add_format({'bold': True}))
        self.worksheet.write(0, 5, 'Link', self.workbook.add_format({'bold': True}))
        self.worksheet.write(0, 6, 'Image', self.workbook.add_format({'bold': True}))
        self.worksheet.write(0, 7, 'Specification', self.workbook.add_format({'bold': True}))

    def GetPreSKUList(self):
        for sku in self.exceldata.get('Unnamed: 0'):
            data = self.exceldata.get('Unnamed: 0').get(sku)
            if(data != "Varenr." and data != "VARENR." and data is not NaN):
                data = str(data).strip()
                self.sku_list.append(data)
        
        return self.sku_list;
    
    def WritetoExcelFile(self, sku_list, preskulist):
        # The sku list is of the Product Type
        for product in sku_list:
            title = product.getTitle()
            sku = str(product.getSKU())
            category = product.getCategory()
            price = product.getPrice()
            description = product.getDescription()
            link  = product.getLink()
            image = product.getImageLink()
            specs = product.getSpecifications()
            if(sku in preskulist):
                self.worksheet.write(self.row, 0, title)
                self.worksheet.write(self.row, 1, sku)
                self.worksheet.write(self.row, 2, category)
                self.worksheet.write(self.row, 3, price)
                self.worksheet.write(self.row, 4, description)
                self.worksheet.write(self.row, 5, link)
                self.worksheet.write(self.row, 6, image)
                self.worksheet.write(self.row, 7, specs)
                self.row +=1;
    
    def WriteAlltoExcelFile(self, sku_list):
        # The sku list is of the Product Type
        for product in sku_list:
            title = product.getTitle()
            sku = str(product.getSKU())
            category = product.getCategory()
            price = product.getPrice()
            description = product.getDescription()
            link  = product.getLink()
            image = product.getImageLink()
            specs = product.getSpecifications()
            # write to the file
            self.worksheet.write(self.row, 0, title)
            self.worksheet.write(self.row, 1, sku)
            self.worksheet.write(self.row, 2, category)
            self.worksheet.write(self.row, 3, price)
            self.worksheet.write(self.row, 4, description)
            self.worksheet.write(self.row, 5, link)
            self.worksheet.write(self.row, 6, image)
            self.worksheet.write(self.row, 7, specs)
            self.row +=1;
        

    def closeWorkBook(self):
        self.workbook.close()
                
    
    
