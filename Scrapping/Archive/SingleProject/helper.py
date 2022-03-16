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
def GetNewCreatedSheet(client, index):
    sheet = client.open("Street Output")
    list_of_sheets = sheet.worksheets()
    return list_of_sheets[index]

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
    df = read_csv("DallasMaster.csv", usecols=col_list)
    return df