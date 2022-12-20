from dataclasses import dataclass, field as dc_field
from collections import OrderedDict
# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import utils as gspread_utils
from gspread.worksheet import Worksheet
from modules.base import BaseClass
from modules.decorator import Debugger
from modules.logger import Logger, logger_name
from modules.worksheet import Bdfs_Worksheet
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

logger_name.name = "Bdfs_Worksheet_Destination"

#
# Rules; 
#   pulls the worksheet data, does all the changes, only pushes changes when commit() is called.
#
class Bdfs_Worksheet_Destination(Bdfs_Worksheet):

    # This is only in the Destination class
    @Debugger
    def __checkSetup(self):
        # if we don't know what cols are expected, we cannot check the sheet is setup properly
        if [] == self.getExpectedColumns():
            #fail if no one set the spreadsheetId on the wrapper class
            Logger.critical("Cols expected was not set before instantiating Spreadsheet class")