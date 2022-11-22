import gspread

# @todo the spreadsheet ID should be given by the extending class
#   If this class is called directly, then it should error out because it should never have a
#   spreadsheet ID.

#setup logging
import logging
from modules.logger import logger
#define a sub-logger just for this code
logger = logging.getLogger('logs.Spreadsheet')


class Spreadsheet:
    # placeholders for cacheable items
    service_account = None
    spreadsheet = None
    spreadsheetId = None
    worksheet_list = None
    worksheetKeeperPattern = None

    # pass in the sheet ID if it was passed
    def __init__(self):
        if None == self.spreadsheetId:
            #fail if no one set the spreadsheetId on the wrapper class
            raise Exception("class Spreadsheet cannot implement __init__ on it's own. Extend and pass a Spreadsheet Id")


    # set the sheet Id in case we want to override the default
    def setSpreadsheetId(id = None):
        this.spreadsheetId = id

    def getSpreadsheetId(self):
        return self.spreadsheetId


    # setup the service account if not setup, return it either way
    def getServiceAccount(self):
        if None == self.service_account: 
            self.service_account = gspread.service_account()
        return self.service_account


    # setup the sheet object if not setup, return it either way
    def getSheet(self, use_cached = True):
        # make sure we have a service account setup
        self.getServiceAccount()

        if None == self.spreadsheet or False == use_cached:
            self.spreadsheet = self.service_account.open_by_key(self.spreadsheetId)

        return self.spreadsheet

    # scrub out the worksheets we don't care about based on the pattern
    # pattern: sheets we care about include "inventory" in the title
    def setWorksheets(self, worksheetList):
        if None == self.worksheetKeeperPattern:
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
    def getWorksheets(self):
        return self.worksheet_list


    # list all the worksheets in the spreadsheet. If use_cache is true, then return the stored object
    # if use_cached is false, go retrieve it again
    def listWorksheets(self, use_cache = True):
        # make sure we have a sheet object setup
        self.getSheet()

        # if the worksheet list is false or the code wants to retrieve a new list, retrieve it
        if None == self.worksheet_list or False == use_cache:
            # make sure we are setting the sheets appropriately
            self.setWorksheets(self.spreadsheet.worksheets())

        return self.worksheet_list


    # print the worksheets to the console
    def outputWorksheets(self):
        # make sure that we have worksheets before we try to output them
        self.listWorksheets()
        for sheet in self.worksheet_list:
            print("    " + str(sheet.title))


    def checkWorksheetColumns(this):
        columns = ["Title"]
        for worksheet in self.getWorksheets():
            print(str(this.spreadsheet.get("'%s'!A1:Z1", worksheet.title)))
