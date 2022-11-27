import sys
from modules.base import BaseClass


class MethodValidation(BaseClass):
    _params = []
    _validations = []
    _setup = {}
    _validated = []
    _methodName = ""

    def __init__(self, methodName, params, validations):
        self._params = params
        self._validate = validate
        self._methodName = methodName

        self.__checkParams()


    def __checkParams(self): 
        for param in self._params:
            self.__setupParam(param)

    def __setupParams(self, param=None):
        self.debug("__checkParams(param={})".format(param))

        setup = {param: {"inValidate": False, "inParams": False}}

        if paramName in self.getParams():
            param = params[paramName]
            methodString = "{}={}".format(paramName, param)
        else:
            inParams = False

        if paramName in self.getValidations():
            inValidate = True
            if not inParams:
                raise NestedCacheException("'{}' was requested as validation in __setupMethod(), but it was not passed in params to be validated".format(paramName))

        return param, inValidate, methodString, validate.remove(paramName)

    def getParams(self):
        return self._params

    def getValidations(self):
        return self._validations