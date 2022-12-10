import sys
from modules.config import config
from modules.helper import Helper
from modules.validations.exception import Validation_Exception


class Validation_Data():
    classBeingValidated = None

class Validation():

    def __init__(self, classBeingValidated):
        self.data = Validation_Data()
        self.data.classBeingValidated = classBeingValidated
        self.__doValidations()


    def __doValidations(self):
        raise Validation_Exception("You must create a __doValidations method")



    # Calls the logging method of the class that owns the method we are validating, instead of
    #   Needing to call Validation._methodName - thus removing the looping dependency on logger from Validation
    #   while also allowing the same signature for calling all the way through, no human needs to remember
    #   anything different than what we're doing in all the other classes in this code base
    def _method(self, method, data=None):

        if None == self.data.classBeingValidated:
            raise Validation_Exception("_classBeingValidated must be set before calling self._method() in any Validation class")

        if True == config("debug_validations"):
            # call the validation_method_debug function on the class that owns the method we're validating
            #   allows for overriding whether we even output this data, based on the config.ini
            self.data.classBeingValidated.validation_method_debug(method, data)


    def __getParamValues(self):
        self._method("__getParamValues")
        return self.data.paramValues


    def __getParamValue(self, param):
        self._method("__getParamValue", locals())
        return self.__getParamValues()[param]

    ####
    #
    # Validators: Existence
    #
    ####

    def validation_notNone(self, param, paramValue=None):
        self._method("validation_notNone", locals())

        if None == paramValue:
            raise Validation_Exception("{} was passed as None, but needs to be set for method {}".format(param, self.data.methodName))
        return True


    def validation_isType(self, item, param, paramValue=None):
        self._method("validation_isType", locals())

        if Helper.existsInStr(",", item): # we have more than one type that this thing can be, so call multiple
            return self.validation_isType_multiple(item, param, paramValue)

        if not Helper.isType(item, paramValue):
            raise Validation_Exception("{} was expected to be type {}, but {} was found for method {}".format(param, item, str(type(paramValue)), self.data.methodName))
        return True


    def validation_isType_multiple(self, item, param, paramValue=None):
        self._method("validatation_isType_multiple", locals())

        if not Helper.existsInStr(",", item):
            raise Validation_Exception("validation_isType_multiple expects a comma separated list of types {} was found for method {}".format(item, self.data.methodName))
        spltz = item.split(",")

        response = False
        for isType in spltz:
            # if we get an expected type, return True and stop processing
            if Helper.isType(isType, paramValue):
                return True

        # we didn't get any of the types that we expected
        raise Validation_Exception("validation_isType_multiple expected {} to be one of {} but {} was found with value {} for method {}".format(param, item, type(paramValue), paramValue, self.data.methodName))


    def validation_ifSetType(self, item, param, paramValue=None):
        self._method("validation_ifSetType", locals())        

        if not None == paramValue:
            self.validation_isType(item, param, paramValue)

    def validation_ifSet(self, item, param, paramValue=None):
        self._method("validation_ifSet", locals())

        # prep for being a validation method
        item = f"validation_{item}"

        if not None == paramValue:
            Helper.callMethod(klass=self, alternateKlass=self.data.classBeingValidated, methodName=item, param=param, paramValue=paramValue)


    def validation_contains(self, item, param, paramValue):
        self._method("validate_contains", locals())

        if not Helper.existsInStr(",", item):
            raise Validation_Exception("'contains' validation expects a comma seperated list of items to check against, '{}' was found for method {}".format(item, self.data.methodName))

        items = item.split(",")
        
        if Helper.existsIn(item=paramValue, lookIn=items):
            return True
        else:
            raise Validation_Exception("One of [{}] was expected, but '{}' was found for parameter {} for method {}".format(item, paramValue,param, self.data.methodName))

    ####
    #
    # Validators: Math
    #
    ####

    # takes in a [gt:1]
    def validation_gt(self, item, param, paramValue=None):
        self._method("validation_gt", locals())

        if self.validation_isType('int', param, paramValue) and paramValue <= int(item):
            raise Validation_Exception("{} was expected to be greater than {}, {} !> {} for method {}".format(param, item, paramValue, item, self.data.methodName))
        return True

    # takes in a [gte:1]
    def validation_gte(self, item, param, paramValue=None):
        self._method("validation_gte", locals())

        self.validation_isType('int', param, paramValue)

        if self.validation_isType('int', param, paramValue) and paramValue < int(item):
            raise Validation_Exception("{} was expected to be greater than or equal to {}, {} was found for method {}".format(param, item, paramValue, self.data.methodName))
        return True

    # takes in a [lt:1]
    def validation_lt(self, item, param, paramValue=None):
        self._method("validation_lt", locals())

        if self.validation_isType('int', param, paramValue) and paramValue >= int(item):
            raise Validation_Exception("{} was expected to be less than {}, {} was found for method {}".format(param, item, paramValue, self.data.methodName))
        return True

    # takes in a [lte:1]
    def validation_lte(self, item, param, paramValue=None):
        self._method("validation_lte", locals())

        if self.validation_isType('int', param, paramValue) and paramValue > int(item):
            raise Validation_Exception("{} was expected to be less than or equal to {}, {} was found for method {}".format(param, item, paramValue, self.data.methodName))
        return True

    ####
    #
    # Validators: Math, param comparison
    #
    ####


    # takes in a [lt_param:{fieldName}]
    def validation_lt_param(self, item:str, param:str, paramValue:int=None):
        self._method("validation_field_lt", locals())
        item = int(self.__getParamValue(item))

        if self.validation_isType('int', param, paramValue) and paramValue >= item:
            raise Validation_Exception("{} was expected to be less than {}, {} was found for method {}".format(param, item, paramValue, self.data.methodName))
        return True

    # takes in a [lte_param:{fieldName}]
    def validation_lte_param(self, item:str, param:str, paramValue:int=None):
        self._method("validation_field_lte", locals())
        item = int(self.__getParamValue(item))

        if self.validation_isType('int', param, paramValue) and paramValue > item:
            raise Validation_Exception("{} was expected to be less than or equal to {}, {} was found for method {}".format(param, item, paramValue, self.data.methodName))
        return True

    # takes in a [gt_param:{fieldName}]
    def validation_gt_param(self, item:str, param:str, paramValue:int=None):
        self._method("validation_field_gt", locals())
        item = int(self.__getParamValue(item))

        if self.validation_isType('int', param, paramValue) and paramValue <= item:
            raise Validation_Exception("{} was expected to be greater than {}, {} was found for method {}".format(param, item, paramValue, self.data.methodName))
        return True

    # takes in a [lte_param:{fieldName}]
    def validation_gte_param(self, item:str, param:str, paramValue:int=None):
        self._method("validation_field_gte", locals())
        item = int(self.__getParamValue(item))

        if self.validation_isType('int', param, paramValue) and paramValue < item:
            raise Validation_Exception("{} was expected to be greater than or equal to {}, {} was found for method {}".format(param, item, paramValue, self.data.methodName))
        return True