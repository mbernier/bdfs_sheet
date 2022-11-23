import gspread
from modules.base import BaseClass

# @todo the spreadsheet ID should be given by the extending class
#   If this class is called directly, then it should error out because it should never have a
#   spreadsheet ID.

class Worksheet(BaseClass):
    worksheetObj = None
    expectedCols = []
    first_row = []
    numCols = None
    title = None
    missing_columns = []

    def __init__(self, worksheetObj):
        super(Worksheet, self).__init__()
        self.debug("Worksheet init() for worksheet: " + str(worksheetObj.title))
        self.worksheetObj = worksheetObj
        self.first_row = worksheetObj.row_values[1]
        self.numCols = len(self.first_row)
        self.title = worksheetObj,title
        self.info("The row is %i cols long" % self.numCols)

    def checkColumns(self, cols_expected, cols_expected_extra):
        self.debug("Workheet.checkColumns()")

        # What columns do we need to care about?
        colsToCheck = self.expectedCols()

        #
        # The following is actually checking the columns
        #

        # does the first_row contain everything in the colsToCheck
        firstrow_result = self.compareLists(self.first_row, colsToCheck)

        if firstrow_result:
            self.info("The worksheet %s has all the columns we expect" % worksheet.title)
        else: 
            self.info("The worksheet %s does not have all the columns we expect" % worksheet.title)
            #figure out what's missing and complain so that we can get that shit fixed
            self.missing_columns = list(set(colsToCheck) - set(self.first_row))
            self.console("Worksheet: {} is missing these columns: ".format(self.title), data=str(self.missing_columns))


            if True == addMissingColumns:
                worksheet.update_cell(1, 2, 'Bingo!')
                # self.addColumnsToWorkSheet(worksheet, missing_columns)
        sys.exit()


    def expectedCols(self, cols_expected, cols_expected_extra):
        # set the columns to the default
        self.expectedCols = cols_expected

        # if we are checking extras and we have extra cols to check, then let's loop through. Otherwise, just do the normal thing
        if True == checkExtras and [] != cols_expected_extra:

            # if we have extra columns that we need to check, loop through the options
            for extraColCheck, colTitles in cols_expected_extra.items():

                # if we find that the key for the extra columns is in the worksheet title, 
                # then append the extras columns to check and then check against the new combined list
                if extraColCheck in worksheet.title:
                     self.expectedCols += cols_expected_extra[extraColCheck]

        return self.expectedCols


    def addColumns(self):
