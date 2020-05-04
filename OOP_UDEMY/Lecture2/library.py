class Library:

    def __init__(self, listOfBooks):
        self.availableBooks = listOfBooks

    def displayAvailableBooks(self):
        print("\nAvailable Books: ")
        for book in self.availableBooks:
            print(book)

    def lendBook(self, requestedBook):
        if requestedBook in self.availableBooks:
            print("You have now borrowed the book")
            self.availableBooks.remove(requestedBook)
        else:
            print("Sorry th book is not available in out list.")

    def addBook(self, returnedBook):
        self.availableBooks.append(returnedBook)
        print("You have returned the book. Thank You!")

class Customer:
    def requestBook(self):
        print("Enter the name of the book you would like to borrow: ")
        self.book = input()
        return self.book

    def returnBook(self):
        print("Enter the name of the book which you are returning: ")
        self.book = input()
        return self.book



library = Library(['Think and Grow Rich', 'Harry Potter', 'Fantastic Beasts', 'Love Life'])
customer = Customer()

while True:
    print("\nEnter 1 to display the available books")
    print("Enter 2 to request for a book")
    print("Enter 3 to return a book")
    print("Enter 4 to exit")

    userChoice = int(input())

    if userChoice is 1:
        library.displayAvailableBooks()
    elif userChoice is 2:
        requestBook = customer.requestBook()
        library.lendBook(requestBook)
    elif userChoice is 3:
        returnBook = customer.returnBook()
        library.addBook(returnBook)
    elif userChoice is 4:
        quit()
    
