import math

mAB = int(input())
mBC = int(input())

# Apply the Pythagorean formula for hypotnuese 

mAC = math.sqrt((math.pow(mAB, 2)) + (math.pow(mBC, 2)))

1
M = mAC / 2

angle = str(2 * math.pi * M)

if (int(angle[angle.find(".") + 1]) > 3):
    print(math.ceil(float(angle)))
else:
    print(math.floor(float(angle)))