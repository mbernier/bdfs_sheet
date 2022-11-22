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


    # pass in the sheet ID if it was passed
    def __init__(self):
        super(Spreadsheet, self).__init__()
        self.debug("  Spreadsheet.__init__()")
        if None == self.spreadsheetId:
            #fail if no one set the spreadsheetId on the wrapper class
            raise Exception("class Spreadsheet cannot implement __init__ on it's own. Extend and pass a Spreadsheet Id")
        self.getSheet()


    # set the sheet Id in case we want to override the default
    def setSpreadsheetId(id = None):
        self.debug("  Spreadsheet.setSpreadsheetId(%s)", id)
        this.spreadsheetId = id

    def getSpreadsheetId(self):
        self.debug("  Spreadsheet.getSpreadsheetId()")
        return self.spreadsheetId


    # setup the service account if not setup, return it either way
    def getServiceAccount(self):
        self.debug("  Spreadsheet.getServiceAccount()")
        if None == self.service_account: 
            self.service_account = gspread.service_account()
        return self.service_account


    # setup the sheet object if not setup, return it either way
    def getSheet(self, use_cache = True):
        self.debug("  Spreadsheet.getSheet(%s)" % str(use_cache))
        # make sure we have a service account setup
        self.getServiceAccount()

        if None == self.spreadsheet or False == use_cache:
            self.spreadsheet = self.service_account.open_by_key(self.spreadsheetId)

        return self.spreadsheet

    # scrub out the worksheets we don't care about based on the pattern
    # pattern: sheets we care about include "inventory" in the title
    def setWorksheets(self, worksheetList):
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
    def getWorksheets(self):
        self.debug("Spreadsheet.getWorksheets()")
        return self.worksheet_list


    # list all the worksheets in the spreadsheet. If use_cache is true, then return the stored object
    # if use_cached is false, go retrieve it again
    def listWorksheets(self, use_cache = True):
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
            print("    " + str(sheet.title))


    def checkWorksheetColumns(self):
        self.debug("Spreadsheet.checkWorksheetColumns()")
        columns = ["Title"]
        for worksheet in self.getWorksheets():
            print(str(this.spreadsheet.get("'%s'!A1:Z1", worksheet.title)))
