# T Test cases
T = int(input())

for itr in range(T):
    # n cubes
    n = int(input())
    number = input()
    listNumbers = list()
    count = 0

    for nums in number:
        if nums != " ":
            listNumbers.insert(count, int(nums))
            count += 1
    
    count = 0

    if len(listNumbers) > n or len(listNumbers) < n:
        pass
    else:
        lenght = len(listNumbers) - 1
        start = 0
        end =  lenght
        for i in range(len(listNumbers) - 1):
            if listNumbers[start] > listNumbers[start+1] or listNumbers[start] == listNumbers[start+1]:
                if listNumbers[end] > listNumbers[end-1] or listNumbers[end] == listNumbers[end-1]:
                    count += 1
                    start += 1
                    end = lenght - start
                elif end == (start + 1):
                    # collision detected
                    count += 1
                    break
            elif end == start:
                # collision detected 2
                # count += 1
                break
            else:
                # pattern not matched
                break        
    
    if ( count == int(len(listNumbers) / 2) ):
        print("Yes")
    else:
        print("No")
