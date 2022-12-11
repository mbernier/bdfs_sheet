import sys, gspread
from modules.spreadsheets.bdfs_test import BdfsInventory_Test_Spreadsheet

worksheetName = "test_easy_data"
copyFromWorksheetName = "demo_worksheet"


####
#
# Setup the sheet for testing, creates these spreadsheets out of the scope of the Bdfs functionality
#   so when this is run, you have to re-setup Bdfs_Spreadsheet otherwise, it doens't know about the 
#   new sheets
#
####
print("running setup")
sheet = BdfsInventory_Test_Spreadsheet()
spreadsheet = sheet.setupSpreadsheet()

# see if the sheetName 
try:
    testWorksheetExists = spreadsheet.worksheet(worksheetName)
    print(f"Worksheet: {worksheetName} found, deleting it")
    spreadsheet.del_worksheet(testWorksheetExists)
except gspread.exceptions.WorksheetNotFound:
    print(f"Worksheet: {worksheetName} isn't found, creating it")

worksheet1 = spreadsheet.worksheet(copyFromWorksheetName)
worksheet2 = worksheet1.duplicate(1, None, worksheetName)

del sheet
del spreadsheet
del worksheet1
del worksheet2



####
#
# Create a spreadsheet for the tests to run on
#
####
sheet = BdfsInventory_Test_Spreadsheet() 
test_worksheet = sheet.getWorksheet(worksheetName)


def test_getTitle():
    title = test_worksheet.getTitle()
    assert worksheetName == title

def test_setTitle():
    title = test_worksheet.getTitle()

    newTitle = "test_easy_data_new_title"

    test_worksheet.setTitle(newTitle)

    assert newTitle == test_worksheet.getTitle()
    assert title == test_worksheet.getOriginalTitle()


def test_getA1():
    assert "A1" == test_worksheet.getA1(1,1)
    assert "E5" == test_worksheet.getA1(5,5)


def test_getDataRange():
    dataRange = test_worksheet.getDataRange()
    assert dataRange == "A1:C3"


def test_getData():
    data = test_worksheet.getData()
    assert data.__class__.__name__ == "WorksheetData"
    #worksheet Data will be tested in tests/test_modules/worksheets/test_worksheetdata


def test_getExpectedColumns():
    cols = test_worksheet.getExpectedColumns()
    assert cols == ['Updated Date', 'Title', 'Hardware', 'Published', 'Type', 'On BDFS?', 'Vendor', 'Handle', 'Type', 'Glass', 'SKU', 'SEO Title', 'Tags', 'Sarto SKU', 'Color', 'UnitedPorte URL', 'Image 1 URL', 'Image 1 SEO', 'Image 2 URL', 'Image 2 SEO', 'Image 3 URL', 'Image 3 SEO', 'Image 4 URL', 'Image 4 SEO', 'Image 5 URL', 'Image 5 SEO', 'Description']

def test_getColumns():
    cols = test_worksheet.getColumns()
    assert cols == ['Name', 'Birthday', 'Email']

def test_gspread_worksheet_removeColumns():
    counts = test_worksheet.getColumnCounts()
    # assert counts['data'] == 3
    gspread_worksheet_column_count = counts['gspread_worksheet']
  

def test_getColumnCounts():
    counts = test_worksheet.getColumnCounts()
    # also tests the gspread_worksheet_resize_to_data, bc if the data width is the same we got it right
    # not setting to a specific number, bc we don't care what the width is, just that they are the same
    assert counts['data'] == counts['gspread_worksheet'] 



#     # wrapper function to take care of some pre-work on removing columns
#     @Debugger
#     @validate_arguments(start=['lt_param:stop'])
#     def removeColumns(self, column:int=None, start:int=None, stop:int=None):
#         if None != column:
#             start = column
#             end = column

#         if None == start or None == end:
#             raise Exception("You must provide a start and end range for removeColumns()")

#         self.__removeColumns_Data(start, end)




#     def playground(self):
#         self.info("# of columns in worksheet: {}".format(self.__getWorksheetColumnCount()))
#         self.info("# of columns in dataStore: {}".format(self.getColumnCount()))

#         # we don't need to remove the empty columns at the end, because we already pulled the data
#         #   and we will commit what we want to keep, so we don't need to clean up the sheet we only need
#         #   to keep the local data clean.      
#         # self.removeEmptyColumnsTrailing()

#         # @todo make sure that any data that gets updated in the data object have their "updated_date" field changed to time.now()



    
#     # This one was fun, in order to reduce the number of API calls that we need to make, we want to remove empty columns from the spreadsheets
#     #   In order to do this, we have to walk forward through the columns and the the sheet to find empty columns
#     #   Then, figure out what the ranges of the empty columns are, so we can hold them
#     #   Once we know all the ranges, work the list backwards...
#     #   If you don't work the list backwards, you will delete the columns then the ranges don't match the sheet or array
#     #   This means you delete data.
#     #   e.g [1:a,2:b,3:"",4:"",5:c,6:d,7:"",8:e,9:f,10:g]
#     #       if you delete 3->4, your array looks like this, which is fine bc the indeces are correct:
#     #       [1:a,2:b,5:c,6:d,7:"",8:e,9:f,10:g]
#     #       but, your sheet looks like this:
#     #       [1:a,2:b,3:c,4:d,5:"",6:e,7:f,8:g]
#     #       so, when you go to delete 7, it either isn't there or now "f" is in the 7th spot, so if you pass [7:7]
#     #           to the worksheet delete function, it will delete "f" instead of deleting the correct item
#     def X_removeEmptyColumns(self, removeTrailingEmpties = False):
#         self.debug("removeEmptyColumns(removeTrailingEmpties={})".format(removeTrailingEmpties))

#         counter = 1
#         delete_items = []

#         # get the current known columns
#         columns = self.getColumns()

#         # start of the next range
#         start = None

#         # end of the range
#         end = None

#         # list of ranges to delete
#         ranges = []

#         # go through the columns we pulled and identify the index of any empties
#         for column in columns:
#             if column == "":
#                 # only do things if the column is empty
#                 if None == start:
#                     # start is empty, so we are in the first pass through the loop
#                     start = counter
#                     end = counter
#                     self.debug("Setting start to {}".format(counter))
#                 elif counter == end+1:
#                     # if we are still in a range of empties, increase the range
#                     end = counter
#                     self.debug("Setting end to {}".format(counter))
#                 else:
#                     # we reached another empty number, which means the previous range is completed
#                     ranges.append({"start":start, "end": end})
#                     start = counter
#                     end = counter
#                     self.debug("New item is {}".format(counter))
            
#             # count which column we are on
#             counter+= 1

#         # only do this if we have actual range to delete
#         if None != start and None != end:
#             # add the last range that we saw to ranges array
#             ranges.append({"start":start, "end": end})

#         #are there empty columns after the known columns in the first row?
#         currentSheetColsAvailable = self.__getWorksheetObj().col_count

#         if removeTrailingEmpties:
#             self.debug("We have permission to remove the trailing empty columns")
#             # I was deleting the empties off the end, but there was a race condition on the delete that would cause the next function
#             #   to think that there were more columns than there actually were because the range delete for the end of the sheet was taking
#             #   a while to run. So, we don't remove those anymore.
#             #
#             # if the next column is larger than currentSheetColsAvailable, then we are at the end of the sheet
#             #   so we don't need to delete anything
#             if len(columns)+1 < currentSheetColsAvailable: 
#                 # go ahead and trim everything off the end too, just for funsies
#                 ranges.append({"start":len(columns)+1, "end": currentSheetColsAvailable})

#         # if we do a removal, return that we did
#         didWeRemoveRanges = False

#         # go backwards throug the ranges, so that we don't invalidate the ranges (see comments before method)
#         while len(ranges) > 0:
#             rangeToKill = ranges.pop()

#             self.info("Removing item from {}:{} from columns".format(rangeToKill["start"], rangeToKill["end"]))
#             del columns[rangeToKill["start"]:rangeToKill["end"]]

#             self.info("Removing item from {}:{} from worksheet".format(
#                     self.getA1(1, rangeToKill["start"]), 
#                     self.getA1(1, rangeToKill["end"])))
#             self.__getWorksheetObj().delete_columns(rangeToKill["start"], rangeToKill["end"])
#             didWeRemoveRanges = True

#         # make sure to update the columns in this object, so we have the correct current list
#         self.__setColumnList(columns)

#         # return true if we did some cleanup
#         return didWeRemoveRanges



#     # Check that the columns in the worksheet match what is expected
#     # addMissingColumns will cause anything that is missing to be added to the spreadsheet

#     # # 
#     # # Original info, assumed the sheet was source of truth, needs to be converted to object as source of truth
#     # #             

#     # worksheet.checkColumns(self.getExpectedColumns(), self.getExtraExpectedColumns())
#     # if addMissingColumns:
#     #     # remove the empty columns
#     #     # clean up the empties so that we have a good measure of the sheet
#     #     worksheet.removeEmptyColumns()

#     #     # add in the new columns, so that we have everything we need
#     #     addedColumns = worksheet.addMissingColumns()

#     #     self.info("{} columns were added to {}".format(addedColumns, worksheet.getTitle()))

#     #     # double check that we don't have extra empties at the end of the sheet, just in case
#     #     worksheet.removeEmptyColumns(removeTrailingEmpties=True)

#     #     # since we can't control how the data gets added in previous steps or how it was in the original sheet, 
#     #     #   make sure it is clean here. By default, this stores to the worksheet when it's done running. To cancel that
#     #     #   add storeToWorksheet = False
#     #     sheetData = worksheet.sortTheColumns()
#     # self.console("We are only running one worksheet right now, see Spreadhsheet.py line 188")


#     def X_checkColumns(self, cols_expected, cols_expected_extra):
#         self.debug("Workheet.checkColumns(cols_expected={},cols_expected_extra={})".format(cols_expected, cols_expected_extra))

#         # What columns do we need to care about?
#         colsToCheck = self.calculateExpectedColumns(cols_expected, cols_expected_extra)

#         #
#         # The following is actually checking the columns
#         #

#         # does the first_row contain everything in the colsToCheck
#         firstrow_result = self.compareLists(self.getColumns(), colsToCheck)

#         if firstrow_result:
#             self.info("The worksheet %s has all the columns we expect" % self.getTitle())
#         else: 
#             self.info("The worksheet %s does not have all the columns we expect" % self.getTitle())
#             #figure out what's missing and complain so that we can get that shit fixed
#             missing_columns = list(set(colsToCheck) - set(self.getColumns()))
#             self.setMissingColumns(missing_columns)
#             self.console("Worksheet: {} is missing these columns: ".format(self.getTitle()), data=str(self.getMissingColumns()))


#     # Create a list of columns that we are expecting to find in this worksheet
#     # @return the list of expected columns
#     def X_calculateExpectedColumns(self, cols_expected: list, cols_expected_extra: dict, checkExtras: bool = True):
#         self.debug("calculateExpectedColumns(cols_expected={},cols_expected_extra={}, checkExtras={})".format(cols_expected, cols_expected_extra, checkExtras))
#         # set the columns to the default
#         expectedCols = cols_expected

#         # if we are checking extras and we have extra cols to check, then let's loop through. Otherwise, just do the normal thing
#         if True == checkExtras and [] != cols_expected_extra:

#             # if we have extra columns that we need to check, loop through the options in the expected list and see if there are matches
#             for extraColCheck, colTitles in cols_expected_extra.items():

#                 # if we find that the key for the extra columns is in the worksheet title, 
#                 # then append the extras columns to check and then check against the new combined list
#                 if extraColCheck in self.getTitle():
#                      expectedCols += cols_expected_extra[extraColCheck]
        
#         return self.setExpectedColumns(expectedCols)


#     # Go through the missing columns and add them to the worksheet at the end of the worksheet

# #  Consider pulling all the data from the worksheet, modifying this locally, then replacing it back into the sheet
# #   Getting All Values From a Worksheet as a List of Lists
# #   list_of_lists = worksheet.get_all_values()
# # 
# #   Getting All Values From a Worksheet as a List of Dictionaries
# #   list_of_dicts = worksheet.get_all_records()
# # 
# #   order of ops:
# #       pull everything
# #       worksheet.clear()
# #       replace the sheet with a placeholder text to say "under construction"
# #       Do the data manipulation to sort the data to match "expected cols" order
# #       drop the data back in with self.__getWorksheetObj().batch_update(batch_update)
# # 
# #   to test: 
# #       pull everything
# #       clear: worksheet.clear()
# #       write everything
# #       see what happens
# #
# #   https://docs.gspread.org/en/latest/user-guide.html#getting-all-values-from-a-worksheet-as-a-list-of-lists

#     def X_addMissingColumns(self):
#         self.debug("addMissingColumns()")

#         self.debug("Attempting to add these columns: {}".format(self.getMissingColumns()))

#         missingColumnCount = len(self.getMissingColumns())
#         self.debug("missingColumnCount: {}".format(missingColumnCount))

#         # if there are no missing columns, do nothing!
#         if 0 != missingColumnCount: 

#             currentSheetColsAvailable = self.__getWorksheetObj().col_count
#             self.debug("currentSheetColsAvailable: {}".format(currentSheetColsAvailable))

#             expectedColumnCount = len(self.getExpectedColumns())
#             self.debug("expectedColumnCount: {}".format(expectedColumnCount))

#             str_list = list(filter(None, self.getColumns()))
#             self.debug("current count: {}".format(len(str_list)))

#             nextColumnIndex = self.getColumnCount()+1
#             totalColumnsNeeded = 0
#             # add more columns to the current worksheet to make sure we can keep adding columns
#             if (nextColumnIndex + missingColumnCount) > int(currentSheetColsAvailable):
#                 totalColumnsNeeded= nextColumnIndex + missingColumnCount - int(currentSheetColsAvailable)
#                 self.debug("Adding {} empty columns".format(totalColumnsNeeded))
#                 # to be careful, add enough columns to handle all the missing columns
#                 self.__getWorksheetObj().add_cols(totalColumnsNeeded)
            
#             startCell = self.__getWorksheetObj().cell(1, nextColumnIndex)
#             endCell = self.__getWorksheetObj().cell(1, self.getColumnCount()+1 + missingColumnCount)
#             rangeToUpdate = "{}:{}".format(startCell.address, endCell.address)

#             # push the data over the API
#             self.batch_update(rangeToUpdate, [self.getMissingColumns()])
            
#             self.setMissingColumns([])

#         return missingColumnCount


#     # # actually create a new column in the worksheet, if columnNumber is included it will create the column 
#     # def addColumn(self, columnName: str = ""):
#     #     self.debug("addColumn({})".format(columnName))

#     #     # we want to add a column at the next open position after the current columns, so grab the current column list length
#     #     newColumnNumber = self.getColumnCount() + 1

#     #     self.info("Adding a column to position [1,{}] with title {}".format(newColumnNumber, columnName))

#     #     # add the column name in the new column, row 1 
#     #     response = self.__getWorksheetObj().update_cell(1, newColumnNumber, columnName)

#     #     self.info("Response from the update_cell call: {}".format(response))

#     #     # internal call to update our cache without pulling it from the worksheet, will also update the column count
#     #     self.__addToColumnList(columnName)

#     #     return self.getColumns()

#     # make sure the columns are in the order we want for human readability
#     #   you can write it to the worksheet if you would like, or not with storeToWorkSheet = True/False
#     #   @returns the ordered list or a list of orderedDicts for use in other methods
#     def X_sortTheColumns(self, cols_to_keep, data, storeToWorksheet = True, returnAsOrderedDicts = False):
#         self.debug(
#             "Worksheet.sortTheColumns(cols_to_keep={}, data={}, storeToWorksheet={},returnAsOrderedDicts={})"
#                 .format(
#                     cols_to_keep,
#                     data,
#                     storeToWorksheet, 
#                     returnAsOrderedDicts))

#         #seed the list with the columns as the first row
#         output_list = [cols_to_keep]

#         # here if we need it, if returnAsOrderedDicts is True
#         ordered_dicts = []

#         # go through all the data and get it in the right order
#         for data_row in data:
#             # lists are ordered, so if we pull the data from the data_from_sheet in the right order and add it to our list
#             #   then we have the data in the right order
#             temp_list = []

#             #setting up the variable, in case we need to use it
#             temp_ordered_dict = None

#             # if we need the ordered Dict, set it up
#             if returnAsOrderedDicts:
#                 temp_ordered_dict = OrderedDict()

#             #use cols_expected as the order we care about, add to the temp_list in the right order 
#             for key in cols_to_keep:

#                 temp_list.append(data_row[key])

#                 if returnAsOrderedDicts:
#                     temp_ordered_dict[key] = data_row[key]

#             # add the temp_list to our output in row order
#             output_list.append(temp_list)

#         # calculate the A1 Notation of the range from A1 -> the height and width of our new List
#         end_cell = gself.getA1(len(output_list),len(temp_list))

#         self.debug("The output_list data is {}".format(output_list))

#         if storeToWorksheet:
#             #remove all the stuff in the sheet that's there right now
#             self.clearAllRecords()

#             #push the data to the spreadsheet
#             self.batch_update("A1:{}".format(end_cell), output_list)

#         #only return this if it's asked for
#         if returnAsOrderedDicts:
#             return ordered_dicts

#         #by default we return the list object
#         return output_list

#     def X_removeAllButExpectedColumns(self, storeToWorksheet=True, returnAsOrderedDicts = False):
#         self.debug("removeAllButExpectedColumns()")
#         cols_expected = self.getExpectedColumns()
#         self.sortTheColumns(cols_to_keep=cols_expected, storeToWorksheet=storeToWorksheet, returnAsOrderedDicts=returnAsOrderedDicts)





#     ####
#     #
#     # Row Methods
#     #
#     ####
#     # 'add_dimension_group_rows', 
#     # 'add_rows', 
#     # 'append_row', 
#     # 'append_rows', 
#     # 'delete_dimension_group_rows', 
#     # 'delete_row', 
#     # 'delete_rows', 
#     # 'frozen_row_count', 
#     # 'hide_rows', 
#     # 'insert_row', 
#     # 'insert_rows', 
#     # 'row_count', 
#     # 'row_values', 
#     # 'rows_auto_resize', 
#     # 'unhide_rows', 


#     def getRowCount(self):
#         self.debug("getRowCount()")
#         return self.getData().height()


#     ####
#     #
#     # Cell Methods
#     #
#     ####
#     # 'acell'
#     # 'cell',
#     # 'get_all_cells', 
#     # 'merge_cells', 
#     # 'unmerge_cells',

#     # creates A1 notation for the row and column given
#     def getA1(self, row, column):
#         self.debug("getA1(row={}, col={})", (row, col))
#         return gspread_utils.rowcol_to_a1(row, col)



#     def commit(self):
#         dataRange = self.getDataRange()
#         sheetData = self.__getSheetData()

#         values = sheetData.getData()

#         batch_update = [{
#             'range': dataRange,
#             'values': values,
#         }]

#         self.debug("Updating the spreadsheet with this data: ", batch_update)

#         worksheet = self.__getWorksheetObj()

#         # if the title is changed, push it
#         if self.getTitle() != worksheet.title:
#             worksheet.update_title(self.getTitle())
        
#         # do a batch update, because doing this one column at a time hit the rate limits super fast
#         worksheet.batch_update(batch_update)


#     ####
#     #
#     # Delete Data From the Sheet
#     #
#     ####
#     # 'clear', 
#     # 'batch_clear', 

#     # clears out all the data from the spreadsheet
#     #   Most of the time the workflow here is to clear your sheet, so you can write the worksheet data to it
#     #   consider carefully what could go wrong if you don't have data in the worksheet and you do not commit
#     #   the worksheetData object's data to the sheet. That's dangerous!
#     @Debugger
#     @validate_arguments
#     def clearAllRecords(self, deleteWorksheetData:bool=False):
#         self.__getWorksheetObj().clear()
#         # This is DANGEROUS, bc you can lose ALL of your data
#         if deleteWorkSheetData:
#             self._sheetData = WorksheetData()
