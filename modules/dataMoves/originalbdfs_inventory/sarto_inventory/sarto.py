from pydantic import validate_arguments
from modules.caches.flat import UPDATE_TIMESTAMP_KEY
from modules.dataMoves.exception import DataMove_Exception
from modules.decorator import Debugger
from modules.dataMove import DataMove
from modules.helper import Helper

# @todo get the information about how each door is built
#   - Does it have solid wood frame? Solid all the way through?
#   - does it have a beehive interior, something else?
#   - what other data should we get from Sarto about the doors?
class Originalbdfs_Inventory_To_Sarto_Inventory(DataMove):
    sourceClassPath = "originalbdfs_inventory.OriginalBdfs_Spreadsheet_Source"
    sourceWorksheetName = "sarto_barn_single_inventory"

    destinationClassPath = "sarto_inventory.Sarto_Inventory_Spreadsheet_Destination"
    destinationWorksheetNames = ["barndoor_single", "slabs_single"]

    destinationWorksheetCreateIfNotFound = True #this is redundant, is in the parent class

    @Debugger
    @validate_arguments
    def doorFields(self, worksheetName:str, sourceData:dict):
        self.run_hook("\nstart_doorFields", worksheetName=worksheetName, sourceData=sourceData)
        
        expectedCols = self.destinationWorksheets[worksheetName].getColumns()
        originalData = sourceData.copy()

        # URL
        sourceData['URL'] = self.prepUrl(sourceData.copy())
        
        # URL key
        sourceData['URL_key'] = self.prepUrlKey(sourceData.copy(), worksheetName=worksheetName)

        # Door Count
        sourceData['Door Count'] = sourceData['Type']
        
        # Type
        sourceData['Type'] = 'Barn Door'
                
        # Lites
        sourceData['Lites'] = self.prepLites(sourceData)

        # Hardware
        sourceData, hardwareSKU = self.prepHardware(sourceData)

        # Glass
        sourceData, glassSKU = self.prepGlass(sourceData)
        
        sourceData['Pre-drilled For Hardware'] = "No"

        # Parse out the model name and number
        sourceData['Model'] = self.prepModel(sourceData.copy(), worksheetName=worksheetName)

        # this will rewrite sourceData with the new images 
        sourceData = self.prepImages(sourceData)

        # Description
        sourceData['Description'] = self.prepDescription(sourceData.copy())

        sourceData['Shipping'] = 180

        sourceData['Discount'] = self.prepDiscount(worksheetName)

        # {vendor}::{modelname}_{modelNumber}::{door_type}::glass_{glass_type}::hardware_{hardware_type}_{hardware_color}
        # sartodoors::lydia_3355::single::white::glass_clear::hardware_rail_black
        sourceData['SKU'] = "{}::{}::{}::{}::{}".format(
                "sartodoors",
                sourceData['Model'].replace(" ","_"),
                sourceData['Type'],
                sourceData['Color'],
                glassSKU,
                hardwareSKU).lower()

        # clean up the keys
        sourceDataKeys = sourceData.keys()

        for key in expectedCols:
            outputData = None
            sourceKey = key
            # original sheet has shitty keys, this was supposed to be easier than fixing spreadsheet

            if "\"x" in sourceKey:
                #destination wants '18"x40"' and source has '18" x40"'
                sourceKey = sourceKey.replace("\"x","\" x ").replace("  ", " ")
            

            if "Cost:" in key:
                if not UPDATE_TIMESTAMP_KEY in key:
                    # Map in the discount for Sarto doors, from the public retail price
                    sourceData[key] = self.calculatePrice(sourceKey, worksheetName, sourceData.copy())
                elif self.cleanPriceKey(key) in sourceDataKeys:
                    sourceData[key] = sourceData[self.cleanPriceKey(key)]

            elif "Price:" in key:
                sourceKey = sourceKey.replace("Retail Price: ", "Price:")
                if sourceKey in sourceDataKeys:
                    sourceData[key] = sourceData[sourceKey]

            elif not key in sourceDataKeys:
                sourceData[key] = None
        
        self.run_hook("end_doorFields", newFields=Helper.listDiff(sourceData, originalData))
        return sourceData


    @Debugger
    @validate_arguments
    def barndoor_single(self, sourceData:dict):
        self.run_hook("\nstart_mapFields_barndoor_single", hardware=sourceData['Hardware'])
        if not "Slab" in sourceData['Hardware']:
            self.skipItem['barndoor_single'] = False
            self.run_hook("mapFields_barndoor_single_is_not_slab")
            self.run_hook("mapFields_barndoor_single_is_not_slab_pre_door_fields")
            sourceData = self.doorFields('barndoor_single', sourceData.copy())
            self.run_hook("mapFields_barndoor_single_is_not_slab_post_door_fields")
        else:
            self.run_hook("mapFields_barndoor_single_is_slab")
            self.skipItem['barndoor_single'] = True
        self.run_hook("end_mapFields_barndoor_single")
        return sourceData
    

    @Debugger
    @validate_arguments
    def slabs_single(self, sourceData:dict):
        self.run_hook("\nstart_mapFields_slabs_single", hardware=sourceData['Hardware'])
    
        if "Slab" in sourceData['Hardware']:
            self.skipItem['slabs_single'] = False
            self.run_hook("mapFields_slabs_single_is_slab")
            self.run_hook("mapFields_slabs_single_is_slab_pre_door_fields")
            sourceData = self.doorFields('slabs_single', sourceData.copy())
            self.run_hook("mapFields_slabs_single_is_slab_post_door_fields")
        else:
            self.run_hook("mapFields_slabs_single_is_not_slab")
            self.skipItem['slabs_single'] = True
        self.run_hook("end_mapFields_slabs_single")
        return sourceData


    @Debugger
    @validate_arguments
    def prepUrl(self, sourceData:dict):
        self.run_hook('start_prepUrl')
        url = sourceData['UnitedPorte URL']
        self.run_hook('end_prepUrl')
        return url


    @Debugger
    @validate_arguments
    def prepUrlKey(self, sourceData:dict, worksheetName:str):
        self.run_hook("start_prepUrlKey", url=sourceData['URL'])
        output = None
        if "" == sourceData['URL']:
            self.run_hook("prepUrlKey_url_is_blank", url=sourceData['URL'])
            self.noteProblem(worksheetName, "URL", f"Door with no URL: '{sourceData['Title']}'")
        else:
            self.run_hook("prepUrlKey_url_not_blank", url=sourceData['URL'])
            #sarto URL Key
            output = sourceData['UnitedPorte URL'].replace("https://unitedporte.us/","")
        
        self.run_hook("end_prepUrlKey", urlKey=output)
        return output


    @Debugger
    @validate_arguments
    def prepModel(self, sourceData:dict, worksheetName:str):
        self.run_hook("start_prepModel")
        output = None
        if "" != sourceData['Title']:
            self.run_hook("prepModel_title_not_empty", title=sourceData['Title'])
            splitTitle = sourceData['Title'].split(" ")
            if 1 < len(splitTitle):
                output = f"{splitTitle[0]} {splitTitle[1]}"
        else:
            self.run_hook("prepModel_title_is_empty", title=sourceData['Title'])
            self.noteProblem(worksheetName, "Title", f"Door with No Title: '{', '.join(sourceData)}'")
            return
        self.run_hook("end_prepModel")
        return output

    @Debugger
    @validate_arguments
    def prepGlass(self, sourceData:dict):
        glassSKU = "glass_"
        if sourceData['Glass'] == "No":
            sourceData['Has Glass'] = "No"
            sourceData['Glass Finish'] = "None"
            glassSKU += "No"
        else:
            sourceData['Has Glass'] = "Yes"
            sourceData['Glass Finish'] = sourceData['Glass']
            glassSKU += f"{sourceData['Glass Finish']}"
        return sourceData, glassSKU
    
    @Debugger
    @validate_arguments
    def prepHardware(self, sourceData:dict):
        hardwareSKU = "hardware_"
        if sourceData['Hardware'] == "Slab":
            sourceData['Hardware Type'] = "None"
            sourceData['Hardware Color'] = "None"
            sourceData['Hardware'] = "None"
            hardwareSKU += "No"
        else:
            sourceData['Hardware Type'] = "Rail"
            sourceData['Hardware Color'] = sourceData['Hardware']
            sourceData['Hardware'] = f"{sourceData['Hardware']} Rail with predrilled holes, {sourceData['Hardware']} Hangers with wheels, Door stops, Plastic Fin Floor guide, and Mounting screws"
            hardwareSKU += f"{sourceData['Hardware Type']}_{sourceData['Hardware Color']}"
        return sourceData
    
    @Debugger
    @validate_arguments
    def prepLites(self, sourceData):
        return sourceData['Glass Lites'].replace("lites","").replace("Lites", "").strip()