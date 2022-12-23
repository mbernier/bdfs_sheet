# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination

class Sarto_Inventory_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):

    spreadsheetId = '16gp8awjSaawEdBvV6bLDUQoA5Ha-j1NB82O2Zifhmns'

    worksheetKeeperPattern = "inventory"

    worksheet_class = "modules.worksheets.bdfs_inventory.destinations.Sarto_Inventory_Worksheet_Destination"