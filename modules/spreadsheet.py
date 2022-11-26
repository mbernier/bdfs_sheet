import gspread,datetime,sys
from modules.base import BaseClass

# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import utils as gspread_utils
from pprint import pprint

# @todo the spreadsheet ID should be given by the extending class
#   If this class is called directly, then it should error out because it should never have a
#   spreadsheet ID.

class Spreadsheet(BaseClass): 

    spreadsheetId = None
    service_account = None
    worksheetKeeperPattern = None

    spreadsheet = None
    worksheet_list = []
    _worksheet_objs = {}

    # from BaseClass - allows us to set sub loggers
    logger_name = "Spreadsheet"

    worksheetClassName = None

    # pass in the sheet ID if it was passed
    def __init__(self):

        # placeholders for cacheable items

        #this HAS to come after super() call, otherwise you get errors bc the logger isn't setup yet
        self.debug("__init__()")

        # let's make sure that the wrapper class is playing by the rules
        self.__checkSetup()

        self.getWorksheetClassName()

        # make sure we have a service account setup
        self.__setupServiceAccount()

        # if we get this far, then we should setup the spreadsheet object
        self.__setupSpreadsheet()

        # get the worksheets ahead of any work to be done
        self.__setupWorksheetList()


    # quick check that the things we want passed in are in fact passed
    # otherwise, just fail
    def __checkSetup(self):
        self.debug("__checkSetup()")

        #if we don't have the spreadsheetId we cannot connect to it
        if None == self.getSpreadsheetId():
            self.critical("SpreadsheetId was not set before instantiating Spreadsheet class")
            #fail if no one set the spreadsheetId on the wrapper class
            raise Exception("class Spreadsheet cannot implement __init__ on it's own. Extend and pass a Spreadsheet Id")

        # we don't NEED the keeperPattern, but if we want to reduce the work and prevent errors later it's a good idea
        if None == self.getWorksheetKeeperPattern():
            self.warning("worksheetKeeperPattern is not set, this is OK")

        if None == self.worksheet_class:
            self.critical("You must set a worksheet_class in your Spreadsheet Object: ".self.__class__.__name__)
    

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
    def __setupServiceAccount(self):
        self.debug("__setupServiceAccount()")
        if None == self.service_account: 
            self.service_account = gspread.service_account()
        return self.service_account


    # setup the sheet object if not setup, return it either way
    def __setupSpreadsheet(self, use_cache = True):
        self.debug("__setupSpreadsheet(%s)" % str(use_cache))

        if None == self.spreadsheet or False == use_cache:
            self.spreadsheet = self.service_account.open_by_key(self.spreadsheetId)

        return self.spreadsheet


    # scrub out the worksheets we don't care about based on the pattern
    # pattern: sheets we care about include "inventory" in the title
    def __setupWorksheetList(self) -> list:
        self.debug("setupWorksheetList()")

        # retrieve the worksheets from the gpsread spreadsheet obj
        worksheetList = self.spreadsheet.worksheets()

        keeperPattern = self.getWorksheetKeeperPattern()

        # clear out the worksheets we don't need
        for sheet in worksheetList:
            # only restrict the worksheet list if there is a keeper pattern
            if None == keeperPattern or keeperPattern in sheet.title:
                self.__appendWorksheetTitle(sheet.title)
                self.__setWorksheetObj(worksheetTitle=sheet.title, worksheetObj=sheet)

        return self.getWorksheets()

    # Allow passing in the correct object type to storage
    def __setWorksheetObj(self, worksheetTitle, worksheetObj):
        self.debug("__setWorksheetObj(worksheetTitle={},worksheetObj={})", (worksheetTitle, worksheetObj))
        
        tempObj = self.__getWorksheetObjs().get(worksheetTitle)
        
        typeOfWorksheet = worksheetObj.__class__.__name__

        if None == tempObj:
            tempObj = {typeOfWorksheet: worksheetObj}
        else:
            tempObj[typeOfWorksheet] = worksheetObj

        self._worksheet_objs[worksheetTitle] = tempObj


    def __getWorksheetObjs(self):
        self.debug("__getWorksheetObjs()")
        return self._worksheet_objs


    def __getWorksheetStorage(self, worksheetTitle):
        self.debug("__getworksheetStorage(worksheetTitle={})".format(worksheetTitle))
        allworksheets = self.__getWorksheetObjs()
        return allworksheets.get(worksheetTitle)        


    def __getWorksheetObj(self, worksheetTitle, worksheetClassName):
        self.debug("__getWorksheetObj(worksheetTitle={},className={})",(worksheetTitle,worksheetClassName))

        worksheetStorage = self.__getWorksheetStorage(worksheetTitle)
        if None == worksheetStorage:
            return None

        worksheetObj = worksheetStorage.get(worksheetClassName)
        if None == worksheetObj:
            return None

        return worksheetObj


    def __appendWorksheetTitle(self, worksheetTitle):
        self.debug("__appendWorksheetTitle({})".format(worksheetTitle))
        self.worksheet_list.append(worksheetTitle)


    # quick getter for the worksheet list
    def getWorksheets(self) -> list:
        self.debug("getWorksheets()")
        return self.worksheet_list


    def getWorksheet(self, worksheetTitle):
        self.debug("getWorksheet(worksheetName={})".format(worksheetTitle))
        if [] == self.worksheet_list:
            raise Exception("Worksheets were not added to the Spreadsheet properly.")
        return self.__setupWorksheet(worksheetTitle)


    def getWorksheetClassName(self):
        self.debug("getWorksheetClassName()")
        if None == self.worksheetClassName:
            self.worksheetClassName = self.worksheet_class.split(".").pop()
        return self.worksheetClassName


    def getWorksheetClass(self):
        self.debug("getWorksheetClass()")
        return self.importClass(self.worksheet_class)


    # Check if this class' worksheetObj is setup in our storage, if it isn't - instantiate it and store it
    #      Will use the other object that is setup, which is the one from gspread
    #       We do this without hardcoding the gspread classname in, so that we never need to know it
    def __setupWorksheet(self, worksheetTitle):
        self.debug("__setupWorksheet(worksheetObj={})".format(worksheetTitle))
        
        # if it's not setup, then set it up
        worksheetClassName = self.getWorksheetClassName()

        worksheetObj = self.__getWorksheetObj(worksheetTitle, worksheetClassName)
                
        # if it's not setup, go ahead and do that
        if None == worksheetObj:
            worksheetClass = self.getWorksheetClass()
            worksheetStorage = self.__getWorksheetStorage(worksheetTitle)
            key = list(worksheetStorage.keys())[0]
            worksheetObjToPass = worksheetStorage[key]
            self.__setWorksheetObj(worksheetTitle=worksheetTitle, worksheetObj=worksheetClass(worksheetObjToPass))
        
        # return the object that we want to workwith
        return self.__getWorksheetObj(worksheetTitle=worksheetTitle, worksheetClassName=worksheetClassName)


    # only checks the columns, doesn't do anything to adjust or fix them
    # colsToCheck allows you to pass in something new to check against, rather than whatever is in cols_expected
    # checkExtras will allow you to bypass checking against the cols_expected_extra columns
    def checkWorksheetColumns(self, colsToCheck = None, checkExtras = True, addMissingColumns = False):
        self.debug("checkWorksheetColumns(colsToCheck={},checkExtras={},addMissingColumns={})".format(colsToCheck,checkExtras,addMissingColumns))
        # if nothing was passed through, then use the default. Otherwise, use what was passed

        for worksheetTitle in self.getWorksheets():
            worksheet = self.getWorksheet(worksheetTitle)

            worksheet.playground()

            sys.exit()

            #do this at the END of your processing, to make sure the data gets stored in the worksheet properly
            # up to this point, everything is just done in the copy of the worksheet
            # this helps keep the number of API calls to a minimum, so we don't get in trouble
            worksheet.commit()

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