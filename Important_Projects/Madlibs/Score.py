from random import randint

class Score:
    def __init__(self):
        # member array that holds the binary score of the current string being refered
        self.__binary_score_frequency_list = []
        self.__blank_words_count = 0

    def process(self, string):
        # making the count to 0 at each iteration
        self.__blank_words_count = 0
        new_string = self.__blank_string(string)
        print(new_string)
        place_holder_array = []

        for i in range(self.__blank_words_count):
            place_holder_array.append(input("Fill Placeholder {}: ".format(str(i+1))))
        
        # fill out the placeholder of the new string 
        new_string = new_string.format(*place_holder_array)
        
        # print out the message to the user
        print("Your Output: ")
        print(new_string)
    
        if (new_string.lower() == string.lower()):
            self.__binary_score_frequency_list.append(1)
        else:
            self.__binary_score_frequency_list.append(0)
        
        print("Expected Output")
        print(string)
    
    # get the binary score frequency list 
    def GetScore(self):
        onesFreq = 0
        zerosFreq = 0

        for frequency in self.__binary_score_frequency_list:
            if frequency == 1:
                onesFreq +=1 
            else:
                zerosFreq +=1
        
        # find the largest 
        if (max(onesFreq, zerosFreq) == onesFreq):
            print("Madlibs Won")
        else:
            print("Madlibs Loss")
        
    
    # define the private member fuction that returns the random blanked string
    def __blank_string(self, string):
        # split the string
        string_array = string.split()
        # loop until the array gets blanked
        indexCount = 0
        maxCountOut = 0
        while(True):
            # if the max count out is > 4, then
            if maxCountOut != 4:
                # if the random number is 1, then
                if (randint(0, 1) == 1):
                    # increment the maxCout
                    maxCountOut +=1
                    # if the string length is > 4, then
                    if len(string_array[indexCount]) > 4:
                        # check if the string contains the string that contains the ,
                        if "," not in string_array[indexCount]:
                            # init the empty placeholder
                            string_array[indexCount] = "{}"
                            # increment the blank words count 
                            self.__blank_words_count +=1
                # increment the indexCount 
                indexCount +=1
                # check at each iteration if the indexCount exceeds the length
                if (indexCount >= len(string_array)):
                    indexCount = 0
            else:
                break
        
        new_string = ""

        for string in string_array:
            new_string += (string + " ")
        
        return new_string.strip()
            

    