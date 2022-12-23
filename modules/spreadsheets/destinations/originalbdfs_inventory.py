# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination

class OriginalBdfs_Inventory_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):

    spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'

    worksheetKeeperPattern = "inventory"

    worksheet_class = "modules.worksheets.bdfs_inventory.destinations.OriginalBdfs_Inventory_Worksheet_Destination"