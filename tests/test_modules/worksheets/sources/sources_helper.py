import gspread
from modules.spreadsheets.sources.bdfs_test import BdfsInventory_Test_Spreadsheet_Source

def worksheet_helper(test_worksheet, worksheetName, copyFromWorksheetName, renameWorksheetName, method=None):
    if method == True or method.__name__ in ["test_commit", "test_commit_with_larger_data"]:

        sheet = BdfsInventory_Test_Spreadsheet_Source()
        spreadsheet = sheet.setupSpreadsheet()

        # see if the sheetName 
        try:
            testWorksheetExists = spreadsheet.worksheet(worksheetName)
            print(f"Worksheet: {worksheetName} found, deleting it")
            spreadsheet.del_worksheet(testWorksheetExists)

        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet: {worksheetName} isn't found, creating it")

        try:
            testWorksheetExists = spreadsheet.worksheet(renameWorksheetName)
            print(f"Worksheet: {renameWorksheetName} found, deleting it")
            spreadsheet.del_worksheet(testWorksheetExists)

        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet: {renameWorksheetName} wasn't found, isn't that nice!")

        worksheet1 = spreadsheet.worksheet(copyFromWorksheetName)
        worksheet2 = worksheet1.duplicate(1, None, worksheetName)

        del sheet
        del spreadsheet
        del worksheet1
        del worksheet2
        ####
        #
        # Create a spreadsheet for the tests to run on
        #
        ####
        sheet = BdfsInventory_Test_Spreadsheet_Source() 
        test_worksheet = sheet.getWorksheet(worksheetName)
    return test_worksheet