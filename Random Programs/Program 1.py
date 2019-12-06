import random

# Task1
word = input()

# variables 
i = '0'
j = '0'
first = "0"
middle = "0"
last = "0"

for itr in range(len(word)):
    i = random.randint(0, len(word)-1)
    j = random.randint(0, len(word)-1)
    while(word[j] < word[i]):
        j = random.randint(0, len(word)-1)
    
    first = word[i]
    last = word[j]

    middle = last
    word.replace(last, first, j)
    word.replace(first, middle, i)

print(word)
