from modules.dataMoves.originalbdfs_inventory.sarto_inventory.sarto import Originalbdfs_Inventory_To_Sarto_Inventory
from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base

if __name__ == "__main__":

    migrator = Originalbdfs_Inventory_To_Sarto_Inventory()
    migrator.run()