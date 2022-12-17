import pytest

from modules import caches
from modules.caches.flat import Flat_Cache
from modules.caches.nested import Nested_Cache
from modules.caches.exception import Nested_Cache_Exception
from modules.caches.exception import Flat_Cache_Exception

def test_cache_creation():
     cache = Nested_Cache([], [])
     assert cache != None
     assert cache.getAsListOfLists() == [[]]


def test_empty_cache_select():
    cache = Nested_Cache([], [])
    value = cache.select(row=0,position="test")
    assert value == None

def test_empty_cache_cache_select():
    cache = Nested_Cache([], [])
    value = cache.select(0, "test")
    assert value == None


def test_cache_trySetOnNewRow():
    cache = Nested_Cache(['a'],[[1]])
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.insert(1, position="a", data=1)
    assert excinfo.value.message == "Row 2 doesn't exist, to add it use appendRow()"
    value = cache.select(0, "a")
    assert value == None

def test_cache_trysetOnNewRow2():
    cache = Nested_Cache(['a'],[[1]])
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.insert(row=1, position="a", data=1)
    assert excinfo.value.message == "Row 1 doesn't exist, to add it use appendRow()"
    
    cache.insert([1])

    value = cache.select(1, "a")
    assert value == 1


def test_cache_set_again():
    cache = Nested_Cache(['a'],[[2]])
    value = cache.select(0, "a")

    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.insert(0, "a", 1)
    assert excinfo.value.message == "There is already data at row:1 location:a/index:0, to change this data use update(row, location/index, data)"


def test_cache_set_again2():
    cache = Nested_Cache(["a"],[[2]])
    value = cache.select(position="a", row=1)

    with pytest.raises(Nested_Cache_Exception) as excinfo:
        cache.insert(row=0, position="a", data=1)
    # assert excinfo.value.message == "Nested_Cache has 2 at a. To update data in the cache, use update()"
    assert excinfo.value.message == "There is already data at row:1 location:a/index:0, to change this data use update(row, location/index, data)"


def test_update():
    cache = Nested_Cache(['b'],[[3]])
    cache.update(0, position="b", data=5)
    assert 5 == cache.select(0, "b")


def test_update2():
    cache = Nested_Cache(['b'],[[3]])
    cache.update(row=0,position="b",data=5)
    assert 5 == cache.select(row=0, position="b")


def test_update_exception():
    cache = Nested_Cache(['b'],[[3]])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update(0, position=2, data=5)
    assert excinfo.value.message == "Location '2' does not exist, try \"add_location('2')\""
    assert 3 == cache.select(0, "b")


def test_update_exception2():
    cache = Nested_Cache(['b'],[[3]])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update(row=0,position="c",data=5)
    assert excinfo.value.message == "Location 'c' does not exist, try \"add_location('c')\""
    assert 3 == cache.select(row=0, position="b")


def test_getAsDict():
    cache = Nested_Cache(['b','c','d'],[[3],[None, 4, None],[None, None, 5]])
    assert cache.select(0) == {'b': 3, 'c': None, 'd': None}
    assert cache.select(1) == {'b': None, 'c': 4, 'd': None}
    assert cache.select(2) == {'b': None, 'c': None, 'd': 5}


def test_getLocationThatExists():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.select(2, "b") == 5


def test_getLocationThatExists2():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.select(row=2,position="b") == 5


def test_getLocationThatDoesntExist():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        assert cache.select(2,"e") == None
    assert excinfo.value.message == "Location 'e' does not exist, try \"add_location('e')\""


def test_getLocationThatDoesntExist2():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        assert cache.select(row=2,position="e") == None
    assert excinfo.value.message == "Location 'e' does not exist, try \"add_location('e')\""

    




def test_select():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.select(2) == {'b': 5, 'c': None, 'd': None}

def test_select2():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.select(row=2) == {'b': 5, 'c': None, 'd': None}



# Adding data to columns that exist should change nothing about the width
def test_width_fromAdds():
    cache = Nested_Cache(['b','c','d'],[[3]])
    assert 3 == cache.width()
    rowItem = cache.select(row=0, position='c')
    print(f"RowItem: {rowItem}")
    assert None == rowItem
    cache.update(row=0, position="c", data=4)
    assert 3 == cache.width()
    cache.update(row=0, position="d", data=4)
    assert 3 == cache.width()


# def test_unset():
#     cache = Nested_Cache(['b'],[[3]])
#     cache.unsetData(1, "b")
#     assert None == cache.select(1, "b")

# def test_unset2():
#     cache = Nested_Cache(['b'],[[3]])
#     cache.unsetData(row=1, location="b")
#     assert None == cache.select(row=1, location="b")


# def test_unset_fail():
#     cache = Nested_Cache(['b'],[[3]])
#     with pytest.raises(Nested_Cache_Exception) as excinfo:
#         cache.unsetData(1, location="c")
#     assert excinfo.value.message == "Location 'c' doesn't exist, to add it use addLocation(location)"


#     assert 3 == cache.select(1, "b")

# def test_unset_fail2():
#     cache = Nested_Cache(['b'],[[3]])

#     with pytest.raises(Nested_Cache_Exception) as excinfo:
#         cache.unsetData(row=1, location="c")
#     assert excinfo.value.message == "Location 'c' doesn't exist, to add it use addLocation(location)"
    
#     assert 3 == cache.select(row=1, location="b")


# def test_unset_fail3():
#     cache = Nested_Cache(['b'],[[3]])
#     with pytest.raises(Nested_Cache_Exception) as excinfo:
#         cache.unset(row=1, location="c")
#     assert excinfo.value.message == "unset() is not valid for Nested_Cache, use either unsetRow() or unsetData()"

# def test_unsetRow():
#     cache = Nested_Cache(['b','c'],[[3],[4]])
#     cache.unsetRow(2)
#     assert cache.select(2) == [None, None]

# def test_unsetRow2():
#     cache = Nested_Cache(['b','c'],[[3],[4]])
#     cache.unsetRow(row=2)
#     assert cache.select(row=2) == [None, None]

# def test_unsetRow_asDict():
#     cache = Nested_Cache(['b','c'],[[3],[4]])
#     cache.unsetRow(2)
#     assert cache.select(2, asObj="dict") == {'b':None, 'c':None}

# def test_unsetRow_asDict2():
#     cache = Nested_Cache(['b','c'],[[3],[4]])
#     cache.unsetRow(row=2)
#     assert cache.select(row=2, asObj="dict") == {'b':None, 'c':None}


# def test_height_fromDeletes():
#     cache = Nested_Cache(['b','c','d'],[[3],[3,4],[5,1,5]])
#     with pytest.raises(Nested_Cache_Exception) as excinfo:
#         cache.set(row=3,location="d",data=4)
#     assert excinfo.value.message == "There is already data at row:3 location:d/index:2, to change this data use update(row, location/index, data)"
    
#     cache.deleteRow(row=2)
#     # print(cache.height())
#     assert 2 == cache.height()
#     cache.deleteRow(row=1)
#     assert 1 == cache.height()


# def test_deleteRow():
#     cache = Nested_Cache(['b','c','d'],[[3],[4],[4]])
#     cache.deleteRow(2)
#     assert cache.select(2) == [4, None, None]

# def test_deleteRow_getAsDict():
#     cache = Nested_Cache(['b','c','d'],[[3],[4],[4]])
#     cache.deleteRow(2)
#     assert cache.select(2, asObj="dict") == {'b': 4, 'c': None, 'd': None}

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
#     assert None == cache.select(2, "c")
#     assert cache.select(1) == [3, 2, 1] 
#     assert cache.select(3) == [5, 4, 3]
#     assert cache.select(2) == [4, None, 2]


# def test_delete2():
#     cache = Nested_Cache(['b','c','d'],[[3, 2, 1],[4, 3, 2],[5, 4, 3]])
#     cache.delete(row=2, location="c")
#     assert cache.select(row=1) == [3, 2, 1]
#     assert cache.select(row=3) == [5, 4, 3]
#     assert cache.select(row=2) == [4, None, 2]
#     assert None == cache.select(row=2,location="c")