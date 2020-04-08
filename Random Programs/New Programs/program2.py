# open the file 
file = open("file.txt", "r") #onlue read the file

# let a list be of slpllited words 
list = file.read().split() # khali params means split in terms of space

file.close()

# let an empty dict
repeatedWords = []

# not a good solution
# iteration of O(n^2)
for value in list:

    # let the count of each value 
    count = 0

    if value in repeatedWords:
        pass
    else:
        # nested iteration 
        for sub_value in list:
            if value.lower() == sub_value.lower():
                count += 1
    
    if count > 1:
        repeatedWords.append(value.lower())

print(repeatedWords)