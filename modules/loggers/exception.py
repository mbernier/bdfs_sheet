from modules.exception import Bdfs_Exception

class Logger_Exception(Bdfs_Exception):
    def __init__(self, message="Helper Exception raised"):
        self.message = message
        super().__init__(self.message)