import gspread, sys
from dataclasses import dataclass, field as dc_field
from collections import OrderedDict
# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import utils as gspread_utils
from gspread.worksheet import Worksheet
from modules.base import BaseClass
from modules.decorator import Debugger
from modules.logger import Logger
from modules.worksheets.exception import Bdfs_Worksheet_Exception
from modules.worksheets.data import Bdfs_Worksheet_Data
from pydantic import validate_arguments

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


@dataclass
class Worksheet_DataClass():
    title:str  = dc_field(default_factory=str)              # The Sheet title
    gspread_worksheet:Worksheet = None                      # The worksheet object itself, allows us to run gspread functions
    expectedColumns:list = dc_field(default_factory=list)   # A list of columns we expect to have in the sheet
    uncommitted_title: str = dc_field(default_factory=str)  # temp storage if we change the title of the worksheet, until commit
    sheetData:Bdfs_Worksheet_Data = dc_field(default_factory=Bdfs_Worksheet_Data)         # source of truth for the data of the worksheet
    changes:dict[bool] = dc_field(default_factory=dict)     # {"title": False, "data": False}
    sheet_retrieved:bool = False

#
# Rules; 
#   pulls the worksheet data, does all the changes, only pushes changes when commit() is called.
#
class Bdfs_Worksheet(BaseClass):

    logger_name = "Worksheet"

    @Debugger
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __init__(self, worksheet:Worksheet):
        self.data = Worksheet_DataClass()
        # store the gspread worksheet for use later
        self.data.gspread_worksheet = worksheet
        self.data.title = worksheet.title

        # double check we have the required params from the extension class
        self.__checkSetup()

        # setup the changes items we want to track here
        self.data.changes = {"title": False, "data": False}

        # we have not retrieved the sheet yet
        self.data.sheet_retrieved

        self.getTitle()

    @Debugger
    def __checkSetup(self):
        # if we don't know what cols are expected, we cannot check the sheet is setup properly
        if [] == self.getExpectedColumns():
            #fail if no one set the spreadsheetId on the wrapper class
            Logger.critical("Cols expected was not set before instantiating Spreadsheet class")
            raise Exception("cols_expected parameter is not set")


    # Register a change
    @Debugger
    @validate_arguments
    def changed(self, index:str, value:bool=True):
        if index in self.data.changes.keys():
            self.data.changes[index] = value
        else:
            raise Bdfs_Worksheet_Exception(f"there is no {index} in data.changes, add it to __setup() to track it")


    # Detect a change
    @Debugger
    @validate_arguments
    def isChanged(self, index):
        if index in self.data.changes.keys():
            return self.data.changes[index]
        else:
            raise Bdfs_Worksheet_Exception(f"there is no {index} in data.changes, add it to __setup() to track it")


    ####
    #
    # gSpread worksheet accessor methods - all private
    #
    ####
    # get rid of any trailing columns that exist, we do this when we get ready to commit only
    @Debugger
    def gspread_worksheet_resize_to_data(self): 
        Logger.debug("Resizing the google worksheet to the current data size")
        #rezize the spreadsheet to the data - makes our lives easier later on
        self.data.gspread_worksheet.resize(cols=self.getColumnCounts()['data'])


    ####
    #
    # Sheet functionality on our WorksheetData object that mirrors gspread functionality
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
    # 'update_title'

    # if we have a new title passed, return that, otherwise return the original title
    @Debugger
    def getTitle(self): #tested
        if "" == self.data.uncommitted_title:
            return self.getOriginalTitle()
        return self.data.uncommitted_title


    # always returns self.data.title
    @Debugger
    def getOriginalTitle(self): #tested
        return self.data.title


    # if a new title is set, store it until we commit the sheet
    @Debugger
    @validate_arguments
    def setTitle(self, title:str) -> str: #tested
        # only do this if the data is diff, you know?
        if title != self.data.title:
            self.data.uncommitted_title = title
            self.changed('title')
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

    #will return something like -- "A1:CT356"
    @Debugger
    def getDataRange(self) -> str: #tested
        dataRange = f"{self.getA1(1,1)}:{self.getA1(self.height()+1, self.width())}"
        return dataRange


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
    @Debugger
    def commit(self):
        
        # if the title is changed, push it
        if self.isChanged('title') == True:
            self.data.gspread_worksheet.update_title(self.getTitle())
            # reset the flag, in case we do other things
            self.changed('title', False)
        
        # if the data has changed, then update the google sheet
        if self.isChanged('data') == True:
            # so we don't have to screw with empty rows or calculating anything, resize to the data available
            self.gspread_worksheet_resize_to_data()

            # get the meta about our new data to commit
            dataRange = self.getDataRange()

            headers = self.getColumns()
            values = self.getDataAsListOfLists()

            batch_update = [{
                'range': dataRange,
                'values': [headers]+values,
            }]

            # Logger.debug("Updating the spreadsheet with this data: ", batch_update)
            # do a batch update, because doing this one column at a time hit the rate limits super fast
            # also, because we are sending in the data range of our local data, we can go outside the worksheet's data range!
            self.data.gspread_worksheet.batch_update(batch_update)
            # reset the flag, in case we do other things
            self.changed('data', False)


    ####
    #
    # Delete Data From the Sheet
    #
    ####
    # 'clear', 
    # 'batch_clear', 

    ####
    #
    # Data Cache - Create
    #
    ####

    @Debugger
    def getData(self): #tested
        # we can defer grabbing the data until we get here
        if False == self.data.sheet_retrieved:
            
            self.data.sheetData = Bdfs_Worksheet_Data(self.data.gspread_worksheet.get_all_values())

            # we are now the same as the google worksheet, nothing to commit
            self.changed('data', False)
            # we got the data, set the flag
            self.data.sheet_retrieved = True


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

    @Debugger
    def getExpectedColumns(self): #tested
        return self.__mergeExpectedColumns()


    # since we have multiple options for how the columns should be setup
    #   Get the columns that we care about and return them
    @Debugger
    def __mergeExpectedColumns(self):
        expectedCols = self.cols_expected
        for index in self.cols_expected_extra:
            if index in self.getTitle():
                expectedCols.extend(self.cols_expected_extra[index])
        return expectedCols


    # The only place to retrieve the first row of data from the sheet
    # use_cache = True will return the cache, if False it gets data from the live worksheet
    #   if there are empty columns at the end, the row_values() method will not get them, it will get everything from
    #       the first column to the last value in the row
    @Debugger
    def getColumns(self): #tested
        self.getData()
        return self.data.sheetData.getHeaders()


    # return the number of columns in the worksheet
    @Debugger
    def getColumnCounts(self): 
        obj = {
            'data': self.width(),
            'gspread_worksheet': len(self.data.gspread_worksheet.row_values(1))
        }
        return obj


    @Debugger
    @validate_arguments
    def addColumn(self, name:str, index:int=None):
        self.getData()
        # will handle adding at the end or the index, depending on what's passed
        self.data.sheetData.addHeader(name=name, index=index)
        self.changed("data")


    # wrapper function to take care of some pre-work on removing columns
    @Debugger
    @validate_arguments
    def removeColumns(self, column:int=None, start:int=None, stop:int=None):
        self.getData()
        raise Exception("remove_columns is not built or tested yet")


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

    @Debugger
    def getRowCount(self):
        return self.height()


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
    @Debugger
    @validate_arguments
    def getA1(self, row, column):
        return gspread_utils.rowcol_to_a1(row, column)



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

    ####
    #
    # Meta Methods
    #
    ####

    def width(self):
        self.getData()
        return self.data.sheetData.width()

    def height(self):
        self.getData()
        return self.data.sheetData.height()

    def getDataAsListOfLists(self):
        self.getData()
        return self.data.sheetData.getAsListOfLists()
   
    def getDataAsListOfDicts(self):
        self.getData()
        return self.data.sheetData.getAsListOfDicts()
   
