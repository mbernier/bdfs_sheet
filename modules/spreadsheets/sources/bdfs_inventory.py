# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheets.source import Bdfs_Spreadsheet_Source

class BdfsInventory_Spreadsheet_Source(Bdfs_Spreadsheet_Source):

    spreadsheetId = '18XKqjmJrWk1TVRfJtUm584wUaPU3vMzt7EoKTgA_Vmo'

    worksheetKeeperPattern = "inventory"

    worksheet_class = "modules.worksheets.bdfs_inventory.sources.BdfsInventory_Worksheet_Source"