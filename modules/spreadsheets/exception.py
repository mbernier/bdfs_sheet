from modules.exception import Bdfs_Exception

class Bdfs_Spreadsheet_Exception(Bdfs_Exception):
    def __init__(self, message="Spreadsheet_Exception raised"):
        self.message = message
        super().__init__(self.message)

class Bdfs_Spreadsheet_Source_Exception(Bdfs_Spreadsheet_Exception):
    def __init__(self, message="Spreadsheet_Source_Exception raised"):
        self.message = message
        super().__init__(self.message)

class Bdfs_Spreadsheet_Destination_Exception(Bdfs_Spreadsheet_Exception):
    def __init__(self, message="Spreadsheet_Source_Exception raised"):
        self.message = message
        super().__init__(self.message)