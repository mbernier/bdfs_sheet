from modules.decorator import Debugger
from modules.dataMove import DataMove
from pydantic import validate_arguments
from modules.dataMoves.exception import DataMove_Exception

class Originalbdfs_Inventory_To_Sarto_Inventory(DataMove):
    sourceClassPath = "originalbdfs_inventory.OriginalBdfs_Spreadsheet_Source"
    sourceWorksheetName = "test_sarto_single_inventory"

    destinationClassPath = "sarto_inventory.Sarto_Inventory_Spreadsheet_Destination"
    destinationWorksheetName = "barndoor_single"

    @Debugger
    @validate_arguments
    def mapFields(self, sourceData:dict):
        print(f"sourceData: {sourceData}")
        outputData = {}
        expectedCols = self.destination_expectedCols
        print(f"expCols: {expectedCols}")
        # Redundant items: Title, Glass, Color, SKU
        
        # URL
        sourceData['URL'] = sourceData['UnitedPorte URL']
        #sarto URL Key
        sourceData['URL_key'] = sourceData['UnitedPorte URL'].replace("https://unitedporte.us/","")
        
        # Door Count
        sourceData['Door Count'] = sourceData['Type']
        
        # Type
        sourceData['Type'] = 'Barn Door'
                
        # Lites
        sourceData['Lites'] = sourceData['Glass Lites'].replace("lites","").replace("Lites", "").strip()
        
        # Parse out the model name and number
        splitTitle = sourceData['Title'].split(" ")
        sourceData['Model'] = f"{splitTitle[0]} {splitTitle[1]}"

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
            
            if not sourceKey in sourceData.keys():
                raise DataMove_Exception(f" '{sourceKey} was not found in sources, does it need to be mapped?")
            
            outputData[outputKey] = sourceData[sourceKey]
        
        print(f"outputData: {outputData}")
        return outputData