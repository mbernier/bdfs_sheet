import gspread, time
from dataclasses import dataclass, field as dc_field
from modules.base import Base_Class
from modules.logger import Logger
from modules.decorator import Debugger
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import Worksheet, utils as gspread_utils
from pydantic import validate_arguments

# @todo the spreadsheet ID should be given by the extending class
#   If this class is called directly, then it should error out because it should never have a
#   spreadsheet ID.

@dataclass
class Spreadsheet_Data():
    spreadsheetId:str = dc_field(default_factory=str)
    worksheetClassName:str = dc_field(default_factory=str)
    worksheetKeeperPattern:str = dc_field(default_factory=str)
    worksheets:dict = dc_field(default_factory=dict)
    gspread_worksheets:dict = dc_field(default_factory=dict)
    spreadsheet = None
    # from Base_Class - allows us to set sub loggers
    logger_name:str = "Spreadsheet"
    service_account = None


class Bdfs_Spreadsheet(Base_Class): 

    data:Spreadsheet_Data = Spreadsheet_Data()

    # pass in the sheet ID if it was passed
    @Debugger
    def __init__(self):
        self.data = Spreadsheet_Data()
        self.worksheets = {}

        # let's make sure that the wrapper class is playing by the rules
        #if we don't have the spreadsheetId we cannot connect to it
        if None == self.getSpreadsheetId():
            Logger.critical("SpreadsheetId was not set before instantiating Spreadsheet class")

        # we don't NEED the keeperPattern, but if we want to reduce the work and prevent errors later it's a good idea
        if None == self.getWorksheetKeeperPattern():
            Logger.warning("worksheetKeeperPattern is not set, this is OK")

        if None == self.data.worksheetClassName:
            Logger.critical("You must set a worksheet_class in your Spreadsheet Object: ".self.__class__.__name__)

        self.getWorksheetClassName()

        # make sure we have a service account setup
        self.setupServiceAccount()

        # if we get this far, then we should setup the spreadsheet object
        self.setupSpreadsheet()

        # get the worksheets ahead of any work to be done
        self.setupWorksheets()


    @Debugger
    def getWorksheetClass(self):
        return self.importClass(self.worksheet_class)


    # if we haven't parsed the worksheet class name, do it, otherwise return it
    @Debugger
    def getWorksheetClassName(self):
        if self.data.worksheetClassName == "":
            if self.worksheet_class != None:
                self.data.worksheetClassName = self.worksheet_class.split(".").pop()
            else:
                raise Bdfs_Spreadsheet_Exception("worksheet_class is not set in child class")

        return self.data.worksheetClassName


    # setup the service account if not setup, return it either way
    @Debugger
    def setupServiceAccount(self):
        if None == self.data.service_account:
            self.data.service_account = gspread.service_account()
        return self.data.service_account


    # setup the sheet object if not setup, return it either way
    @Debugger
    @validate_arguments
    def setupSpreadsheet(self, use_cache:bool = True):
        if None == self.data.spreadsheet or False == use_cache:
            try:
                self.data.spreadsheet = self.data.service_account.open_by_key(self.data.spreadsheetId)
            except gspread.exceptions.APIError:
                Logger.error("We got rate limited, going to sleep for 60 seconds and try again")
                time.sleep(65)
                try:
                    self.data.spreadsheet = self.data.service_account.open_by_key(self.data.spreadsheetId)
                except gspread.exceptions.APIError:
                    # @todo - this would be a great place for Temporal to jump in and help
                    Logger.critical("65 seconds of sleep was not long enough, we pissed Google off - consider more sleep time, or retry at a later date")
        return self.data.spreadsheet


    # scrub out the worksheets we don't care about based on the pattern
    # pattern: sheets we care about include the keeperPattern in the title
    #   We store the local copy of theworksheet, bc it has a reference to the gspread worksheet
    @Debugger
    @validate_arguments
    def setupWorksheets(self, use_cache=True) -> list:
        
        if False == use_cache or {} == self.getWorksheets():

            # retrieve the worksheets from the gpsread spreadsheet obj
            gspread_worksheets = self.data.spreadsheet.worksheets()
            
            # clear out the worksheets we don't need
            for sheet in gspread_worksheets:

                self.registerWorksheet(sheet)

        return self.getWorksheets()


    @Debugger
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def registerWorksheet(self, worksheet: Worksheet, bypassKeeperPattern=False):
        keeperPattern = self.getWorksheetKeeperPattern()
        title = worksheet.title

        # only restrict the worksheet list if there is a keeper pattern
        if "" == keeperPattern or keeperPattern in title or True == bypassKeeperPattern:
            # create the place for the worksheets, but don't actually grab them yet - reduces API calls
            self.data.worksheets[title] = None

        self.data.gspread_worksheets[title] = worksheet


    @Debugger
    def getWorksheets(self):
        return self.data.worksheets

    @Debugger
    def getWorksheetKeeperPattern(self):
        if self.data.worksheetKeeperPattern == "": # this is the default in the data class
            # get this from the subclass
            if self.worksheetKeeperPattern != None:
                self.data.worksheetKeeperPattern = self.worksheetKeeperPattern
            else:
                raise Bdfs_Spreadsheet_Exception("worksheetKeeperPattern is set to None in child class, set to \"\" instead")

        return self.data.worksheetKeeperPattern


    # get the id that we have set and return it
    @Debugger
    def getSpreadsheetId(self):
        if self.data.spreadsheetId == "":
            if self.spreadsheetId != None:
                self.data.spreadsheetId = self.spreadsheetId
            else:
                raise Bdfs_Spreadsheet_Exception("Spreadsheet ID is not set in child class")

        return self.data.spreadsheetId


    @Debugger
    @validate_arguments
    def getWorksheet(self, worksheetTitle:str, skipKept=False):
        self.setupWorksheets() #make sure they're setup before someone tries to get one
        
        if {} == self.getWorksheets() and 0 == len(self.data.gspread_worksheets.keys()):
            raise Bdfs_Spreadsheet_Exception("Worksheets were not added to the Spreadsheet properly.")
        
        if worksheetTitle in self.getWorksheets():
            if None == self.getWorksheets()[worksheetTitle]:
                self.createWorksheet(worksheetTitle)
            return self.data.worksheets[worksheetTitle]
        elif True == skipKept: # we don't care that this isn't in the keeper pattern
            if worksheetTitle in self.data.gspread_worksheets.keys(): # if it exists, go ahead and grab it
                self.registerWorksheet(self.data.gspread_worksheets[worksheetTitle], bypassKeeperPattern=True)
            # this will call this function again, to make the worksheet get setup - tricky, but it works
            return self.getWorksheet(worksheetTitle)
        else:
            raise Bdfs_Spreadsheet_Exception(f"The worksheet '{worksheetTitle}' was not found in the kept worksheets: {list(self.getWorksheets().keys())}")
    
    
    @Debugger
    @validate_arguments
    def createWorksheet(self, worksheetTitle):
        """This is its own method so it can be overridden by Migrator
            Finds the worksheet class name and then instantiates a worksheet obj"""
        worksheetClass = self.getWorksheetClass()
        self.data.worksheets[worksheetTitle] = worksheetClass(self.data.gspread_worksheets[worksheetTitle])