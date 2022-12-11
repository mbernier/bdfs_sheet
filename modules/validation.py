import sys
from modules.config import config
from modules.helper import Helper
from modules.logger import Logger
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
            raise Validation_Exception("_classBeingValidated must be set before calling Logger.validation_method_debug() in any Validation class")

        if True == config("debug_validations"):
            # call the validation_method_debug function on the class that owns the method we're validating
            #   allows for overriding whether we even output this data, based on the config.ini
            self.data.classBeingValidated.validation_method_debug(method, data)


    def __getParamValues(self):
        Logger.validation_method_debug("__getParamValues")
        return self.data.paramValues


    def __getParamValue(self, param):
        Logger.validation_method_debug("__getParamValue", locals())
        return self.__getParamValues()[param]

    ####
    #
    # Validators: Existence
    #
    ####

    @staticmethod
    def validation_notNone(param, paramValue=None):
        Logger.validation_method_debug("validation_notNone", locals())

        if None == paramValue:
            raise Validation_Exception("{} was passed as None, but needs to be set".format(param))
        return True


    @staticmethod
    def validation_isType(item, param, paramValue=None):
        Logger.validation_method_debug("validation_isType", locals())

        if Helper.existsInStr(",", item): # we have more than one type that this thing can be, so call multiple
            return Validation.validation_isType_multiple(item, param, paramValue)

        if not Helper.isType(item, paramValue):
            raise Validation_Exception("{} was expected to be type {}, but {} was found".format(param, item, str(type(paramValue))))
        return True

    @staticmethod
    def validation_isType_multiple(item, param, paramValue=None):
        Logger.validation_method_debug("validatation_isType_multiple", locals())

        if not Helper.existsInStr(",", item):
            raise Validation_Exception("validation_isType_multiple expects a comma separated list of types {} was found".format(item))
        spltz = item.split(",")

        response = False
        for isType in spltz:
            # if we get an expected type, return True and stop processing
            if Helper.isType(isType, paramValue):
                return True

        # we didn't get any of the types that we expected
        raise Validation_Exception("validation_isType_multiple expected {} to be one of {} but {} was found with value {}".format(param, item, type(paramValue), paramValue))


    @staticmethod
    def validation_ifSetType(item, param, paramValue=None):
        Logger.validation_method_debug("validation_ifSetType", locals())        

        if not None == paramValue:
            Validation.validation_isType(item, param, paramValue)

    @staticmethod
    def validation_ifSet(item, param, paramValue=None):
        Logger.validation_method_debug("validation_ifSet", locals())

        # prep for being a validation method
        item = f"validation_{item}"

        if not None == paramValue:
            Helper.callMethod(klass=self, alternateKlass=self.data.classBeingValidated, methodName=item, param=param, paramValue=paramValue)

    @staticmethod
    def validation_contains(item, param, paramValue):
        Logger.validation_method_debug("validate_contains", locals())

        if not Helper.existsInStr(",", item):
            raise Validation_Exception("'contains' validation expects a comma seperated list of items to check against, '{}' was found".format(item))

        items = item.split(",")
        
        if Helper.existsIn(item=paramValue, lookIn=items):
            return True
        else:
            raise Validation_Exception("One of [{}] was expected, but '{}' was found for parameter {}".format(item, paramValue,param))

    ####
    #
    # Validators: Math
    #
    ####

    # takes in a [gt:1]
    @staticmethod
    def validation_gt(item, param, paramValue=None):
        Logger.validation_method_debug("validation_gt", locals())

        if Validation.validation_isType('int', param, paramValue) and paramValue <= int(item):
            raise Validation_Exception("{} was expected to be greater than {}, {} !> {}".format(param, item, paramValue, item))
        return True

    # takes in a [gte:1]
    @staticmethod
    def validation_gte(item, param, paramValue=None):
        Logger.validation_method_debug("validation_gte", locals())

        Validation.validation_isType('int', param, paramValue)

        if Validation.validation_isType('int', param, paramValue) and paramValue < int(item):
            raise Validation_Exception("{} was expected to be greater than or equal to {}, {} was found".format(param, item, paramValue))
        return True

    # takes in a [lt:1]
    @staticmethod
    def validation_lt(item, param, paramValue=None):
        Logger.validation_method_debug("validation_lt", locals())

        if Validation.validation_isType('int', param, paramValue) and paramValue >= int(item):
            raise Validation_Exception("{} was expected to be less than {}, {} was found".format(param, item, paramValue))
        return True

    # takes in a [lte:1]
    @staticmethod
    def validation_lte(item, param, paramValue=None):
        Logger.validation_method_debug("validation_lte", locals())

        if Validation.validation_isType('int', param, paramValue) and paramValue > int(item):
            raise Validation_Exception("{} was expected to be less than or equal to {}, {} was found".format(param, item, paramValue))
        return True

    ####
    #
    # Validators: Math, param comparison
    #
    ####


    # takes in a [lt_param:{fieldName}]
    @staticmethod
    def validation_lt_param(item:str, param:str, paramValue:int=None):
        Logger.validation_method_debug("validation_field_lt", locals())

        if Validation.validation_isType('int', param, paramValue) and paramValue >= item:
            raise Validation_Exception("{} was expected to be less than {}, {} was found".format(param, item, paramValue))
        return True

    # takes in a [lte_param:{fieldName}]
    @staticmethod
    def validation_lte_param(item:str, param:str, paramValue:int=None):
        Logger.validation_method_debug("validation_field_lte", locals())

        if Validation.validation_isType('int', param, paramValue) and paramValue > item:
            raise Validation_Exception("{} was expected to be less than or equal to {}, {} was found".format(param, item, paramValue))
        return True

    # takes in a [gt_param:{fieldName}]
    @staticmethod
    def validation_gt_param(item:str, param:str, paramValue:int=None):
        Logger.validation_method_debug("validation_field_gt", locals())
        

        if Validation.validation_isType('int', param, paramValue) and paramValue <= item:
            raise Validation_Exception("{} was expected to be greater than {}, {} was found".format(param, item, paramValue))
        return True

    # takes in a [lte_param:{fieldName}]
    @staticmethod
    def validation_gte_param(item:str, param:str, paramValue:int=None):
        Logger.validation_method_debug("validation_field_gte", locals())
        

        if Validation.validation_isType('int', param, paramValue) and paramValue < item:
            raise Validation_Exception("{} was expected to be greater than or equal to {}, {} was found".format(param, item, paramValue))
        return True


    @staticmethod
    def validation_oneIsNotNone(item1, item2):
        Logger.method("validation_oneIsNotNone", locals())
        
        # if either of these are false, then we are good to go
        paramNotNone = (None != item1)
        otherParamNotNone = (None != item2)

        if False == paramNotNone and False == otherParamNotNone:
            raise Validation_Exception("Either {} or {} was expected to not be 'None'".format(item1, item2))
        return True    