from modules.worksheets.destination import Bdfs_Worksheet_Destination
from modules.logger import logger_name

logger_name.name = "Test_Worksheet_Destination"

class Test_Worksheet_Destination(Bdfs_Worksheet_Destination):
    cols_expected = ['Name', 'Birthday', 'Email']

    cols_expected_extra = {}

    def __init__(self, worksheet):
        super().__init__(worksheet)