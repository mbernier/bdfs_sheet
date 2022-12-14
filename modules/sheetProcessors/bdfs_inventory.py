# Gives us BDFS Inventory sheet processing specific functionality
# Allows for the configuration and specifics to be sandboxed
# Extends SheetProcessor to share that functionality

from modules.sheetProcessor import SheetProcessor


class Bdfs_Inventory_SheetProcessor(SheetProcessor):

    # spreadsheet_class = {"module": "modules.spreadsheets.bdfs_inventory", "class": "Bdfs_Spreadsheet"}
    source_spreadsheet_class = "modules.spreadsheets.sources.bdfs_inventory.Bdfs_Inventory_Spreadsheet_Source" 
    destination_spreadsheet_class = "modules.spreadsheets.destinations.bdfs_inventory.Bdfs_Inventory_Spreadsheet_Destination" 