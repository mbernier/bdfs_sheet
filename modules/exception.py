class Bdfs_Exception(Exception):
    def __init__(self, message="BDFS Exception raised"):
        self.message = message
        super().__init__(self.message)   