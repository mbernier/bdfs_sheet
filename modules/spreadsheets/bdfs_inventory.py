# spreadsheet class specific to the BDFS Inventory spreadsheet
# allows us to sandbox the specifics that we need for this spreadsheet into one place

from modules.spreadsheet import Spreadsheet

class Bdfs_Spreadsheet(Spreadsheet):
	
	spreadsheetId = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'

	# calls the parent __init__ method to make sure the spreadsheetId gets set
	def _init_(self): 
		super(Bdfs_Spreadsheet, self).__init__(self.spreadsheetId)

	def getSpreadsheetId(self):
		return self.spreadsheetId

	