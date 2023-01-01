import sys
from collections import OrderedDict
from pydantic import validate_arguments
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.dataMoves.exception import DataMove_Exception
from modules.caches.flat import UPDATE_TIMESTAMP_KEY, UPDATE_TIMESTAMP_POSTFIX, Flat_Cache
from modules.caches.exception import Nested_Cache_Exception
from modules.decorator import Debugger
from modules.helper import Helper
from modules.helpers.exception import Helper_Exception
from modules.logger import Logger, logger_name


class DataMove():

    sourceBasePath = "modules.spreadsheets.sources."
    sourceSpreadsheet = None
    sourceWorksheet = None

    destinationBasePath = "modules.spreadsheets.destinations."
    destinationSpreadsheet = None
    destinationWorksheets = {}
    destination_expectedCols = {}

    destinationWorksheetCreateIfNotFound = True
    destinationStartHeights = {}
    problemsIdentified = {}

    skipItem = {}

    newData = {}

    sourceAlwaysOverridesDestination = False

    problemsWorksheetName = "problems"

    hooks:dict = {}
    
    @Debugger
    def __init__(self) -> None:
        self.problemsIdentified = {}
        self.newData = {}

        self.run_hook('pre_init')

        self.run_hook('pre_init_spreadsheets')

        self.run_hook('pre_source_init_spreadsheet')
        sourceklassObj = self.getSourceClass()
        self.sourceSpreadsheet = sourceklassObj()
        self.run_hook('post_source_init_spreadsheet')

        self.run_hook('pre_destination_init_spreadsheet')
        destklassObj = self.getDestinationClass()
        self.destinationSpreadsheet = destklassObj()
        self.run_hook('post_destination_init_spreadsheet')

        self.run_hook('post_init_spreadsheets')

        self.run_hook('pre_source_get_worksheets')
        self.sourceWorksheet = self.sourceSpreadsheet.getWorksheet(worksheetTitle=self.sourceWorksheetName)
        self.run_hook('post_source_get_worksheets')

        self.run_hook('pre_destination_worksheet_setup_loop', data=self.destinationWorksheetNames)
        for worksheet in self.destinationWorksheetNames:
            self.run_hook('pre_destination_open_create_worksheet', data=worksheet)
            self.destinationWorksheets[worksheet] = self.openOrCreateDestinationWorksheet(worksheet)
            self.run_hook('post_destination_open_create_worksheet', data=worksheet)
            # easy way to make destination fetch the data
            self.destinationStartHeights[worksheet] = self.destinationWorksheets[worksheet].height()
    
        self.run_hook('post_destination_worksheet_setup_loop', data=self.destinationWorksheetNames)

        self.run_hook('pre_destinations_setup')
        self.setupDestinations()
        self.run_hook('post_destinations_setup')
        
        self.run_hook("post_init")


    @Debugger
    @validate_arguments
    def openOrCreateDestinationWorksheet(self, worksheetName):
        try:
            return self.destinationSpreadsheet.getWorksheet(worksheetTitle=worksheetName)
        except Bdfs_Spreadsheet_Exception as err:
            # allow not creating the spreadsheet, if wanted
            if True == self.destinationWorksheetCreateIfNotFound:
                return self.destinationSpreadsheet.insertWorksheet(worksheetName=worksheetName)
            else:
                raise DataMove_Exception(err.message)
        

    # first thing that runs in __init__
    @Debugger
    @validate_arguments
    def run_hook(self, name:str, **kwargs):
        args = Helper.prepArgs(**kwargs)
        if "([], [])" == str(args):
            args = ""
        Logger.info(f"Hook: {name}::{args}")
        logger_name.name = "MapData"
        
        if Helper.classHasMethod(klass=self, methodName=name):
            Helper.callMethod(klass=self, methodName=name, **kwargs)


    @Debugger
    def getSourceClass(self):
        self.run_hook('\npre_source_get_class', data=self.sourceBasePath + self.sourceClassPath)
        spreadsheetClass = self.getSpreadsheetClass(self.sourceBasePath + self.sourceClassPath)
        self.run_hook('post_source_get_class', data=self.sourceBasePath + self.sourceClassPath)

        return spreadsheetClass

    @Debugger
    def getDestinationClass(self):
        self.run_hook('\npre_destination_get_class', data=(self.destinationBasePath + self.destinationClassPath))
        spreadsheet = self.getSpreadsheetClass(self.destinationBasePath + self.destinationClassPath)
        self.run_hook('pre_destination_get_class', data=(self.destinationBasePath + self.destinationClassPath))
        
        return spreadsheet

    @Debugger
    @validate_arguments
    def getSpreadsheetClass(self, spreadsheet_class:str):
        self.run_hook("\npre_get_spreadsheet_class")
        classObj = Helper.importClass(spreadsheet_class)
        self.run_hook("post_get_spreadsheet_class")
        return classObj


    @Debugger
    def setupDestinations(self):
        self.run_hook('\npre_setupDestinations')
        for worksheet in self.destinationWorksheetNames:
            # Make sure the columns we need at the destination are setup
            self.destinationWorksheets[worksheet].alignToColumns(self.destinationWorksheets[worksheet].getExpectedColumns())
        self.run_hook('post_setupDestinations')

    @Debugger
    def map(self):
        self.run_hook('\npre_map')

        # for each row in the source spreadsheet, get the fields set up the way we want them and then apply them to the appropriate destination worksheet
        for row in range(0, self.sourceWorksheet.height()):
            # get the data we will start with
            sourceData = self.sourceWorksheet.getRow(row, update_timestamp=True)

            # reset to false for the next item
            self.skipItem = {} # allows mapFields() to identify a row to skip

            # undo whatever has been done before for this data
            self.newData = {}
            
            self.run_hook("map_pre_mapFields")
            # merge the source and Destination data, based on whatever rules you need
            self.__mapFields(sourceData)
            self.run_hook("map_post_mapFields")
            
            self.checkMappedData()

        self.run_hook('post_map')

    @Debugger
    @validate_arguments
    def checkMappedData(self):
        self.run_hook("start_checkMappedData")
        newDataKeys = self.newData.keys()
        for worksheetName in self.destinationWorksheets.keys():
            # don't keep going
            if True == self.skipItem[worksheetName]:
                self.run_hook("checkMappedData_did_skip_item", data=worksheetName)
                continue
            self.run_hook("checkMappedData_did_not_skip_item", data=worksheetName)

            if not worksheetName in newDataKeys:
                raise DataMove_Exception(f"Data from MapFields did not include a key for destination worksheet '{worksheetName}'")

            if not worksheetName in self.destinationWorksheets.keys():
                raise DataMove_Exception(f"Destination worksheet '{worksheetName}' not in destinationWorksheets list: '{self.destinationWorksheets.keys()}'")

            #
            # Check if we mapped all of the expected Columns
            #
            newDataWorksheetKeys = self.newData[worksheetName].keys()

            # map the source keys to the destination keys we are expecting
            modifiedData = OrderedDict()

            self.run_hook("checkMappedData_pre_key_loop", data=worksheetName)
            for key in self.destinationWorksheets[worksheetName].getExpectedColumns():
                self.run_hook("checkMappedData_in_key_loop", data=key)
                #skip checking the keys for update_timestamp, as we will check them down the line
                # update_timestamp will be updated in destination when the row is written
                # the update_timestamps for the keys we're keeping will be grabbed when we decide if we're keeping source or destination
                self.run_hook("checkMappedData_pre_update_timestamp_check", data=key)
                if UPDATE_TIMESTAMP_KEY in key:
                    continue
                self.run_hook("checkMappedData_post_update_timestamp_check", data=key)

                # we decided during mapping that we don't want this sourceRow in the destination, skip processing
                if True == self.skipItem[worksheetName]:
                    self.run_hook("checkMappedData_did_skip_item")
                    continue
                self.run_hook("checkMappedData_did_not_skip_item")

                self.run_hook("checkMappedData_pre_key_in_mapped_data", data=key, mapped_data_keys=newDataWorksheetKeys)
                if not key in newDataWorksheetKeys:
                    raise DataMove_Exception(f" '{key} was not found in sources, it should be mapped before we can push data to destination")
                self.run_hook("checkMappedData_post_key_in_mapped_data")

                self.run_hook("checkMappedData_pre_cleanSourceDataForDestination", data=key, worksheetName=worksheetName)
                #cleanData will come back with the original key and if there was a timestamp on source or destination, that timestamp with the appropriate key
                modifiedData = self.cleanSourceDataForDestination(key, worksheetName)
                self.run_hook("checkMappedData_post_cleanSourceDataForDestination", cleanData=modifiedData)
            self.run_hook("checkMappedData_post_key_loop", data=worksheetName)

            self.storeTheData(worksheetName, modifiedData)

        self.run_hook("end_checkMappedData")


    @Debugger
    @validate_arguments
    def storeTheData(self, worksheetName:str, modifiedData:dict):
        # if everything in destination expectedCols is in modified Data, then we are good,
        # because the previous step made sure that we only have the keys we want + timestamp keys
        # everything else was dropped through exclusion
        self.run_hook("start_storeTheData")
        if True == Helper.compareLists(modifiedData, self.destinationWorksheets[worksheetName].getExpectedColumns()):
            self.run_hook("storeTheData_pre_putRow",data=modifiedData)
            # putRow will determine, based on uniqueKeys, whether this should be an insert or update
            self.destinationWorksheets[worksheetName].putRow(modifiedData)
            self.run_hook("storeTheData_post_putRow")
            self.run_hook("storeTheData_success")
        else:
            self.run_hook("storeTheData_fail",data=modifiedData)
            # do NOT DELETE THESE PRINT STATEMENTS
            print(f"\nLeft: {Helper.listDiff(modifiedData.keys(), self.destinationWorksheets[worksheetName].getExpectedColumns())}")
            print(f"\nRight: {Helper.listDiff(self.destinationWorksheets[worksheetName].getExpectedColumns(), modifiedData.keys())}\n")
            raise DataMove_Exception(f"There are columns missing from modified data for worksheet '{worksheetName}'. Received {list(modifiedData.keys())} Expected {self.destinationWorksheets[worksheetName].getExpectedColumns()}")
        self.run_hook("end_storeTheData")


    @Debugger
    @validate_arguments
    def getDestinationRow(self, worksheetName):
        self.run_hook("start_getDestinationRow", worksheetName=worksheetName)
        
        self.run_hook("getDestinationRow_pre_get_destination_unique_field")
        destinationUniqueField = self.destinationWorksheets[worksheetName].getUniqueField()
        self.run_hook("getDestinationRow_post_get_destination_unique_field", destinationUniqueField=destinationUniqueField)

        destinationData = {}

        self.run_hook("getDestinationRow_pre_check_destination_unique_field")
        # get the destination row, based on the unique column if there is one, do nothing otherwise
        if None != destinationUniqueField:
            try:
                self.run_hook("getDestinationRow_check_destination_unique_field_pre_getRow")
                destinationData = self.destinationWorksheets[worksheetName].getRow(unique=self.newData[worksheetName][destinationUniqueField])
                self.run_hook("getDestinationRow_check_destination_unique_field_post_getRow", destinationData=destinationData)
            except Nested_Cache_Exception as err:
                destinationData = {}
        self.run_hook("end_getDestinationRow", worksheetName=worksheetName)
        return destinationData

    @Debugger
    @validate_arguments
    def cleanSourceDataForDestination(self, key, worksheetName):
        self.run_hook("\nstart_cleanSourceDataForDestination",key=key, worksheetName=worksheetName)

        #
        # Decide which version of data we want, based on timestamps
        #
        timestampKey = Flat_Cache.makeTimestampName(key)
        
        useNew = True #if False, use the data from destination

        #
        # Get the keys for the newData Dict
        #
        self.run_hook("start_cleanSourceDataForDestination_pre_get_newDataTimestamp")
        newDataKeys = list(self.newData[worksheetName].keys())
        newDataHasTimestampKey = timestampKey in newDataKeys
        newDataTimestamp:float = 0.0
        if True == newDataHasTimestampKey:
            newDataTimestamp = self.newData[worksheetName][timestampKey]
        self.run_hook("start_cleanSourceDataForDestination_post_get_newDataTimestamp", newDataTimestamp=newDataTimestamp)

        #
        # Destination Data Keys
        #
        self.run_hook("start_cleanSourceDataForDestination_pre_get_destinationDataTimestamp")
        destinationData = self.getDestinationRow()
        destinationDataKeys = []
        destinationHasTimestampKey = False
        destinationTimestamp:float = 0.0
        if len(destinationData) > 0:
            destinationDataKeys = destinationData.keys()
            destinationHasTimestampKey = timestampKey in destinationDataKeys
            if True == destinationHasTimestampKey:
                destinationTimestamp = destinationData[timestampKey]       
        self.run_hook("start_cleanSourceDataForDestination_post_get_destinationDataTimestamp", destinationTimestamp=destinationTimestamp)

        #setup outputData to get overridden by either source or destination, based on usedNew and the timestamp
        outputData = {key: None}

        self.run_hook("start_cleanSourceDataForDestination_pre_compareTimestamps")
        if destinationTimestamp > newDataTimestamp:
            self.run_hook("start_cleanSourceDataForDestination_in_compareTimestamps_useDestination_data")
            # this is the only time when destination data is the right data to keep
            outputData = self.cleanSourceDataForDestination_useDestination(key, timestampKey, destinationData)
        else:
            self.run_hook("start_cleanSourceDataForDestination_in_compareTimestamps_useSource_data")        
            outputData = self.cleanSourceDataForDestination_useSource(worksheetName, key, timestampKey)
        self.run_hook("start_cleanSourceDataForDestination_post_compareTimestamps")            
        
        self.run_hook("end_cleanSourceDataForDestination",outputData=outputData)
        return outputData

    @Debugger
    @validate_arguments
    def cleanSourceDataForDestination_useSource(self, worksheetName, key, timestampKey):
        self.run_hook("start_cleanSourceDataForDestination_pre_useNew_data", data=self.newData[worksheetName][key])
        outputData = {}
        newDataKeys = self.newData.keys()
        # the new data is the winner
        outputData[key] = self.newData[worksheetName][key]
        self.run_hook("start_cleanSourceDataForDestination_pre_useNew_newData_has_timestamp", timestampKey=timestampKey)
        # does new data have a timestamp key for this field?
        if timestampKey in newDataKeys:
            self.run_hook("start_cleanSourceDataForDestination_pre_in_useNew_newData_has_timestamp")
            # timestamp for this key is in newData
            outputData[timestampKey] = self.newData[worksheetName][timestampKey]
            self.run_hook("start_cleanSourceDataForDestination_post_in_useNew_newData_has_timestamp", timestamp=self.newData[worksheetName][timestampKey])
        else:
            # timestamp for this key is not in the newData
            pass
        self.run_hook("start_cleanSourceDataForDestination_post_useNew_newData_has_timestamp", timestampKey=timestampKey)
        self.run_hook("start_cleanSourceDataForDestination_post_useNew_data")


    @Debugger
    @validate_arguments
    def cleanSourceDataForDestination_useDestination(self, key, timestampKey, destinationData):
        outputData = {}
        self.run_hook("start_cleanSourceDataForDestination_pre_useDestination_data", data=destinationData[key])
        # the destination data is what we want, use that data
        outputData[key] = destinationData[key]
        if timestampKey in destinationData[key]:
            self.run_hook("start_cleanSourceDataForDestination_useDestination_data_pre_has_timestamp")
            # destination has the timestamp key, so pass that value along
            outputData[timestampKey] = destinationData[timestampKey]
            self.run_hook("start_cleanSourceDataForDestination_useDestination_data_post_has_timestamp", timestamp=destinationData[timestampKey])

        self.run_hook("start_cleanSourceDataForDestination_post_useDestination_data")

    @Debugger
    @validate_arguments
    def __mapFields(self, sourceData:dict):
        self.run_hook("\nstart_mapFields")
        #bc we will only grab the data based on the destination columns
            # we can copy the data into the worksheet specific dict and then use
            # mapFields to clean it up
        self.run_hook("mapFields_pre_loop_worksheet")
        for worksheetName in self.destinationWorksheetNames:
            self.run_hook("mapFields_in_loop_worksheet", worksheetName=worksheetName)
            # start the skip off right
            self.skipItem[worksheetName] = False

            newData = self.handleWorksheetMethods(worksheetName, sourceData)
            
            self.newData[worksheetName] = None # make sure there is a place for the data

            self.run_hook("mapFields_loop_worksheet_pre_skipItem", skip=self.skipItem[worksheetName])
            # the mapFields methods can cause us to skip processing of a field, so we want to go ahead and do that here bc we have no data to process
            if False == self.skipItem[worksheetName]:
                self.run_hook("mapFields_loop_worksheet_in_skipItem")
                self.newData[worksheetName] = newData
            
            self.run_hook("mapFields_loop_worksheet_post_skipItem")
        self.run_hook("mapFields_post_loop_worksheet")
        self.run_hook("end_mapFields")
    

    @Debugger
    @validate_arguments
    def handleWorksheetMethods(self, worksheetName:str, sourceData:dict):
        self.run_hook("start_handleWorksheetMethods")
        methodName = f"mapFields_{worksheetName}"
        
        try:
            self.run_hook("handleWorksheetMethods_pre_callMethod", methodName=methodName)
            # tries to run methodName from self, passing it the sourceData as kwarg
            newData = Helper.callMethod(klass=self, methodName=methodName, sourceData=sourceData.copy())
            self.run_hook("handleWorksheetMethods_post_callMethod", methodName=methodName)
        except Helper_Exception as err:
            if "but no method with that name exists" in err.message:
                raise DataMove_Exception(f"DataMove requires a mapFields method for each worksheet and you need a method called '{methodName}' on {self.__class__.__name__}")
            else:
                # pass it back
                raise Helper_Exception(err.message)
        
        self.run_hook("end_handleWorksheetMethods")
        return newData
        

    @Debugger
    @validate_arguments
    def mapField(self, destinationWorksheet:str, field:str, data=None):
        self.run_hook("\nstart_mapField", worksheetName=destinationWorksheet, field=field, data=data)
        if destinationWorksheet not in self.newData.keys():
            self.run_hook("mapField_create_new_dict")
            self.newData[destinationWorksheet] = {field: data}
        else:
            self.run_hook("mapField_add_to_dict")
            self.newData[destinationWorksheet][field] = data
        self.run_hook("end_mapField")


    @Debugger
    def run(self):
        self.run_hook('\npre_run')

        self.run_hook('pre_destination_run_map')
        self.map()
        self.run_hook('post_destination_run_map')

        for worksheetName in self.destinationWorksheetNames:
            self.run_hook('pre_destination_run_commit')
            self.commit(worksheetName)
            self.run_hook('post_destination_run_commit')
        
        self.run_hook('pre_run_problems')
        self.problems()
        self.run_hook('post_run_problems')
        
        self.run_hook('post_run')


    @Debugger
    @validate_arguments
    def noteProblem(self, worksheetName:str, problemType:str, problemDescription:str):
        self.run_hook('\npre_problems_note')
        
        self.skipItem[worksheetName] = True

        # setup the problems dict
        if len(self.problemsIdentified) == 0:
            self.problemsIdentified = {worksheetName: {problemType: [problemDescription]}}
        elif not worksheetName in self.problemsIdentified.keys():
            # add the worksheet to the problemsIdentified
            self.problemsIdentified[worksheetName] = {problemType: [problemDescription]}
        elif not problemType in self.problemsIdentified[worksheetName].keys():
            # append the problem type to the dict that is already there
            self.problemsIdentified[worksheetName][problemType] = [problemDescription]
        else:        
            # add the problem description
            self.problemsIdentified[worksheetName][problemType].append(problemDescription)

        self.run_hook('post_problems_note')


    @Debugger
    def problems(self):
        self.run_hook('\npre_problems')
        if None != self.problemsWorksheetName:
            try:
                problemsWorksheet = self.destinationSpreadsheet.getWorksheet(worksheetTitle=self.problemsWorksheetName, skipKept=True)
            except Bdfs_Spreadsheet_Exception as err:
                problemsWorksheet = self.destinationSpreadsheet.insertWorksheet(worksheetName=self.problemsWorksheetName, bypassKeeperPattern=True)

            # unset bc this isn't an inventory sheet
            # must be unset before a getData() call is made in deleteAllData()
            problemsWorksheet.data.uniqueField = None
            for worksheetName in self.destinationWorksheetNames:
                # Delete anything with this worksheet's name in the Worksheet Name column
                problemsWorksheet.deleteRowWhere("Worksheet Name", worksheetName)
                if 0 > len(self.problemsIdentified) and worksheetName in self.problemsIdentified.keys():
                    expectedCols = ["Worksheet Name", "Problem Type", "Problem Message"]

                    # Make sure the columns we need at the destination are setup
                    problemsWorksheet.alignToColumns(expectedCols)

                    for index in self.problemsIdentified[worksheetName].keys():
                        values = self.problemsIdentified[worksheetName][index]
                        for value in values:
                            dataToPush = [worksheetName, index, value]
                            problemsWorksheet.putRow(dataToPush)
            
            self.run_hook('pre_problems_commit')
            problemsWorksheet.commit()
            self.run_hook('post_problems_commit')
        else:
            for index in self.problemsIdentified[worksheetName].keys():
                values = self.problemsIdentified[worksheetName][index]
                # do NOT DELETE THIS PRINT STATEMENT
                print(f"\n\n {index} Problems: ")
                for value in values:
                    # do NOT DELETE THIS PRINT STATEMENT
                    print(f"\t- {value}")

        self.run_hook('post_problems')


    @Debugger
    @validate_arguments
    def commit(self, worksheetName:str):
        self.run_hook('\npre_destination_worksheet_commit', data=worksheetName)
        self.destinationWorksheets[worksheetName].commit()
        self.run_hook('post_destination_worksheet_commit', data=worksheetName)


    ####
    #
    # Resuable Prep Methods
    #
    ####

    @Debugger
    @validate_arguments
    def prepImages(self, sourceData:dict):
        self.run_hook("start_prepImages")
                # image URLs, up to 10 of them
        for counter in range(1,11):
            imageKey = f"Image {counter} URL"
            
            imageUrl = ""
            if imageKey in sourceData:
                imageUrl = sourceData[imageKey]
            
            sourceData[imageKey] = imageUrl

        self.run_hook("end_prepImages")
        return sourceData
    
    @Debugger
    @validate_arguments
    def prepDescription(self, sourceData):
        self.run_hook('start_prepDescription')
        description = ""
        if "Description" in sourceData:
            description = sourceData['Description']
        self.run_hook('end_prepDescription')
        return description

    @Debugger
    @validate_arguments
    def prepDiscount(self, worksheetName):
        return float(self.destinationWorksheets[worksheetName].discount())

    @Debugger
    @validate_arguments
    def calculatePrice(self, key:str, worksheetName, sourceData:dict):
        if not "Discount" in sourceData.keys():
            raise DataMove_Exception("Discount needs to be available in sourceData before calculatePrice() is run")
        
        sourceKey = self.cleanPriceKey(key)
        
        priceString = str(sourceData[sourceKey]).replace(",","").replace("$","")
        priceFloat = float(priceString)

        price = 1
        if '' != priceFloat: # sometimes we don't have a price for a door
            price = priceFloat

        return price * (1 - self.prepDiscount(worksheetName=worksheetName))