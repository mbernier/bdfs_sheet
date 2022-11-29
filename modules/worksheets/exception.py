from modules.exception import BdfsException

class WorksheetException(BdfsException):
    def __init__(self, message="Helper Exception raised"):
        self.message = message
        super().__init__(self.message)