class Employee:
    def employeeDetails(self):
        self.name = "Osama"

    @staticmethod
    def welcomeMessage():
        print("Welcome to the Organization")

employee = Employee()

employee.employeeDetails()

print(employee.name)

employee.welcomeMessage()