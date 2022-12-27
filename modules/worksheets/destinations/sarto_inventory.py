import sys
from modules.worksheets.destination import Bdfs_Worksheet_Destination
from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base

class Sarto_Inventory_Worksheet_Destination(Bdfs_Worksheet_Destination):

    def setupParams(self):
        print("Got to Sarto_Inventory_Worksheet_Destination")
        # sets up all the params we need from some very basic data
        base = Sarto_Inventory_Base()
        self.data.expectedColumns = base.cols_expected
        self.data.expectedColumns_extra = base.cols_expected_extra
        self.data.uniqueField = base.uniqueField
        self.data.discount = base.discount
        print(f"self.data.uniqueField: {self.data.uniqueField}")