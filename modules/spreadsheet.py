import gspread,datetime,sys
from modules.base import BaseClass
from modules.worksheet import Worksheet

# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import utils as gspread_utils

# @todo the spreadsheet ID should be given by the extending class
#   If this class is called directly, then it should error out because it should never have a
#   spreadsheet ID.

class Spreadsheet(BaseClass):

    spreadsheetId = None
    service_account = None
    worksheetKeeperPattern = None

    spreadsheet = None
    worksheet_list = None

    cols_expected = []
    cols_expected_extra = []

    # from BaseClass - allows us to set sub loggers
    logger_name = "Spreadsheet"

    # pass in the sheet ID if it was passed
    def __init__(self):

        # placeholders for cacheable items

        #this HAS to come after super() call, otherwise you get errors bc the logger isn't setup yet
        self.debug("__init__()")

        # let's make sure that the wrapper class is playing by the rules
        self.checkSetup()

        # make sure we have a service account setup
        self.getServiceAccount()

        # if we get this far, then we should setup the spreadsheet object
        self.getSheet()


    # quick check that the things we want passed in are in fact passed
    # otherwise, just fail
    def checkSetup(self):
        self.debug("checkSetup()")

        #if we don't have the spreadsheetId we cannot connect to it
        if None == self.getSpreadsheetId():
            self.critical("SpreadsheetId was not set before instantiating Spreadsheet class")
            #fail if no one set the spreadsheetId on the wrapper class
            raise Exception("class Spreadsheet cannot implement __init__ on it's own. Extend and pass a Spreadsheet Id")

        # if we don't know what cols are expected, we cannot check the sheet is setup properly
        if [] == self.getExpectedColumns():
            #fail if no one set the spreadsheetId on the wrapper class
            self.critical("Cols expected was not set before instantiating Spreadsheet class")
            raise Exception("cols_expected parameter is not set")

        # we don't NEED the keeperPattern, but if we want to reduce the work and prevent errors later it's a good idea
        if None == self.getWorksheetKeeperPattern():
            self.warning("worksheetKeeperPattern is not set, this is OK")

    
    def setExpectedColumns(self, expectedColumns):
        self.debug("setExpectedColumns({})".format(expectedColumns))
        self.cols_expected = expectedColumns
        return self.getExpectedColumns()

    def getExpectedColumns(self):
        self.debug("getExpectedColumns()")
        return self.cols_expected

    def getExtraExpectedColumns(self):
        self.debug("getExtraExpectedColumns()")
        return self.cols_expected_extra

    def setExtraExpectedColumns(self, extraColumns):
        self.debug("setExtraExpectedcolumns({})".format(extraColumns))
        self.cols_expected_extra = extraColumns
        return self.getExtraExpectedColumns()

    def getWorksheetKeeperPattern(self):
        self.debug("getWorksheetKeeperPattern()")
        return self.worksheetKeeperPattern

    def setWorksheetKeeperPattern(self, worksheetKeeperPattern):
        self.debug("setWorksheetKeeperPattern({})".format(worksheetKeeperPattern))
        self.worksheetKeeperPattern = worksheetKeeperPattern
        return getWorksheetKeeperPattern()

    # set the sheet Id in case we want to override the default
    def setSpreadsheetId(id = None):
        self.debug("setSpreadsheetId(%s)", id)
        self.spreadsheetId = id
        return self.getSpreadsheetId()


    # get the id that we have set and return it
    def getSpreadsheetId(self):
        self.debug("getSpreadsheetId()")
        return self.spreadsheetId


    # setup the service account if not setup, return it either way
    def getServiceAccount(self):
        self.debug("getServiceAccount()")
        if None == self.service_account: 
            self.service_account = gspread.service_account()
        return self.service_account


    # setup the sheet object if not setup, return it either way
    def getSheet(self, use_cache = True):
        self.debug("getSheet(%s)" % str(use_cache))

        if None == self.spreadsheet or False == use_cache:
            self.spreadsheet = self.service_account.open_by_key(self.spreadsheetId)

        return self.spreadsheet


    # scrub out the worksheets we don't care about based on the pattern
    # pattern: sheets we care about include "inventory" in the title
    def setWorksheetList(self, worksheetList) -> list:
        self.debug("setWorksheetList(%s)" % str(worksheetList))
        if None == self.getWorksheetKeeperPattern():
            # no pattern is set, allow all the sheets through
            self.worksheet_list = worksheetList
        else:
            # if we have a pattern, we should follow it
            tempSheets = []
            # clear out the worksheets we don't need
            for sheet in worksheetList:
                if self.getWorksheetKeeperPattern() in sheet.title:
                    tempSheets.append(sheet)
            self.worksheet_list = tempSheets
        return self.getWorksheetList()


    # quick setter for the worksheet list
    def getWorksheetList(self, use_cache = True) -> list:
        self.debug("getWorksheets()")
        if None == self.worksheet_list or False == use_cache:
            self.listWorksheets()
        return self.worksheet_list


    # list all the worksheets in the spreadsheet. If use_cache is true, then return the stored object
    # if use_cached is false, go retrieve it again
    def listWorksheets(self, use_cache = True) -> list:
        self.debug("listWorksheets(%s)" % str(use_cache))

        # if the worksheet list is false or the code wants to retrieve a new list, retrieve it
        if None == self.worksheet_list or False == use_cache:
            # make sure we are setting the sheets appropriately
            self.setWorksheetList(self.spreadsheet.worksheets())

        return self.getWorksheetList()


    # print the worksheets to the console
    def outputWorksheets(self):
        self.debug("outputWorksheets()")
        # make sure that we have worksheets before we try to output them
        self.listWorksheets()
        for sheet in self.getWorksheetList():
            self.console(str(sheet.title))


    # only checks the columns, doesn't do anything to adjust or fix them
    # colsToCheck allows you to pass in something new to check against, rather than whatever is in cols_expected
    # checkExtras will allow you to bypass checking against the cols_expected_extra columns
    def checkWorksheetColumns(self, colsToCheck = None, checkExtras = True, addMissingColumns = False):
        self.debug("checkWorksheetColumns(colsToCheck={},checkExtras={},addMissingColumns={})".format(colsToCheck,checkExtras,addMissingColumns))
        # if nothing was passed through, then use the default. Otherwise, use what was passed
        if None == colsToCheck:
            colsToCheck = self.getExpectedColumns()

        for worksheet in self.getWorksheetList():
            # setup the worksheet, do an initial pull of the data, then we can modify all we want and commit
            worksheet = Worksheet(worksheet)

            # Right now, this can get all the data and sets up the cache in the WorksheetData class wrapped around NestedCache
            # We need to figure out how to do the functionality below within the cached sheetData
            # - making sure to keep the headers, data, etc up to date as we go
            # - once it's cleaned, organized, we need to commit the data to the google sheet

            # decide what we need to keep from DataStore class and the X_ methods on worksheet, based on what we need to build below, as well


                # 1. given a list of columns that we need, compare to the columns we have and return the diff:
                #     a. Columns in the spreadsheet that are not in getExpectedColumns
                #     b. Columns in expected that are not in the spreadsheet
                # 2. Decide what to do with the extra columns in the sheet
                #     - offer a flag to ignore columns in spreadsheet that are not in expected (keep them)
                #     - if flag is not set to ignore, then throw an error
                # 3. Add the missing expected columns to the spreadsheet
                # 
                #
                #



            raise Exception("Processing is stopped in Spreadsheet line ~190")
            sys.exit()






            # 
            # Original info, assumed the sheet was source of truth, needs to be converted to object as source of truth
            #             

            worksheet.checkColumns(self.getExpectedColumns(), self.getExtraExpectedColumns())
            if addMissingColumns:
                # remove the empty columns
                # clean up the empties so that we have a good measure of the sheet
                worksheet.removeEmptyColumns()

                # add in the new columns, so that we have everything we need
                addedColumns = worksheet.addMissingColumns()

                self.info("{} columns were added to {}".format(addedColumns, worksheet.getTitle()))

                # double check that we don't have extra empties at the end of the sheet, just in case
                worksheet.removeEmptyColumns(removeTrailingEmpties=True)

                # since we can't control how the data gets added in previous steps or how it was in the original sheet, 
                #   make sure it is clean here. By default, this stores to the worksheet when it's done running. To cancel that
                #   add storeToWorksheet = False
                sheetData = worksheet.sortTheColumns()
            self.console("We are only running one worksheet right now, see Spreadhsheet.py line 188")
            sys.exit()