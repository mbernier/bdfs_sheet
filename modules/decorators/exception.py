from modules.exception import Bdfs_Exception

class Decorator_Exception(Bdfs_Exception):
    def __init__(self, message="Decorator Exception raised"):
        self.message = message
        super().__init__(self.message)    