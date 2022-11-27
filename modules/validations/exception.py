class ValidationException(Exception):
    def __init__(self, message="Cache Exception raised"):
        self.message = message
        super().__init__(self.message)    

# class Exception(ValidationException):
#     """Exception raised for errors in the cache functionality.

#     Attributes:
#         message -- explanation of the error
#     """

#     def __init__(self, message="Cache Exception raised"):
#         self.message = message
#         super().__init__(self.message)