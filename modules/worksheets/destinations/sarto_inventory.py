
from modules.worksheets.destination import Bdfs_Worksheet_Destination
from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base

class Sarto_Inventory_Worksheet_Destination(Bdfs_Worksheet_Destination):

    def setupParams(self):
        # sets up all the params we need from some very basic data
        base = Sarto_Inventory_Base()
        self.cols_expected = base.cols_expected
        self.cols_expected_extra = base.cols_expected_extra