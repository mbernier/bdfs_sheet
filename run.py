from modules.dataMoves.originalbdfs_inventory.sarto_inventory.sarto import Originalbdfs_Inventory_To_Sarto_Inventory
from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base
from modules.spreadsheets.destinations.sarto_inventory import Sarto_Inventory_Spreadsheet_Destination
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.caches.nested import Nested_Cache

if __name__ == "__main__":

    migrator = Originalbdfs_Inventory_To_Sarto_Inventory()
    migrator.run()