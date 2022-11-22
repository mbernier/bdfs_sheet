import sys, getopt, os, gspread
from modules.spreadsheet import Spreadsheet

# @todo refactor to pull out the getops functionality from this script
#	create a class that takes in getopt options and data
# 	and then have this Sheet Processor extend that class and pass the configuration
class SheetProcessor:
    # set the default spreadsheet id from the constants or configuration
    spreadsheet = None

    def main(self, argv):
        outputfile = ''

        default_output = os.path.basename(__file__) + ' -h to see available commands and information'
        help_output = """
            -s or --spreadsheet-id is the ID of the spreadsheet that you want to parse
            -lw or --list-worksheets will get you a list of the worksheets that are available
            -w or worksheets is the comma seperated list of worksheets to process, use "-w all" to process all available worksheets
        """

        try:
            opts, args = getopt.getopt(argv, "hs:w:l",["spreadsheet-id=","worksheets="])
 
        except getopt.GetoptError as msg:
            print(msg)
            print(default_output)
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print(help_output)
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
                print(default_output)
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