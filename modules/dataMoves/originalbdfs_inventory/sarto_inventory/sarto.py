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
        expectedCols = self.destination_expectedCols
        # URL
        sourceData['URL'] = sourceData['UnitedPorte URL']
        # Title
        sourceData['Title'] = sourceData['Title']
        # Door Count
        sourceData['Door Count'] = sourceData['Type']
        # Type
        sourceData['Type'] = 'Barn Door'
        # Glass
        sourceData['Glass'] = sourceData['Glass']
        # Lites
        sourceData['Lites'] = sourceData['Glass Lites'].replace("lites","").strip()
        # Color
        sourceData['Color'] = sourceData['Color']
        # Hardware
        sourceData['Hardware'] = sourceData['Hardware']
        # SKU
        sourceData['SKU'] = sourceData['SKU']

        # image URLs, up to 10 of them
        for counter in range(1,11):
            imageKey = f"Image {counter} URL"
            
            imageUrl = ""
            if imageKey in sourceData:
                imageUrl = sourceData[imageKey]
            
            sourceData[imageKey] = imageUrl
                
        # Description
        description = ""
        if "Description" in sourceData:
            description = sourceData['Description']
        sourceData['Description'] = description

        for key in expectedCols:
            sourceKey = key
            outputKey = key

            # original sheet has shitty keys, this is easier than fixing spreadsheet
            if "Cost:" in key:
                sourceKey = key.replace("Cost: ", "Cost:")
                outputKey = key
            elif "Price:" in key:
                sourceKey = key.replace("Retail Price: ", "Price:")
                outputKey = key

            # fix another key issue            
            if "\"x" in sourceKey:
                sourceKey = sourceKey.replace("\"x","\" x ")

            outputData[outputKey] = sourceData[sourceKey]
        
        return outputData