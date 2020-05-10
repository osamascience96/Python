class MusicalInstruments:
    numberOfMajorKeys = 12

class StringInstruments(MusicalInstruments):
    typeOfWood = "Tonewood"


class Guitar(StringInstruments):
    def __init__(self):
        self.numberOfStrings = 6
        print("This Guitar of consists of {} strings, it is made of {} and it can plays {} keys".format(self.numberOfStrings, self.typeOfWood, self.numberOfMajorKeys))
    

guitar = Guitar()
