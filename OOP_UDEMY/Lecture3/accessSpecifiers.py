class Car:
    numberOfWheels = 4
    _color = "Black"
    __yearOfManufacture = 2017 #stored as _Car__yearOfManufacture

class BMW(Car):
    def __init__(self):
        print("Protected attribute Color: ", self._color)

car = Car()
print("Public attribute numberOfWheels: ",car.numberOfWheels)


bmw = BMW()
# not a good practice
print("The naming convention for the protected variable can be used outside: ",bmw._color)

# still not a good practice to do so.
print("Private Attribute year of Manufacture: ",car._Car__yearOfManufacture)

