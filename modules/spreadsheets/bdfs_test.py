from modules.spreadsheet import Bdfs_Spreadsheet
from modules.logger import logger_name
logger_name.name = "BdfdInventory_Test_Spreadsheet"

# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

class BdfsInventory_Test_Spreadsheet(Bdfs_Spreadsheet):

    spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'

    worksheetKeeperPattern = "test"

    # worksheet_class = {"module": "modules.spreadsheets.bdfs_inventory", "class": "Bdfs_Spreadsheet"}
    worksheet_class = "modules.worksheets.bdfs_test.BdfsInventory_Test_Worksheet"