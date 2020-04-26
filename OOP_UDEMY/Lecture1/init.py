class Employee:

    def __init__(self, name):
        self.name = name
    
    def displayEmployeeDetails(self):
        print(self.name)


employee = Employee("Osama")
employeeTwo = Employee("Ali")
employee.displayEmployeeDetails()
employeeTwo.displayEmployeeDetails()