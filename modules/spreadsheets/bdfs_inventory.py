# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheet import Spreadsheet

class Bdfs_Spreadsheet(Spreadsheet):

    spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'
    worksheetKeeperPattern = "inventory"

    # from BaseClass - allows us to set sub loggers
    logger_name = "Bdfs_Spreadsheet"