# Write an object oriented program to create a precious stone.
# Not more than 5 precious stones can be held in possession at a
# given point of time. If there are more than 5 precious stones,
# delete the first stone and store the new one.

class Stone:

    # the ctor function
    def __init__(self):
        self.stoneList = []
    
    def AppendStoneList(self, stoneName):
        # check the size of the stone 
        if (len(self.stoneList) < 5):
            self.stoneList.append(stoneName)
        else:
            # remove the item from the 0th index 
            del self.stoneList[0]
            # append the data
            self.stoneList.append(stoneName)
    
    def displayStoneList(self):
        print(self.stoneList)


stone = Stone()

stone.AppendStoneList("Perl")
stone.AppendStoneList("Khurd")
stone.AppendStoneList("Veer")
stone.AppendStoneList("Monga")
stone.AppendStoneList("gudi")

# add the stone after the length exceeds
stone.AppendStoneList("Yugarh")


stone.displayStoneList()

