from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.logger import logger_name
logger_name.name = "Test_Spreadsheet_Destination"

class Test_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "test"

    worksheet_class = "modules.worksheets.destinations.bdfs_test.Test_Worksheet_Destination"