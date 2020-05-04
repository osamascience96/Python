class Car:
    def __init__(self, SetOfCars):
        self.carsAvailable = SetOfCars
    
    def displayAvailableCars(self):
        print("\nCars Availabe: ")
        print(self.carsAvailable)
    
    def rentACar(self, rentedCar):
        priceOfCar = self.carsAvailable.pop(rentedCar)
        return priceOfCar

    def addACar(self, returnedCar):
        if (returnedCar == "Hatchback"):
            self.carsAvailable["Hatchback"] = 30
        elif (returnedCar == "Sedan"):
            self.carsAvailable["Sedan"] = 50
        else:
            self.carsAvailable["SUV"] = 100
        
        print("The Car is Returned, Thank You!")
        

class Customer:
    def requestCar(self):
        print("Enter the Car for Rent: ")
        self.car = input()
        return self.car

    def returnCar(self):
        print("Enter the Car you want to return: ")
        self.car = input()
        return self.car

    @staticmethod
    def fare(priceOfCar, durationOfDays):
        print("Your Fare for the rent is : " + str(priceOfCar * int(durationOfDays)))
        print("Car is Rented")

car = Car({"Hatchback": 30, "Sedan": 50, "SUV": 100})
customer = Customer()

while True:
    print("\nEnter 1 to display the available Cars")
    print("Enter 2 to rent a Car")
    print("Enter 3 to return a Car")
    print("Enter 4 to exit")

    userChoice = int(input())

    if userChoice is 1:
        car.displayAvailableCars()
    elif userChoice is 2:
        requestCar = customer.requestCar()
        price = car.rentACar(requestCar)
        print("ENter the days, you want to rent a car: ")
        duration = input()
        customer.fare(price, duration)
    elif userChoice is 3:
        returnCar = customer.returnCar()
        car.addACar(returnCar)
    elif userChoice is 4:
        quit()

