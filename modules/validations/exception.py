from modules.exception import BdfsException

class ValidationException(BdfsException):
    def __init__(self, message="Validation Exception raised"):
        self.message = message
        super().__init__(self.message)

class FieldValidationException(ValidationException):
    def __init__(self, message="FieldValidation Exception raised"):
        self.message = message
        super().__init__(self.message)

class MethodValidationException(ValidationException):
    def __init__(self, message="FieldValidation Exception raised"):
        self.message = message
        super().__init__(self.message)