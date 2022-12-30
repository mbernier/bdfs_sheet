import gspread, sys
from dataclasses import dataclass, field as dc_field
from collections import OrderedDict
# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import utils as gspread_utils
from gspread.worksheet import Worksheet
from modules.base import Base_Class
from modules.caches.flat import Flat_Cache
from modules.decorator import Debugger
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
    sheetData:Bdfs_Worksheet_Data = None                    # source of truth for the data of the worksheet, DO NOT call factory here
    expectedColumns:list = dc_field(default_factory=list)   # A list of columns we expect to have in the sheet
    expectedColumns_extra:list = dc_field(default_factory=list)
    uncommitted_title: str = dc_field(default_factory=str)  # temp storage if we change the title of the worksheet, until commit
    changes:dict[bool] = dc_field(default_factory=dict)     # {"title": False, "data": False}
    sheet_retrieved:bool = False
    id: int = dc_field(default_factory=int)
    uniqueField: str = dc_field(default_factory=str)
#
# Rules; 
#   pulls the worksheet data, does all the changes, only pushes changes when commit() is called.
#
class Bdfs_Worksheet(Base_Class):
    cols_expected = None
    cols_expected_extra = None
    
    @Debugger
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __init__(self, worksheet:Worksheet):
        self.data = Worksheet_DataClass()
        # store the gspread worksheet for use later
        self.data.gspread_worksheet = worksheet
        self.data.title = worksheet.title
        self.data.id = worksheet.id
        self.data.uniqueField = None 

        # a hook to allow setting up params
        self.setupParams()

        # double check we have the required params from the extension class
        self.checkSetup()

        # setup the changes items we want to track here
        self.data.changes = {"title": False, "data": False}

        # we have not retrieved the sheet yet
        self.data.sheet_retrieved = False

        self.getTitle()


    @Debugger
    def checkSetup(self):
        pass #this functionality is moved to the Destination class

    @Debugger
    def setupData(self, sheetData=None):
        return sheetData # do nothing by default

    @Debugger
    def setupParams(self):
        if None != self.cols_expected: 
            self.data.expectedColumns = self.cols_expected

        if None != self.cols_expected_extra: 
            self.data.expectedColumns_extra = self.cols_expected_extra

    ####
    #
    # Record whether something has been changed, which lets testing validate that source/destination are used properly
    #      Source should NEVER have anything changed
    #
    ####

    # Register a change
    @Debugger
    @validate_arguments
    def changed(self, index:str, value:bool=True):

        if True == value: #only throw a fit if the code is trying to change data
            self.modifiesData() # because this is called when data is modified

        if index in self.data.changes.keys():
            self.data.changes[index] = value
        else:
            raise Bdfs_Worksheet_Exception(f"there is no '{index}' in data.changes keys, add it to __setup() to track it")


    # Detect a change, does not have __modifiedData() bc this is a read-only method
    @Debugger
    @validate_arguments
    def isChanged(self, index:str) -> bool:
        if index in self.data.changes.keys():
            return self.data.changes[index]
        else:
            raise Bdfs_Worksheet_Exception(f"there is no {index} in data.changes, add it to __setup() to track it")



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
    def getTitle(self) -> str:
        if "" == self.data.uncommitted_title:
            return self.getOriginalTitle()
        return self.data.uncommitted_title


    # always returns self.data.title
    @Debugger
    def getOriginalTitle(self) -> str:
        return self.data.title

    
    @Debugger
    def getId(self):
        return self.data.id

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
    @validate_arguments
    def getDataRange(self) -> str: #tested
        height = self.height()+1
        width = self.width()+1
        dataRange = f"{self.getA1(1,1)}:{self.getA1(height, width)}"
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
    def getData(self):
        # we can defer grabbing the data until we get here
        if False == self.data.sheet_retrieved:
            sheetData = self.data.gspread_worksheet.get_all_values()
            
            # allows modifying the data before it is passed to Worksheet_Data if needed
            sheetData = self.setupData(sheetData)
            
            # doing this to make dataclass happy and pass a bool, instead of str
            uniqueField = None
            if self.data.uniqueField != "" and None != self.data.uniqueField: 
                uniqueField = self.data.uniqueField
            
            self.data.sheetData = Bdfs_Worksheet_Data(sheetData, uniqueField = uniqueField)

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



    # The only place to retrieve the first row of data from the sheet
    # use_cache = True will return the cache, if False it gets data from the live worksheet
    #   if there are empty columns at the end, the row_values() method will not get them, it will get everything from
    #       the first column to the last value in the row
    @Debugger
    def getColumns(self) -> list:
        self.getData()
        return self.data.sheetData.getHeaders()


    # return the number of columns in the worksheet
    @Debugger
    def getColumnCounts(self) -> dict: 
        obj = {
            'data': self.width(),
            'gspread_worksheet': len(self.data.gspread_worksheet.row_values(1))
        }
        return obj



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
    # Row Methods
    #
    ####

    @Debugger
    @validate_arguments
    def getRow(self, row:int=None, update_timestamp=True) -> Flat_Cache:
        return self.data.sheetData.select(row=row, update_timestamp=update_timestamp)


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

    @Debugger
    @validate_arguments
    def getCell(self, row:int, column:str):
        return self.data.sheetData.select(row,column)


    # creates A1 notation for the row and column given
    @Debugger
    @validate_arguments
    def getA1(self, row, column) -> str:
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

    @Debugger
    def width(self) -> int:
        self.getData()
        return self.data.sheetData.width()

    @Debugger
    def height(self) -> int:
        self.getData()
        return self.data.sheetData.height()

    @Debugger
    @validate_arguments
    def getDataAsListOfLists(self, update_timestamp:bool=False) -> list[list]:
        self.getData()
        return self.data.sheetData.getAsListOfLists(update_timestamp=update_timestamp)
   
    @Debugger
    @validate_arguments
    def getDataAsListOfDicts(self, update_timestamp:bool=False) -> list[dict]:
        self.getData()
        return self.data.sheetData.getAsListOfDicts()
   
