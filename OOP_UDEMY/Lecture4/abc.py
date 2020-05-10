# Abstract base class
from abc import ABCMeta, abstractmethod

# set the meta property of the shape class to abstract base class
class Shape(metaclass = ABCMeta):
    @abstractmethod
    def area(self):
        return 0

class Square(Shape):
    side = 4
    def area(self):
        print("Area of Square: ", self.side * self.side)

class Rectangle(Shape):
    width = 5
    height = 10
    def area(self):
        print("Area of the Rectangle: ", self.width * self.height)


square = Square()
square.area()

rect = Rectangle()
rect.area()
