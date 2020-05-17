class Person:
    def __init__(self):
        self.__name = ""


class Patient(Person):
    __sickness = "default"

    def setName(self, patientName):
        self.__name = patientName
    
    def getName(self):
        return self.__name

    
    def setSickness(self, disease):
        self.__sickness = disease
    
    def getSickness(self):
        return self.__sickness


p1 = Patient()

p1.setName("Mike")
print(p1.getName())

p1.setSickness("Fever")
print(p1.getSickness())