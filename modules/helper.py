from modules.helpers.exception import HelperException

class Helper:
    

    ####
    #
    # Dynamic calling functionality
    #
    ####
    @staticmethod
    def callMethod(klass=None, *args, **kwargs):

        # get the method name off the function call    
        methodName = kwargs['methodName']
        del kwargs['methodName']

        # make sure that this method exists and that we can call it
        if Helper.classHasMethod(klass, methodName) and callable(validFunc := getattr(klass, methodName)):
            return validFunc(**kwargs)
        else:
            raise HelperException("Tried to call {}.{} but no method with that name exists".format(Helper.className(klass), methodName))

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
    def compareLists(list1, list2) -> list:
        result =  all(elem in list1 for elem in list2)
        return result


    @staticmethod
    def checkArgs(required=[], **kwargs):
        for arg in kwargs:
            if arg in required and None == kwargs[arg]:
                raise HelperException("You must pass {} to Cache, NoneType was found".format(arg))


    @staticmethod
    def existsIn(item, lookIn):
        
        if Helper.is_dict(lookIn):
            return Helper.existsInDict(item, lookIn)

        elif Helper.is_list(lookIn):
            return Helper.existsInList(item, lookIn)
        
        elif Helper.is_str(lookIn):
            return Helper.existsInStr(item, lookIn)
        
        else:
            raise HelperException("No existsIn validation method exists for {}".format(lookInType))


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
    def isType(type, item):
        type = type.lower()

        if type == 'dict':
            return Helper.is_dict(item)

        if type == 'list':
            return Helper.is_list(item)

        if type == 'int':
            return Helper.is_int(item)

        if type == 'str':
            return Helper.is_str(item)

        if type == 'flatcache':
            return Helper.is_flatcache(item)

        if type == 'Nestedcache':
            return Helper.is_nestedcache(item)

        # raise Exception for everything else
        raise HelperException("isType doesn't know about type '{}'".format(type))

    @staticmethod
    def is_dict(item):
        return isinstance(item, dict)

    @staticmethod
    def is_int(item):
        return isinstance(item, int)

    @staticmethod
    def is_list(item):
        return isinstance(item, list)

    @staticmethod
    def is_str(item):
        return isinstance(item, str)

    @staticmethod
    def is_nestedcache(item):
        return isinstance(item, NestedCache)

    @staticmethod
    def is_flatcache(item):
        from modules.caches.flat import FlatCache
        return isinstance(item, FlatCache)

    def is_tuple(item):
        from modules.caches.nested import NestedCache
        return isinstance(item, tuple)
