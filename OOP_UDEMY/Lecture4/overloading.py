class Square:
    def __init__(self, side):
        self.side = side
    
    # overloading the add operator by adding the sides of the 2 squares
    def __add__(self, squareObj):
        return((4 * self.side) + (4 * squareObj.side))

squareOne = Square(4)
squareTwo = Square(5)
print("Sum of sides of both the squares = ", squareOne + squareTwo)