from modules.exception import BdfsException
from modules.validations.exception import Validation_Exception

class Cache_Exception(BdfsException):
    def __init__(self, message="Cache Exception raised"):
        self.message = message
        super().__init__(self.message)    

class Flat_Cache_Exception(Cache_Exception):
    def __init__(self, message="Flat_Cache Exception raised"):
        self.message = message
        super().__init__(self.message)

class Nested_Cache_Row_Exception(Flat_Cache_Exception):
    def __init__(self, message="Flat_Cache Exception raised"):
        self.message = message
        super().__init__(self.message)

class Nested_Cache_Exception(Cache_Exception):
    def __init__(self, message="Nested_Cache Exception raised"):
        self.message = message
        super().__init__(self.message)