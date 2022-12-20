from modules.spreadsheets.source import Bdfs_Spreadsheet_Source
from modules.logger import logger_name

logger_name.name = "Test_Spreadsheet_Source"

class Test_Inventory_Spreadsheet_Source(Bdfs_Spreadsheet_Source):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "test"

    worksheet_class = "modules.worksheets.sources.bdfs_test.Test_Worksheet_Source"