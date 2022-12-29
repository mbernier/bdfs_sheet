import sys
from collections import OrderedDict
from modules.caches.exception import Flat_Cache_Exception
from modules.caches.flat import Flat_Cache
from modules.caches.nested import Nested_Cache
from modules.helper import Helper
from modules.dataMoves.originalbdfs_inventory.sarto_inventory.sarto import Originalbdfs_Inventory_To_Sarto_Inventory
from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.spreadsheets.destinations.sarto_inventory import Sarto_Inventory_Spreadsheet_Destination
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base
from modules.worksheets.data import Bdfs_Worksheet_Data
from modules.worksheets.destination import Bdfs_Worksheet_Destination
from modules.worksheets.exception import Bdfs_Worksheet_Destination_Exception

if __name__ == "__main__":

    migrator = Originalbdfs_Inventory_To_Sarto_Inventory()
    migrator.run()