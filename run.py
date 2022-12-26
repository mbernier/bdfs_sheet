from modules.dataMoves.originalbdfs_inventory.sarto_inventory.sarto import Originalbdfs_Inventory_To_Sarto_Inventory
from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base
from modules.spreadsheets.destinations.sarto_inventory import Sarto_Inventory_Spreadsheet_Destination
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.caches.nested import Nested_Cache

if __name__ == "__main__":

    # migrator = Originalbdfs_Inventory_To_Sarto_Inventory()
    # migrator.run()


    cache = Nested_Cache(['b','c','d','e','f'],[[3,4,5,6,7],[1,2,3,4,5]], 'b')
    cache.update(row=0, position='b', data=1)
    print(cache.getUniques())