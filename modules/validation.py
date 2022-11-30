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
            raise ValidationException("{} was passed as None, but needs to be set".format(param))
        return True


    def validation_isType(self, item, param, paramValue=None):
        self._method("validation_isType", locals())

        if not Helper.isType(item, paramValue):
            raise ValidationException("{} was expected to be type {}, but {} was found for {}".format(param, item, str(type(paramValue)), param))
        return True

    def validation_ifSetType(self, item, param, paramValue=None):
        self._method("validation_ifSetType", locals())        

        if not None == paramValue:
            self.validation_isType(item, param, paramValue)

    def validate_oneOf(self, item, param, paramValue):
        self._method("validate_oneOf", locals())

        if not Helper.existsInStr(",", item):
            raise ValidationException("oneOf validation expects a comma seperated list of items to check against")

        items = item.split(",")
        
        if Helper.existsIn(item=param, lookIn=items):
            return True
        else:
            raise ValidationException("One of {} was expected, but {} was found for parameter {}".format(item, paramValue,param))

    ####
    #
    # Validators: Math
    #
    ####

    def validation_gt(self, item, param, paramValue=None):
        self._method("validation_gt", locals())
        if paramValue < int(item):
            raise ValidationException("{} was expected to be gt than {}".format(paramValue, item))
        return True
