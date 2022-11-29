from modules.exception import BdfsException

class DecoratorException(BdfsException):
    def __init__(self, message="Decorator Exception raised"):
        self.message = message
        super().__init__(self.message)    