import pytest

from modules import caches
from modules.caches.flat import Flat_Cache
from modules.caches.nested import Nested_Cache
from modules.caches.exception import Nested_Cache_Exception
from modules.caches.exception import Flat_Cache_Exception

#raise Exception("Need to test with new Data Row functionality replacing original functionality")

def test_cache_creation():
     cache = Nested_Cache([], [])
     assert cache != None
     assert cache.getAsListOfLists() == [[]]


def test_empty_cache_get_row_item():
    cache = Nested_Cache([], [])
    value = cache.get_row_item(row=1,location="test")
    assert value == None

def test_empty_cache_cache_get_row_item():
    cache = Nested_Cache([], [])
    value = cache.get_row_item(1, "test")
    assert value == None


def test_cache_trySetOnNewRow():
    cache = Nested_Cache(['a'],[[1]])
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.set_row_item(2, location="a", data=1)
    assert excinfo.value.message == "Row 2 doesn't exist, to add it use appendRow()"
    value = cache.get_row_item(2, "a")
    assert value == None

def test_cache_trysetOnNewRow2():
    cache = Nested_Cache(['a'],[[1]])
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.set_row_item(row=2, location="a", data=1)
    assert excinfo.value.message == "Row 2 doesn't exist, to add it use appendRow()"
    
    cache.appendRow(location='a', data=1)

    value = cache.get_row_item(2, "a")
    assert value == 1


def test_cache_set_again():
    cache = Nested_Cache(['a'],[[2]])
    value = cache.get_row_item(1, "a")

    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.set_row_item(1, "a", 1)
    assert excinfo.value.message == "There is already data at row:1 location:a/index:0, to change this data use updateData(row, location/index, data)"


def test_cache_set_again2():
    cache = Nested_Cache(["a"],[[2]])
    value = cache.get_row_item(location="a", row=1)

    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.set_row_item(row=1, location="a", data=1)
    # assert excinfo.value.message == "Nested_Cache has 2 at a. To update data in the cache, use updateData()"
    assert excinfo.value.message == "There is already data at row:1 location:a/index:0, to change this data use updateData(row, location/index, data)"


def test_updateData():
    cache = Nested_Cache(['b'],[[3]])
    cache.updateData(1, location="b", data=5)
    assert 5 == cache.get_row_item(1, "b")


def test_update2():
    cache = Nested_Cache(['b'],[[3]])
    cache.updateData(row=1,location="b",data=5)
    assert 5 == cache.get_row_item(row=1, location="b")


def test_update_exception():
    cache = Nested_Cache(['b'],[[3]])
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.updateData(1, index=2, data=5)
    assert excinfo.value.message == "Index '2' doesn't exist, to add it use addLocation(location)"
    assert 3 == cache.get_row_item(1, "b")


def test_update_exception2():
    cache = Nested_Cache(['b'],[[3]])
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.updateData(row=1,location="c",data=5)
    assert excinfo.value.message == "Location 'c' doesn't exist, to add it use addLocation(location)"
    assert 3 == cache.get_row_item(row=1, location="b")


def test_getAsList():
    cache = Nested_Cache(['b','c','d'],[[3],[None, 4, None],[None, None, 5]])
    assert cache.getRowAsList(1) == [3, None, None]
    assert cache.getRowAsList(2) == [None, 4, None]
    assert cache.getRowAsList(3) == [None, None, 5]


def test_getAsDict():
    cache = Nested_Cache(['b','c','d'],[[3],[None, 4, None],[None, None, 5]])
    assert cache.getRowAsDict(1, asObj="dict") == {'b': 3, 'c': None, 'd': None}
    assert cache.getRowAsDict(2, asObj="dict") == {'b': None, 'c': 4, 'd': None}
    assert cache.getRowAsDict(3, asObj="dict") == {'b': None, 'c': None, 'd': 5}


def test_getLocationThatExists():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.get_row_item(3, "b") == 5


def test_getLocationThatExists2():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.get_row_item(row=3,location="b") == 5


def test_getLocationThatDoesntExist():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.get_row_item(3, "e") == None


def test_getLocationThatDoesntExist2():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.get_row_item(row=3,location="e") == None




def test_getRow():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(3) == [5, None, None]

def test_getRow2():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(row=3) == [5, None, None]

def test_getRowAsList():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(row=3, asObj="list") == [5, None, None]


def test_getRowAsDict():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(3, asObj="dict") == {'b': 5, 'c': None, 'd': None}

def test_getRowAsDict2():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(row=3, asObj="dict") == {'b': 5, 'c': None, 'd': None}





# Adding data to columns that exist should change nothing about the width
def test_width_fromAdds():
    cache = Nested_Cache(['b','c','d'],[[3]])
    assert 3 == cache.width()
    cache.set_row_item(row=1,location="c",data=4)
    assert 3 == cache.width()
    cache.set_row_item(row=1,location="d",data=4)
    assert 3 == cache.width()



# adding columns that don't exist should fail gloriously
def test_fail_fromAddingColsThatDontExist():
    # Adding these should change nothing about the width
    cache = Nested_Cache(['b','c','d'],[[3]])
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.set_row_item(row=1,location="e",data=4)
    assert excinfo.value.message == "Location 'e' doesn't exist, to add it use addLocation(location)"


def test_addUnrecognizedLocation():
    cache = Nested_Cache(['b'],[[3]])

    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.set_row_item(row=2, location='c', data=3)
    assert excinfo.value.message == "Row 2 doesn't exist, to add it use appendRow()"


# def test_unset():
#     cache = Nested_Cache(['b'],[[3]])
#     cache.unsetData(1, "b")
#     assert None == cache.get_row_item(1, "b")

# def test_unset2():
#     cache = Nested_Cache(['b'],[[3]])
#     cache.unsetData(row=1, location="b")
#     assert None == cache.get_row_item(row=1, location="b")


# def test_unset_fail():
#     cache = Nested_Cache(['b'],[[3]])
#     with pytest.raises(Nested_Cache_Exception) as excinfo:
#         cache.unsetData(1, location="c")
#     assert excinfo.value.message == "Location 'c' doesn't exist, to add it use addLocation(location)"


#     assert 3 == cache.get_row_item(1, "b")

# def test_unset_fail2():
#     cache = Nested_Cache(['b'],[[3]])

#     with pytest.raises(Nested_Cache_Exception) as excinfo:
#         cache.unsetData(row=1, location="c")
#     assert excinfo.value.message == "Location 'c' doesn't exist, to add it use addLocation(location)"
    
#     assert 3 == cache.get_row_item(row=1, location="b")


# def test_unset_fail3():
#     cache = Nested_Cache(['b'],[[3]])
#     with pytest.raises(Nested_Cache_Exception) as excinfo:
#         cache.unset(row=1, location="c")
#     assert excinfo.value.message == "unset() is not valid for Nested_Cache, use either unsetRow() or unsetData()"

# def test_unsetRow():
#     cache = Nested_Cache(['b','c'],[[3],[4]])
#     cache.unsetRow(2)
#     assert cache.getRow(2) == [None, None]

# def test_unsetRow2():
#     cache = Nested_Cache(['b','c'],[[3],[4]])
#     cache.unsetRow(row=2)
#     assert cache.getRow(row=2) == [None, None]

# def test_unsetRow_asDict():
#     cache = Nested_Cache(['b','c'],[[3],[4]])
#     cache.unsetRow(2)
#     assert cache.getRow(2, asObj="dict") == {'b':None, 'c':None}

# def test_unsetRow_asDict2():
#     cache = Nested_Cache(['b','c'],[[3],[4]])
#     cache.unsetRow(row=2)
#     assert cache.getRow(row=2, asObj="dict") == {'b':None, 'c':None}


# def test_height_fromDeletes():
#     cache = Nested_Cache(['b','c','d'],[[3],[3,4],[5,1,5]])
#     with pytest.raises(Nested_Cache_Exception) as excinfo:
#         cache.set(row=3,location="d",data=4)
#     assert excinfo.value.message == "There is already data at row:3 location:d/index:2, to change this data use updateData(row, location/index, data)"
    
#     cache.deleteRow(row=2)
#     # print(cache.height())
#     assert 2 == cache.height()
#     cache.deleteRow(row=1)
#     assert 1 == cache.height()


# def test_deleteRow():
#     cache = Nested_Cache(['b','c','d'],[[3],[4],[4]])
#     cache.deleteRow(2)
#     assert cache.getRow(2) == [4, None, None]

# def test_deleteRow_getAsDict():
#     cache = Nested_Cache(['b','c','d'],[[3],[4],[4]])
#     cache.deleteRow(2)
#     assert cache.getRow(2, asObj="dict") == {'b': 4, 'c': None, 'd': None}

# def test_deleteColumn_noIndex():
#     pass
#     print("Nothing being tested in test_deleteColumn")

# def test_deleteColumn_noLocation():
#     pass
#     print("Nothing being tested in test_deleteColumn_noLocation")

# def test_deleteColumn_noMatchIndexLocation():
#     pass
#     print("Nothing being tested in test_deleteColumn_noMatchIndexLocation")


# def test_deleteRow():
#     pass
#     print("Nothing being tested in test_deleteRow")
    # try to delete row 0
    # try to delete item from row 0

# def test_clear():
#     cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
#     cache.clear()
#     assert cache._storage == []


# def test_clear2():
#     cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
#     cache.clear()
#     assert cache._storage == []


# def test_delete():
#     cache = Nested_Cache(['b','c','d'],[[3, 2, 1],[4, 3, 2],[5, 4, 3]])
#     cache.delete(2, "c")
#     assert None == cache.get_row_item(2, "c")
#     assert cache.getRow(1) == [3, 2, 1] 
#     assert cache.getRow(3) == [5, 4, 3]
#     assert cache.getRow(2) == [4, None, 2]


# def test_delete2():
#     cache = Nested_Cache(['b','c','d'],[[3, 2, 1],[4, 3, 2],[5, 4, 3]])
#     cache.delete(row=2, location="c")
#     assert cache.getRow(row=1) == [3, 2, 1]
#     assert cache.getRow(row=3) == [5, 4, 3]
#     assert cache.getRow(row=2) == [4, None, 2]
#     assert None == cache.get_row_item(row=2,location="c")