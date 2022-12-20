# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.logger import logger_name

logger_name.name = "BdfsInventory_Spreadsheet_Destination"

class BdfsInventory_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):

    spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'

    worksheetKeeperPattern = "inventory"

    # worksheet_class = {"module": "modules.spreadsheets.bdfs_inventory", "class": "Bdfs_Spreadsheet"}
    worksheet_class = "modules.worksheets.bdfs_inventory.destinations.BdfsInventory_Worksheet_Destination"