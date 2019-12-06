n = input()
words = list()
distinctWords = list()

# loop n times 
for iterator in range(int(n)):
    word = input()
    words.insert(iterator, word)

# print the list for checking 
print(words)

# code for the distinct words 
count = 0
distinctount = 0
for itr in words:
    if count == 0:
        distinctWords.insert(count, itr)
        distinctount += 1
    else:
        if itr in distinctWords:
            pass
        else:
            distinctWords.insert(count, itr)
            distinctount += 1
    count += 1

# print the list of distinct words for checking 
print(distinctWords)
print("Distinct Words", distinctount)

# code for words frequency
output = ""
frequency = 0
for freqWord in distinctWords:
    for i in range(count):
        if freqWord == words[i]:
            frequency += 1
    output = output + str(frequency) + " "
    frequency = 0

print("Frequency of each word in disinct list ", output)
        

