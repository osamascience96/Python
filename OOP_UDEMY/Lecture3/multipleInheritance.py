class OperatingSystem:
    multiTasking = True
    name = "Mac OS"

class Apple:
    website = "www.apple.com"
    name = "Apple"

class MacBook(Apple, OperatingSystem):
    def __init__(self):
        if self.multiTasking is True:
            print("This is multitasking system. Visit {} for more details".format(self.website))
            print("Name: ",self.name)

macbook = MacBook()
