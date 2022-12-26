import sys
from modules.worksheets.source import Bdfs_Worksheet_Source
from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base

class Sarto_Inventory_Worksheet_Source(Bdfs_Worksheet_Source):
    
    def setupParams(self):
        # sets up all the params we need from some very basic data
        base = Sarto_Inventory_Base()
        self.data.expectedColumns = base.cols_expected
        self.data.expectedColumns_extra = base.cols_expected_extra
        self.data.uniqueField = base.uniqueField
