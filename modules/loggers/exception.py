from modules.exception import BdfsException

class Logger_Exception(BdfsException):
    def __init__(self, message="Helper Exception raised"):
        self.message = message
        super().__init__(self.message)