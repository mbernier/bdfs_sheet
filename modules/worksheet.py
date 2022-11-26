import gspread, sys

# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import utils as gspread_utils

from modules.base import BaseClass
from collections import OrderedDict
from pprint import pprint 

from modules.worksheets.data import WorksheetData

# @todo the spreadsheet ID should be given by the extending class
#   If this class is called directly, then it should error out because it should never have a
#   spreadsheet ID.

# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
# '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
# '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
# '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_add_dimension_group', '_auto_resize', 
# '_delete_dimension_group', '_finder', '_get_sheet_property', '_hide_dimension', '_list_cells', 
# '_properties', '_set_hidden_flag', '_unhide_dimension', 'acell', 'add_cols', 'add_dimension_group_columns', 
# 'add_dimension_group_rows', 'add_protected_range', 'add_rows', 'append_row', 'append_rows', 'batch_clear', 
# 'batch_format', 'batch_get', 'batch_update', 'cell', 'clear', 'clear_basic_filter', 'clear_note', 'client', 
# 'col_count', 'col_values', 'columns_auto_resize', 'copy_range', 'copy_to', 'cut_range', 'define_named_range', 
# 'delete_columns', 'delete_dimension', 'delete_dimension_group_columns', 'delete_dimension_group_rows', 
# 'delete_named_range', 'delete_protected_range', 'delete_row', 'delete_rows', 'duplicate', 'export', 'find', 
# 'findall', 'format', 'freeze', 'frozen_col_count', 'frozen_row_count', 'get', 'get_all_cells', 'get_all_records', 
# 'get_all_values', 'get_note', 'get_values', 'hide', 'hide_columns', 'hide_rows', 'id', 'index', 'insert_cols', 
# 'insert_note', 'insert_row', 'insert_rows', 'isSheetHidden', 'list_dimension_group_columns', 'list_dimension_group_rows', 
# 'merge_cells', 'range', 'resize', 'row_count', 'row_values', 'rows_auto_resize', 'set_basic_filter', 'show', 'sort', 
# 'spreadsheet', 'tab_color', 'title', 'unhide_columns', 'unhide_rows', 'unmerge_cells', 'update', 'update_acell', 
# 'update_cell', 'update_cells', 'update_index', 'update_note', 'update_tab_color', 'update_title', 'updated', 'url']

#
# Rules; 
#   pulls the worksheet data, does all the changes, only pushes changes when commit() is called.
#
class Worksheet(BaseClass):

    logger_name = "Worksheet"

    _worksheetObj = None            # The worksheet object itself, allows us to run gspread functions
    _expectedColumns: list = []           # A list of columns we expect to have in the sheet
    _title = None                   # The Sheet title

    def __init__(self, worksheetObj):

        self.debug("__init()__ for worksheet: " + str(worksheetObj.title))

        # store the worksheetObj for use later
        self.__setWorksheetObj(worksheetObj)

        # double check we have the required params from the extension class
        self.__checkSetup()

        # source of truth for the data of the worksheet
        self._sheetData = []

        self._setSheetData()



    def __checkSetup(self):
        # if we don't know what cols are expected, we cannot check the sheet is setup properly
        if [] == self.getExpectedColumns():
            #fail if no one set the spreadsheetId on the wrapper class
            self.critical("Cols expected was not set before instantiating Spreadsheet class")
            raise Exception("cols_expected parameter is not set")



    ####
    #
    # Worksheet connection Methods
    #
    ####

    # getter for the param worksheetObj
    def __getWorksheetObj(self):
        self.debug("__getWorksheetObj")
        return self._worksheetObj

    def __setWorksheetObj(self, worksheetObj):
        self.debug("__setWorksheetObj(worksheetObj={})".format(worksheetObj))
        self._worksheetObj = worksheetObj
        return self.__getWorksheetObj()

    ####
    #
    # Sheet functionality
    #
    ####
    # 'id', 
    # 'index', 
    # 'export', 
    # 'isSheetHidden', 
    # 'spreadsheet', 
    # 'title', 
    # 'url'
    # 'update_index', 
    # 'update_title', 
    def getTitle(self):
        self.debug("getTitle()")
        self._title = self.__getWorksheetObj().title


    def setTitle(self, title):
        self.debug("setTitle(title={})".format(title))
        self._title = title
        return self.getTitle()


    ####
    #
    # Read Data from the sheet Methods
    #
    ####
    # 'get_all_records', 
    # 'get_all_values', 
    # 'batch_get', 
    # 'get', 
    # 'get_values', 

    # Gets everything from the sheet, without being a List of dicts
    # @todo are we using this? it should be moved to use workSheetData
    def getAllValues(self):
        self.debug("getAllValues()")
        records = self.__getWorksheetObj().get_all_values()
        return records


    # gets evertyhing as a list of dicts
    # @todo are we using this? it should be moved to use workSheetData
    def getAllRecords(self):
        self.debug("getAllRecords()")
        records = self.__getWorksheetObj().get_all_records()
        return records

    #will return something like -- "A1:CT356"
    def getDataRange(self):
        self.debug("getDataRange()")
        sheetData = self.__getSheetData()
        return sheetData.getRange()

    ####
    #
    # Write Data to the Sheet
    #
    ####, 
    # 'batch_update',
    # 'update', 
    # 'update_acell', 
    # 'update_cell', 
    # 'update_cells', 
    # 'update_note', 
    # 'updated',  

    # write the data out to the google worksheet
    def commit(self):
        self.debug("commit()")

        dataRange = self.getDataRange()
        sheetData = self.__getSheetData()

        values = sheetData.getData()

        batch_update = [{
            'range': dataRange,
            'values': values,
        }]

        self.debug("Updating the spreadsheet with this data: ", batch_update)

        worksheet = self.__getWorksheetObj()

        # if the title is changed, push it
        if self.getTitle() != worksheet.title:
            worksheet.update_title(self.getTitle())
        
        # do a batch update, because doing this one column at a time hit the rate limits super fast
        worksheet.batch_update(batch_update)


    ####
    #
    # Delete Data From the Sheet
    #
    ####
    # 'clear', 
    # 'batch_clear', 

    # clears out all the data from the spreadsheet
    #   Most of the time the workflow here is to clear your sheet, so you can write the worksheet data to it
    #   consider carefully what could go wrong if you don't have data in the worksheet and you do not commit
    #   the worksheetData object's data to the sheet. That's dangerous!
    def clearAllRecords(self, deleteWorksheetData = False):
        self.debug("clearAllRecords()")
        self.__getWorksheetObj().clear()
        # This is DANGEROUS, bc you can lose ALL of your data
        if deleteWorkSheetData:
            self._sheetData = WorksheetData()




    ####
    #
    # Data Cache - Create
    #
    ####

    # if we mess with _sheetData, then we need to update headersList, HeadersFlatCache
    def _setSheetData(self):
        self.debug("_setSheetData()")
        self._sheetData = WorksheetData(self.getAllValues())

    def getData(self):
        self.debug("getData()")
        return self._sheetData




    #####
    #
    # Column Methods
    #
    #####
    # 'add_cols', 
    # 'add_dimension_group_columns', 
    # 'col_count', 
    # 'col_values', 
    # 'delete_columns', 
    # 'frozen_col_count', 
    # 'hide_columns', 
    # 'insert_cols', 
    # 'unhide_columns', 
    # 'list_dimension_group_columns', 
    # 'columns_auto_resize', 
    # 'sort'


    def getExpectedColumns(self):
        self.debug("getExpectedColumns()")
        return self.__mergeExpectedColumns()


    # since we have multiple options for how the columns should be setup
    #   Get the columns that we care about and return them
    def __mergeExpectedColumns(self):
        self.debug("__mergeExpectedColumns()")
        expectedCols = self.cols_expected
        for index in self.cols_expected_extra:
            if index in self.getTitle():
                expectedCols.extend(self.cols_expected_extra[index])
        return expectedCols


    # The only place to retrieve the first row of data from the sheet
    # use_cache = True will return the cache, if False it gets data from the live worksheet
    #   if there are empty columns at the end, the row_values() method will not get them, it will get everything from
    #       the first column to the last value in the row
    def getColumns(self):
        self.debug("getColumns(use_cache={})".format(use_cache))
        return self.getData().getHeaders()
        

    # return the number of columns in the worksheet
    def getColumnCount(self):
        self.debug("getColumnCount()")
        return self.getData().width()

    def __getWorksheetColumnCount(self):
        self.debug("__getWorksheetColumnCount()")
        return self._worksheetObj.col_count


    def removeEmptyColumnsTrailing(self):
        self.debug("removeEmptyColumnsTrailing()")

        #we don't want to remove the last column in the data, we want the next column
        dataColumnCount = self.getColumnCount() + 1
        worksheetObjColumnCount = self.__getWorksheetColumnCount()

        if worksheetObjColumnCount > dataColumnCount:
            self.removeWorksheetColumns(start=dataColumnCount, end=worksheetObjColumnCount)
            

    def removeColumns(self, column=None, start=None, stop=None):
        self.debug("removeWorksheetColumns(column={},range={})", (column, range))
        if None != column:
            start = column
            end = column

        if None == start or None == end:
            raise Exception("You must provide a start and end range for removeWorkSheetColumns()")

        self.__removeColumns_Data(start, end)

    # def __removeColumns_Worksheet(self, start, end):
    #     self.debug("__removeWorksheetColumns(start={}, end={})", (start, end))
    #     startCell = self.getA1(1, start)
    #     endCell = self.getA1(1, end)
    #     self.__getWorksheetObj().delete_columns(startCell, endCell)

    def __removeColumns_Data(self, start, end):
        self.debug("__removeDataColumns(start={}, end={})", (start, end))
        self._sheetData.removeHeaders(start, end)


    def playground(self):
        self.info("# of columns in worksheet: {}".format(self.__getWorksheetColumnCount()))
        self.info("# of columns in dataStore: {}".format(self.getColumnCount()))
        self.removeEmptyColumnsTrailing()

        # @todo make sure that any data that gets updated in the data object have their "updated_date" field changed to time.now()



    
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
    def X_removeEmptyColumns(self, removeTrailingEmpties = False):
        self.debug("removeEmptyColumns(removeTrailingEmpties={})".format(removeTrailingEmpties))

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

        if removeTrailingEmpties:
            self.debug("We have permission to remove the trailing empty columns")
            # I was deleting the empties off the end, but there was a race condition on the delete that would cause the next function
            #   to think that there were more columns than there actually were because the range delete for the end of the sheet was taking
            #   a while to run. So, we don't remove those anymore.
            #
            # if the next column is larger than currentSheetColsAvailable, then we are at the end of the sheet
            #   so we don't need to delete anything
            if len(columns)+1 < currentSheetColsAvailable: 
                # go ahead and trim everything off the end too, just for funsies
                ranges.append({"start":len(columns)+1, "end": currentSheetColsAvailable})

        # if we do a removal, return that we did
        didWeRemoveRanges = False

        # go backwards throug the ranges, so that we don't invalidate the ranges (see comments before method)
        while len(ranges) > 0:
            rangeToKill = ranges.pop()

            self.info("Removing item from {}:{} from columns".format(rangeToKill["start"], rangeToKill["end"]))
            del columns[rangeToKill["start"]:rangeToKill["end"]]

            self.info("Removing item from {}:{} from worksheet".format(
                    self.getA1(1, rangeToKill["start"]), 
                    self.getA1(1, rangeToKill["end"])))
            self.__getWorksheetObj().delete_columns(rangeToKill["start"], rangeToKill["end"])
            didWeRemoveRanges = True

        # make sure to update the columns in this object, so we have the correct current list
        self.__setColumnList(columns)

        # return true if we did some cleanup
        return didWeRemoveRanges



    # Check that the columns in the worksheet match what is expected
    # addMissingColumns will cause anything that is missing to be added to the spreadsheet

    # # 
    # # Original info, assumed the sheet was source of truth, needs to be converted to object as source of truth
    # #             

    # worksheet.checkColumns(self.getExpectedColumns(), self.getExtraExpectedColumns())
    # if addMissingColumns:
    #     # remove the empty columns
    #     # clean up the empties so that we have a good measure of the sheet
    #     worksheet.removeEmptyColumns()

    #     # add in the new columns, so that we have everything we need
    #     addedColumns = worksheet.addMissingColumns()

    #     self.info("{} columns were added to {}".format(addedColumns, worksheet.getTitle()))

    #     # double check that we don't have extra empties at the end of the sheet, just in case
    #     worksheet.removeEmptyColumns(removeTrailingEmpties=True)

    #     # since we can't control how the data gets added in previous steps or how it was in the original sheet, 
    #     #   make sure it is clean here. By default, this stores to the worksheet when it's done running. To cancel that
    #     #   add storeToWorksheet = False
    #     sheetData = worksheet.sortTheColumns()
    # self.console("We are only running one worksheet right now, see Spreadhsheet.py line 188")


    def X_checkColumns(self, cols_expected, cols_expected_extra):
        self.debug("Workheet.checkColumns(cols_expected={},cols_expected_extra={})".format(cols_expected, cols_expected_extra))

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
    def X_calculateExpectedColumns(self, cols_expected: list, cols_expected_extra: dict, checkExtras: bool = True):
        self.debug("calculateExpectedColumns(cols_expected={},cols_expected_extra={}, checkExtras={})".format(cols_expected, cols_expected_extra, checkExtras))
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

    def X_addMissingColumns(self):
        self.debug("addMissingColumns()")

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

            # push the data over the API
            self.batch_update(rangeToUpdate, [self.getMissingColumns()])
            
            self.setMissingColumns([])

        return missingColumnCount


    # # actually create a new column in the worksheet, if columnNumber is included it will create the column 
    # def addColumn(self, columnName: str = ""):
    #     self.debug("addColumn({})".format(columnName))

    #     # we want to add a column at the next open position after the current columns, so grab the current column list length
    #     newColumnNumber = self.getColumnCount() + 1

    #     self.info("Adding a column to position [1,{}] with title {}".format(newColumnNumber, columnName))

    #     # add the column name in the new column, row 1 
    #     response = self.__getWorksheetObj().update_cell(1, newColumnNumber, columnName)

    #     self.info("Response from the update_cell call: {}".format(response))

    #     # internal call to update our cache without pulling it from the worksheet, will also update the column count
    #     self.__addToColumnList(columnName)

    #     return self.getColumns()

    # make sure the columns are in the order we want for human readability
    #   you can write it to the worksheet if you would like, or not with storeToWorkSheet = True/False
    #   @returns the ordered list or a list of orderedDicts for use in other methods
    def X_sortTheColumns(self, cols_to_keep, data, storeToWorksheet = True, returnAsOrderedDicts = False):
        self.debug(
            "Worksheet.sortTheColumns(cols_to_keep={}, data={}, storeToWorksheet={},returnAsOrderedDicts={})"
                .format(
                    cols_to_keep,
                    data,
                    storeToWorksheet, 
                    returnAsOrderedDicts))

        #seed the list with the columns as the first row
        output_list = [cols_to_keep]

        # here if we need it, if returnAsOrderedDicts is True
        ordered_dicts = []

        # go through all the data and get it in the right order
        for data_row in data:
            # lists are ordered, so if we pull the data from the data_from_sheet in the right order and add it to our list
            #   then we have the data in the right order
            temp_list = []

            #setting up the variable, in case we need to use it
            temp_ordered_dict = None

            # if we need the ordered Dict, set it up
            if returnAsOrderedDicts:
                temp_ordered_dict = OrderedDict()

            #use cols_expected as the order we care about, add to the temp_list in the right order 
            for key in cols_to_keep:

                temp_list.append(data_row[key])

                if returnAsOrderedDicts:
                    temp_ordered_dict[key] = data_row[key]

            # add the temp_list to our output in row order
            output_list.append(temp_list)

        # calculate the A1 Notation of the range from A1 -> the height and width of our new List
        end_cell = gself.getA1(len(output_list),len(temp_list))

        self.debug("The output_list data is {}".format(output_list))

        if storeToWorksheet:
            #remove all the stuff in the sheet that's there right now
            self.clearAllRecords()

            #push the data to the spreadsheet
            self.batch_update("A1:{}".format(end_cell), output_list)

        #only return this if it's asked for
        if returnAsOrderedDicts:
            return ordered_dicts

        #by default we return the list object
        return output_list

    def X_removeAllButExpectedColumns(self, storeToWorksheet=True, returnAsOrderedDicts = False):
        self.debug("removeAllButExpectedColumns()")
        cols_expected = self.getExpectedColumns()
        self.sortTheColumns(cols_to_keep=cols_expected, storeToWorksheet=storeToWorksheet, returnAsOrderedDicts=returnAsOrderedDicts)





    ####
    #
    # Row Methods
    #
    ####
    # 'add_dimension_group_rows', 
    # 'add_rows', 
    # 'append_row', 
    # 'append_rows', 
    # 'delete_dimension_group_rows', 
    # 'delete_row', 
    # 'delete_rows', 
    # 'frozen_row_count', 
    # 'hide_rows', 
    # 'insert_row', 
    # 'insert_rows', 
    # 'row_count', 
    # 'row_values', 
    # 'rows_auto_resize', 
    # 'unhide_rows', 


    def getRowCount(self):
        self.debug("getRowCount()")
        return self.getData().height()


    ####
    #
    # Cell Methods
    #
    ####
    # 'acell'
    # 'cell',
    # 'get_all_cells', 
    # 'merge_cells', 
    # 'unmerge_cells',

    # creates A1 notation for the row and column given
    def getA1(self, row, column):
        self.debug("getA1(row={}, col={})", (row, col))
        return gspread_utils.rowcol_to_a1(row, col)



    ####
    #
    # Filters
    #
    ####
    # 'clear_basic_filter', 
    # 'set_basic_filter',

    ####
    #
    # Ranges
    #
    ####
    # 'client', 
    # 'copy_range', 
    # 'cut_range', 
    # 'define_named_range', 
    # 'delete_named_range', 
    # 'delete_protected_range', 
    # 'add_protected_range', 
     # 'range', 


    ####
    #
    # Notes
    #
    ####
    # 'clear_note', 
    # 'get_note', 
    # 'insert_note', 

    ####
    #
    # Copy
    #
    ####
    # 'copy_to', 
    # 'duplicate', 

    ####
    #
    # Dimensions
    #
    ####
    # 'delete_dimension', 
    # 'delete_dimension_group_columns', 
    # 'list_dimension_group_rows', 

    ####
    #
    # Search the data
    #
    ####
    # 'find', 
    # 'findall', 

    ####
    #
    # Style methods
    #
    ####
    # 'batch_format'
    # 'update_tab_color', 
    # 'tab_color', 
    # 'format', 
    # 'resize',


    ####
    #
    # Data visibility
    #
    ####
    # 'freeze', 
    # 'hide', 
    # 'show',