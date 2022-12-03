import sys
from modules.logger import Logger
from modules.helper import Helper
from modules.validation import Validation
from modules.validations.field import FieldValidation
from modules.validations.exception import MethodValidationException

class MethodValidation(Validation):

    # example payload, the only defined parameter is classBeingValidated, otherwise it is all params that are being passed
    # {
    #     'classBeingValidated': <modules.caches.nested.NestedCache object at 0x79eae58aea00>, 
    #     'locations': {
    #         'validations': ['notNone', 'isType:list'], 
    #         'data': ['col1', 'col2', 'col3']}, 
    #     'data': {
    #         'validations': ['notNone', 'isType:list'], 
    #         'data': []}
    # }
    def __init__(self, classBeingValidated, method, **kwargs):

        self._classBeingValidated = classBeingValidated
        self._field = method
        self.__doValidations(kwargs)


    def __doValidations(self, paramData):
        
        passTheseArgs = {}

        # set up the args dict for passing to FieldValidation
        for key in paramData:
            passTheseArgs[key] = paramData[key]['data']

        for key in paramData:
            # print((self._classBeingValidated, key,  paramData[key]['validations'], passTheseArgs))
            #            FieldValidations(classBeingValidated, field, validations, args)
            validation = FieldValidation(classBeingValidated=self._classBeingValidated, 
                                            method=self._field,
                                            field=key,
                                            validations=paramData[key]['validations'], 
                                            paramValues=passTheseArgs)