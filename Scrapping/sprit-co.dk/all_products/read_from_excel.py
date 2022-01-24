from numpy import NaN
import pandas
import xlsxwriter

class Excel:

    def __init__(self, loc):
        data = pandas.read_excel(loc)
        
        self.sku_list = list()
        self.exceldata = data.to_dict()

        self.workbook = xlsxwriter.Workbook('sku_products.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        # write headings
        self.worksheet.write(0, 0, 'Title', self.workbook.add_format({'bold': True}))
        self.worksheet.write(0, 1, 'URL', self.workbook.add_format({'bold': True}))
        self.worksheet.write(0, 2, 'SKU', self.workbook.add_format({'bold': True}))

    def GetPreSKUList(self):
        for sku in self.exceldata.get('Unnamed: 0'):
            data = self.exceldata.get('Unnamed: 0').get(sku)
            if(data != "Varenr." and data != "VARENR." and data is not NaN):
                data = str(data).strip()
                self.sku_list.append(data)
        
        return self.sku_list;
    
    def WritetoExcelFile(self, sku_list, preskulist):
        # The sku list is of the Product Type
        row = 1
        for product in sku_list:
            title = product.getTitle()
            link  = product.getLink()
            sku = str(product.getSKU())
            if(sku in preskulist):
                self.worksheet.write(row, 0, title)
                self.worksheet.write(row, 1, link)
                self.worksheet.write(row, 2, sku)

                row +=1;
        

    def closeWorkBook(self):
        self.workbook.close()
                
    
    
