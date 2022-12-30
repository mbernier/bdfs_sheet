import sys
from dataclasses import dataclass, field as dc_field
from modules.worksheet import Worksheet_DataClass
from modules.worksheets.destination import Bdfs_Worksheet_Destination
from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base

@dataclass
class Sarto_Worksheet_DataClass(Worksheet_DataClass):
    discount:int = dc_field(default_factory=int)

class Sarto_Inventory_Worksheet_Destination(Bdfs_Worksheet_Destination):
    dataClass = "modules.worksheets.destinations.sarto_inventory.Sarto_Worksheet_DataClass"

    def setupParams(self):
        print("Got to Sarto_Inventory_Worksheet_Destination")
        # sets up all the params we need from some very basic data
        base = Sarto_Inventory_Base()

        self.data.expectedColumns = base.cols_expected
        self.data.expectedColumns_extra = base.cols_expected_extra
        self.data.uniqueField = base.uniqueField
        self.data.discount = base.discount
        print(f"self.data.uniqueField: {self.data.uniqueField}")