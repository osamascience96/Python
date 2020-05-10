class Furniture:
    _typeOfFurniture = "tweekwood"
    def setFurnitureType(self, typeOfFurniture):
        self._typeOfFurniture = typeOfFurniture

class Chair(Furniture):
    # set the private property
    __chairLegs = 4

    def displayFurniture(self):
        print("The chair has {} legs and has the type of {} materail".format(self.__chairLegs,self._typeOfFurniture))


chair = Chair()

chair.displayFurniture()

# set the material to another value 
chair.setFurnitureType("Multani Wood")
chair.displayFurniture()