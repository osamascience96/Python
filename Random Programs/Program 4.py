q = input()
num = 0

def print_from_stream(n, stream):
    count = 0
    global num
    if stream == "increment":
        num += n
        print(num)
    elif stream == "decrement":
        num -= n
        print(num)
    elif stream == "even" or stream == "":
        while n != 0:
            if (count % 2 == 0):
                print(count)
                n -= 1
            count += 1
    elif stream == "odd":
        while n != 0:
            if (count % 2 != 0):
                print(count)
                n -= 1
            count += 1  


for n in range(int(q)):
    streamType = ""
    number = ""
    string = input()
    for itr in string:
        
        if itr.isnumeric():
            number = number + itr
        elif itr.isalpha():
            streamType = streamType + itr
    
    # passing the arguments
    print_from_stream(int(number), streamType)