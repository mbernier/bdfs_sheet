import sys
from modules.helpers.exception import Helper_Exception
from gspread.worksheet import Worksheet
# from multipledispatch import dispatch
from pydoc import locate

class Helper:
    
    def __init__(self):
        pass

    ####
    #
    # Dynamic calling functionality
    #
    ####
    @staticmethod
    def importClass(modulePath):
        spltz = modulePath.split(".")
        classname = spltz.pop()
        path = ".".join(spltz)
        mod = __import__(path, fromlist=[classname])
        klass = getattr(mod, classname)
        return klass

    @staticmethod
    def callMethod(*args, **kwargs):

        if "klass" not in kwargs.keys():
            raise Helper_Exception('klass param must be defined for callMethod()')

        klass = kwargs['klass']
        del kwargs['klass']

        if type(klass) is str:
            raise Helper_Exception('klass param must be an instance of a class and not a str')

        if "methodName" not in kwargs.keys():
            raise Helper_Exception("'methodName' must be passed to Helper.callMethod()")

        # get the method name off the function call    
        methodName = kwargs['methodName']
        del kwargs['methodName']

        alternateKlass = None
        if "alternateKlass" in kwargs.keys():
            alternateKlass = kwargs['alternateKlass']
            
            if type(alternateKlass) is str:
                raise Helper_Exception('alternateKlass param must be an instance of a class and not a str')

            # remove from params
            del kwargs['alternateKlass']


        # make sure that this method exists and that we can call it
        if Helper.classHasMethod(klass=klass, methodName=methodName) and callable(validFunc := getattr(klass, methodName)):
        
            return validFunc(*args, **kwargs)
        
        elif None != alternateKlass:            

            if Helper.classHasMethod(klass=alternateKlass, methodName=methodName) and callable(validFunc := getattr(alternateKlass, methodName)):
                return validFunc(*args, **kwargs)
            else:

                raise Helper_Exception("Tried to call {}.{}({}) and {}.{}({}) but no method with that name exists in either class"
                                        .format(Helper.className(klass), methodName, Helper.prepArgs(args,**kwargs), 
                                                Helper.className(alternateKlass), methodName, Helper.prepArgs(args, **kwargs)))        

        else:
            # if we get here, we didn't find the method
            raise Helper_Exception("Tried to call {}.{}({}) but no method with that name exists".format(Helper.className(klass), methodName, Helper.prepArgs(args,**kwargs)))



    @staticmethod
    def classHasMethod(klass, methodName):
        return hasattr(klass, methodName)

    @staticmethod
    def className(klass=None):
        return klass.__class__.__name__


    ####
    #
    # Helper Methods for repeated functionality
    #
    ####

    #does list1 contain everything in list2?
    @staticmethod
    def compareLists(list1, list2) -> bool:
        result =  all(elem in list1 for elem in list2)
        return result


    @staticmethod
    def existsIn(item, lookIn):
        
        if Helper.is_dict(lookIn):
            return Helper.existsInDict(item, lookIn)

        elif Helper.is_list(lookIn):
            return Helper.existsInList(item, lookIn)
        
        elif Helper.is_str(lookIn):
            return Helper.existsInStr(item, lookIn)

        else:
            raise Helper_Exception("No existsIn validation method exists for {}".format(type(lookIn)))


    @staticmethod
    def existsInDict(item, lookIn):
        return item in lookIn.keys()


    @staticmethod
    def existsInList(item, lookIn):
        return item in lookIn


    @staticmethod
    def existsInStr(item, lookIn):
        return item in lookIn

    
    @staticmethod
    def isType(typeName, item):

        # typeName = typeName.lower()
        helper = Helper()
        methodName = f"is_{typeName}"

        if Helper.classHasMethod(helper, methodName):
            return Helper.callMethod(klass=helper, methodName=methodName, item=item)

        # raise Exception for everything else
        raise Helper_Exception("isType doesn't know about type '{}'".format(typeName))

    @staticmethod 
    def is_dict(item):
        return isinstance(item, dict)

    @staticmethod
    def is_int(item):
        # true returns as type int... of course
        if Helper.is_bool(item):
            return False
        return isinstance(item, int)

    @staticmethod
    def is_bool(item):
        return isinstance(item, bool)

    @staticmethod
    def is_list(item):
        return isinstance(item, list)

    @staticmethod
    def is_str(item):
        return isinstance(item, str)

    @staticmethod
    def is_Nested_Cache(item):
        from modules.caches.nested import Nested_Cache
        return isinstance(item, Nested_Cache)

    @staticmethod
    def is_Nested_Cache_Rows_Location(item):
        from modules.caches.nested_cache.rows.location import Nested_Cache_Rows_Location
        return isinstance(item, Nested_Cache_Rows_Location)

    @staticmethod
    def is_Flat_Cache(item):
        from modules.caches.flat import Flat_Cache
        return isinstance(item, Flat_Cache)

    @staticmethod
    def is_tuple(item):
        from modules.caches.nested import Nested_Cache
        return isinstance(item, tuple)

    @staticmethod
    def output_dir(item):
        dirs = dir(item)
        # print(dirs)
        for dirItem in dirs:
            print(f"{dirItem}:{getattr(item, dirItem)}")

    # There is a copy of this in decorators.py, so that we can reduce cyclical imports
    @staticmethod
    def prepArgs(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        
        return args_repr, kwargs_repr

