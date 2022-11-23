import gspread
from modules.base import BaseClass

# @todo the spreadsheet ID should be given by the extending class
#   If this class is called directly, then it should error out because it should never have a
#   spreadsheet ID.

class Spreadsheet(BaseClass):
    # placeholders for cacheable items
    service_account = None
    spreadsheet = None
    spreadsheetId = None
    worksheet_list = None
    worksheetKeeperPattern = None

    # from BaseClass - allows us to set sub loggers
    logger_name = "Spreadsheet"
    cols_expected = []
    cols_expected_extra = []


    # pass in the sheet ID if it was passed
    def __init__(self):
        # has to be called to setup all the BaseClass wonderfulness, otherwise things like the logger don't get instantiated
        super(Spreadsheet, self).__init__()

        #this HAS to come after super() call, otherwise you get errors bc the logger isn't setup yet
        self.debug("Spreadsheet.__init__()")

        # let's make sure that the wrapper class is playing by the rules
        self.checkSetup()

        # if we get this far, then we should setup the spreadsheet object
        self.getSheet()
        

    # quick check that the things we want passed in are in fact passed
    # otherwise, just fail
    def checkSetup(self):
        self.debug("Spreadsheet.checkSetup()")

        #if we don't have the spreadsheetId we cannot connect to it
        if None == self.spreadsheetId:
            self.critical("SpreadsheetId was not set before instantiating Spreadsheet class")
            #fail if no one set the spreadsheetId on the wrapper class
            raise Exception("class Spreadsheet cannot implement __init__ on it's own. Extend and pass a Spreadsheet Id")

        # if we don't know what cols are expected, we cannot check the sheet is setup properly
        if [] == self.cols_expected:
            #fail if no one set the spreadsheetId on the wrapper class
            self.critical("Cols expected was not set before instantiating Spreadsheet class")
            raise Exception("cols_expected parameter is not set")

        # we don't NEED the keeperPattern, but if we want to reduce the work and prevent errors later it's a good idea
        if None == self.worksheetKeeperPattern:
            self.warning("Spreadsheet.worksheetKeeperPattern is not set, this is OK")


    # set the sheet Id in case we want to override the default
    def setSpreadsheetId(id = None):
        self.debug("Spreadsheet.setSpreadsheetId(%s)", id)
        this.spreadsheetId = id


    # get the id that we have set and return it
    def getSpreadsheetId(self):
        self.debug("Spreadsheet.getSpreadsheetId()")
        return self.spreadsheetId


    # setup the service account if not setup, return it either way
    def getServiceAccount(self):
        self.debug("Spreadsheet.getServiceAccount()")
        if None == self.service_account: 
            self.service_account = gspread.service_account()
        return self.service_account


    # setup the sheet object if not setup, return it either way
    def getSheet(self, use_cache = True):
        self.debug("Spreadsheet.getSheet(%s)" % str(use_cache))
        # make sure we have a service account setup
        self.getServiceAccount()

        if None == self.spreadsheet or False == use_cache:
            self.spreadsheet = self.service_account.open_by_key(self.spreadsheetId)

        return self.spreadsheet


    # scrub out the worksheets we don't care about based on the pattern
    # pattern: sheets we care about include "inventory" in the title
    def setWorksheets(self, worksheetList) -> list:
        self.debug("Spreadsheet.setWorksheets(%s)" % str(worksheetList))
        if None == self.worksheetKeeperPattern:
            self.debug()
            # no pattern is set, allow all the sheets through
            self.worksheet_list = worksheetList
        else:
            # if we have a pattern, we should follow it
            tempSheets = []
            # clear out the worksheets we don't need
            for sheet in worksheetList:
                if  self.worksheetKeeperPattern in sheet.title:
                    tempSheets.append(sheet)
            self.worksheet_list = tempSheets
        return self.getWorksheets()


    # quick setter for the worksheet list
    def getWorksheets(self, use_cache = True) -> list:
        self.debug("Spreadsheet.getWorksheets()")
        if None == self.worksheet_list or False == use_cache:
            self.listWorksheets()
        return self.worksheet_list


    # list all the worksheets in the spreadsheet. If use_cache is true, then return the stored object
    # if use_cached is false, go retrieve it again
    def listWorksheets(self, use_cache = True) -> list:
        self.debug("Spreadsheet.listWorksheets(%s)" % str(use_cache))

        # if the worksheet list is false or the code wants to retrieve a new list, retrieve it
        if None == self.worksheet_list or False == use_cache:
            # make sure we are setting the sheets appropriately
            self.setWorksheets(self.spreadsheet.worksheets())

        return self.worksheet_list


    # print the worksheets to the console
    def outputWorksheets(self):
        self.debug("Spreadsheet.outputWorksheets()")
        # make sure that we have worksheets before we try to output them
        self.listWorksheets()
        for sheet in self.getWorksheets():
            self.console(str(sheet.title))

    # only checks the columns, doesn't do anything to adjust or fix them
    # colsToCheck allows you to pass in something new to check against, rather than whatever is in cols_expected
    # checkExtras will allow you to bypass checking against the cols_expected_extra columns
    def checkWorksheetColumns(self, colsToCheck = None, checkExtras = True, addMissingColumns = False):
        self.debug("Spreadsheet.checkWorksheetColumns()")

        # if nothing was passed through, then use the default. Otherwise, use what was passed
        if None == colsToCheck:
            colsToCheck = self.cols_expected

        for worksheet in self.getWorksheets():
            self.info("Worksheet: " + str(worksheet.title))

            #
            # The following is all logic to setup the columns that we need to check against
            #

            # set the columns to the default
            colsToCheck = self.cols_expected

            # if we are checking extras and we have extra cols to check, then let's loop through. Otherwise, just do the normal thing
            if True == checkExtras and [] != self.cols_expected_extra:

                # if we have extra columns that we need to check, loop through the options
                for extraColCheck, colTitles in self.cols_expected_extra.items():

                    # if we find that the key for the extra columns is in the worksheet title, 
                    # then append the extras columns to check and then check against the new combined list
                    if extraColCheck in worksheet.title:
                         colsToCheck += self.cols_expected_extra[extraColCheck]

            #
            # The following is actually checking the columns
            #

            # get everything from the first row
            first_row = worksheet.row_values(1)
            
            row_length = len(first_row)
            self.info("The row is %i cols long" % row_length)

            # does the first_row contain everything in the colsToCheck
            firstrow_result = self.compareLists(first_row, colsToCheck)

            if firstrow_result:
                self.info("The worksheet %s has all the columns we expect" % worksheet.title)
            else: 
                self.info("The worksheet %s does not have all the columns we expect" % worksheet.title)
                #figure out what's missing and complain so that we can get that shit fixed
                missing_columns = list(set(colsToCheck) - set(first_row))
                self.console("Worksheet: {} is missing these columns: ".format(worksheet.title), data=str(missing_columns))
                if True == addMissingColumns:
                    self.addColumnsToWorkSheet(worksheet, missing_columns)

    def addColumnsToWorkSheet(self, worksheet, columnsToAdd):
        self.error("NEED TO ADD THIS FUNCTIONALITY")

