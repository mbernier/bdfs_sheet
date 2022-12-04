from modules.exception import BdfsException

class Decorator_Exception(BdfsException):
    def __init__(self, message="Decorator Exception raised"):
        self.message = message
        super().__init__(self.message)    