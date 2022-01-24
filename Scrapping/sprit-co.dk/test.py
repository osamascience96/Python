from all_products.read_from_excel import Excel
from all_products.Product import Product

listofprods = list()
roughlist = ['111-22222', '111-22322']

prodObj1 = Product('Product1', 'www.facebook.com', '111-22222')
prodObj2 = Product('Product2', 'www.twitter.com', '111-22322')
prodObj3 = Product('Product3', 'www.youtube.com', '111-22622')

listofprods.append(prodObj1)
listofprods.append(prodObj2)
listofprods.append(prodObj3)

excelObj = Excel('all_products/provided_data.xlsx')
excelObj.WritetoExcelFile(listofprods, roughlist)

