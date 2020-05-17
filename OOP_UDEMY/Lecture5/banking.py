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
                print("Authentication Failed")
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


# work on the menu...