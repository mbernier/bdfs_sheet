import gspread, sys
from modules.base import BaseClass

# @todo the spreadsheet ID should be given by the extending class
#   If this class is called directly, then it should error out because it should never have a
#   spreadsheet ID.

['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
'__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
'__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
'__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_add_dimension_group', '_auto_resize', 
'_delete_dimension_group', '_finder', '_get_sheet_property', '_hide_dimension', '_list_cells', 
'_properties', '_set_hidden_flag', '_unhide_dimension', 'acell', 'add_cols', 'add_dimension_group_columns', 
'add_dimension_group_rows', 'add_protected_range', 'add_rows', 'append_row', 'append_rows', 'batch_clear', 
'batch_format', 'batch_get', 'batch_update', 'cell', 'clear', 'clear_basic_filter', 'clear_note', 'client', 
'col_count', 'col_values', 'columns_auto_resize', 'copy_range', 'copy_to', 'cut_range', 'define_named_range', 
'delete_columns', 'delete_dimension', 'delete_dimension_group_columns', 'delete_dimension_group_rows', 
'delete_named_range', 'delete_protected_range', 'delete_row', 'delete_rows', 'duplicate', 'export', 'find', 
'findall', 'format', 'freeze', 'frozen_col_count', 'frozen_row_count', 'get', 'get_all_cells', 'get_all_records', 
'get_all_values', 'get_note', 'get_values', 'hide', 'hide_columns', 'hide_rows', 'id', 'index', 'insert_cols', 
'insert_note', 'insert_row', 'insert_rows', 'isSheetHidden', 'list_dimension_group_columns', 'list_dimension_group_rows', 
'merge_cells', 'range', 'resize', 'row_count', 'row_values', 'rows_auto_resize', 'set_basic_filter', 'show', 'sort', 
'spreadsheet', 'tab_color', 'title', 'unhide_columns', 'unhide_rows', 'unmerge_cells', 'update', 'update_acell', 
'update_cell', 'update_cells', 'update_index', 'update_note', 'update_tab_color', 'update_title', 'updated', 'url']


class Worksheet(BaseClass):
    _worksheetObj = None
    _expectedColumns = []
    _columns = []
    _column_count = None
    _title = None
    _missing_columns = []

    def __init__(self, worksheetObj):
        super(Worksheet, self).__init__()
        self.debug("Worksheet init() for worksheet: " + str(worksheetObj.title))
        
        self.__setWorksheetObj(worksheetObj)

        # will get the column list from the first row of the worksheet, also updates the column count
        self.__updateColumnListFromWorksheet()
        
        self.setTitle(worksheetObj.title)
        
        self.info("The row is %i cols long" % self.getColumnCount())


    # set first_row to the names of the columns in the worksheet and update the column count
    def __updateColumnListFromWorksheet(self):
        self.debug("Worksheet.__updateColumnListFromWorksheet()")
        self._columns = self.getColumns(False)
        self.__updateColumnCount()


    # this should ONLY be done when you are modifying columns and you know that you don't need to pull again from the spreadsheet
    #   e.g. removeEmptyColumns() is using this bc we have just audited and removed all empty columns, leaving only the remaining columns
    #       that have a name in them
    def __setColumnList(self, listOfColumns):
        self.debug("Worksheet.__setColumnList({})".format(listOfColumns))
        self._columns = listOfColumns
        self.__updateColumnCount()


    # allows updating the cache of the column titles without pulling from the worksheet again
    def __addToColumnList(self, columnTitle:str):
        self.debug("Worksheet.__addToColumnList({})".format(columnTitle))
        self._columns.append(columnTitle)
        self.__updateColumnCount()
        return self.getColumns()


    # count the nubmer of columns in the first_row
    # this should never be called except where we are updating the columns themselves
    def __updateColumnCount(self):
        self.debug("Worksheet.__updateColumnCount()")
        self._column_count = len(self.getColumns())
        return self.getColumnCount()

    # method to double check that our cache and the worksheet are the same
    def testColumnCacheAgainstWorksheet(self):
        self.debug("Worksheet.__testColumnCacheAgainstWorksheet()")
        if self.compareLists(self.getColumns(use_cache=True), self.getColumns(use_cache=False)):
            self.info("The column list and the worksheet are the same!")
            return True 
        else:
            self.error("The column list and the worksheet are NOT the same!")
            return False

    # getter for the param worksheetObj
    def __getWorksheetObj(self):
        return self._worksheetObj

    def __setWorksheetObj(self, worksheetObj):
        self._worksheetObj = worksheetObj
        return self.__getWorksheetObj()

    # The only place to retrieve the first row of data from the sheet
    # use_cache = True will return the cache, if False it gets data from the live worksheet
    #   if there are empty columns at the end, the row_values() method will not get them, it will get everything from
    #       the first column to the last value in the row
    def getColumns(self, use_cache = True):
        self.debug("Worksheet.getColumns({})".format(use_cache))
        if use_cache:
            return self._columns
        else:
            return self.__getWorksheetObj().row_values(1)


    # return the numCols value
    def getColumnCount(self):
        self.debug("Worksheet.getColumnCount()")
        return self._column_count


    def getTitle(self):
        self.debug("Worksheet.getTitle()")
        return self._title


    def setTitle(self, title):
        self.debug("Worksheet.setTitle({})".format(title))
        self._title = title
        return self.getTitle()


    def getMissingColumns(self):
        self.debug("Worksheet.getMissingColumns()")
        return self._missing_columns


    def setMissingColumns(self, columns):
        self.debug("Worksheet.setMissingColumns({})".format(columns))
        self._missing_columns = columns
        return self.getMissingColumns()

    def setExpectedColumns(self, columns):
        self.debug("Worksheet.setExpectedColumns({})".format(columns))
        self._expectedColumns = columns
        return self.getExpectedColumns()

    def getExpectedColumns(self):
        self.debug("Worksheet.getExpectedColumns()")
        return self._expectedColumns

    # This one was fun, in order to reduce the number of API calls that we need to make, we want to remove empty columns from the spreadsheets
    #   In order to do this, we have to walk forward through the columns and the the sheet to find empty columns
    #   Then, figure out what the ranges of the empty columns are, so we can hold them
    #   Once we know all the ranges, work the list backwards...
    #   If you don't work the list backwards, you will delete the columns then the ranges don't match the sheet or array
    #   This means you delete data.
    #   e.g [1:a,2:b,3:"",4:"",5:c,6:d,7:"",8:e,9:f,10:g]
    #       if you delete 3->4, your array looks like this, which is fine bc the indeces are correct:
    #       [1:a,2:b,5:c,6:d,7:"",8:e,9:f,10:g]
    #       but, your sheet looks like this:
    #       [1:a,2:b,3:c,4:d,5:"",6:e,7:f,8:g]
    #       so, when you go to delete 7, it either isn't there or now "f" is in the 7th spot, so if you pass [7:7]
    #           to the worksheet delete function, it will delete "f" instead of deleting the correct item
    def removeEmptyColumns(self):
        self.debug("Worksheet.removeEmptyColumns()")

        counter = 1
        delete_items = []

        # get the current known columns
        columns = self.getColumns()

        # start of the next range
        start = None

        # end of the range
        end = None

        # list of ranges to delete
        ranges = []

        # go through the columns we pulled and identify the index of any empties
        for column in columns:
            if column == "":
                # only do things if the column is empty
                if None == start:
                    # start is empty, so we are in the first pass through the loop
                    start = counter
                    end = counter
                    self.debug("Setting start to {}".format(counter))
                elif counter == end+1:
                    # if we are still in a range of empties, increase the range
                    end = counter
                    self.debug("Setting end to {}".format(counter))
                else:
                    # we reached another empty number, which means the previous range is completed
                    ranges.append({"start":start, "end": end})
                    start = counter
                    end = counter
                    self.debug("New item is {}".format(counter))
            
            # count which column we are on
            counter+= 1

        # only do this if we have actual range to delete
        if None != start and None != end:
            # add the last range that we saw to ranges array
            ranges.append({"start":start, "end": end})

        #are there empty columns after the known columns in the first row?
        currentSheetColsAvailable = self.__getWorksheetObj().col_count

        # I was deleting the empties off the end, but there was a race condition on the delete that would cause the next function
        #   to think that there were more columns than there actually were because the range delete for the end of the sheet was taking
        #   a while to run. So, we don't remove those anymore.
        #
        #
        # if the next column is larger than currentSheetColsAvailable, then we are at the end of the sheet
        #   so we don't need to delete anything
        # if len(columns)+1 < currentSheetColsAvailable: 
        #     # go ahead and trim everything off the end too, just for funsies
        #     ranges.append({"start":len(columns)+1, "end": currentSheetColsAvailable})

        # go backwards throug the ranges, so that we don't invalidate the ranges (see comments before method)
        while len(ranges) > 0:
            rangeToKill = ranges.pop()

            self.info("Removing item from {}:{} from columns".format(rangeToKill["start"], rangeToKill["end"]))
            del columns[rangeToKill["start"]:rangeToKill["end"]]

            self.info("Removing item from {}:{} from worksheet".format(rangeToKill["start"], rangeToKill["end"]))
            self.__getWorksheetObj().delete_columns(rangeToKill["start"], rangeToKill["end"])

        # make sure to update the columns in this object, so we have the correct current list
        self.__setColumnList(columns)


    # Check that the columns in the worksheet match what is expected
    # addMissingColumns will cause anything that is missing to be added to the spreadsheet
    def checkColumns(self, cols_expected, cols_expected_extra):
        self.debug("Workheet.checkColumns({},{})".format(cols_expected, cols_expected_extra))

        # What columns do we need to care about?
        colsToCheck = self.calculateExpectedColumns(cols_expected, cols_expected_extra)

        #
        # The following is actually checking the columns
        #

        # does the first_row contain everything in the colsToCheck
        firstrow_result = self.compareLists(self.getColumns(), colsToCheck)

        if firstrow_result:
            self.info("The worksheet %s has all the columns we expect" % self.getTitle())
        else: 
            self.info("The worksheet %s does not have all the columns we expect" % self.getTitle())
            #figure out what's missing and complain so that we can get that shit fixed
            missing_columns = list(set(colsToCheck) - set(self.getColumns()))
            self.setMissingColumns(missing_columns)
            self.console("Worksheet: {} is missing these columns: ".format(self.getTitle()), data=str(self.getMissingColumns()))


    # Create a list of columns that we are expecting to find in this worksheet
    # @return the list of expected columns
    def calculateExpectedColumns(self, cols_expected: list, cols_expected_extra: dict, checkExtras: bool = True):
        self.debug("Worksheet.calculateExpectedColumns({},{}, {})".format(cols_expected, cols_expected_extra, checkExtras))
        # set the columns to the default
        expectedCols = cols_expected

        # if we are checking extras and we have extra cols to check, then let's loop through. Otherwise, just do the normal thing
        if True == checkExtras and [] != cols_expected_extra:

            # if we have extra columns that we need to check, loop through the options in the expected list and see if there are matches
            for extraColCheck, colTitles in cols_expected_extra.items():

                # if we find that the key for the extra columns is in the worksheet title, 
                # then append the extras columns to check and then check against the new combined list
                if extraColCheck in self.getTitle():
                     expectedCols += cols_expected_extra[extraColCheck]
        
        return self.setExpectedColumns(expectedCols)


    # Go through the missing columns and add them to the worksheet at the end of the worksheet

#  Consider pulling all the data from the worksheet, modifying this locally, then replacing it back into the sheet
#   Getting All Values From a Worksheet as a List of Lists
#   list_of_lists = worksheet.get_all_values()
# 
#   Getting All Values From a Worksheet as a List of Dictionaries
#   list_of_dicts = worksheet.get_all_records()
# 
#   order of ops:
#       pull everything
#       worksheet.clear()
#       replace the sheet with a placeholder text to say "under construction"
#       Do the data manipulation to sort the data to match "expected cols" order
#       drop the data back in with self.__getWorksheetObj().batch_update(batch_update)
# 
#   to test: 
#       pull everything
#       clear: worksheet.clear()
#       write everything
#       see what happens
#
#   https://docs.gspread.org/en/latest/user-guide.html#getting-all-values-from-a-worksheet-as-a-list-of-lists

    def addMissingColumns(self):
        self.debug("Worksheet.addMissingColumns()")

        self.debug("Attempting to add these columns: {}".format(self.getMissingColumns()))

        missingColumnCount = len(self.getMissingColumns())
        self.debug("missingColumnCount: {}".format(missingColumnCount))

        # if there are no missing columns, do nothing!
        if 0 != missingColumnCount: 

            currentSheetColsAvailable = self.__getWorksheetObj().col_count
            self.debug("currentSheetColsAvailable: {}".format(currentSheetColsAvailable))

            expectedColumnCount = len(self.getExpectedColumns())
            self.debug("expectedColumnCount: {}".format(expectedColumnCount))

            str_list = list(filter(None, self.getColumns()))
            self.debug("current count: {}".format(len(str_list)))

            nextColumnIndex = self.getColumnCount()+1
            totalColumnsNeeded = 0
            # add more columns to the current worksheet to make sure we can keep adding columns
            if (nextColumnIndex + missingColumnCount) > int(currentSheetColsAvailable):
                totalColumnsNeeded= nextColumnIndex + missingColumnCount - int(currentSheetColsAvailable)
                self.debug("Adding {} empty columns".format(totalColumnsNeeded))
                # to be careful, add enough columns to handle all the missing columns
                self.__getWorksheetObj().add_cols(totalColumnsNeeded)
            
            startCell = self.__getWorksheetObj().cell(1, nextColumnIndex)
            endCell = self.__getWorksheetObj().cell(1, self.getColumnCount()+1 + missingColumnCount)
            rangeToUpdate = "{}:{}".format(startCell.address, endCell.address)

            batch_update = [{
                'range': rangeToUpdate,
                'values': [self.getMissingColumns()],
            }]

            self.console(batch_update)

            # do a batch update, because doing this one column at a time hit the rate limits super fast
            self.__getWorksheetObj().batch_update(batch_update)

        return self.getColumns()


    # actually create a new column in the worksheet, if columnNumber is included it will create the column 
    def addColumn(self, columnName: str = ""):
        self.debug("Worksheet.addColumn({})".format(columnName))

        # we want to add a column at the next open position after the current columns, so grab the current column list length
        newColumnNumber = self.getColumnCount() + 1

        self.info("Adding a column to position [1,{}] with title {}".format(newColumnNumber, columnName))

        # add the column name in the new column, row 1 
        response = self.__getWorksheetObj().update_cell(1, newColumnNumber, columnName)

        self.info("Response from the update_cell call: {}".format(response))

        # internal call to update our cache without pulling it from the worksheet, will also update the column count
        self.__addToColumnList(columnName)

        return self.getColumns()