import sys
from pydantic import validate_arguments
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.dataMoves.exception import DataMove_Exception
from modules.decorator import Debugger
from modules.helper import Helper
from modules.logger import Logger, logger_name


class DataMove():

    sourceSpreadsheet = None
    sourceWorksheet = None

    destinationSpreadsheet = None
    destinationWorksheets = None
    destination_expectedCols = []

    destinationWorksheetCreateIfNotFound = True
    problemsIdentified = {}

    sourceAlwaysOverridesDestination = False

    problemsWorksheetName = "problems"

    hooks:dict = {}
    
    @Debugger
    def __init__(self) -> None:
        problemsIdentified = {}

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

        self.run_hook('pre_destination_worksheet_setup_loop', self.destinationWorksheetNames)
        for worksheet in self.destinationWorksheetNames:
            self.destinationWorksheets[worksheet] = self.openOrCreateDestinationWorksheet(worksheet)
            # easy way to make destination fetch the data
            self.destinationStartHeight[worksheet] = self.destinationWorksheets[worksheet].height()
        self.run_hook('post_destination_worksheet_setup_loop', self.destinationWorksheetNames)

        self.run_hook('pre_destinations_setup')
        self.setupDestinations()
        self.run_hook('post_destinations_setup')
        
        self.run_hook("post_init")


    @Debugger
    @validate_arguments
    def openOrCreateDestinationWorksheet(self, worksheetName):
        self.run_hook('pre_destination_open_create_worksheet', worksheetName)
        try:
            return self.destinationSpreadsheet.getWorksheet(worksheetTitle=worksheetName)
        except Bdfs_Spreadsheet_Exception as err:
            # allow not creating the spreadsheet, if wanted
            if True == self.destinationWorksheetCreateIfNotFound:
                self.run_hook('post_destination_open_create_worksheet', worksheetName)
                return self.destinationSpreadsheet.insertWorksheet(worksheetName=worksheetName)
            else:
                raise DataMove_Exception(err.message)
        

    # first thing that runs in __init__
    @Debugger
    @validate_arguments
    def run_hook(self, name:str, **kwargs):
        logger_name.name = "MapData"
        Logger.warning(f"Checking MapData hook: {name}")
        
        if Helper.classHasMethod(klass=self, methodName=name):
            Helper.callMethod(klass=self, methodName=name, **kwargs)


    @Debugger
    def getSourceClass(self):
        basePath = "modules.spreadsheets.sources."

        self.run_hook('pre_source_get_class', data=basePath + self.sourceClassPath)

        spreadsheetClass = self.getSpreadsheetClass(basePath + self.sourceClassPath)

        self.run_hook('post_source_get_class', data=basePath + self.sourceClassPath)

        return spreadsheetClass

    @Debugger
    def getDestinationClass(self):
        basePath = "modules.spreadsheets.destinations."
        
        self.run_hook('pre_destination_get_class', data=basePath + self.destinationClassPath)
        
        spreadsheet = self.getSpreadsheetClass(basePath + self.destinationClassPath)
        
        self.run_hook('pre_destination_get_class', data=basePath + self.destinationClassPath)
        
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
            sourceData = self.sourceWorksheet.getRow(row, update_timestamp=False)

            # reset to false for the next item
            self.skipItem = False # allows mapFields() to identify a row to skip

            # merge the source and Destination data, based on whatever rules you need
            newData = self.mapFields(sourceData, destinationData)

            newDataKeys = newData.keys()

            for worksheetName in self.destinationWorksheetNames:

                if worksheetName not in newDataKeys:
                    raise DataMove_Exception(f"Data from MapFields did not include a key for destination worksheet '{worksheetName}'")

                if worksheetName not in self.destinationWorksheets.keys():
                    raise DataMove_Exception(f"Destination worksheet '{worksheetName}' not in destinationWorksheets list: '{self.destinationWorksheets.keys()}'")

                destinationDataKeys = self.destinationWorksheets[worksheetName].getColumns()
                destinationUniqueField = self.destinationWorksheets[worksheetName].getUniqueField()
                destinationData = {}

                # get the destination row, based on the unique column if there is one, do nothing otherwise
                if None != destinationUniqueField:
                    destinationData = self.destinationWorksheets[worksheetName].select(unique=newData[destinationUniqueField])

                # map the source keys to the destination keys we are expecting
                modifiedData = {}
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
                    newDataKeys = newData[worksheetName].keys()

                    if not key in newDataKeys:
                        raise DataMove_Exception(f" '{key} was not found in sources, it should be mapped before we can push data to destination")

                    #
                    # Decide which version of data we want, based on timestamps
                    #
                    timestampKey = key+"_update_timestamp"
                    
                    useNew = True #if False, use the data from destination
                                        
                    if timestampKey in destinationDataKeys:
                        if timestampKey in newDataKeys:
                            if newDataKeys[timestampKey] == '' or newDataKeys[timestampKey] < destinationDataKeys[timestampKey]:
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

                    # we decided that the newData version is what we want
                    if True == useNew:
                        modifiedData[key] = newData[worksheetName][key]
                        if timestampKey in newDataKeys:
                            modifiedData[timestampKey] = newData[worksheetName][timestampKey]
                    else:
                        # the destination data is what we want, use that data
                        modifiedData[key] = destinationData[key]
                        if timestampKey in destinationData[key]:
                            modifiedData[timestampKey] = destinationData[timestampKey]

                    outputData = []

                    if list(modifiedData.keys()) == self.destination_expectedCols[worksheetName]:
                        for column in self.destination_expectedCols[worksheetName]:
                            outputData.append(modifiedData[column])
                        # putRow will determine, based on uniqueKeys, whether this should be an insert or update
                        self.destinationWorksheets[worksheetName].putRow(outputData)
                    else:
                        print(f"\nLeft: {Helper.listDiff(modifiedData, self.destination_expectedCols[worksheetName])}")
                        print(f"\nRight: {Helper.listDiff(self.destination_expectedCols[worksheetName], modifiedData)}\n")
                        raise DataMove_Exception(f"There are columns missing from modified data for worksheet '{worksheetName}'. Received {list(modifiedData.keys())} Expected {self.destination_expectedCols[worksheetName]}")

        self.run_hook('post_map')

    @Debugger
    @validate_arguments
    def mapFields(self, sourceData:dict):
        pass


    @Debugger
    def run(self):
        self.run_hook('pre_run')

        self.run_hook('pre_destination_run_map')
        self.map(worksheetName)
        self.run_hook('post_destination_run_map')

        for worksheetName in self.destinationNames:           
            self.run_hook('pre_destination_run_commit')
            self.commit(worksheetName)
            self.run_hook('post_destination_run_commit')
        
        self.run_hook('pre_run_problems')
        self.problems()
        self.run_hook('post_run_problems')
        
        self.run_hook('post_run')


    @Debugger
    @validate_arguments
    def noteProblem(self, problemType, problemDescription):
        self.run_hook('pre_problems_note')
        
        self.skipItem = True
        if not problemType in self.problemsIdentified.keys():
            self.problemsIdentified[problemType] = [problemDescription]
        else:
            self.problemsIdentified[problemType].append(problemDescription)

        self.run_hook('post_problems_note')


    @Debugger
    def problems(self):
        self.run_hook('pre_problems')
        if None != self.problemsWorksheetName:
            try:
                problemsWorksheet = self.destinationSpreadsheet.getWorksheet(worksheetTitle=self.problemsWorksheetName)
            except Bdfs_Spreadsheet_Exception as err:
                problemsWorksheet = self.destinationSpreadsheet.insertWorksheet(worksheetName=self.problemsWorksheetName)

            # unset bc this isn't an inventory sheet
            # must be unset before a getData() call is made in deleteAllData()
            problemsWorksheet.data.uniqueField = None

            # Delete anything with this worksheet's name in the Worksheet Name column
            problemsWorksheet.deleteRowWhere("Worksheet Name", self.destinationWorksheetName)

            expectedCols = ["Worksheet Name", "Problem Type", "Problem Message"]

            # Make sure the columns we need at the destination are setup
            problemsWorksheet.alignToColumns(expectedCols)
    
            for index in self.problemsIdentified.keys():
                values = self.problemsIdentified[index]
                for value in values:
                    dataToPush = [self.destinationWorksheetName, index, value]
                    problemsWorksheet.putRow(dataToPush)
            
            self.run_hook('pre_problems_commit')
            problemsWorksheet.commit()
            self.run_hook('post_problems_commit')
        else:
            for index in self.problemsIdentified.keys():
                values = self.problemsIdentified[index]
                print(f"\n\n {index} Problems: ")
                for value in values:
                    print(f"\t- {value}")

        self.run_hook('post_problems')

    @Debugger
    def commit(self, worksheetName:str):
        self.run_hook('pre_destination_worksheet_commit', worksheetName)
        self.destinationWorksheets.commit()
        self.run_hook('post_destination_worksheet_commit', worksheetName)