from modules.decorator import Debugger
from modules.dataMove import DataMove
from pydantic import validate_arguments


class Originalbdfs_Inventory_To_Sarto_Inventory(DataMove):
    sourceClassPath = "originalbdfs_inventory.OriginalBdfs_Spreadsheet_Source"
    sourceWorksheetName = "sarto_barn_single_inventory"

    destinationClassPath = "originalbdfs_inventory.OriginalBdfs_Spreadsheet_Destination"
    destinationWorksheetName = "barndoor_single"

    @Debugger
    @validate_arguments
    def mapFields(self, sourceData:dict):

        # hourly = float(sourceData["Yearly Salary"]) / 2008
        # sourceData["Hourly Pay"] = round(hourly,2)
        
        # total_pay = int(sourceData["Hours Worked"]) * hourly
        # sourceData["Total Pay"] = round(total_pay,2)
        
        return sourceData
