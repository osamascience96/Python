class Auto:
    def __init__(self):
        pass

    def displayMessage(self, x):
        print(x)

class Vechile(Auto):
    def __init__(self):
        self.__color = ""


rav4 = Vechile()
rav4.displayMessage("My Car is RAV4")