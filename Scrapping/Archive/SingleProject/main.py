from time import sleep
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from helper import GetDallasMasterColumnsDict, GetFreeIndex, ScriptExists, RemoveScript, GetNewCreatedSheet, lineSeperator, ClearScreen, AskMessage
import tarrant_run_1, tarrant_run_2, dallas_scraping, ellis_run, denton_run_1, denton_run_2, johnson_run_1, johnson_run_2

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
                sleep(2)
                break;
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
                sleep(2)
                break;
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
                script_exists = ScriptExists(output_client, "Output", "Tarrant");
                if script_exists is False:
                    ClearScreen()
                    tarrant_run_1.run(input_streets=input_streets, output=out_sheet)
                else:
                    print(lineSeperator())
                    print("It looks like the Script already Exists in the File")
                    print(lineSeperator())
                    print("Clearing the Old Script Data for you")
                    print(lineSeperator())
                    is_removed = RemoveScript(output_client, "Output", "Tarrant")
                    if is_removed is True:
                        print("The Script is removed for you, it'll start running shortly")
                        ClearScreen()
                        tarrant_run_1.run(input_streets=input_streets, output=out_sheet)
                    else:
                        print("The Script cannot be removed and the script cannot run at this point")
                        break
                print(lineSeperator())
                sleep(2)
                break
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None

    # Run tarrant second instance
    while option is None:
        try:
            print("Do you want to Execute the Tarrant Script 2?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                script_exists = ScriptExists(final_client, "Final", "Tarrant")
                if script_exists is False:
                    ClearScreen()
                    index = GetFreeIndex(final_client, "Final")
                    tarrant_run_2.run(GetNewCreatedSheet(output_client, index), final_client=final_sheet)
                else:
                    print(lineSeperator())
                    print("It looks like the Script already Exists in the File")
                    print(lineSeperator())
                    print("Clearing the Old Script Data for you")
                    print(lineSeperator())
                    is_removed = RemoveScript(final_client, "Final", "Tarrant")
                    if is_removed is True:
                        print("The Script is removed for you, it'll start running shortly")
                        ClearScreen()
                        index = GetFreeIndex(final_client, "Final")
                        tarrant_run_2.run(GetNewCreatedSheet(output_client, index), final_client=final_sheet)
                    else:
                        print("The Script cannot be removed and the script cannot run at this point")
                        break
                print(lineSeperator())
                sleep(2)
                break;
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
                script_exists = ScriptExists(output_client, "Output", "Dallas Scrapping");
                if script_exists is False:
                    ClearScreen()
                    dallas_scraping.run(GetDallasMasterColumnsDict(), out_sheet)
                else:
                    print(lineSeperator())
                    print("It looks like the Script already Exists in the File")
                    print(lineSeperator())
                    print("Clearing the Old Script Data for you")
                    print(lineSeperator())
                    is_removed = RemoveScript(output_client, "Output", "Dallas Scrapping")
                    if is_removed is True:
                        print("The Script is removed for you, it'll start running shortly")
                        ClearScreen()
                        dallas_scraping.run(GetDallasMasterColumnsDict(), out_sheet)
                    else:
                        print("The Script cannot be removed and the script cannot run at this point")
                        break
                print(lineSeperator())
                sleep(2)
                break
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
                script_exists = ScriptExists(output_client, "Output", "Ellis Scrapping");
                if script_exists is False:
                    ClearScreen()
                    ellis_run.run(input_streets, out_sheet)
                else:
                    print(lineSeperator())
                    print("It looks like the Script already Exists in the File")
                    print(lineSeperator())
                    print("Clearing the Old Script Data for you")
                    print(lineSeperator())
                    is_removed = RemoveScript(output_client, "Output", "Ellis Scrapping")
                    if is_removed is True:
                        print("The Script is removed for you, it'll start running shortly")
                        ClearScreen()
                        ellis_run.run(input_streets, out_sheet)
                    else:
                        print("The Script cannot be removed and the script cannot run at this point")
                        break
                print(lineSeperator())
                sleep(2)
                break
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
                script_exists = ScriptExists(output_client, "Output", "Denton");
                if script_exists is False:
                    ClearScreen()
                    denton_run_1.run(input_streets, out_sheet)
                else:
                    print(lineSeperator())
                    print("It looks like the Script already Exists in the File")
                    print(lineSeperator())
                    print("Clearing the Old Script Data for you")
                    print(lineSeperator())
                    is_removed = RemoveScript(output_client, "Output", "Denton")
                    if is_removed is True:
                        print("The Script is removed for you, it'll start running shortly")
                        ClearScreen()
                        denton_run_1.run(input_streets, out_sheet)
                    else:
                        print("The Script cannot be removed and the script cannot run at this point")
                        break
                print(lineSeperator())
                sleep(2)
                break
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None
    # Run Denton instance 2
    while option is None:
        try:
            print("Do you want to Execute the Denton Script 2?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                script_exists = ScriptExists(final_client, "Final", "Denton")
                if script_exists is False:
                    ClearScreen()
                    index = GetFreeIndex(final_client, "Final")
                    denton_run_2.run(GetNewCreatedSheet(output_client, index + 1), final_sheet)
                else:
                    print(lineSeperator())
                    print("It looks like the Script already Exists in the File")
                    print(lineSeperator())
                    print("Clearing the Old Script Data for you")
                    print(lineSeperator())
                    is_removed = RemoveScript(final_client, "Final", "Denton")
                    if is_removed is True:
                        print("The Script is removed for you, it'll start running shortly")
                        ClearScreen()
                        index = GetFreeIndex(final_client, "Final")
                        denton_run_2.run(GetNewCreatedSheet(output_client, index), final_sheet)
                    else:
                        print("The Script cannot be removed and the script cannot run at this point")
                        break
                print(lineSeperator())
                sleep(2)
                break
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
                script_exists = ScriptExists(output_client, "Output", "Johnson");
                if script_exists is False:
                    ClearScreen()
                    johnson_run_1.run(input_streets, out_sheet)
                else:
                    print(lineSeperator())
                    print("It looks like the Script already Exists in the File")
                    print(lineSeperator())
                    print("Clearing the Old Script Data for you")
                    print(lineSeperator())
                    is_removed = RemoveScript(output_client, "Output", "Johnson")
                    if is_removed is True:
                        print("The Script is removed for you, it'll start running shortly")
                        ClearScreen()
                        johnson_run_1.run(input_streets, out_sheet)
                    else:
                        print("The Script cannot be removed and the script cannot run at this point")
                        break
                print(lineSeperator())
                sleep(2)
                break
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None
    # Run Johnson instance 2
    while option is None:
        try:
            print("Do you want to Execute the Johnson Script 2?")
            print(lineSeperator())
            option = int(input(AskMessage()))
            if option == 1:
                script_exists = ScriptExists(final_client, "Final", "Johnson")
                if script_exists is False:
                    ClearScreen()
                    index = GetFreeIndex(final_client, "Final")
                    johnson_run_2.run(GetNewCreatedSheet(output_client, index), final_sheet)
                else:
                    print(lineSeperator())
                    print("It looks like the Script already Exists in the File")
                    print(lineSeperator())
                    print("Clearing the Old Script Data for you")
                    print(lineSeperator())
                    is_removed = RemoveScript(final_client, "Final", "Johnson")
                    if is_removed is True:
                        print("The Script is removed for you, it'll start running shortly")
                        ClearScreen()
                        index = GetFreeIndex(final_client, "Final")
                        johnson_run_2.run(GetNewCreatedSheet(output_client, index), final_sheet)
                    else:
                        print("The Script cannot be removed and the script cannot run at this point")
                        break
                print(lineSeperator())
                sleep(2)
                break
            else:
                ClearScreen()
                break
        except ValueError:
            ClearScreen()
    
    ClearScreen()

    option = None