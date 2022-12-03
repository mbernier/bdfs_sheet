import sys
from modules.logger import Logger
from modules.helper import Helper
from modules.validations.exception import ValidationException


class Validation(Logger):

    def __init__(self, classBeingValidated, **kwargs):

        self._classBeingValidated = classBeingValidated
        self.__doValidations()


    def __doValidations(self):
        raise ValidationException("You must create a __doValidations method")

    ####
    #
    # Validators: Existence
    #
    ####

    def validation_notNone(self, param, paramValue=None):
        self._method("validation_notNone", locals())

        if None == paramValue:
            raise ValidationException("{} was passed as None, but needs to be set for method {}".format(param, self._field))
        return True


    def validation_isType(self, item, param, paramValue=None):
        self._method("validation_isType", locals())

        if not Helper.isType(item, paramValue):
            raise ValidationException("{} was expected to be type {}, but {} was found for method {}".format(param, item, str(type(paramValue)), param), self._field)
        return True

    def validation_ifSetType(self, item, param, paramValue=None):
        self._method("validation_ifSetType", locals())        

        if not None == paramValue:
            self.validation_isType(item, param, paramValue)

    def validation_contains(self, item, param, paramValue):
        self._method("validate_contains", locals())

        if not Helper.existsInStr(",", item):
            raise ValidationException("'contains' validation expects a comma seperated list of items to check against, '{}' was found for method {}".format(item, self._field))

        items = item.split(",")
        
        if Helper.existsIn(item=paramValue, lookIn=items):
            return True
        else:
            raise ValidationException("One of [{}] was expected, but '{}' was found for parameter {} for method {}".format(item, paramValue,param, self._field))

    ####
    #
    # Validators: Math
    #
    ####

    def validation_gt(self, item, param, paramValue=None):
        self._method("validation_gt", locals())

        if self.validation_isType('int', param, paramValue) and paramValue <= int(item):
            raise ValidationException("{} was expected to be greater than {}, {} was found for method {}".format(param, item, paramValue, self._field))
        return True

    def validation_gte(self, item, param, paramValue=None):
        self._method("validation_gte", locals())

        self.validation_isType('int', param, paramValue)

        if self.validation_isType('int', param, paramValue) and paramValue < int(item):
            raise ValidationException("{} was expected to be greater than or equal to {}, {} was found for method {}".format(param, item, paramValue, self.field))
        return True
