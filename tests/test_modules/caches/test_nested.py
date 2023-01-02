import pytest, pydantic
from collections import OrderedDict
from modules import caches
from modules.caches.flat import UPDATE_TIMESTAMP_KEY, Flat_Cache
from modules.caches.nested import Nested_Cache
from modules.caches.exception import Nested_Cache_Exception
from modules.caches.exception import Flat_Cache_Exception

####
#
# Init
#
####

def test_cache_creation():
     cache = Nested_Cache([{}])
     assert cache != None
     assert len(cache.getAsListOfLists()) == 0 #only update timestamp should be returned


def test_empty_cache_select():
    cache = Nested_Cache([{}])

    with pytest.raises(Nested_Cache_Exception) as excinfo:
        value = cache.select(row=0,position="test")
    assert excinfo.value.message == "Row 0 doesn't exist, to add it use insertRow(rowData)"

####
#
# Select
#
####


def test_select():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}, {'b':None,'c':4,'d':None}, {'b':None,'c':None,'d':5}])
    assert cache.select(2, update_timestamp=False) == {'b': None, 'c': None, 'd': 5}


def test_select2():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}, {'b':None,'c':4,'d':None}, {'b':None,'c':None,'d':5}])
    assert cache.select(row=2, update_timestamp=False) == {'b': None, 'c': None, 'd': 5}


def test_select_all():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}, {'b':None,'c':4,'d':None}, {'b':None,'c':None,'d':5}])
    allData = cache.selectRow()
    assert len(allData) == 3
    assert len(allData[0]) == 7
    assert len(allData[1]) == 7
    assert len(allData[2]) == 7


####
#
# Insert
#
####

def test_empty_cache_select2():
    cache = Nested_Cache([{}])
    
    assert cache.height() == 0

    cache.insertRow({'test':1})

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert_location("test")
    assert excinfo.value.message == "Position 'test' already exists, you cannot insert a new location to Flat_Cache that already exists"

    assert cache.height() == 1
    
    cache.insertRow({'test':1})

    value = cache.select(0, "test")

    assert value == 1

    value = cache.select(1, "test")

    assert value == 1


def test_empty_cache_select3():
    cache = Nested_Cache([{}])
    
    assert cache.height() == 0

    cache.insert_location("test")

    assert cache.height() == 1
    assert cache.headerRowOnly == True

    value = cache.select(0, "test")

    assert value == None

    cache.insertRow({'test':1})

    with pytest.raises(IndexError) as excinfo:
        value = cache.select(1, "test")
    assert "list index out of range" in str(excinfo.value)

    value = cache.select(0, "test")

    assert value == 1
    


def test_cache_trySetOnNewRow():
    cache = Nested_Cache([{'a':1}])

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.insert(1, position="a", data=1)
    assert "unexpected keyword arguments: 'position', 'data' (type=type_error)" in str(excinfo.value)

    value = cache.select(0, "a")

    assert value == 1


def test_cache_trysetOnNewRow2():
    cache = Nested_Cache([{'a':1}])

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.insert(row=1, position="a", data=1)
    assert "unexpected keyword arguments: 'row', 'position', 'data' (type=type_error)" in str(excinfo.value)
    
    cache.insertRow({'a':2})

    value = cache.select(1, "a")
    assert value == 2


def test_cache_set_again():
    cache = Nested_Cache([{'a':2}])
    value = cache.select(0, "a")

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.insert(0, "a", 1)
    assert "1 positional arguments expected but 4 given" in str(excinfo.value)


def test_cache_set_again2():
    cache = Nested_Cache([{'a':2}])
    value = cache.select(position="a", row=0)

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.insert(row=0, position="a", data=1)
    assert "unexpected keyword arguments: 'row', 'position', 'data'" in str(excinfo.value)

    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.insert()
    assert "There is no Nested_Cache.insert() method, maybe you meant insertRow()?" in str(excinfo.value)

####
#
# Update
#
####

def test_update():
    cache = Nested_Cache([{'b':3}])
    cache.update(0, position="b", data=5)
    assert 5 == cache.select(0, "b")


def test_update2():
    cache = Nested_Cache([{'b':3}])
    cache.update(row=0,position="b",data=5)
    assert 5 == cache.select(row=0, position="b")


def test_update_exception():
    cache = Nested_Cache([{'b':3}])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update(0, position=2, data=5)
    assert excinfo.value.message == "Location '2' does not exist, try \"insert_location('2')\""
    assert 3 == cache.select(0, "b")


def test_update_exception2():
    cache = Nested_Cache([{'b':3}])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update(row=0,position="c",data=5)
    assert excinfo.value.message == "Location 'c' does not exist, try \"insert_location('c')\""
    assert 3 == cache.select(row=0, position="b")


def test_getAsDict():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}, {'b':None,'c':4,'d':None}, {'b':None,'c':None,'d':5}])
    assert cache.selectRow(0, update_timestamp=False) == {'b': 3, 'c': None, 'd': None}
    assert cache.selectRow(1, update_timestamp=False) == {'b': None, 'c': 4, 'd': None}
    assert cache.selectRow(2, update_timestamp=False) == {'b': None, 'c': None, 'd': 5}

####
#
# Get Location
#
####


def test_getLocationThatExists():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}, {'b':None,'c':4,'d':None}, {'b':None,'c':None,'d':5}])
    assert cache.select(0, 'b') == 3
    assert cache.select(1, 'c') == 4
    assert cache.select(2, "b") == None
    assert cache.select(2, 'd') == 5

def test_getLocationThatExists2():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}, {'b':None,'c':4,'d':None}, {'b':None,'c':None,'d':5}])
    assert cache.select(row=0, position='b') == 3
    assert cache.select(row=1, position='c') == 4
    assert cache.select(row=2, position="b") == None
    assert cache.select(row=2, position='d') == 5


def test_getLocationThatDoesntExist():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}, {'b':None,'c':4,'d':None}, {'b':None,'c':None,'d':5}])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        assert cache.select(2,"e") == None
    assert excinfo.value.message == "Location 'e' does not exist, try \"insert_location('e')\""


def test_getLocationThatDoesntExist2():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}, {'b':None,'c':4,'d':None}, {'b':None,'c':None,'d':5}])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        assert cache.select(row=2,position="e") == None
    assert excinfo.value.message == "Location 'e' does not exist, try \"insert_location('e')\""

####
#
# Meta Methods
#
####
   

# Adding data to columns that exist should change nothing about the width
def test_width_fromAdds():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}])
    assert 3 == cache.width()

    rowItem = cache.select(row=0, position='c')
    assert None == rowItem
    
    cache.update(row=0, position="c", data=4)
    assert 3 == cache.width()
    
    cache.update(row=0, position="d", data=4)
    assert 3 == cache.width()

####
#
# Delete
#
####

def test_delete_column():
    cache = Nested_Cache([{'b':3,'c':None,'d':None}])
    
    cache.deleteColumn('c')
    assert cache.select(0, update_timestamp=False) == {'b': 3, 'd': None}

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.deleteColumn(1)
    assert "str type expected" in str(excinfo.value)

def test_delete_columns():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7}])
    
    cache.deleteColumns(['c','d','e'])
    assert cache.select(0, update_timestamp=False) == {'b': 3, 'f': 7}


def test_delete_columns_check_first_row():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7}])

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.deleteColumns([1,2,3])
    assert "str type expected" in str(excinfo.value)


def test_delete_columns_check_multi_rows():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}])
    
    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.deleteColumns([1,2,3])
    assert "str type expected" in str(excinfo.value)

    cache.deleteColumns(['c','d','e'])

    assert cache.selectRow(0, update_timestamp=False) == {'b': 3, 'f': 7}
    assert cache.selectRow(1, update_timestamp=False) == {'b': 1, 'f': 5}

####
#
# Row Methods
#
####

def test_updateRow():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}])
    cache.updateRow(1, {'b':10,'c':20,'d':30,'e':40,'f':50})

    assert cache.select(0, update_timestamp=False) == {'b': 3, 'c': 4,'d': 5,'e': 6,'f': 7}
    assert cache.selectRow(1, update_timestamp=False) == {'b': 10, 'c': 20,'d': 30,'e': 40,'f': 50}


def test_getRowAsList():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}])
    rowList = cache.getRowAsList(0)
    assert rowList.index(3) == 0
    assert rowList.index(4) == 1
    assert rowList.index(5) == 2
    assert rowList.index(6) == 3
    assert rowList.index(7) == 4

    rowList = cache.getRowAsList(1)
    assert rowList.index(1) == 0
    assert rowList.index(2) == 1
    assert rowList.index(3) == 2
    assert rowList.index(4) == 3
    assert rowList.index(5) == 4

def test_getRowAsDict():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}])
    rowList = cache.getRowAsDict(0)
    assert rowList['b'] == 3
    assert rowList['c'] == 4
    assert rowList['d'] == 5
    assert rowList['e'] == 6
    assert rowList['f'] == 7

    rowList = cache.getRowAsDict(1)
    assert rowList['b'] == 1
    assert rowList['c'] == 2
    assert rowList['d'] == 3
    assert rowList['e'] == 4
    assert rowList['f'] == 5

####
#
# Reorder Columns
#
####

def test_reorderColumns():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}])
    cache.reorderColumns(['f','b','d','c','e'])
    assert cache.selectRow(0, update_timestamp=False) == {'f': 7, 'b': 3, 'd': 5, 'c': 4, 'e': 6}
    assert cache.selectRow(1, update_timestamp=False) == {'f': 5, 'b': 1, 'd': 3, 'c': 2, 'e': 4}
    
    somedataKeys = cache.selectRow(0).keys()
    assert Flat_Cache.makeTimestampName("b") in somedataKeys
    assert Flat_Cache.makeTimestampName("c") in somedataKeys
    assert Flat_Cache.makeTimestampName("d") in somedataKeys
    assert Flat_Cache.makeTimestampName("e") in somedataKeys
    assert Flat_Cache.makeTimestampName("f") in somedataKeys


# ####
# #
# # Test for uniqueness
# #
# ####

# verify that unique gets setup
def test_unique_load():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    print(cache.getUniques())
    assert cache.getUniques() == [3, 1]

# do an initial load with 2 of the same item in the unique field
def test_unique_load_fail():    
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':3,'c':2,'d':3,'e':4,'f':5}], 'b')
    assert "'3' for position 'b' violates uniqueness" in str(excinfo.value)

# add a unique that isn't in the locations
def test_unique_insert():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    cache.insertRow({'b':2,'c':3,'d':4,'e':5,'f':6})
    assert cache.getUniques() == [3, 1, 2]

# add a unique that is already set up
def test_unique_insert_fail():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.insertRow({'b':3,'c':3,'d':4,'e':5,'f':6})
    assert "'3' for position 'b' violates uniqueness" in str(excinfo.value)
    
# try to remove the unique column from the data
def test_unique_deleteColumn():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.deleteColumn('b')
    assert "You cannot delete the unique column 'b'" in str(excinfo.value)
    
# try to replace a row that has the same unique value
def test_unique_updateRow_same_unique():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    cache.updateRow(row=0, rowData={'b':3,'c':4,'d':5,'e':6,'f':7})
    assert cache.getUniques() == [3, 1]

# try to replace a row that doesn't have the same unique value
def test_unique_updateRow_diff_unique():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    cache.updateRow(row=0, rowData={'b':2,'c':4,'d':5,'e':6,'f':7})
    assert cache.getUniques() == [2, 1]


# try to unset the value of the unique columns from the data
def test_unique_updateRow_same_unique():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    cache.update(row=0, position='b', data=3)
    assert cache.getUniques() == [3,1]

# try to unset the value of the unique columns from the data
def test_unique_updateRow_diff_unique_is_unique():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    cache.update(row=0, position='b', data=5)
    assert cache.getUniques() == [5,1]

# try to unset the value of the unique columns from the data
def test_unique_updateRow_diff_unique_not_unique():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.update(row=0, position='b', data=1)
    assert "'1' for position 'b' violates uniqueness" in str(excinfo.value)

# try a select with row and unique
def test_unique_unique_select_row_and_unique():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        row = cache.selectRow(row=0,unique=3)
    assert "Passing row and unique together is poor form, pick one" in str(excinfo.value)
    
# try a select with unique only
def test_unique_select_by_unique():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    row = cache.selectRow(unique=3)
    assert row == {'b': 3, 'c': 4,'d': 5,'e': 6,'f': 7}
    row = cache.selectRow(unique=1)
    assert row == {'b':1,'c':2,'d':3,'e':4,'f':5}

# test an update/insert based on data that exists
def test_unique_select_by_unique():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    # will cause an update, so uniques will stay the same
    row = cache.putRow({'b':3,'c':6,'d':7,'e':8,'f':9})
    assert cache.getUniques() == [3,1]
    
    # will cause an insert, so uniques will change
    row = cache.putRow({'b':4,'c':99,'d':100,'e':101,'f':102})
    assert cache.getUniques() == [3,1,4]

def testGetLocations():
    cache = Nested_Cache([{'b':3,'c':4,'d':5,'e':6,'f':7},{'b':1,'c':2,'d':3,'e':4,'f':5}], 'b')
    locations = cache.getLocations()
    assert locations == ['b','c','d','e','f']    
    locations = cache.getLocations(update_timestamp=True)
    assert locations == ['b','c','d','e','f', Flat_Cache.makeTimestampName('b'), Flat_Cache.makeTimestampName('c'), Flat_Cache.makeTimestampName('d'), Flat_Cache.makeTimestampName('e'), Flat_Cache.makeTimestampName('f'), UPDATE_TIMESTAMP_KEY]
