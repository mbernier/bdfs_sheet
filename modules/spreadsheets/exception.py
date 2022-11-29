from modules.exception import BdfsException

class SpreadSheetException(BdfsException):
    def __init__(self, message="Helper Exception raised"):
        self.message = message
        super().__init__(self.message)