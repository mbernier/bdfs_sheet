

class CacheException(Exception):
    def __init__(self, message="Cache Exception raised"):
        self.message = message
        super().__init__(self.message)    

class FlatCacheException(CacheException):
    """Exception raised for errors in the cache functionality.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Cache Exception raised"):
        self.message = message
        super().__init__(self.message)

class NestedCacheException(CacheException):
    def __init__(self, message="Cache Exception raised"):
        self.message = message
        super().__init__(self.message)