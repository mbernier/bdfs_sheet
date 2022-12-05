import sys
from modules.config import config
from modules.helper import Helper
from modules.validations.exception import Validation_Exception


class Validation():

    def __init__(self, classBeingValidated):
        self._classBeingValidated = classBeingValidated
        self.__doValidations()


    def __doValidations(self):
        raise Validation_Exception("You must create a __doValidations method")



    # Calls the logging method of the class that owns the method we are validating, instead of
    #   Needing to call Validation._methodName - thus removing the looping dependency on logger from Validation
    #   while also allowing the same signature for calling all the way through, no human needs to remember
    #   anything different than what we're doing in all the other classes in this code base
    def _method(self, method, data=None):

        if None == self._classBeingValidated:
            raise Validation_Exception("_classBeingValidated must be set before calling self._method() in any Validation class")

        # call the validation_method_debug function on the class that owns the method we're validating
        #   allows for overriding whether we even output this data, based on the config.ini
        self._classBeingValidated.validation_method_debug(method, data)

    ####
    #
    # Validators: Existence
    #
    ####

    def validation_notNone(self, param, paramValue=None):
        self._method("validation_notNone", locals())

        if None == paramValue:
            raise Validation_Exception("{} was passed as None, but needs to be set for method {}".format(param, self._methodName))
        return True


    def validation_isType(self, item, param, paramValue=None):
        self._method("validation_isType", locals())

        if not Helper.isType(item, paramValue):
            raise Validation_Exception("{} was expected to be type {}, but {} was found for method {}".format(param, item, str(type(paramValue)), self._methodName))
        return True

    def validation_ifSetType(self, item, param, paramValue=None):
        self._method("validation_ifSetType", locals())        

        if not None == paramValue:
            self.validation_isType(item, param, paramValue)

    def validation_contains(self, item, param, paramValue):
        self._method("validate_contains", locals())

        if not Helper.existsInStr(",", item):
            raise Validation_Exception("'contains' validation expects a comma seperated list of items to check against, '{}' was found for method {}".format(item, self._methodName))

        items = item.split(",")
        
        if Helper.existsIn(item=paramValue, lookIn=items):
            return True
        else:
            raise Validation_Exception("One of [{}] was expected, but '{}' was found for parameter {} for method {}".format(item, paramValue,param, self._methodName))

    ####
    #
    # Validators: Math
    #
    ####

    def validation_gt(self, item, param, paramValue=None):
        self._method("validation_gt", locals())

        if self.validation_isType('int', param, paramValue) and paramValue <= int(item):
            raise Validation_Exception("{} was expected to be greater than {}, {} was found for method {}".format(param, item, paramValue, self._methodName))
        return True

    def validation_gte(self, item, param, paramValue=None):
        self._method("validation_gte", locals())

        self.validation_isType('int', param, paramValue)

        if self.validation_isType('int', param, paramValue) and paramValue < int(item):
            raise Validation_Exception("{} was expected to be greater than or equal to {}, {} was found for method {}".format(param, item, paramValue, self._methodName))
        return True
