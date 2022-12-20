from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.logger import logger_name
logger_name.name = "Simple_Spreadsheet_Destination"

class Simple_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "test"

    worksheet_class = "modules.worksheets.destinations.simple_sheet.Simple_Worksheet_Destination"