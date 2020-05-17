class ValueError:
    testValue = "@"


class InvalidInput(ValueError):
    def checkInput(self, str):
        if self.testValue in str:
            print("The input is invalud")
        else:
            print("The input is correct")


input = InvalidInput()
input.checkInput("George@Mate")