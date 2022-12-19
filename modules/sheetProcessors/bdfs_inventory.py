# Gives us BDFS Inventory sheet processing specific functionality
# Allows for the configuration and specifics to be sandboxed
# Extends SheetProcessor to share that functionality

from modules.sheetProcessor import SheetProcessor
from modules.logger import logger_name
logger_name.name = "BdfdInventory_SheetProcessor"

class BdfsInventory_SheetProcessor(SheetProcessor):

    # spreadsheet_class = {"module": "modules.spreadsheets.bdfs_inventory", "class": "Bdfs_Spreadsheet"}
    spreadsheet_class = "modules.spreadsheets.bdfs_inventory.BdfsInventory_Spreadsheet" 