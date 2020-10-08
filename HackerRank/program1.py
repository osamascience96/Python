def Find(number):
    result = ""
    if(number % 2 != 0):
        result = "Weird"
    elif(number % 2 == 0 and (number >= 2 and number <= 5)):
        result = "Not Weird"
    elif(number % 2 == 0 and (number >= 6 and number <= 20)):
        result = "Weird"
    elif(number % 2 == 0 and (number > 20)):
        result = "Not Weird"
    
    return result

if __name__ == '__main__':
    n = int(input().strip())
    print(Find(n))