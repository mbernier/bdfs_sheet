from modules.spreadsheets.source import Bdfs_Spreadsheet_Source
from modules.logger import logger_name
logger_name.name = "BdfdInventory_Test_Spreadsheet_Source"

class BdfsInventory_Test_Spreadsheet_Source(Bdfs_Spreadsheet_Source):
    spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'

    worksheetKeeperPattern = "test"

    worksheet_class = "modules.worksheets.sources.bdfs_test.BdfsInventory_Test_Worksheet_Source"