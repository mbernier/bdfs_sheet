from modules.worksheets.source import Bdfs_Worksheet_Source
from modules.logger import logger_name

logger_name.name = "Test_Worksheet_Source"

class Test_Worksheet_Source(Bdfs_Worksheet_Source):
    cols_expected = ['Name', 'Birthday', 'Email']

    cols_expected_extra = {}

    def __init__(self, worksheet):
        super().__init__(worksheet)