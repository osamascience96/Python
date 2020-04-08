# let a list be 
list = [7,1,7,3,4,8,1,13,6]
# let a dictionary be 
dict = {}

for i in range(len(list)):
    # apply the check for 1, 2, 3
    if list[i] == 1 or list[i] == 2 or list[i] == 3:
        # if the number exists in dictionary
        if list[i] in dict: 
            dict[list[i]] += 1
        else:
            dict[list[i]] = 1
    else:
        # nested for loop for other numbers rather than 1
        # list the numbers in loop by half of each number range

        # boolean check
        isPrime = True

        for n in range(2, int(list[i]/2) + 1):
            if (list[i] % n == 0):
                isPrime = False
                break
        
        if (isPrime == True):
            # if the number exists in dictionary
            if list[i] in dict: 
                dict[list[i]] += 1
            else:
                dict[list[i]] = 1

print(dict)                