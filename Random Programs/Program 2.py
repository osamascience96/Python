def drawSqaure(length):
    for i in range(length):
        asterisk = ''
        if (i == 0 or i == length-1):
            for j in range(length):
                asterisk += "*"
            asterisk += " "
            for l in range(length):
                asterisk += "*"
            print(asterisk)
        else:
            for a in range(length):
                asterisk += "*"
            asterisk += " "
            for b in range(length):
                if (b == 0 or b == length-1):
                    asterisk += "*"
                else:
                    asterisk += " "
            print(asterisk)




length = input()

drawSqaure(int(length))