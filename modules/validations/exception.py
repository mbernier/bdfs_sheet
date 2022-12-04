from modules.exception import BdfsException

class Validation_Exception(BdfsException):
    def __init__(self, message="Validation Exception raised"):
        self.message = message
        super().__init__(self.message)

class Validation_Field_Exception(Validation_Exception):
    def __init__(self, message="Validation_Field Exception raised"):
        self.message = message
        super().__init__(self.message)

class Validation_Method_Exception(Validation_Exception):
    def __init__(self, message="Validation_Field Exception raised"):
        self.message = message
        super().__init__(self.message)