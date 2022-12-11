import gspread,datetime,sys
from dataclasses import dataclass, field as dc_field
from modules.base import BaseClass
from modules.logger import Logger
from modules.decorator import Debugger
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
    spreadsheet = None
    # from BaseClass - allows us to set sub loggers
    logger_name:str = "Spreadsheet"
    service_account = None


class Spreadsheet(BaseClass): 

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

        if None == self.data.worksheet_class:
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
        return self.importClass(self.data.worksheet_class)


    # if we haven't parsed the worksheet class name, do it, otherwise return it
    @Debugger
    def getWorksheetClassName(self):
        if None == self.data.worksheetClassName:
            self.data.worksheetClassName = self.data.worksheet_class.split(".").pop()
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
            self.data.spreadsheet = self.data.service_account.open_by_key(self.data.spreadsheetId)
        return self.data.spreadsheet


    # scrub out the worksheets we don't care about based on the pattern
    # pattern: sheets we care about include the keeperPattern in the title
    #   We store the local copy of theworksheet, bc it has a reference to the gspread worksheet
    @Debugger
    def setupWorksheets(self) -> list:
        if 0 == len(self.getWorksheets()):

            # retrieve the worksheets from the gpsread spreadsheet obj
            worksheetList = self.data.spreadsheet.worksheets()

            keeperPattern = self.getWorksheetKeeperPattern()

            worksheetClass = self.getWorksheetClass()

            # clear out the worksheets we don't need
            for sheet in worksheetList:
                # only restrict the worksheet list if there is a keeper pattern
                if None == keeperPattern or keeperPattern in sheet.title:
                    self.data.worksheets[sheet.title] = worksheetClass(sheet)

        return self.getWorksheets()

    @Debugger
    def getWorksheets(self):
        return self.data.worksheets

    @Debugger
    def getWorksheetKeeperPattern(self):
        return self.data.worksheetKeeperPattern


    # get the id that we have set and return it
    @Debugger
    def getSpreadsheetId(self):
        return self.data.spreadsheetId


    @Debugger
    def getWorksheet(self, worksheetTitle:str):
        if 0 == len(self.getWorksheets()):
            raise Exception("Worksheets were not added to the Spreadsheet properly.")
        return self.getWorksheets()[worksheetTitle]



    # # only checks the columns, doesn't do anything to adjust or fix them
    # # colsToCheck allows you to pass in something new to check against, rather than whatever is in cols_expected
    # # checkExtras will allow you to bypass checking against the cols_expected_extra columns
    # @Debugger
    # @validate_arguments
    # def checkWorksheetColumns(self, colsToCheck:list=None, checkExtras:bool=True, addMissingColumns:bool=False):
    #     # if nothing was passed through, then use the default. Otherwise, use what was passed

    #     for worksheetTitle in self.getWorksheets():
    #         worksheet = self.getWorksheet(worksheetTitle)

    #         worksheet.playground()

    #         sys.exit()

    #         #do this at the END of your processing, to make sure the data gets stored in the worksheet properly
    #         # up to this point, everything is just done in the copy of the worksheet
    #         # this helps keep the number of API calls to a minimum, so we don't get in trouble
    #         worksheet.commit()

    #         # Right now, this can get all the data and sets up the cache in the WorksheetData class wrapped around Nested_Cache
    #         # We need to figure out how to do the functionality below within the cached sheetData
    #         # - making sure to keep the headers, data, etc up to date as we go
    #         # - once it's cleaned, organized, we need to commit the data to the google sheet

    #         # decide what we need to keep from DataStore class and the X_ methods on worksheet, based on what we need to build below, as well


    #             # 1. given a list of columns that we need, compare to the columns we have and return the diff:
    #             #     a. Columns in the spreadsheet that are not in getExpectedColumns
    #             #     b. Columns in expected that are not in the spreadsheet
    #             # 2. Decide what to do with the extra columns in the sheet
    #             #     - offer a flag to ignore columns in spreadsheet that are not in expected (keep them)
    #             #     - if flag is not set to ignore, then throw an error
    #             # 3. Add the missing expected columns to the spreadsheet