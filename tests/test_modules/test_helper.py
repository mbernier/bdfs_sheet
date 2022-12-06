import pytest, inspect, types
from modules.helper import Helper
from modules.helpers.exception import Helper_Exception

####
#
# Scenario code, giving test method something to play with
#
####

class Test:

    def methodExists(self):
        return "methodExists"

    def methodExists2(self, param):
        return "methodExists2"

    def methodExists_positional(self, one, two, three):
        return "methodExists_positional(one,two,three)"

    def methodExists_named(self, one, two, three):
        return "methodExists_named(one,two,three)"

    def methodExists_positional_named(self, one, two, three, four):
        return "methodExists_positional_named(one,two,three,four)"

class Test2:

    def another_methodExists(self):
        return "another_methodExists"

    def another_methodExists2(self):
        return "another_methodExists2"

    def another_methodExists_positional(self, one, two, three):
        return "another_methodExists_positional(one,two,three)"

    def another_methodExists_named(self, one, two, three):
        return "another_methodExists_named(one,two,three)"

    def another_methodExists_positional_named(self, one, two, three, four):
        return "another_methodExists_positional_named(one,two,three,four)"


def aMethod(*args, **kwargs):
    return Helper.prepArgs(args, **kwargs)


####
#
# Helper.classHasMethod
#
####

def test_helper_classHasMethod():
    test = Test()
    assert True == Helper.classHasMethod(test, "methodExists")
    assert False == Helper.classHasMethod(test, "someMethod")

####
#
# Helper.className
#
####

def test_className():
    test = Test()
    test2 = Test2()
    assert "Test" == Helper.className(test)
    assert "Test2" == Helper.className(test2)


####
#
# Helper.prepArgs
#
####

def test_helper_prepArgs_positional():
    value = aMethod(1,2,3)
    assert (['(1, 2, 3)'], []) == value

def test_helper_prepArgs_named():
    value = aMethod(one=1,two=2,three=3)
    assert (['()'], ['one=1', 'two=2', 'three=3']) == value

def test_helper_prepArgs_positional_and_named():
    value = aMethod(1,2,three=3,four=4)
    assert (['(1, 2)'], ['three=3', 'four=4']) == value


####
#
# Helper.callMethod, strings not classes passed
#
####

def test_helper_callMethod_klass_is_not_a_class():
    with pytest.raises(Helper_Exception) as excinfo:
        value = Helper.callMethod(klass="test", methodName="methodExists")
    assert excinfo.value.message == "klass param must be an instance of a class and not a str"


def test_helper_callMethod_alternateKlass_is_not_a_class():
    test = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        value = Helper.callMethod(klass=test, alternateKlass="testing", methodName="notAMethodThatExists")
    assert excinfo.value.message == "alternateKlass param must be an instance of a class and not a str"

####
#
# Helper.callMethod no params passed
#
####

def test_helper_callMethod():
    test = Test()
    value = Helper.callMethod(klass=test, methodName="methodExists")
    assert "methodExists" == value

def test_helper_callMethod_alternateKlass():
    test = Test()
    test2 = Test2()
    value = Helper.callMethod(klass=test, alternateKlass=test2, methodName="another_methodExists")
    assert "another_methodExists" == value

def test_helper_callMethod_fail_no_methodName():
    test = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(klass=test)
    assert excinfo.value.message == "'methodName' must be passed to Helper.callMethod()"

def test_helper_callMethod_fail():
    test = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(klass=test, methodName="somemethod")
    assert excinfo.value.message == "Tried to call Test.somemethod((['()'], [])) but no method with that name exists"

def test_helper_callMethod_alternateKlass_fail():
    test = Test()
    test2 = Test2()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(klass=test, alternateKlass=test2, methodName="somemethod")
    assert excinfo.value.message == "Tried to call Test.somemethod((['()'], [])) and Test2.somemethod((['()'], [])) but no method with that name exists in either class"

####
#
# Helper.callMethod positional params passed
#
####

def test_helper_callMethod_positional_params():
    test = Test()
    value = Helper.callMethod(1,2,3, klass=test, methodName="methodExists_positional")
    assert "methodExists_positional(one,two,three)" == value

def test_helper_callMethod_positional_params_alternateKlass():
    test = Test()
    test2 = Test2()
    value = Helper.callMethod(1, 2, 3, klass=test, alternateKlass=test2, methodName="another_methodExists_positional")
    assert "another_methodExists_positional(one,two,three)" == value

def test_helper_callMethod_positional_params_fail_no_methodName():
    test = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod("somemethod",1, 2, 3, klass=test)
    assert excinfo.value.message == "'methodName' must be passed to Helper.callMethod()"

def test_helper_callMethod_positional_params_fail():
    test = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(1, 2, 3, klass=test, methodName="somemethod")
    assert excinfo.value.message == "Tried to call Test.somemethod((['(1, 2, 3)'], [])) but no method with that name exists"

def test_helper_callMethod_positional_params_alternateKlass_fail():
    test = Test()
    test2 = Test2()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(1, 2, 3, klass=test, alternateKlass=test2, methodName="somemethod")
    assert excinfo.value.message == "Tried to call Test.somemethod((['(1, 2, 3)'], [])) and Test2.somemethod((['(1, 2, 3)'], [])) but no method with that name exists in either class"


####
#
# Helper.callMethod named params passed
#
####

def test_helper_callMethod_named_params():
    test = Test()
    value = Helper.callMethod(one=1, two=2, three=3, klass=test, methodName="methodExists_named")
    assert "methodExists_named(one,two,three)" == value

def test_helper_callMethod_named_params_alternateKlass():
    test = Test()
    test2 = Test2()
    value = Helper.callMethod(one=1, two=2, three=3, klass=test, alternateKlass=test2, methodName="another_methodExists_named")
    assert "another_methodExists_named(one,two,three)" == value

def test_helper_callMethod_named_params_fail_no_methodName():
    test = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(one=1, two=2, three=3, klass=test)
    assert excinfo.value.message == "'methodName' must be passed to Helper.callMethod()"

def test_helper_callMethod_named_params_fail():
    test = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(one=1, two=2, three=3, klass=test, methodName="somemethod")
    assert excinfo.value.message == "Tried to call Test.somemethod((['()'], ['one=1', 'two=2', 'three=3'])) but no method with that name exists"

def test_helper_callMethod_named_params_alternateKlass_fail():
    test = Test()
    test2 = Test2()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(one=1, two=2, three=3, klass=test, alternateKlass=test2, methodName="somemethod")
    assert excinfo.value.message == "Tried to call Test.somemethod((['()'], ['one=1', 'two=2', 'three=3'])) and Test2.somemethod((['()'], ['one=1', 'two=2', 'three=3'])) but no method with that name exists in either class"


####
#
# Helper.callMethod positional and named params passed
#
####

def test_helper_callMethod_positional_and_named_params():
    test = Test()
    value = Helper.callMethod(1,2,three=3,four=4,klass=test, methodName="methodExists_positional_named")
    assert "methodExists_positional_named(one,two,three,four)" == value

def test_helper_callMethod_positional_and_named_params_alternateKlass():
    test = Test()
    test2 = Test2()
    value = Helper.callMethod(1,2,three=3,four=4,klass=test, alternateKlass=test2, methodName="another_methodExists_positional_named")
    assert "another_methodExists_positional_named(one,two,three,four)" == value

def test_helper_callMethod_positional_and_named_params_fail_no_methodName():
    test = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(1,2,three=3,four=4,klass=test)
    assert excinfo.value.message == "'methodName' must be passed to Helper.callMethod()"

def test_helper_callMethod_positional_and_named_params_fail():
    test = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(1,2,three=3,four=4,klass=test, methodName="somemethod")
    assert excinfo.value.message == "Tried to call Test.somemethod((['(1, 2)'], ['three=3', 'four=4'])) but no method with that name exists"

def test_helper_callMethod_positional_and_named_params_alternateKlass_fail():
    test = Test()
    test2 = Test2()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.callMethod(1,2,three=3,four=4,klass=test, alternateKlass=test2, methodName="somemethod")
    assert excinfo.value.message == "Tried to call Test.somemethod((['(1, 2)'], ['three=3', 'four=4'])) and Test2.somemethod((['(1, 2)'], ['three=3', 'four=4'])) but no method with that name exists in either class"


####
#
# Helper.compareLists
#
####

def test_compare_lists():
    list1 = [1,2,3,4]
    list2 = [1,2,3,4,5]
    # list 1 does not have everything in list 2
    assert False == Helper.compareLists(list1, list2)

    # list 2 has everything in list 1
    assert True ==  Helper.compareLists(list2, list1)


####
#
# Helper.is_type
#
####

def test_is_dict():
    dictionary = {"one": 1, "two": 2}
    notDictionary = [1,2,3]
    assert True == Helper.is_dict(dictionary)
    assert False == Helper.is_dict(notDictionary)

def test_is_int():
    integer = 2
    notDictionary = [1,2,3]
    assert True == Helper.is_int(integer)
    assert False == Helper.is_int(notDictionary)

def test_is_list():
    dictionary = {"one": 1, "two": 2}
    notDictionary = [1,2,3]
    assert True == Helper.is_list(notDictionary)
    assert False == Helper.is_list(dictionary)

def test_is_str():
    string = "this is string"
    notDictionary = [1,2,3]
    assert True == Helper.is_str(string)
    assert False == Helper.is_str(notDictionary)

def test_is_nested_cache():
    from modules.caches.nested import Nested_Cache

    cache = Nested_Cache()
    notCache = "a string"
    assert True == Helper.is_Nested_Cache(cache)
    assert False == Helper.is_Nested_Cache(notCache)


def test_is_flat_cache():
    from modules.caches.flat import Flat_Cache

    cache = Flat_Cache()
    notCache = "a string"
    assert True == Helper.is_Flat_Cache(cache)
    assert False == Helper.is_Flat_Cache(notCache)

def test_is_tuple():
    aTuple = (1, 2, 3)
    notATuple = "a string"

    assert True == Helper.is_tuple(aTuple)
    assert False == Helper.is_tuple(notATuple)

def test_isType():
    adict = {"one":1, "two":2}
    alist = [1,2,3,4]
    atuple = (1,2,3,"four")
    astring = "a string is this is"
    from modules.caches.nested import Nested_Cache
    ncache = Nested_Cache()
    from modules.caches.flat import Flat_Cache
    fcache = Flat_Cache()

    assert True == Helper.isType(dict.__name__,    adict)
    assert True == Helper.isType("dict",           adict)
    assert False == Helper.isType("list",          adict)
    assert False == Helper.isType("tuple",         adict)
    assert False == Helper.isType("str",           adict)
    assert False == Helper.isType("Flat_Cache",    adict)
    assert False == Helper.isType("Nested_Cache",  adict)

    assert True == Helper.isType(list.__name__,    alist)
    assert True == Helper.isType("list",           alist)
    assert False == Helper.isType("dict",          alist)
    assert False == Helper.isType("tuple",         alist)
    assert False == Helper.isType("str",           alist)
    assert False == Helper.isType("Flat_Cache",    alist)
    assert False == Helper.isType("Nested_Cache",  alist)

    assert True == Helper.isType(tuple.__name__,   atuple)
    assert True == Helper.isType("tuple",          atuple)
    assert False == Helper.isType("list",          atuple)
    assert False == Helper.isType("dict",          atuple)
    assert False == Helper.isType("str",           atuple)
    assert False == Helper.isType("Flat_Cache",    atuple)
    assert False == Helper.isType("Nested_Cache",  atuple)

    assert True == Helper.isType(str.__name__,     astring)
    assert True == Helper.isType("str",            astring)
    assert False == Helper.isType("list",          astring)
    assert False == Helper.isType("dict",          astring)
    assert False == Helper.isType("tuple",         astring)
    assert False == Helper.isType("Flat_Cache",    astring)
    assert False == Helper.isType("Nested_Cache",  astring)

    assert True == Helper.isType(Helper.className(ncache),  ncache)
    assert True == Helper.isType("Nested_Cache",            ncache)
    assert False == Helper.isType("list",                   ncache)
    assert False == Helper.isType("dict",                   ncache)
    assert False == Helper.isType("tuple",                  ncache)
    assert False == Helper.isType("str",                    ncache)
    assert False == Helper.isType("Flat_Cache",             ncache)

    assert True == Helper.isType(Helper.className(fcache),  fcache)
    assert True == Helper.isType("Flat_Cache",              fcache)
    assert False == Helper.isType("list",                   fcache)
    assert False == Helper.isType("dict",                   fcache)
    assert False == Helper.isType("tuple",                  fcache)
    assert False == Helper.isType("str",                    fcache)
    assert False == Helper.isType("Nested_Cache",           fcache)


####
#
# Helper.existsIn
#
####


def test_exists_in_dict():
    key1 = "key1"
    key2 = "key2"
    dictionary = {"key1":"something", "key3":"somethingElse"}
    assert True == Helper.existsIn(key1, dictionary)
    assert False == Helper.existsIn(key2, dictionary)

def test_exists_in_list():
    key1 = "key1"
    key2 = "key2"
    alist = ["key1", "something", "key3", "somethingElse"]
    assert True == Helper.existsIn(key1, alist)
    assert False == Helper.existsIn(key2, alist)


def test_exists_in_str():
    key1 = "key1"
    key2 = "key2"
    astring = "this is a string with key1 in it"
    assert True == Helper.existsIn(key1, astring)
    assert False == Helper.existsIn(key2, astring)    

def test_exists_in_fail():
    key1 = "key1"
    key2 = "key2"
    aThing = Test()
    with pytest.raises(Helper_Exception) as excinfo:
        Helper.existsIn(key1, aThing)
    assert excinfo.value.message == "No existsIn validation method exists for <class 'tests.test_modules.test_helper.Test'>"

    with pytest.raises(Helper_Exception) as excinfo:
        Helper.existsIn(key2, aThing)
    assert excinfo.value.message == "No existsIn validation method exists for <class 'tests.test_modules.test_helper.Test'>"
    

# not doing a test for this Helper Method: 
#   output_dir