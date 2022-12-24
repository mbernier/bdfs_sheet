from modules.decorator import Debugger
from modules.dataMove import DataMove
from pydantic import validate_arguments


class Originalbdfs_Inventory_To_Sarto_Inventory(DataMove):
    sourceClassPath = "originalbdfs_inventory.OriginalBdfs_Spreadsheet_Source"
    sourceWorksheetName = "sarto_barn_single_inventory"

    destinationClassPath = "sarto_inventory.Sarto_Inventory_Spreadsheet_Destination"
    destinationWorksheetName = "barndoor_single"

    @Debugger
    @validate_arguments
    def mapFields(self, sourceData:dict):
        outputData = {}

        # URL
        outputData['Url'] = sourceData['UnitedPorte URL']
        # Title
        outputData['Title'] = sourceData['Title']
        # Door Count
        outputData['Door Count'] = sourceData['Type']
        # Type
        outputData['Type'] = 'Barn Door'
        # Glass
        outputData['Glass'] = sourceData['Glass']
        # Lites
        outputData['Lites'] = sourceData['Glass Lites'].replace("lites","").strip()
        # Color
        outputData['Color'] = sourceData['Color']
        # Hardware
        outputData['Hardware'] = sourceData['Hardware']
        # SKU
        outputData['SKU'] = sourceData['SKU']

        # image URLs, up to 10 of them
        for counter in range(1,11):
            imageKey = f"Image {counter} URL"
            if imageKey in sourceData:
                outputData[imageKey] = sourceData[imageKey]

        # Description
        outputData['Description'] = sourceData['Description']
        
        return outputData