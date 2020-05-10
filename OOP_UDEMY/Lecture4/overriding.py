class Employee:
    def setNumberOfWorkingHours(self):
        self.workingHours = 40
    
    def getNumberOfWorkingHours(self):
        return self.workingHours

class Trainee(Employee):
    # override the method
    def setNumberOfWorkingHours(self):
        self.workingHours = 45
    
    # reset the working hours back to 40
    def resetNumberOfWorkingHours(self):
        super().setNumberOfWorkingHours()


employee = Employee()
employee.setNumberOfWorkingHours()
print("The number of working hours {}".format(employee.getNumberOfWorkingHours()))

trainee = Trainee()
trainee.setNumberOfWorkingHours()
print("The number of working hours {}".format(trainee.getNumberOfWorkingHours()))

trainee.resetNumberOfWorkingHours()
print("The number of working hours {}".format(trainee.getNumberOfWorkingHours()))