from sys import argv
from os import path
from os import remove
from PhoneNum import PhoneNum
from WriteCSV import CSVWriter

contactfilesArray = argv

argumentsLength = len(contactfilesArray)

if(argumentsLength == 1):
    print("Contact List Not Provided")
else:
    if(argumentsLength == 3):
        file1 = contactfilesArray[1];
        file2 = contactfilesArray[2];

        # check if the file provided is the csv file or not
        fileonearray = file1.split(".");
        filetwoarray = file2.split(".");

        if(len(fileonearray) == 1 or len(filetwoarray) == 1):
            print("File Arguments not provided correctly")
        else:
            if(fileonearray[1] != "csv" or filetwoarray[1] != "csv"):
                print("Invalid File Extention Provided. Provide only csv files.")
            else:
                # read the files
                try:
                    file1Object = open(file1, "r");
                    file2Object = open(file2, "r");

                    file1ObjectArray = file1Object.read().split(",");
                    file2ObjectArray = file2Object.read().split(",");

                    # close the file objects 
                    file1Object.close()
                    file2Object.close()

                    # loop through the numbers in file2array
                    for number in file2ObjectArray:
                        # if the number is in the file1array
                        if number in file1ObjectArray:
                            # remove all the escape characters using the strip function
                            number = number.strip()
                            # add to the static list
                            PhoneNum.ResultantList.append(number)
                    # check if the file exists wih the name LIST-C in the current directory
                    if(path.exists('LIST-C.csv')):
                        # delete the current directory
                        remove("LIST-C.csv")
                    
                    # create the file
                    fileobj = open("LIST-C.csv", "w+");
                    # close the flle object
                    fileobj.close()

                    #  init the csvwriter object
                    csvobj = CSVWriter(PhoneNum.ResultantList);
                    # write to the resultant file
                    csvobj.writeresultantfile();
                    # display the list 
                    csvobj.displayList();
                except FileNotFoundError:
                    print("File Not Found")
    elif(argumentsLength > 3):
        print("Invalid Arguments List Length")
    else:
        print("Less arguments Provided")