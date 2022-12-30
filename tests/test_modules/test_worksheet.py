import time
from gspread import Worksheet
from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.worksheet import Bdfs_Worksheet

class Good_Simple_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "demo"

    worksheet_class = "tests.test_modules.worksheets.test_destination.Good_Worksheet_Destination"


# this test just makes sure that what we are doing in Worksheet __init__ is tested and fails if it doesn't work
def test_worksheet_init():
    sheet = Good_Simple_Spreadsheet_Destination()
    sheet.setupSpreadsheet()
    time.sleep(5)

    gspread_worksheets = sheet.data.spreadsheet.worksheets()
    time.sleep(5)
    
    assert type(gspread_worksheets[0]) == Worksheet

    worksheet = Bdfs_Worksheet(gspread_worksheets[0])

    assert type(worksheet) == Bdfs_Worksheet