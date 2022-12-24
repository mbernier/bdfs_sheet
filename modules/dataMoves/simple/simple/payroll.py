from modules.decorator import Debugger
from modules.dataMove import DataMove
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Destination_Exception
from pydantic import validate_arguments


class SimpleToSimple_Payroll(DataMove):
    sourceClassPath = "simple_sheet.Simple_Spreadsheet_Source"
    sourceWorksheetName = "demo_worksheet"

    destinationClassPath = "simple_sheet.Simple_Spreadsheet_Destination"
    destinationWorksheetName = "test_payroll"


    @Debugger
    def init_pre_worksheets(self):
        # since this is a test script, delete the old one, so we can have a clean run here
        try:
            self.destinationSpreadsheet.deleteWorksheet(self.destinationWorksheetName)
        except Bdfs_Spreadsheet_Destination_Exception as err:
            pass #This happens bc the worksheet wasn't there, except and ignore
        
        # create the new worksheet if it doesn't exist
        self.destinationWorksheet = self.destinationSpreadsheet.insertWorksheet(self.destinationWorksheetName)


    @Debugger
    @validate_arguments
    def mapFields(self, sourceData:dict):
        #     1. Modify/Add some data in the Destination
        #         1. Calculate Hourly pay = yearly salary / 2008
        #         2. Calculate Total Pay = hourly pay * hours worked

        hourly = float(sourceData["Yearly Salary"]) / 2008
        sourceData["Hourly Pay"] = round(hourly,2)
        
        total_pay = int(sourceData["Hours Worked"]) * hourly
        sourceData["Total Pay"] = round(total_pay,2)
        
        return sourceData