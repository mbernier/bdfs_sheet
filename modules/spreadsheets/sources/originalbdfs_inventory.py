# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheets.source import Bdfs_Spreadsheet_Source
from modules.logger import logger_name

logger_name.name = "OriginalBdfs_Inventory_Spreadsheet_Source"

class OriginalBdfs_Spreadsheet_Source(Bdfs_Spreadsheet_Source):

    spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'

    worksheetKeeperPattern = "inventory"

    worksheet_class = "modules.worksheets.bdfs_inventory.sources.OriginalBdfs_Inventory_Worksheet_Source"