# Gives us BDFS Inventory sheet processing specific functionality
# Allows for the configuration and specifics to be sandboxed
# Extends SheetProcessor to share that functionality

from modules.sheetProcessor import SheetProcessor

class BdfsInventory_SheetProcessor(SheetProcessor):

    # from BaseClass - allows us to set sub loggers
    logger_name = "BdfsInventory_SheetProcessor"

    # spreadsheet_class = {"module": "modules.spreadsheets.bdfs_inventory", "class": "Bdfs_Spreadsheet"}
    spreadsheet_class = "modules.spreadsheets.bdfs_inventory.BdfsInventory_Spreadsheet" 