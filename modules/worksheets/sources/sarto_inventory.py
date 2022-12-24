from modules.worksheets.source import Bdfs_Worksheet_Source
from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base

class Sarto_Inventory_Worksheet_Source(Bdfs_Worksheet_Source):
    
    def setupParams(self):
        # sets up all the params we need from some very basic data
        sartocolumns = Sarto_Inventory_Base()
        self.cols_expected = sartocolumns.cols_expected
        self.cols_expected_extra = sartocolumns.cols_expected_extra
