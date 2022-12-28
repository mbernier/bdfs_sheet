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
    destinationWorksheet = None
    destination_expectedCols = []

    problemsWorksheetName = None

    destinationWorksheetCreateIfNotFound = True
    problemsIdentified = {}
    
    problemsWorksheetName = "problems"

    hooks:dict = {}
    
    @Debugger
    def __init__(self) -> None:
        problemsIdentified = {}

        self.run_hook('pre_init')

        self.run_hook('pre_init_spreadsheets')

        self.run_hook('pre_init_source_spreadsheet')
        sourceklassObj = self.getSourceClass()
        self.sourceSpreadsheet = sourceklassObj()
        self.run_hook('post_init_source_spreadsheet')

        self.run_hook('pre_init_destination_spreadsheet')
        destklassObj = self.getDestinationClass()
        self.destinationSpreadsheet = destklassObj()
        self.run_hook('post_init_destination_spreadsheet')

        self.run_hook('post_init_spreadsheets')

        self.run_hook('pre_init_worksheets')
        self.sourceWorksheet = self.sourceSpreadsheet.getWorksheet(worksheetTitle=self.sourceWorksheetName)

        self.destinationWorksheet = self.openOrCreateDestinationWorksheet(self.destinationWorksheetName)

        # easy way to make destination fetch the data
        self.destinationStartHeight = self.destinationWorksheet.height()
        self.run_hook('post_init_worksheets')

        self.run_hook('pre_init_setupDestination')
        self.setupDestination()
        self.run_hook('post_init_setupDestination')
        
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
    def run_hook(self, name:str):
        logger_name.name = "MapData"
        Logger.warning(f"Checking MapData hook: {name}")
        
        if Helper.classHasMethod(klass=self, methodName=name):
            Helper.callMethod(klass=self, methodName=name)


    @Debugger
    def getSourceClass(self):
        basePath = "modules.spreadsheets.sources."
        return self.getSpreadsheetClass(basePath + self.sourceClassPath)


    @Debugger
    def getDestinationClass(self):
        basePath = "modules.spreadsheets.destinations."
        return self.getSpreadsheetClass(basePath + self.destinationClassPath)


    @Debugger
    @validate_arguments
    def getSpreadsheetClass(self, spreadsheet_class:str):
        return Helper.importClass(spreadsheet_class)


    @Debugger
    def setupDestination(self):
        self.run_hook('pre_setupDestination')
        # The columns we will write to the destination
        self.destination_expectedCols = self.destinationWorksheet.getExpectedColumns()

        # Make sure the columns we need at the destination are setup
        self.destinationWorksheet.alignToColumns(self.destination_expectedCols)
        self.run_hook('post_setupDestination')

    @Debugger
    def map(self):
        self.run_hook('pre_map')
        for row in range(0, self.sourceWorksheet.height()):
            # get the data we will start with
            sourceData = self.sourceWorksheet.getRow(row, update_timestamp=False)
            
            # reset to false for the next item
            self.skipItem = False # allows mapFields() to identify a row to skip

            # merge the source and Destination data, based on whatever rules you need
            sourceData = self.mapFields(sourceData)

            # map the keys that we want to keep
            modifiedData = {}
            for key in self.destination_expectedCols:
                
                if key != "update_timestamp" and False == self.skipItem:
                    if not key in sourceData.keys():
                        raise DataMove_Exception(f" '{key} was not found in sources, does it need to be mapped?")
                    
                    modifiedData[key] = sourceData[key]


            if False == self.skipItem: # we are not skipping this item
                destinationData = []

                if list(modifiedData.keys()) == self.destination_expectedCols:
                    for column in self.destination_expectedCols:
                        destinationData.append(modifiedData[column])
                    # putRow will determine, based on uniqueKeys, whether this should be an insert or update
                    self.destinationWorksheet.putRow(destinationData)
                else:
                    print(f"\nLeft: {[x for x in modifiedData if x not in set(self.destination_expectedCols)]}\n")
                    print(f"\nRight: {[x for x in self.destination_expectedCols if x not in set(modifiedData)]}\n")
                    raise DataMove_Exception(f"There are columns missing from modified data. Received {list(modifiedData.keys())} Expected {self.destination_expectedCols}")

        self.run_hook('post_map')

    @Debugger
    @validate_arguments
    def mapFields(self, sourceData:dict):
        pass


    @Debugger
    def run(self):
        self.run_hook('pre_run')
        
        self.run_hook('pre_run_map')
        self.map()
        self.run_hook('post_run_map')
        
        self.run_hook('pre_run_commit')
        self.commit()
        self.run_hook('post_run_commit')
        
        self.run_hook('pre_run_problems')
        self.problems()
        self.run_hook('post_run_problems')
        
        self.run_hook('post_run')


    @Debugger
    @validate_arguments
    def noteProblem(self, problemType, problemDescription):
        self.run_hook('pre_noteProblems')
        
        self.skipItem = True
        if not problemType in self.problemsIdentified.keys():
            self.problemsIdentified[problemType] = [problemDescription]
        else:
            self.problemsIdentified[problemType].append(problemDescription)

        self.run_hook('post_noteProblems')


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
    def commit(self):
        self.run_hook('pre_commit')
        self.destinationWorksheet.commit()
        self.run_hook('post_commit')