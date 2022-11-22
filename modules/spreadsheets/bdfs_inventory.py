# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheet import Spreadsheet

#set up logging for this code
import logging
from modules.logger import logger
#define a sub-logger just for this code
logger = logging.getLogger('logs.Bdfs_Spreadsheet')

class Bdfs_Spreadsheet(Spreadsheet):
	
	spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'
	worksheetKeeperPattern = "inventory"