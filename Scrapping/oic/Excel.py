import xlsxwriter

class Excel:
    def __init__(self):
        # init the row
        self.row = 0
        # init the workbook and worksheet
        self.workBook = xlsxwriter.Workbook('data.xlsx')
        self.workSheet = self.workBook.add_worksheet()
        # init the bold xlsx obj 
        self.bold = self.workBook.add_format({'bold': True})
    
    def setTitle(self, title):
        self.workSheet.write(self.row, 0, title, self.bold)
        self.row +=1;

    def setNewsTitle(self, newsTitle):
        self.row +=2;
        self.workSheet.write(self.row, 0, newsTitle, self.bold)
    
    def setDepartmentTitle(self, departmentTitle):
        self.row +=2;
        self.workSheet.write(self.row, 0, departmentTitle, self.bold)
    
    def setHotNewsList(self, hotnewsList):
        self.row +=1;
        self.workSheet.write(self.row, 0, 'Title', self.bold)
        self.workSheet.write(self.row, 1, 'Link', self.bold)
        # iterate over the list to print to the document
        for hotnews in hotnewsList:
            # get the title and news
            title = hotnews.getTitle()
            link = hotnews.getLink()
            # increment the row
            self.row +=1
            # write on to the excelsheet
            self.workSheet.write(self.row, 0, title)
            self.workSheet.write(self.row, 1, link)
    

    def setDepartmentList(self, departmentList):
        self.row +=1;
        self.workSheet.write(self.row, 0, 'Title', self.bold)
        self.workSheet.write(self.row, 1, 'Link', self.bold)
        # iterate over the list to print to the document
        for department in departmentList:
            # get the title and department
            title = department.getTitle()
            link = department.getLink()
            # increment the row
            self.row +=1
            # write on to the excelsheet
            self.workSheet.write(self.row, 0, title)
            self.workSheet.write(self.row, 1, link)
    
    def setAddresstoExcel(self, address):
        self.row +=2;
        self.workSheet.write(self.row, 0, "Address", self.bold)
        self.workSheet.write(self.row + 1, 0, address)
    
    def closeWorkBook(self):
        self.workBook.close()


if __name__ == "__main__":
    # Test the work book
    excel = Excel()

    excel.setTitle('Osama Ahmad');
    excel.setNewsTitle('Hot News Title')

    excel.closeWorkBook()