import sys
from modules.worksheets.destinations.bdfs_inventory import Bdfs_Inventory_Worksheet_Destination
from modules.worksheets.bases.shopify_doors.barndoor_single import Shopify_BarnDoor_Single_Base
from modules.worksheets.destinations.bdfs_inventory import Bdfs_Inventory_Worksheet_Destination

class Bdfs_Inventory_BarnDoor_Single_Worksheet_Destination(Bdfs_Inventory_Worksheet_Destination):

    def setupParams(self):
        # sets up all the params we need from some very basic data
        base = Shopify_BarnDoor_Single_Base()

        self.data.expectedColumns = base.cols_expected.copy()
        self.data.expectedColumns_extra = base.cols_expected_extra.copy()
        self.data.uniqueField = base.uniqueField
        self.data.discount = base.discount
    
