from modules.exception import Bdfs_Exception

class Bdfs_Worksheet_Exception(Bdfs_Exception):
    def __init__(self, message="Bdfs_Worksheet_Exception raised"):
        self.message = message
        super().__init__(self.message)

class Bdfs_Worksheet_Data_Exception(Bdfs_Exception):
    def __init__(self, message="Bdfs_Worksheet_Data_Exception raised"):
        self.message = message
        super().__init__(self.message)

class Bdfs_Worksheet_Source_Exception(Bdfs_Worksheet_Exception):
    def __init__(self, message="Bdfs_Worksheet_Source_Exception raised"):
        self.message = message
        super().__init__(self.message)

class Bdfs_Worksheet_Destination_Exception(Bdfs_Worksheet_Exception):
    def __init__(self, message="Bdfs_Worksheet_Source_Exception raised"):
        self.message = message
        super().__init__(self.message)