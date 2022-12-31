import gspread
from modules.decorator import Debugger
from modules.spreadsheet import Bdfs_Spreadsheet
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Destination_Exception
from pydantic import validate_arguments


class Bdfs_Spreadsheet_Destination(Bdfs_Spreadsheet): #Passthrough to Bdfs_Spreadsheet
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @Debugger
    @validate_arguments
    def deleteWorksheet(self, worksheetName:str):

        if not worksheetName in self.getWorksheets():
            raise Bdfs_Spreadsheet_Destination_Exception(f"Worksheet '{worksheetName}' is not in the spreadsheet, cannot be deleted")

        if worksheetName in self.data.worksheets.keys():
            self.data.spreadsheet.del_worksheet(self.data.spreadsheet.worksheet(worksheetName))
            # deregister the worksheet
            del self.data.worksheets[worksheetName]
    
        if worksheetName in self.data.gspread_worksheets.keys():
            del self.data.gspread_worksheets[worksheetName]


    @Debugger
    @validate_arguments
    def insertWorksheet(self, worksheetName:str, rows:int=5, cols:int=5, index:int=None, bypassKeeperPattern=False):
        # create and store the new worksheet
        try:
            worksheet = self.data.spreadsheet.add_worksheet(title=worksheetName, rows=rows, cols=cols, index=index)
        except gspread.exceptions.APIError as err:    
            raise Bdfs_Spreadsheet_Destination_Exception(f"A sheet named {worksheetName} already exists at the destination")
        # make sure the local storage knows about the worksheet
        self.registerWorksheet(worksheet=worksheet, bypassKeeperPattern=bypassKeeperPattern)

        return self.getWorksheet(worksheetName)

    @Debugger
    @validate_arguments
    def clearWorksheet(self, worksheetName:str):
        self.data.gspread_worksheets[worksheetName].clear()
