import sys, time
from collections import OrderedDict

from modules.dataMoves.originalbdfs_inventory.sarto_inventory.sarto import Originalbdfs_Inventory_To_Sarto_Inventory

if __name__ == "__main__":

    migrator = Originalbdfs_Inventory_To_Sarto_Inventory()
    migrator.run()