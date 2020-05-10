class Apple:
    manufacturer = "Apple Inc."
    contactWebsite = "www.apple.com/contact"

    def contactDetails(self):
        print("To Contact us, log on to ",self.contactWebsite)


class MacBook(Apple):
    def __init__(self):
        self.yearOfManufacturer = 2017
    
    def manufactureDetails(self):
        print("This MacBook was manufactured in the year {} by {}".format(self.yearOfManufacturer, self.manufacturer))


macbook = MacBook()
macbook.manufactureDetails()
macbook.contactDetails()