from abc import ABCMeta, abstractmethod

# power of one area to the power of the other of any shape

class Shape(metaclass = ABCMeta):
    @abstractmethod
    def __pow__(self, shape):
        return 0


class Square(Shape):
    def __init__(self, side):
        self.area = side * side
    
    # overload the power operator
    def __pow__(self, square):
        return (self.area ** square.area)
        


class Rectangle(Shape):
    def __init__(self, width, height):
        self.area = width * height
    
    # overload the power operator
    def __pow__(self, rect):
        return(self.area ** rect.area)


# Experiment with Square
squareOne = Square(5)
squareTwo = Square(10)

print("The Stack Power of Square is ", squareOne ** squareTwo)

# Experiment with Rectangle
rectOne = Rectangle(2, 4)
rectTwo = Rectangle(4, 2)

print("The Stack Power of Rectangle is ", rectOne ** rectTwo)


    