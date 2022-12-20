from modules.spreadsheet import Bdfs_Spreadsheet
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Destination_Exception

class Bdfs_Spreadsheet_Destination(Bdfs_Spreadsheet): #Passthrough to Bdfs_Spreadsheet
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)