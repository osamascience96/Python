from csv import writer

class CSVWriter:

    def __init__(self, resultantlist):
        self.resultantlist = resultantlist
    
    def writeresultantfile(self):
        fileobj = open("LIST-C.csv", 'a')
        writer_object = writer(fileobj)
        
        for number in self.resultantlist:
            writer_object.writerow([number])    
        
        fileobj.close()
    
    def displayList(self):
        print("The Numbers Concluded are the fillowing:")
        print(self.resultantlist)