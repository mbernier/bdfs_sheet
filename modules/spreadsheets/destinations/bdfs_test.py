from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.logger import logger_name
logger_name.name = "BdfdInventory_Test_Spreadsheet_Destination"

class BdfsInventory_Test_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'

    worksheetKeeperPattern = "test"

    worksheet_class = "modules.worksheets.destinations.bdfs_test.BdfsInventory_Test_Worksheet_Destination"