import sys, getopt, os, gspread
from modules.base import BaseClass
from modules.decorator import Debugger
from modules.logger import Logger

# @todo refactor to pull out the getops functionality from this script
#   create a class that takes in getopt options and data
#   and then have this Sheet Processor extend that class and pass the configuration
class SheetProcessor(BaseClass):
    
    # from BaseClass - allows us to set sub loggers
    logger_name = "SheetProcessor"

    spreadsheet_class = "modules.spreadsheet.Spreadsheet"

    default_output = os.path.basename(__file__) + ' -h to see available commands and information'
    help_output = """


To Use the SheetProcessor, pass in some commands:

    -c or --check-worksheet-cols 
            to make sure the columns are setup properly in the sheet

    --check-and-add-missing-cols 
            to find any columns that are missing and add them

    -s or --spreadsheet-id 
            to pass in the ID of the spreadsheet that you want to parse

    -lw or --list-worksheets 
            will get you a list of the worksheets that are available

    -w or --worksheets 
            to pass in a comma seperated list of worksheets to process, use "-w all" to process all available worksheets


"""
    @Debugger
    def __init__(self):
        # set the default spreadsheet id from the constants or configuration
        self.spreadsheet = None

    @Debugger
    def main(self, argv):
        outputfile = ''

        try:
            opts, args = getopt.getopt(argv, "chs:w:l",["spreadsheet-id=","worksheets=","check-worksheet-cols","check-and-add-missing-cols"])
        except getopt.GetoptError as msg:
            Logger.critical(msg)

        if [] == opts:
            Logger.critical("No Options were passed!"+ "\n" + self.help_output)

        for opt, arg in opts:     
            if opt == '-h' or opt == None:
                Logger.debug("user selected -h option")
                print(self.help_output)
                sys.exit()


            ####
            #
            # Setup the spreadsheet Object now, so we don't need it if someone is just requesting help info
            #
            ####
            self.__setUpSpreadsheet()

            if opt in ("-c", "--check-worksheet-cols"):
                # check the column titles and see if they fit our preferences
                Logger.debug("user selected -c option")
                Logger.console("Checking column titles on worksheets")
                self.checkWorksheetColumns(checkExtras = True, addMissingColumns = False)
                sys.exit()

            if opt in ("--check-and-add-missing-cols"):
                # check the column titles and see if they fit our preferences
                self.debug("user selected -check-and-add-missing-cols option")
                self.console("Checking column titles on worksheets")
                self.checkWorksheetColumns(checkExtras = True, addMissingColumns = True)
                sys.exit()
            
            elif opt in ("-l", "--list-worksheets"):
                Logger.debug("user selected -l option")
                Logger.console("Current Worksheet List:")
                print(self.listWorksheets())
                sys.exit()
            
            elif opt in ("-w", "--worksheets"):
                Logger.debug("user selected -w option")
                Logger.console('Processing worksheet: ' + arg)
                self.processWorksheets(arg)
                sys.exit()
            
            else:
                Logger.console(self.default_output)
                Logger.debug(opts)
                Logger.debug(args)
                Logger.critical("Somehow we got through all options with no option selected")

    # setup the sheet object if not setup, return it either way
    @Debugger
    def __setUpSpreadsheet(self):
        if None == self.spreadsheet:
            # self.spreadsheet = getattr(sys.modules[self.spreadsheet_class["module"]], self.spreadsheet_class["class"])
            spreadsheetClass = self.importClass(self.spreadsheet_class) 
            self.spreadsheet = spreadsheetClass()
        return self.spreadsheet


    # list all the worksheets in the spreadsheet. If use_cache is true, then return the stored object
    # if use_cached is false, go retrieve it again
    @Debugger
    def listWorksheets(self):
        return self.spreadsheet.getWorksheets()


    # call the spreadsheet checkWorksheet functionality, which checks the columns and other features of the spreadsheet
    #   to make sure that the spreadsheet is valid for what we want to do
    @Debugger
    def checkWorksheetColumns(self, checkExtras = True, addMissingColumns = False):
        self.spreadsheet.checkWorksheetColumns(checkExtras = checkExtras, addMissingColumns = addMissingColumns)
        return