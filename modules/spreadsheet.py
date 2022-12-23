import gspread, time
from dataclasses import dataclass, field as dc_field
from modules.base import BaseClass
from modules.logger import Logger
from modules.decorator import Debugger
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import worksheet, utils as gspread_utils
from pprint import pprint

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
    # from BaseClass - allows us to set sub loggers
    logger_name:str = "Spreadsheet"
    service_account = None


class Bdfs_Spreadsheet(BaseClass): 

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
            #fail if no one set the spreadsheetId on the wrapper class
            raise Exception("class Spreadsheet cannot implement __init__ on it's own. Extend and pass a Spreadsheet Id")

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
                raise Bdfs_Spreadsheet_Exception("worksheetKeeperPattern is not set in child class")

        return self.data.worksheetClassName


    # setup the service account if not setup, return it either way
    @Debugger
    def setupServiceAccount(self):
        if None == self.data.service_account:
            self.data.service_account = gspread.service_account()
        return self.data.service_account


    # setup the sheet object if not setup, return it either way
    @Debugger
    def setupSpreadsheet(self, use_cache:bool = True):
        if None == self.data.spreadsheet or False == use_cache:
            try:
                self.data.spreadsheet = self.data.service_account.open_by_key(self.data.spreadsheetId)
            except gspread.exceptions.APIError:
                Logger.error("We got rate limited, going to sleep for 60 seconds and try again")
                time.sleep(60)
                try:
                    self.data.spreadsheet = self.data.service_account.open_by_key(self.data.spreadsheetId)
                except gspread.exceptions.APIError:
                    # @todo - this would be a great place for Temporal to jump in and help
                    Logger.critical("30 seconds of sleep was not long enough, we pissed Google off - consider more sleep time, or retry at a later date")
        return self.data.spreadsheet


    # scrub out the worksheets we don't care about based on the pattern
    # pattern: sheets we care about include the keeperPattern in the title
    #   We store the local copy of theworksheet, bc it has a reference to the gspread worksheet
    @Debugger
    def setupWorksheets(self, use_cache=True) -> list:
        
        if False == use_cache or {} == self.getWorksheets():

            # retrieve the worksheets from the gpsread spreadsheet obj
            gspread_worksheets = self.data.spreadsheet.worksheets()

            keeperPattern = self.getWorksheetKeeperPattern()

            # clear out the worksheets we don't need
            for sheet in gspread_worksheets:

                # only restrict the worksheet list if there is a keeper pattern
                if None == keeperPattern or keeperPattern in sheet.title:
                    # create the place for the worksheets, but don't actually grab them yet - reduces API calls
                    self.data.worksheets[sheet.title] = None

                self.data.gspread_worksheets[sheet.title] = sheet

        return self.getWorksheets()

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
                raise Bdfs_Spreadsheet_Exception("worksheetKeeperPattern is not set in child class")

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
    def getWorksheet(self, worksheetTitle:str):
        self.setupWorksheets() #make sure they're setup before someone tries to get one
        if {} == self.getWorksheets():
            raise Exception("Worksheets were not added to the Spreadsheet properly.")
        
        if worksheetTitle in self.getWorksheets():
            if None == self.getWorksheets()[worksheetTitle]:
                worksheetClass = self.getWorksheetClass()
                self.data.worksheets[worksheetTitle] = worksheetClass(self.data.gspread_worksheets[worksheetTitle])

        return self.getWorksheets()[worksheetTitle]