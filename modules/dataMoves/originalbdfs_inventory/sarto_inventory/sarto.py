from modules.decorator import Debugger
from modules.dataMove import DataMove
from pydantic import validate_arguments
from modules.dataMoves.exception import DataMove_Exception

class Originalbdfs_Inventory_To_Sarto_Inventory(DataMove):
    sourceClassPath = "originalbdfs_inventory.OriginalBdfs_Spreadsheet_Source"
    sourceWorksheetName = "sarto_barn_single_inventory"

    destinationClassPath = "sarto_inventory.Sarto_Inventory_Spreadsheet_Destination"
    destinationWorksheetNames = ["barndoor_single", "slabs"]

    @Debugger
    @validate_arguments
    def mapFields(self, sourceData:dict):
        
        expectedCols = self.destination_expectedCols
        
        # Redundant items: Title, Color, SKU
        
        # URL
        sourceData['URL'] = sourceData['UnitedPorte URL']
        if "" == sourceData['URL']:
            self.noteProblem("URL", f"Door with no URL: '{sourceData['Title']}'")
            return
        else:
            #sarto URL Key
            sourceData['URL_key'] = sourceData['UnitedPorte URL'].replace("https://unitedporte.us/","")

        # Door Count
        sourceData['Door Count'] = sourceData['Type']
        
        # Type
        sourceData['Type'] = 'Barn Door'
                
        # Lites
        sourceData['Lites'] = sourceData['Glass Lites'].replace("lites","").replace("Lites", "").strip()

        # Hardware
        if sourceData['Hardware'] == "slab":
            sourceData['Hardware Type'] = "None"
            sourceData['Hardware Color'] = "None"
            sourceData['Hardware'] = "None"
        else:
            sourceData['Hardware Type'] = "Rail"
            sourceData['Hardware Color'] = sourceData['Hardware'] 
            sourceData['Hardware'] = "Rail with predrilled holes, Hangers with wheels, Door stops, Floor guide, Mounting screws"

        # Glass
        if sourceData['Glass'] == "No":
            sourceData['Has Glass'] = "No"
            sourceData['Glass Finish'] = "None"
        else:
            sourceData['Has Glass'] = "Yes"
            sourceData['Glass Finish'] = sourceData['Glass']

        if 'Finish' not in sourceData.keys():
            sourceData['Finish'] = ""

        if 'Materials' not in sourceData.keys():
            sourceData['Materials'] = ""

        if 'Door Thickness' not in sourceData.keys():
            sourceData['Door Thickness'] = ""
        
        sourceData['Pre-drilled For Hardware'] = "No"

        # Parse out the model name and number
        if "" != sourceData['Title']:
            splitTitle = sourceData['Title'].split(" ")
            if 1 < len(splitTitle):
                sourceData['Model'] = f"{splitTitle[0]} {splitTitle[1]}"
        else:
            self.noteProblem("Title", f"Door with No Title: '{', '.join(sourceData)}'")
            return

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

        sourceData['Shipping'] = 180
        sourceData['Discount'] = self.destinationWorksheet.data.discount

        # clean up the keys
        for key in expectedCols:
            sourceKey = key
            # original sheet has shitty keys, this is easier than fixing spreadsheet
            # fix another key issue            

            if "\"x" in key:
                #destination wants '18"x40"' and source has '18" x40"'
                sourceKey = sourceKey.replace("\"x","\" x ").replace("  ", " ")

            if "Cost:" in key:
                sourceKey = sourceKey.replace("Cost: ", "Cost:")
                outputKey = key
                # Map in the discount for Sarto doors, from the public retail price
            
                newKey = sourceKey.replace("Cost", "Price")
                priceString = sourceData[sourceKey.replace("Cost", "Price")].replace(",","").replace("$","")
                price = 0
                if '' != priceString: # sometimes we don't have a price for a door
                    price = float(priceString)
                outputData = price * (1 - sourceData['Discount'])

            elif "Price:" in key:
                sourceKey = sourceKey.replace("Retail Price: ", "Price:")
                outputKey = key
                outputData = sourceData[sourceKey]
            else:
                continue # nothing to see here, skip it
            
            # write the data to the sourceData obj
            sourceData[key] = outputData


        return sourceData