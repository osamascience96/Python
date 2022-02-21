from itertools import count
from os import system, name

from sqlalchemy import false, true
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


# Script Exists function
def ScriptExists(script_list, name):
    sriptList = script_list[:-1];
    for index in range(len(sriptList)):
        if sriptList[index] == name:
            return index
    
    return 0

# Get Free Index Function
def GetFreeIndex(script_list):
    sriptList = script_list[:-1];
    return (len(sriptList) - 1) + 1 if len(sriptList) > 0 else 0;

# Remove the script function
def RemoveScript(script_list, name):
    sriptList = script_list[:-1];
    for script in sriptList:
        if script == name:
            sriptList.del_worksheet(script)
            return true
    
    return false

