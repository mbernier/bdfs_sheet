import sys
from collections import OrderedDict
from pydantic import validate_arguments
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.dataMoves.exception import DataMove_Exception
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
        print("trying open or create")
        try:
            print("trying getWorksheet")
            return self.destinationSpreadsheet.getWorksheet(worksheetTitle=worksheetName)
        except Bdfs_Spreadsheet_Exception as err:
            print("get failed, trying insert")
            # allow not creating the spreadsheet, if wanted
            if True == self.destinationWorksheetCreateIfNotFound:
                print("get failed, trying insert")
                return self.destinationSpreadsheet.insertWorksheet(worksheetName=worksheetName)
            else:
                print("we did something wrong")
                raise DataMove_Exception(err.message)
        

    # first thing that runs in __init__
    @Debugger
    @validate_arguments
    def run_hook(self, name:str, **kwargs):
        logger_name.name = "MapData"
        Logger.info(f"Checking MapData hook: {name}")
        
        if Helper.classHasMethod(klass=self, methodName=name):
            Helper.callMethod(klass=self, methodName=name, **kwargs)


    @Debugger
    def getSourceClass(self):

        self.run_hook('pre_source_get_class', data=self.sourceBasePath + self.sourceClassPath)

        spreadsheetClass = self.getSpreadsheetClass(self.sourceBasePath + self.sourceClassPath)

        self.run_hook('post_source_get_class', data=self.sourceBasePath + self.sourceClassPath)

        return spreadsheetClass

    @Debugger
    def getDestinationClass(self):
        
        self.run_hook('pre_destination_get_class', data=(self.destinationBasePath + self.destinationClassPath))
        
        spreadsheet = self.getSpreadsheetClass(self.destinationBasePath + self.destinationClassPath)
        
        self.run_hook('pre_destination_get_class', data=(self.destinationBasePath + self.destinationClassPath))
        
        return spreadsheet

    @Debugger
    @validate_arguments
    def getSpreadsheetClass(self, spreadsheet_class:str):
        return Helper.importClass(spreadsheet_class)


    @Debugger
    def setupDestinations(self):
        self.run_hook('pre_setupDestinations')
        for worksheet in self.destinationWorksheetNames:
            # The columns we will write to the destination
            self.destination_expectedCols[worksheet] = self.destinationWorksheets[worksheet].getExpectedColumns()
            
            # Make sure the columns we need at the destination are setup
            self.destinationWorksheets[worksheet].alignToColumns(self.destination_expectedCols[worksheet])
        self.run_hook('post_setupDestinations')

    @Debugger
    def map(self):
        self.run_hook('pre_map')

        # for each row in the source spreadsheet, get the fields set up the way we want them and then apply them to the appropriate destination worksheet
        for row in range(0, self.sourceWorksheet.height()):
            # get the data we will start with
            sourceData = self.sourceWorksheet.getRow(row, update_timestamp=True)

            # reset to false for the next item
            self.skipItem = False # allows mapFields() to identify a row to skip

            # undo whatever has been done before for this data
            self.newData = {}
            # merge the source and Destination data, based on whatever rules you need
            self.__mapFields(sourceData)
            
            # don't keep going
            if True == self.skipItem:
                continue

            newDataKeys = self.newData.keys()

            for worksheetName in self.destinationWorksheetNames:

                if worksheetName not in newDataKeys:
                    raise DataMove_Exception(f"Data from MapFields did not include a key for destination worksheet '{worksheetName}'")

                if worksheetName not in self.destinationWorksheets.keys():
                    raise DataMove_Exception(f"Destination worksheet '{worksheetName}' not in destinationWorksheets list: '{self.destinationWorksheets.keys()}'")

                # map the source keys to the destination keys we are expecting
                modifiedData = OrderedDict()
                for key in self.destination_expectedCols[worksheetName]:
                    #skip checking the keys for update_timestamp, as we will check them down the line
                    # update_timestamp will be updated in destination when the row is written
                    # the update_timestamps for the keys we're keeping will be grabbed when we decide if we're keeping source or destination
                    if "update_timestamp" in key:
                        continue

                    # we decided during mapping that we don't want this sourceRow in the destination, skip processing
                    if True == self.skipItem:
                        continue

                    #
                    # Check if we mapped all of the expected Columns
                    #
                    newDataKeys = self.newData[worksheetName].keys()
                    
                    if not key in newDataKeys:
                        raise DataMove_Exception(f" '{key} was not found in sources, it should be mapped before we can push data to destination")

                    #cleanData will come back with the original key and if there was a timestamp on source or destination, that timestamp with the appropriate key
                    cleanData = self.cleanSourceDataForDestination(key, worksheetName)

                    # add the data to modifiedData, this is an OrderedDict, so theres no clean extend method
                    for cdkey,cdval in cleanData.items():
                        modifiedData[cdkey] = cdval
                
                # if everything in destination expectedCols is in modified Data, then we are good,
                    # because the previous step made sure that we only have the keys we want + timestamp keys
                    # everything else was dropped through exclusion
                if True == Helper.compareLists(modifiedData, self.destination_expectedCols[worksheetName]):
                    # putRow will determine, based on uniqueKeys, whether this should be an insert or update
                    self.destinationWorksheets[worksheetName].putRow(modifiedData)
                else:
                    # do NOT DELETE THESE PRINT STATEMENTS
                    print(f"\nLeft: {Helper.listDiff(modifiedData.keys(), self.destination_expectedCols[worksheetName])}")
                    print(f"\nRight: {Helper.listDiff(self.destination_expectedCols[worksheetName], modifiedData.keys())}\n")
                    raise DataMove_Exception(f"There are columns missing from modified data for worksheet '{worksheetName}'. Received {list(modifiedData.keys())} Expected {self.destination_expectedCols[worksheetName]}")

        self.run_hook('post_map')

    @Debugger
    @validate_arguments
    def cleanSourceDataForDestination(self, key, worksheetName):
        destinationDataColumns = self.destinationWorksheets[worksheetName].getColumns()

        destinationUniqueField = self.destinationWorksheets[worksheetName].getUniqueField()

        #
        # Fetch the data from the destination so we can check it for timestamps
        #
        destinationData = {}
        # get the destination row, based on the unique column if there is one, do nothing otherwise
        if None != destinationUniqueField:
            try:
                destinationData = self.destinationWorksheets[worksheetName].getRow(unique=self.newData[worksheetName][destinationUniqueField])
            except Nested_Cache_Exception as err:
                destinationData = {}
        
        #
        # Get the keys for the newData Dict
        #
        newDataKeys = list(self.newData[worksheetName].keys())
        
        #
        # Decide which version of data we want, based on timestamps
        #
        timestampKey = key+"_update_timestamp"
        
        useNew = True #if False, use the data from destination
                
        if timestampKey in destinationDataColumns and timestampKey in destinationData:
            #destination has the timestamp, does source?
            if timestampKey in newDataKeys:
                # destination Data and newData have the timestamp, which is newer?
                if self.newData[worksheetName][timestampKey] == '':
                    #does destination have an actual timestamp or just a place where it could be?
                    if destinationData[timestampKey] == "":
                        # both have no timestamp, so use the newData
                        useNew = True
                    else:
                        # the newData doesn't have a timestamp, but we know that destination Data does
                        useNew = False
                elif self.newData[worksheetName][timestampKey] < destinationData[timestampKey]:
                    # destination is newer than source
                    useNew = False
                else:
                    useNew = True #redundant to point out the logic
            else:
                # there is no timestamp header in the source, but there is in the destination - use destination
                useNew = False
        else:
            # destination hasn't been updated from source, go ahead and override what is there
            useNew = True
        
        #setup outputData to get overridden by either source or destination, based on usedNew and the timestamp
        outputData = {key: None}

        # we decided that the newData version is what we want
        if True == useNew:
            # the new data is the winner
            outputData[key] = self.newData[worksheetName][key]
            # does new data have a timestamp key for this field?
            if timestampKey in newDataKeys:
                # timestamp for this key is in newData
                outputData[timestampKey] = self.newData[worksheetName][timestampKey]
            else:
                # timestamp for this key is not in the newData
                pass
        else:
            # the destination data is what we want, use that data
            outputData[key] = destinationData[key]
            if timestampKey in destinationData[key]:
                # destination has the timestamp key, so pass that value along
                outputData[timestampKey] = destinationData[timestampKey]
        
        return outputData

    @Debugger
    @validate_arguments
    def __mapFields(self, sourceData:dict):
        
        #bc we will only grab the data based on the destination columns
            # we can copy the data into the worksheet specific dict and then use
            # mapFields to clean it up
        for worksheetName in self.destinationWorksheetNames:
            methodName = f"mapFields_{worksheetName}"
            try:
                # tries to run methodName from self, passing it the sourceData as kwarg
                newData = Helper.callMethod(klass=self, methodName=methodName, sourceData=sourceData.copy())                
            except Helper_Exception as err:
                if "but no method with that name exists" in err.message:
                    raise DataMove_Exception(f"DataMove requires a mapFields method for each worksheet and you need a method called '{methodName}' on {self.__class__.__name__}")
                else:
                    # pass it back
                    raise Helper_Exception(err.message)
            
            # the mapFields methods can cause us to skip processing of a field, so we want to go ahead and do that here bc we have no data to process
            if False == self.skipItem:

                if True == Helper.compareLists(newData, self.destination_expectedCols[worksheetName]):
                    self.newData[worksheetName] = newData
                else:
                    # do NOT DELETE THIS PRINT STATEMENT
                    print(f"\nLeft: {Helper.listDiff(newData.keys(), self.destination_expectedCols[worksheetName])}")
                    print(f"\nRight: {Helper.listDiff(self.destination_expectedCols[worksheetName], newData.keys())}\n")
                    raise DataMove_Exception(f"There are columns missing from modified data for worksheet '{worksheetName}'. Received {list(newData.keys())} Expected {self.destination_expectedCols[worksheetName]}")

    

    @Debugger
    @validate_arguments
    def mapField(self, destinationWorksheet:str, field:str, data=None):
        if destinationWorksheet not in self.newData.keys():
            self.newData[destinationWorksheet] = {field: data}
        else:
            self.newData[destinationWorksheet][field] = data


    @Debugger
    def run(self):
        self.run_hook('pre_run')

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
        self.run_hook('pre_problems_note')
        
        self.skipItem = True

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
        self.run_hook('pre_problems')
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
    def commit(self, worksheetName:str):
        self.run_hook('pre_destination_worksheet_commit', data=worksheetName)
        self.destinationWorksheets[worksheetName].commit()
        self.run_hook('post_destination_worksheet_commit', data=worksheetName)