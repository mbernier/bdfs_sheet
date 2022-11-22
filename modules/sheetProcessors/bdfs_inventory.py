# Gives us BDFS Inventory sheet processing specific functionality
# Allows for the configuration and specifics to be sandboxed
# Extends SheetProcessor to share that functionality

from modules.sheetProcessor import SheetProcessor
from modules.spreadsheets.bdfs_inventory import Bdfs_Spreadsheet

class Bdfs_SheetProcessor(SheetProcessor):

    # set the default spreadsheet id from the constants or configuration
    spreadsheet = None

    # from BaseClass - allows us to set sub loggers
    logger_name = "Bdfs_SheetProcessor"

    # setup the sheet object if not setup, return it either way
    def getSheet(self):
        self.debug("Bdfs_Spreadsheet.getSheet()")
        if None == self.spreadsheet:
            self.spreadsheet = Bdfs_Spreadsheet()

        return self.spreadsheet


    # list all the worksheets in the spreadsheet. If use_cache is true, then return the stored object
    # if use_cached is false, go retrieve it again
    def listWorksheets(self, use_cache = True):
        self.debug("Bdfs_Spreadsheet.listWorksheets(%s)" % str(use_cache))
        self.getSheet()
        return self.spreadsheet.listWorksheets(use_cache)


    # print out the worksheets to the console
    def outputWorksheets(self):
        self.debug("Bdfs_Spreadsheet.outputWorksheets()")
        self.getSheet()
        self.spreadsheet.outputWorksheets()


    # do the processing of the worksheets
    # @todo this is a bullshit placeholder, determine the type of processing or feed a config or something
    def processWorksheets(self, sheets):
        self.debug("Bdfs_Spreadsheet.processWorksheets(%s)" % str(sheets))
        print("Nothing is defined here yet")
        sys.exit()