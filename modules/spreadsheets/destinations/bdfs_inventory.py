# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination


class BdfsInventory_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):

    spreadsheetId = '18XKqjmJrWk1TVRfJtUm584wUaPU3vMzt7EoKTgA_Vmo'

    worksheetKeeperPattern = "inventory"

    # worksheet_class = {"module": "modules.spreadsheets.bdfs_inventory", "class": "Bdfs_Spreadsheet"}
    worksheet_class = "modules.worksheets.destinations.bdfs_inventory.BdfsInventory_Worksheet_Destination"