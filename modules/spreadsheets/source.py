from modules.spreadsheet import Bdfs_Spreadsheet
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Source_Exception

class Bdfs_Spreadsheet_Source(Bdfs_Spreadsheet): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def modifiesData(self):
        raise Bdfs_Spreadsheet_Source_Exception("Source Spreadsheets are not allowed to modify data")