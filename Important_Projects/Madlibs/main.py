import predefined_strings
from Score import Score

if __name__ == "__main__":
    print("Welcome to Madlibs")
    print("Enter 1 to play with famous people quotes")
    print("Enter 2 to play with famous songs line")
    option = int(input("Enter Option to choose the category: "))

    score = Score()
    
    # based on option, play the following mode 
    if option == 1:
        for string in predefined_strings.famous_people_quotes:
            score.process(string)
    elif option == 2:
        for string in predefined_strings.famous_songs_lines:
            score.process(string)
    
    score.GetScore()