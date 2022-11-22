import gspread

# @todo the spreadsheet ID should be given by the extending class
#   If this class is called directly, then it should error out because it should never have a
#   spreadsheet ID.
# This is the BDFS Inventory spreadsheet ID
SPREADSHEET_ID = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'

class Spreadsheet:
    # placeholders for cacheable items
    service_account = None
    spreadsheet = None
    spreadsheetId = SPREADSHEET_ID
    worksheet_list = None    
    

    # pass in the sheet ID if it was passed
    def _init_(id = None):
        if None != id:
            setSheetId(id)


    # set the sheet Id in case we want to override the default
    def setSheetId(id = None):
        this.spreadsheetId = id


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


    # list all the worksheets in the spreadsheet. If use_cache is true, then return the stored object
    # if use_cached is false, go retrieve it again
    def listWorksheets(self, use_cache = True):
        # make sure we have a sheet object setup
        self.getSheet()

        # if the worksheet list is false or the code wants to retrieve a new list, retrieve it
        if None == self.worksheet_list or False == use_cache:
            self.worksheet_list = self.spreadsheet.worksheets()

        return self.worksheet_list


    # print the worksheets to the console
    def outputWorksheets(self):
        # make sure that we have worksheets before we try to output them
        self.listWorksheets()
        for sheet in self.worksheet_list:
            print("    " + str(sheet.title))


    def read_sheet(this):
        print("nothing implemented here")
        sys.exit()
        
        SAMPLE_RANGE_NAME = 'sarto_barn_single!D2:CR'