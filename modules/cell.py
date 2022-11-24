import gspread, sys
# https://github.com/burnash/gspread/blob/master/gspread/utils.py
from gspread import utils as gspread_utils

from modules.base import BaseClass

class Cell(BaseClass):
    
    logger_name = "Cell"

    def __init__(self):
        self._cell = None

    # accessort for the stored cell object, so we can wrap everything
    def _getCell(self):
        self.debug("Cell._getCell()")
        return self._cell

    # a1 Address of the cell
    def getAddress(self):
        self.debug("Cell._getAddress()")
        return self._getCell().address

    # column number of the cell
    def getColumn(self):
        self.debug("Cell._getColumn()")
        return self._getCell().col

    # Row number of the cell
    def getRow(self):
        self.debug("Cell._getColumn()")
        return self._getCell().row

    # get the value in the cell, can convert to num or int if possible using convertToNumber = True
    def getValue(self, convertToNumber = False):
        self.debug("Cell._getValue()")
        if convertToNumber:
            return self._getCell().numeric_value
        return self._getCell().value

    @staticmethod
    def create(address, value):
        cell(row, col, value_render_option='FORMATTED_VALUE')
 

    @staticmethod
    def replace(location, data):
        print("This is not implemented - fix!!")

        # classmethodfrom_address(label, value='')
        # Instantiate a new Cell from an A1 notation address and a value

        # Parameters
        # label (string) – the A1 label of the returned cell

        # value (string) – the value for the returned cell

        # Return type
        # Cell