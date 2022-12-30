import gspread, time
from modules.spreadsheets.destinations.simple_sheet import Simple_Spreadsheet_Destination
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Destination_Exception

def destination_helper(test_worksheet, worksheetName, copyFromWorksheetName, renameWorksheetName, method=None):
    if method == True or method.__name__ in ["test_commit", "test_commit_with_larger_data"]:
        
        sheet = Simple_Spreadsheet_Destination()
        spreadsheet = sheet.setupSpreadsheet()
        time.sleep(5)
        
        # see if the sheetName 
        try:
            sheet.deleteWorksheet(worksheetName)
            time.sleep(5)
            print(f"\tWorksheet: {renameWorksheetName} found, it was deleted")
        except Bdfs_Spreadsheet_Destination_Exception:
            print(f"\tWorksheet: {worksheetName} isn't found, will create it")

        try:
            sheet.deleteWorksheet(renameWorksheetName)
            time.sleep(5)
            print(f"\tWorksheet: {renameWorksheetName} found, it was deleted")

        except Bdfs_Spreadsheet_Destination_Exception:
            print(f"\tWorksheet: {renameWorksheetName} wasn't found, isn't that nice!")

        print(f"\tCreating Worksheet: {worksheetName} from {copyFromWorksheetName}")
        worksheet1 = spreadsheet.worksheet(copyFromWorksheetName)
        worksheet2 = worksheet1.duplicate(1, None, worksheetName) 
        time.sleep(5)

        del spreadsheet
        del worksheet1
        del worksheet2
        ####
        #
        # Create a spreadsheet for the tests to run on
        #
        ####
        sheet.setupWorksheets(use_cache=False)
        test_worksheet = sheet.getWorksheet(worksheetName)
        time.sleep(5)
    return test_worksheet