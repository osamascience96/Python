import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import tarrant_run_1, tarrant_run_2, dallas_scraping, ellis_run, denton_run_1, denton_run_2, johnson_run_1, johnson_run_2

def GetNewCreatedSheet(client, index):
    sheet = client.open("Street Output")
    list_of_sheets = sheet.worksheets()
    return list_of_sheets[index]

if __name__=='__main__':
    print("Getting Google SpreadSheets...")
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
    sheet = streets_client.open('Streets')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)
    input_streets = records_df["Streets"].tolist()

    input_streets = set(input_streets)

    #Clear Output spreadsheet
    out_sheet = output_client.open('Street Output')
    out_sheets_list = out_sheet.worksheets()
    out_sheets_list.reverse()
    for o_sheet in out_sheets_list[:-1]:
        out_sheet.del_worksheet(o_sheet)
    
    #Clear final spreadsheet
    final_sheet = final_client.open('Final Output')
    final_sheets_list = final_sheet.worksheets()
    final_sheets_list.reverse()
    for o_sheet in final_sheets_list[:-1]:
        try:
            final_sheets_list.del_worksheet(o_sheet)
        except: 
            pass

    # Run tarrant first Instance
    tarrant_run_1.run(input_streets=input_streets, output=out_sheet)

    # Run tarrant second instance (Note: Use worksheet output 1)
    tarrant_run_2.run(GetNewCreatedSheet(output_client, 1), final_client=final_sheet)

    # Run dallas scrappping instance 
    dallas_scraping.run(input_streets, out_sheet)

    # Run Ellis Scrapping instance
    ellis_run.run(input_streets, out_sheet)

    # Run Denoton instance 1
    denton_run_1.run(input_streets, out_sheet)
    
    # Run Denton instance 2 (Note: Use worksheet output 4)
    denton_run_2.run(GetNewCreatedSheet(output_client, 4), final_sheet)

    # Run Johnson instance 1 
    johnson_run_1.run(input_streets, out_sheet)

    # Run Johnson instance 2 (Note: Use workshet Output 5)
    johnson_run_2.run(GetNewCreatedSheet(output_client, 5), final_sheet)