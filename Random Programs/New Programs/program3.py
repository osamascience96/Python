list = [1,5,3,4,4,6,7,8,8,11,4]


def recursiveFunc(list):
    if len(list) == 1:
        return list
    else:
        poppedValue = list.pop()
        if poppedValue in recursiveFunc(list):
            return list
        else:
            list.append(poppedValue)
            return list


print(recursiveFunc(list))
