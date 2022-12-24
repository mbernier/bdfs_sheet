from pydantic import validate_arguments
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.decorator import Debugger
from modules.helper import Helper
from modules.logger import Logger, logger_name


class DataMove():

    sourceSpreadsheet = None
    sourceWorksheet = None

    destinationSpreadsheet = None
    destinationWorksheet = None    
    destination_expectedCols = []

    destinationWorksheetCreateIfNotFound = True

    hooks:dict = {}
    
    @Debugger
    def __init__(self) -> None:
        self.run_hook('init_start')

        self.run_hook('init_pre_spreadsheets')
        sourceklassObj = self.getSourceClass()
        self.sourceSpreadsheet = sourceklassObj()
        
        destklassObj = self.getDestinationClass()
        self.destinationSpreadsheet = destklassObj()
        self.run_hook('init_post_spreadsheets')


        self.run_hook('init_pre_worksheets')
        self.sourceWorksheet = self.sourceSpreadsheet.getWorksheet(worksheetTitle=self.sourceWorksheetName)

        try:
            self.destinationWorksheet = self.destinationSpreadsheet.getWorksheet(worksheetTitle=self.destinationWorksheetName)
        except Bdfs_Spreadsheet_Exception as err:
            # allow not creating the spreadsheet, if wanted
            if True == self.destinationWorksheetCreateIfNotFound:
                self.destinationWorksheet = self.destinationSpreadsheet.insertWorksheet(worksheetName=self.destinationWorksheetName)
            else:
                raise Bdfs_Spreadsheet_Exception(err.message)

        self.run_hook('init_post_worksheets')

        self.setupDestination()

        self.run_hook("init_end")


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

        # The columns we will write to the destination
        self.destination_expectedCols = self.destinationWorksheet.getExpectedColumns()

        # Make sure the columns we need at the destination are setup
        self.destinationWorksheet.alignToColumns(self.destination_expectedCols)


    @Debugger
    def map(self):
        self.run_hook('pre_map')
        for row in range(0, self.sourceWorksheet.height()):
            # get the data we will start with
            sourceData = self.sourceWorksheet.getRow(row)
            
            # map the source Data to Destination Data
            modifiedData = self.mapFields(sourceData)

            destinationData = []
            for column in self.destination_expectedCols:
                destinationData.append(modifiedData[column])

            # write the destination data to the destination
            self.destinationWorksheet.addRow(destinationData)

        self.run_hook('post_map')
            

    @Debugger
    @validate_arguments
    def mapFields(self, sourceData:dict):
        pass


    @Debugger
    def run(self):
        self.run_hook('pre_run')
        self.map()
        self.commit()
        self.run_hook('post_run')


    @Debugger
    def commit(self):
        self.run_hook('pre_commit')
        self.destinationWorksheet.commit()
        self.run_hook('post_commit')