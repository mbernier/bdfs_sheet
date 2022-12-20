from modules.worksheets.source import Bdfs_Worksheet_Source
from modules.logger import logger_name

logger_name.name = "BdfsInventory_Test_Worksheet_Source"

class BdfsInventory_Test_Worksheet_Source(Bdfs_Worksheet_Source):
    def __init__(self, worksheet):
        super().__init__(worksheet)