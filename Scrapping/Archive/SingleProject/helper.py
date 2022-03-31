from os import system, name
from pandas import read_csv

# Adds the line seperator to the menu
def lineSeperator():
    return "==+==+==+==+==+==+==+==+==+==+==+==+==+==+==+==+==+==+==+";

# Clear the Screen
def ClearScreen():
    # for windows
    if name == 'nt':
        system("cls")
    else:
        # for mac and linux
        system("clear")


# Prompt Ask Message
def AskMessage():
    return "Press 1 to continue or 0 to exit this Procedure => ";


# Get New Created Sheet
def GetNewCreatedSheet(client, script_name):
    sheet = client.open("Street Output")
    list_of_sheets = sheet.worksheets()
    
    ReturnedSheet = None

    for sheet in list_of_sheets:
        if (sheet.title == script_name):
            ReturnedSheet = sheet
            break

    return ReturnedSheet

# Script Exists function
def ScriptExists(script_client, type, name):
    
    script = None
    if type is 'Output':
        script = script_client.open("Street Output");
    else:
        script = script_client.open("Final Output");
    
    script_list = script.worksheets();

    sriptList = script_list[:-1];
    for index in range(len(sriptList)):
        if sriptList[index] == name:
            return True
    
    return False

# Get Free Index Function
def GetFreeIndex(script_client, type):

    script = None
    if type is 'Output':
        script = script_client.open("Street Output");
    else:
        script = script_client.open("Final Output");
    
    script_list = script.worksheets();

    sriptList = script_list[:-1];
    return (len(sriptList) - 1) + 1 if len(sriptList) > 0 else 0;

# Remove the script function
def RemoveScript(script_client, type, name):

    script = None
    if type is 'Output':
        script = script_client.open("Street Output");
    else:
        script = script_client.open("Final Output");
    
    script_list = script.worksheets();

    sriptList = script_list[:-1];
    for script in sriptList:
        if script == name:
            sriptList.del_worksheet(script)
            return True
    
    return False

def GetDallasMasterColumnsDict():
    col_list = ["STREET_NUM", "FULL_STREET_NAME"];
    
    N = ReadDallasCount() + 1
    
    df = read_csv("DallasMaster.csv", usecols=col_list, skiprows=[i for i in range(1,N)])
    return df

def WriteDallasCount(count):
    file = open("dallas_script_record.txt", "w");
    file.write(str(count))
    file.close()

def ReadDallasCount():
    file = open("dallas_script_record.txt", "r+");
    data = int(file.readline())
    file.close()

    return data


# main
if __name__ == "__main__":
    print(ReadDallasCount())
    WriteDallasCount(2)