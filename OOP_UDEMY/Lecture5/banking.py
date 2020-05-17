from abc import ABCMeta, abstractmethod
from random import randint

class Account(metaclass = ABCMeta):
    @abstractmethod
    def createAccount(self):
        return 0
    @abstractmethod
    def authenticate(self):
        return 0
    @abstractmethod
    def withdraw(self):
        return 0
    @abstractmethod
    def deposit(self):
        return 0
    @abstractmethod
    def displayBalance(self):
        return 0
    
    

class SavingAccount(Account):
    def __init__(self):
        self.SavingAccount = {}

    def createAccount(self, name, initialDeposit):
        self.accountNumber = randint(10000, 99999)
        self.SavingAccount[self.accountNumber] = [name, initialDeposit]
        print("Account Created.")
        print("Your Account Number is {}".format(self.accountNumber))

    def authenticate(self, name, accountNumber):
        if accountNumber in self.SavingAccount.keys():
            if self.SavingAccount[accountNumber][0] == name:
                print("Authentication Successful")
                self.accountNumber = accountNumber
                return True
            else:
                print("Authentication Failed")
                return False
        else:
            print("Authentication Failed")
            return False
    
    def withdraw(self, withdrawalAmount):
        if withdrawalAmount > self.SavingAccount[self.accountNumber][1]:
            print("Insufficient Balance")
        else:
            self.SavingAccount[self.accountNumber][1] -= withdrawalAmount
            print("Successfull Withdrawl")
            print("Available Balance: ")
            self.displayBalance()

    def deposit(self, depositAmount):
        self.SavingAccount[self.accountNumber][1] += depositAmount
        print("Deposit Was Successful")
        self.displayBalance()

    def displayBalance(self):
        print("Avilable Balance: {}".format(self.SavingAccount[self.accountNumber][1]))


savingsAccount = SavingAccount()
while True:
    print("Enter 1 to create a New Account")
    print("Enter 2 to access the existing account")
    print("Enter 3 to exit")
    userChoice = int(input())
    if userChoice is 1:
        print("Enter your Name: ")
        name = input()
        print("Enter the initial deposit: ")
        inititalDeposit = float(input())
        savingsAccount.createAccount(name, inititalDeposit)
    elif userChoice is 2:
        print("Enter Your Name: ")
        name = input()
        print("Enter Your Account Number: ")
        accountNumber = int(input())
        authenticationStatus = savingsAccount.authenticate(name, accountNumber)
        if authenticationStatus is True:
            while True:
                print("Enter 1 to Withdraw")
                print("Enter 2 to deposit")
                print("Enter 3 to display the available balance")
                print("Enter 4 to go back to the previous menu")
                userChoice = int(input())
                if userChoice is 1:
                    print("Enter the Withdrawl amount")
                    withdrawlAmount = float(input())
                    savingsAccount.withdraw(withdrawlAmount)
                elif userChoice is 2:
                    print("Enter the Deposit amount")
                    depositAmount = float(input())
                    savingsAccount.deposit(depositAmount)
                elif userChoice is 3:
                    savingsAccount.displayBalance()
                elif userChoice is 4:
                    break
    elif userChoice is 3:
        break

