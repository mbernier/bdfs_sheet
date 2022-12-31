import sys, time
from collections import OrderedDict
# from modules.dataMoves.originalbdfs_inventory.sarto_inventory.sarto import Originalbdfs_Inventory_To_Sarto_Inventory

if __name__ == "__main__":

    # migrator = Originalbdfs_Inventory_To_Sarto_Inventory()
    # migrator.run()
    od1 = OrderedDict({"one":1, "two":2})
    od2 = OrderedDict({"three":1, "four":2, "one":200})
    print(od1.extend(od2))
    
    