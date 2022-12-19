from modules.exception import BdfsException

class Bdfs_Worksheet_Exception(BdfsException):
    def __init__(self, message="Helper Exception raised"):
        self.message = message
        super().__init__(self.message)

class Bdfs_Worksheet_Data_Exception(BdfsException):
    def __init__(self, message="Helper Exception raised"):
        self.message = message
        super().__init__(self.message)