# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheet import Spreadsheet

class BdfsInventory_Test_Spreadsheet(Spreadsheet):

    spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'

    worksheetKeeperPattern = "test"

    # from BaseClass - allows us to set sub loggers
    logger_name = "BdfsInventory_Test_Spreadsheet"


    # worksheet_class = {"module": "modules.spreadsheets.bdfs_inventory", "class": "Bdfs_Spreadsheet"}
    worksheet_class = "modules.worksheets.bdfs_test.BdfsInventory_Test_Worksheet"