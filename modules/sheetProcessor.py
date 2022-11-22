import sys, getopt, os, gspread
from modules.spreadsheet import Spreadsheet
from modules.base import BaseClass

# @todo refactor to pull out the getops functionality from this script
#	create a class that takes in getopt options and data
# 	and then have this Sheet Processor extend that class and pass the configuration
class SheetProcessor(BaseClass):
    # set the default spreadsheet id from the constants or configuration
    spreadsheet = None

    # from BaseClass - allows us to set sub loggers
    logger_name = "SheetProcessor"

    default_output = os.path.basename(__file__) + ' -h to see available commands and information'
    help_output = """
    To Use the SheetProcessor, pass in some commands:
        -s or --spreadsheet-id is the ID of the spreadsheet that you want to parse
        -lw or --list-worksheets will get you a list of the worksheets that are available
        -w or worksheets is the comma seperated list of worksheets to process, use "-w all" to process all available worksheets
    """
    def __init__(self):
        super(SheetProcessor, self).__init__()

    def main(self, argv):
        self.debug("SheetProcessor.main(%s)" % str(argv))
        outputfile = ''

        try:
            opts, args = getopt.getopt(argv, "chs:w:l",["spreadsheet-id=","worksheets=","check-worksheet-cols"])
 
        except getopt.GetoptError as msg:
            self.critical(msg)
            self.error(self.default_output)
            sys.exit(2)

        if [] == opts:
            self.critical("No Options were passed!")
            self.error(self.help_output)
            sys.exit()

        for opt, arg in opts:     
            if opt == '-h' or opt == None:
                self.debug("user selected -h option")
                print(self.help_output)
                sys.exit()

            # everything from here on needs the spreadsheet to be setup.
            self.getSheet()
            
            if opt in ("-c", "--check-worksheet-cols"):
                # check the column titles and see if they fit our preferences
                self.debug("user selected -c option")
                print("Checking column titles on worksheets")
                self.checkWorksheetColumns()
                sys.exit()
            elif opt in ("-s", "--spreadsheet-id"):
                self.debug("user selected -s option")
                # override spreadsheet ID
                print("Overriding the default worksheet to be: " + arg)  
                self.spreadsheet_id = arg
            
            elif opt in ("-l", "--list-worksheets"):
                self.debug("user selected -l option")
                print("Current Worksheet List:")
                self.outputWorksheets()
                sys.exit()
            
            elif opt in ("-w", "--worksheets"):
                self.debug("user selected -w option")
                print('Processing worksheet: ' + arg)
                self.processWorksheets(arg)
                sys.exit()
            
            else:
                self.critical("Somehow we got through all options with no option selected")
                print(self.default_output)
                print(opts)
                print(args)
                sys.exit()


    # setup the sheet object if not setup, return it either way
    def getSheet(self):
        self.debug("SheetProcessor.getSheet()")
        if None == self.spreadsheet:
            self.spreadsheet = Spreadsheet()

        return self.spreadsheet


    # list all the worksheets in the spreadsheet. If use_cache is true, then return the stored object
    # if use_cached is false, go retrieve it again
    def listWorksheets(self, use_cache = True):
        self.debug("SheetProcessor.listWorksheets(%s)" % str(use_cache))
        return self.spreadsheet.listWorksheets(use_cache)


    # print out the worksheets to the console
    def outputWorksheets(self):
        self.debug("SheetProcessor.outputWorksheets()")
        self.spreadsheet.outputWorksheets()


    # do the processing of the worksheets
    # @todo this is a bullshit placeholder, determine the type of processing or feed a config or something
    def processWorksheets(self, sheets):
        self.debug("SheetProcessor.processWorksheets(%s)" % str(sheets))
        print("Nothing is defined here yet")
        sys.exit()

    def checkWorksheetColumns(self):
        self.debug("SheetProcessor.checkWorksheetColumns()")
        self.spreadsheet.checkWorksheetColumns()
        return