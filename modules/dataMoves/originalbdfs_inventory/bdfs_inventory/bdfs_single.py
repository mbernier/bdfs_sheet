from modules.decorator import Debugger
from modules.dataMove import DataMove
from pydantic import validate_arguments
from modules.dataMoves.exception import DataMove_Exception

class Sarto_Inventory_BarnDoor_Single_BDFS(DataMove):
    sourceClassPath = "sarto_inventory.Sarto_Inventory_Spreadsheet_Source"
    sourceWorksheetName = "barndoor_single"

    destinationClassPath = "bdfs_inventory.Bdfs_Inventory_Spreadsheet_Destination"
    destinationWorksheetName = ["barndoor_single"]

    @Debugger
    @validate_arguments
    def mapFields_barndoor_single(self, sourceData:dict): 

        # Vendor Identifier
        sourceData['Vendor Identifier'] = sourceData['URL_key']

        # Door Count
        sourceData['Number of Doors'] = sourceData['Type']
        
        # Type of Door
        sourceData['Type'] = 'Barn Door'

        #####
        # 
        # Vars For Description and Tags
        # 
        #####
        # Has Glass
        sourceData['Has Glass'] = 

        # Lites
        sourceData['Lites'] = sourceData['Glass Lites'].replace("lites","").replace("Lites", "").strip()

            # Description
            description = ""
            if "Description" in sourceData:
                description = sourceData['Description']
            sourceData['Description'] = description

        ####
        #
        # Images
        #
        ####
        # image URLs, up to 10 of them
        for counter in range(1,11):
            imageKey = f"Image {counter} URL"
            
            imageUrl = ""
            if imageKey in sourceData:
                imageUrl = sourceData[imageKey]
            
            sourceData[imageKey] = imageUrl
                
        ####
        #
        # Price Calculations
        #
        ####
            sourceData['Shipping'] = 180
            sourceData['Discount'] = self.destinationWorksheet.data.discount

        return sourceData