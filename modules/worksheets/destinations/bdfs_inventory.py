
from modules.worksheets.destination import Bdfs_Worksheet_Destination


import sys
from dataclasses import dataclass, field as dc_field
from gspread.worksheet import Worksheet
from modules.worksheet import Worksheet_DataClass
from modules.worksheets.data import Bdfs_Worksheet_Data
from modules.worksheets.destination import Bdfs_Worksheet_Destination
from modules.worksheets.bases.shopify_barndoor import Shopify_Barndoor_Base

@dataclass
class Bdfs_Worksheet_DataClass(Worksheet_DataClass):
    gspread_worksheet:Worksheet = None                      # The worksheet object itself, allows us to run gspread functions
    sheetData:Bdfs_Worksheet_Data = None                    # source of truth for the data of the worksheet, DO NOT call factory here
    title:str  = dc_field(default_factory=str)              # The Sheet title
    expectedColumns:list = dc_field(default_factory=list)   # A list of columns we expect to have in the sheet
    expectedColumns_extra:list = dc_field(default_factory=list)
    uncommitted_title: str = dc_field(default_factory=str)  # temp storage if we change the title of the worksheet, until commit
    changes:dict[bool] = dc_field(default_factory=dict)     # {"title": False, "data": False}
    sheet_retrieved:bool = False
    id: int = dc_field(default_factory=int)
    uniqueField: str = dc_field(default_factory=str)

class Bdfs_Inventory_Worksheet_Destination(Bdfs_Worksheet_Destination):
    dataClass = "modules.worksheets.destinations.bdfs_inventory.Bdfs_Worksheet_DataClass"

    def setupParams(self):
        # sets up all the params we need from some very basic data
        base = Shopify_Barndoor_Base()

        self.data.expectedColumns = base.cols_expected.copy()
        self.data.expectedColumns_extra = base.cols_expected_extra.copy()
        self.data.uniqueField = base.uniqueField

    