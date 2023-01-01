from pydantic import validate_arguments
from modules.caches.flat import UPDATE_TIMESTAMP_KEY
from modules.dataMoves.exception import DataMove_Exception
from modules.decorator import Debugger
from modules.dataMove import DataMove
from modules.helper import Helper


class Originalbdfs_Inventory_To_Sarto_Inventory(DataMove):
    sourceClassPath = "originalbdfs_inventory.OriginalBdfs_Spreadsheet_Source"
    sourceWorksheetName = "sarto_barn_single_inventory"

    destinationClassPath = "sarto_inventory.Sarto_Inventory_Spreadsheet_Destination"
    destinationWorksheetNames = ["barndoor_single", "slabs_single"]

    destinationWorksheetCreateIfNotFound = True

    @Debugger
    @validate_arguments
    def doorFields(self, worksheetName:str, sourceData:dict):
        self.run_hook("\nstart_doorFields", worksheetName=worksheetName, sourceData=sourceData)
        
        expectedCols = self.destinationWorksheets[worksheetName].getColumns()
        originalData = sourceData.copy()

        # URL
        sourceData['URL'] = self.prepUrl(sourceData.copy())
        
        # URL key
        sourceData['URL_key'] = self.prepUrlKey(sourceData.copy())

        # Door Count
        sourceData['Door Count'] = sourceData['Type']
        
        # Type
        sourceData['Type'] = 'Barn Door'
                
        # Lites
        sourceData['Lites'] = sourceData['Glass Lites'].replace("lites","").replace("Lites", "").strip()

        # Hardware
        sourceData = self.prepHardware(sourceData)

        # Glass
        sourceData = self.prepGlass(sourceData)
        
        sourceData['Pre-drilled For Hardware'] = "No"

        # Parse out the model name and number
        sourceData['Model'] = self.prepModel(sourceData.copy())

        # this will rewrite sourceData with the new images 
        sourceData = self.prepImages(sourceData)

        # Description
        sourceData['Description'] = self.prepDescription(sourceData.copy())

        sourceData['Shipping'] = 180

        sourceData['Discount'] = self.prepDiscount(worksheetName)

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
    def mapFields_barndoor_single(self, sourceData:dict):
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
    def mapFields_slabs_single(self, sourceData:dict):
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
    def cleanPriceKey(self,key:str):
        self.run_hook('start_cleanPriceKey')
        key = key.replace("Cost: ", "Price:")
        self.run_hook('end_cleanPriceKey')
        return key


    @Debugger
    @validate_arguments
    def prepUrl(self, sourceData:dict):
        self.run_hook('start_prepUrl')
        url = sourceData['UnitedPorte URL']
        self.run_hook('end_prepUrl')
        return url


    @Debugger
    @validate_arguments
    def prepUrlKey(self, sourceData:dict):
        self.run_hook("start_prepUrlKey", url=sourceData['URL'])
        output = None
        if "" == sourceData['URL']:
            self.run_hook("prepUrlKey_url_is_blank", url=sourceData['URL'])
            self.noteProblem(self.sourceWorksheetName, "URL", f"Door with no URL: '{sourceData['Title']}'")
        else:
            self.run_hook("prepUrlKey_url_not_blank", url=sourceData['URL'])
            #sarto URL Key
            output = sourceData['UnitedPorte URL'].replace("https://unitedporte.us/","")
        
        self.run_hook("end_prepUrlKey", urlKey=output)
        return output


    @Debugger
    @validate_arguments
    def prepModel(self, sourceData:dict):
        self.run_hook("start_prepModel")
        output = None
        if "" != sourceData['Title']:
            self.run_hook("prepModel_title_not_empty", title=sourceData['Title'])
            splitTitle = sourceData['Title'].split(" ")
            if 1 < len(splitTitle):
                output = f"{splitTitle[0]} {splitTitle[1]}"
        else:
            self.run_hook("prepModel_title_is_empty", title=sourceData['Title'])
            self.noteProblem(self.sourceWorksheetName, "Title", f"Door with No Title: '{', '.join(sourceData)}'")
            return
        self.run_hook("end_prepModel")
        return output

    @Debugger
    @validate_arguments
    def prepGlass(self, sourceData:dict):
        
        if sourceData['Glass'] == "No":
            sourceData['Has Glass'] = "No"
            sourceData['Glass Finish'] = "None"
        else:
            sourceData['Has Glass'] = "Yes"
            sourceData['Glass Finish'] = sourceData['Glass']
        
        return sourceData
    
    @Debugger
    @validate_arguments
    def prepHardware(self, sourceData:dict):
        if sourceData['Hardware'] == "Slab":
            sourceData['Hardware Type'] = "None"
            sourceData['Hardware Color'] = "None"
            sourceData['Hardware'] = "None"
        else:
            sourceData['Hardware Type'] = "Rail"
            sourceData['Hardware Color'] = sourceData['Hardware']
            sourceData['Hardware'] = f"{sourceData['Hardware']} Rail with predrilled holes, {sourceData['Hardware']} Hangers with wheels, Door stops, Plastic Fin Floor guide, and Mounting screws"
        
        return sourceData