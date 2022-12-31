import sys
from dataclasses import dataclass, field as dc_field
from collections import OrderedDict
# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import utils as gspread_utils
from gspread.worksheet import Worksheet
from modules.base import Base_Class
from modules.decorator import Debugger
from modules.logger import Logger
from modules.worksheet import Bdfs_Worksheet,Worksheet_DataClass
from modules.worksheets.exception import Bdfs_Worksheet_Destination_Exception
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

class Worksheet_DataClass_Destination(Worksheet_DataClass):
    discount:float = dc_field(default_factory=float)

#
# Rules; 
#   pulls the worksheet data, does all the changes, only pushes changes when commit() is called.
#
class Bdfs_Worksheet_Destination(Bdfs_Worksheet):

    # This is only in the Destination class
    @Debugger
    def checkSetup(self): #parent class __init__ runs this
        # if we don't know what cols are expected, we cannot check the sheet is setup properly
        if [] == self.getExpectedColumns():
            #fail if no one set the spreadsheetId on the wrapper class
            raise Bdfs_Worksheet_Destination_Exception("""
                Cols expected was not set before instantiating Spreadsheet class. If you added setupParams() don't forget to add this to your setupParams() method: 
                ```
                if None != self.cols_expected: 
                    self.data.expectedColumns = self.cols_expected

                if None != self.cols_expected_extra: 
                    self.data.expectedColumns_extra = self.cols_expected_extra")
                ```
        """)
    @Debugger
    def setupData(self, sheetData:list=None)->list:
        if [] == sheetData:
            return [self.getExpectedColumns()]
        return sheetData

    ####
    #
    # Meta Data Methods
    #
    ####

    # allows the data to be modified and registers that it was modified
    # in source, this will throw an exception to prevent modification of data
    @Debugger
    def modifiesData(self):
        self.getData()


    # if a new title is set, store it until we commit the sheet
    @Debugger
    @validate_arguments
    def setTitle(self, title:str) -> str: #tested
        self.modifiesData()
        # only do this if the data is diff, you know?
        if title != self.data.title:
            self.data.uncommitted_title = title
            self.changed('title')
        return self.getTitle()

    ####
    #
    # Column Methods
    #
    ####

    @Debugger
    def getExpectedColumns(self) -> list: #tested
        expectedCols = self.data.expectedColumns
        # check the indexes of extra columns (e.g. single, double)
        for index in self.data.expectedColumns_extra:
            # if the index is in the worksheet title, add them
            if index in self.getTitle():
                # if the columns are already in the expectedCols, don't add them
                for column in self.data.expectedColumns_extra[index]:
                    if column not in expectedCols:
                        expectedCols.append(column)
        return expectedCols
    

    # wrapper function to take care of some pre-work on removing columns
    @Debugger
    @validate_arguments
    def removeColumns(self, columns:list[str]):
        self.modifiesData()
        self.data.sheetData.removeHeaders(headers=columns)


    @Debugger
    @validate_arguments
    def removeColumn(self, column:str):
        self.modifiesData()
        
        self.data.sheetData.removeHeader(header=column) 


    @Debugger
    @validate_arguments
    def addColumn(self, name:str, index:int=None):
        self.modifiesData()
        # will handle adding at the end or the index, depending on what's passed
        self.data.sheetData.addHeader(name=name, index=index)
        self.changed("data")
    

    # This will call a method that will cause the data set to:
        # remove unwanted columns
        # add new columns
        # put the columns in the sorted order
    @Debugger
    @validate_arguments
    def alignToColumns(self, columns:list[str]):
        self.modifiesData()
        self.data.sheetData.alignHeaders(columns)
        self.changed("data")


    ####
    #
    # Row Methods
    #
    ####

    @Debugger
    @validate_arguments
    def addRow(self, rowData:dict):
        self.modifiesData()
        self.data.sheetData.insertRow(rowData)

    @Debugger
    @validate_arguments
    def putRow(self, rowData:dict):
        self.modifiesData()

        # do the update or insert, based on the data that was passed
        self.data.sheetData.putRow(rowData)


    ####
    #
    # Cell Methods
    #
    ####
    

    ####
    #
    # All Data
    #
    ####
    @Debugger
    def deleteAllData(self):
        self.modifiesData() # get the data that we will delete, if we haven't, this is not ideal - we could find a way around this but it isn't a big deal today... sorry if you find this later

        self.data.sheetData.deleteAllData()
        
        self.changed('data') # technically we did change the data, or we will if we commit...

        Logger.info("All local sheet data as been deleted")

    @Debugger
    @validate_arguments
    def deleteRowWhere(self, key:str, value):
        self.modifiesData()
        
        self.data.sheetData.deleteRowWhere(column=key, value=value)
        
        self.changed('data')

    ####
    #
    # gSpread worksheet accessor methods
    #
    ####
    # get rid of any trailing columns that exist, we do this when we get ready to commit only
    @Debugger
    def gspread_worksheet_resize_to_data(self):
        self.modifiesData()
        
        Logger.debug("Resizing the google worksheet to the current data size")
        
        dataColCount = self.getColumnCounts()['data']
        if 0 < dataColCount:
            #rezize the spreadsheet to the data - makes our lives easier later on
            self.data.gspread_worksheet.resize(cols=dataColCount)
        
            self.changed('data')
    
    @Debugger
    def gspread_worksheet_clear(self):
        self.data.gspread_worksheet.clear()
        Logger.info("Clearing the remote spreadsheet")


    # overwrites whatever is in the sheet with the local storage data we have
    #   does not give a fuck what is in the worksheet, it will clear it before writing
    @Debugger
    def commit(self):
        self.modifiesData()
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

            # kill the data in the sheet, so that we are not writing into data that is differently sized than our current local data
            self.gspread_worksheet_clear()

            # do a batch update, because doing this one column at a time hit the rate limits super fast
            # also, because we are sending in the data range of our local data, we can go outside the worksheet's data range!
            self.data.gspread_worksheet.batch_update(batch_update)
            # reset the flag, in case we do other things
            self.changed('data', False)
