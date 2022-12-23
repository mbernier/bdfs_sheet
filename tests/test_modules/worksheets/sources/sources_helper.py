import gspread, time
from modules.spreadsheets.sources.simple_sheet import Simple_Spreadsheet_Source
from modules.spreadsheets.destinations.simple_sheet import Simple_Spreadsheet_Destination
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Source_Exception, Bdfs_Spreadsheet_Destination_Exception

def sources_helper(test_worksheet, worksheetName, copyFromWorksheetName, renameWorksheetName, method=None):
    if method == True or method.__name__ in ["test_commit", "test_commit_with_larger_data"]:
        #buy some favor from google sheets API
        time.sleep(0.5)
        
        sheet = Simple_Spreadsheet_Destination()
        spreadsheet = sheet.setupSpreadsheet()

        # see if the worksheet exists
        try:
            sheet.deleteWorksheet(worksheetName)
            print(f"\tWorksheet: {worksheetName} found, it was deleted")
        except Bdfs_Spreadsheet_Destination_Exception:
            print(f"\tWorksheet: {worksheetName} isn't found, creating it")

        try:
            sheet.deleteWorksheet(renameWorksheetName)
            print(f"\tWorksheet: {renameWorksheetName} found, it was deleted")

        except Bdfs_Spreadsheet_Destination_Exception:
            print(f"\tWorksheet: {renameWorksheetName} wasn't found, isn't that nice!")

        worksheet1 = spreadsheet.worksheet(copyFromWorksheetName)
        worksheet2 = worksheet1.duplicate(1, None, worksheetName)

        del spreadsheet
        del worksheet1
        del worksheet2
        ####
        #
        # Create a spreadsheet for the tests to run on
        #
        ####
        sheet = Simple_Spreadsheet_Source()
        sheet.setupWorksheets(use_cache=False)
        test_worksheet = sheet.getWorksheet(worksheetName)
    return test_worksheet