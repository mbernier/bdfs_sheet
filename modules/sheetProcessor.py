import sys, getopt, os, gspread
from modules.spreadsheet import Spreadsheet

#setup logging
import logging
from modules.logger import logger
#define a sub-logger just for this code
logger = logging.getLogger('logs.SheetProcessor')

# @todo refactor to pull out the getops functionality from this script
#	create a class that takes in getopt options and data
# 	and then have this Sheet Processor extend that class and pass the configuration
class SheetProcessor:
    # set the default spreadsheet id from the constants or configuration
    spreadsheet = None

    default_output = os.path.basename(__file__) + ' -h to see available commands and information'
    help_output = """
    To Use the SheetProcessor, pass in some commands:
        -s or --spreadsheet-id is the ID of the spreadsheet that you want to parse
        -lw or --list-worksheets will get you a list of the worksheets that are available
        -w or worksheets is the comma seperated list of worksheets to process, use "-w all" to process all available worksheets
    """

    def main(self, argv):
        outputfile = ''

        try:
            opts, args = getopt.getopt(argv, "chs:w:l",["spreadsheet-id=","worksheets=","check-worksheet-cols"])
 
        except getopt.GetoptError as msg:
            print(msg)
            print(self.default_output)
            sys.exit(2)

        if [] == opts:
            print("No Options were passed!")
            print(self.help_output)
            sys.exit()

        for opt, arg in opts:     
            if opt == '-h' or opt == None:
                print(self.help_output)
                sys.exit()
            elif opt in ("-c", "--check-worksheet-cols"):
                # check the column titles and see if they fit our preferences
                print("Checking column titles on worksheets")
                self.checkWorksheetColumns()
                sys.exit()
            elif opt in ("-s", "--spreadsheet-id"):
                # override spreadsheet ID
                print("Overriding the default worksheet to be: " + arg)  
                self.spreadsheet_id = arg
            
            elif opt in ("-l", "--list-worksheets"):
                print("Current Worksheet List:")
                self.outputWorksheets()
                sys.exit()
            
            elif opt in ("-w", "--worksheets"):
                print('Processing worksheet: ' + arg)
                self.processWorksheets(arg)
                sys.exit()
            
            else:
                print(self.default_output)
                print(opts)
                print(args)
                sys.exit()


    # setup the sheet object if not setup, return it either way
    def getSheet(self):
        if None == self.spreadsheet:
            self.spreadsheet = Spreadsheet()

        return self.spreadsheet


    # list all the worksheets in the spreadsheet. If use_cache is true, then return the stored object
    # if use_cached is false, go retrieve it again
    def listWorksheets(self, use_cache = True):
        self.getSheet()
        return self.spreadsheet.listWorksheets(use_cache)


    # print out the worksheets to the console
    def outputWorksheets(self):
        self.getSheet()
        self.spreadsheet.outputWorksheets()


    # do the processing of the worksheets
    # @todo this is a bullshit placeholder, determine the type of processing or feed a config or something
    def processWorksheets(self, sheets):
        print("Nothing is defined here yet")
        sys.exit()

    def checkWorksheetColumns(self):
        self.spreadsheet.checkWorksheetColumns()
        return