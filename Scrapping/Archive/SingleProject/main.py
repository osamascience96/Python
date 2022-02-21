from time import time
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from helper import GetFreeIndex, ScriptExists, RemoveScript, lineSeperator, ClearScreen, AskMessage
import tarrant_run_1, tarrant_run_2, dallas_scraping, ellis_run, denton_run_1, denton_run_2, johnson_run_1, johnson_run_2

def GetNewCreatedSheet(client, index):
    sheet = client.open("Street Output")
    list_of_sheets = sheet.worksheets()
    return list_of_sheets[index]

if __name__=='__main__':
    print("Run Scrapping Program?")
    print(lineSeperator())
    inp = input("1 to continue or press any key to exit => ")
    
    try:
        option = int(inp)
        if(option == 1):
            print(lineSeperator())
            print("Getting Google SpreadSheets...")
            ClearScreen()
        else:
            print("Thank You!")
            exit()
    except ValueError:
        print("Thank You!")
        exit()
    
    
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    # Get input file
    creds = ServiceAccountCredentials.from_json_keyfile_name('input.json', scope)
    streets_client = gspread.authorize(creds)

    # Get output File
    out_creds = ServiceAccountCredentials.from_json_keyfile_name('output.json', scope)
    output_client = gspread.authorize(out_creds)

    # Get final File
    final_creds = ServiceAccountCredentials.from_json_keyfile_name('final.json', scope)
    final_client = gspread.authorize(final_creds)

    # Open input spreadsheet and get all the input streets
    print("Get the Input Streets...")
    print(lineSeperator())
    
    sheet = streets_client.open('Streets')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)
    input_streets = records_df["Streets"].tolist()

    input_streets = set(input_streets)

    ClearScreen()

    option = None

    #Clear Output spreadsheet
    out_sheet = output_client.open('Street Output')
    out_sheets_list = out_sheet.worksheets()
    while option is None:
        try:
            print("Do you want to clear the Output File?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                out_sheets_list.reverse()
                for o_sheet in out_sheets_list[:-1]:
                    out_sheet.del_worksheet(o_sheet)
                print(lineSeperator())
                print("Cleared the Output File")
                time(2)
                option = None
            else:
                ClearScreen()
                break;
        except ValueError:
            ClearScreen()
    
    ClearScreen()
    
    #Clear final spreadsheet
    option = None
    final_sheet = final_client.open('Final Output')
    final_sheets_list = final_sheet.worksheets()
    while option is None:
        try:
            print("Do you want to clear the Final File?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                final_sheets_list.reverse()
                for o_sheet in final_sheets_list[:-1]:
                    try:
                        final_sheets_list.del_worksheet(o_sheet)
                    except: 
                        pass
                
                print(lineSeperator())
                print("Cleared the Final File")
                time(2)
                option = None
            else:
                ClearScreen()
                break
        except ValueError:  
            ClearScreen()
    
    ClearScreen()

    option = None

    # Run tarrant first Instance
    while option is None:
        try:
            print("Do you want to Execute the Tarrant Script 1?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                tarrant_run_1.run(input_streets=input_streets, output=out_sheet)
                print(lineSeperator())
                print("Cleared the Tarrant File")
                time(2)
                option = None
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None

    # Run tarrant second instance (Note: Use worksheet output 1)
    while option is None:
        try:
            print("Do you want to Execute the Tarrant Script 2?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                tarrant_run_2.run(GetNewCreatedSheet(output_client, 1), final_client=final_sheet)
                print(lineSeperator())
                print("Cleared the Tarrant File")
                time(2)
                option = None
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None

    # Run dallas scrappping instance 
    while option is None:
        try:
            print("Do you want to Execute the dallas Script?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                dallas_scraping.run(input_streets, out_sheet)
                print(lineSeperator())
                print("Cleared the dallas File")
                time(2)
                option = None
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None

    # Run Ellis Scrapping instance
    while option is None:
        try:
            print("Do you want to Execute the Ellis Script?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                ellis_run.run(input_streets, out_sheet)
                print(lineSeperator())
                print("Cleared the Ellis File")
                time(2)
                option = None
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None

    # Run Denoton instance 1
    while option is None:
        try:
            print("Do you want to Execute the Denton Script 1?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                denton_run_1.run(input_streets, out_sheet)
                print(lineSeperator())
                print("Cleared the Denton File")
                time(2)
                option = None
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None
    
    # Run Denton instance 2 (Note: Use worksheet output 4)
    while option is None:
        try:
            print("Do you want to Execute the Denton Script 2?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                denton_run_2.run(GetNewCreatedSheet(output_client, 4), final_sheet)
                print(lineSeperator())
                print("Cleared the Denton File")
                time(2)
                option = None
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None

    # Run Johnson instance 1 
    while option is None:
        try:
            print("Do you want to Execute the Johnson Script 1?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                johnson_run_1.run(input_streets, out_sheet)
                print(lineSeperator())
                print("Cleared the Johnson File")
                time(2)
                option = None
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None

    # Run Johnson instance 2 (Note: Use workshet Output 5)
    while option is None:
        try:
            print("Do you want to Execute the Johnson Script 2?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                johnson_run_2.run(GetNewCreatedSheet(output_client, 5), final_sheet)
                print(lineSeperator())
                print("Cleared the Johnson File")
                time(2)
                option = None
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None