import pytest

from modules import caches
from modules.caches.nested import NestedCache
from modules.caches.exception import NestedCacheException
from modules.caches.exception import FlatCacheException

def test_cache_creation():
     cache = NestedCache([], [])
     assert cache != None
     assert cache.getAsListOfLists() == [[]]


def test_empty_cache_getData():
    cache = NestedCache([], [])
    value = cache.getData(row=1,location="test")
    assert value == None

def test_empty_cache_getData():
    cache = NestedCache([], [])
    value = cache.getData(1, "test")
    assert value == None


def test_cache_set():
    cache = NestedCache(['a'],[[1]])
    value = cache.getData(1, "a")
    assert value == 1

def test_cache_set2():
    cache = NestedCache(['a'],[[1]])
    cache.set(row=1, location="a", data=1)
    value = cache.getData(1, "a")
    assert value == 1


def test_cache_set_again():
    cache = NestedCache(['a'],[[2]])
    value = cache.getData(1, "a")

    with pytest.raises(NestedCacheException) as excinfo:
        cache.set(1, "a", 1)
    assert excinfo.value.message == "Cache has 2 at 1:a. To update data in the cache, use update()"


def test_cache_set_again2():
    cache = NestedCache(["a"],[[2]])
    value = cache.getData(location="a", row=1)

    with pytest.raises(NestedCacheException) as excinfo:
        cache.set(row=1, location="a", data=1)
    # assert excinfo.value.message == "NestedCache has 2 at a. To update data in the cache, use update()"
    assert excinfo.value.message == "Cache has 2 at 1:a. To update data in the cache, use update()"


def test_unset():
    cache = NestedCache(['b'],[[3]])
    cache.unset(1, "b")
    assert None == cache.getData(1, "b")

def test_unset2():
    cache = NestedCache(['b'],[[3]])
    cache.unset(row=1, location="b")
    assert None == cache.getData(row=1, location="b")


def test_unset_fail():
    cache = NestedCache(['b'],[[3]])
    cache.unset(1, "c")
    assert 3 == cache.getData(1, "b")

def test_unset_fail2():
    cache = NestedCache(['b'],[[3]])
    cache.unset(row=1, location="c")
    assert 3 == cache.getData(row=1, location="b")


def test_update():
    cache = NestedCache(['b'],[[3]])
    cache.update(1, "b", 5)
    assert 5 == cache.getData(1, "b")


def test_update2():
    cache = NestedCache(['b'],[[3]])
    cache.update(row=1,location="b",data=5)
    assert 5 == cache.getData(row=1, location="b")


def test_update_exception():
    cache = NestedCache(['b'],[[3]])
    with pytest.raises(FlatCacheException) as excinfo:
        cache.update(1, "c", 5)
    assert excinfo.value.message == "There is nothing to update at c"
    assert 3 == cache.getData(1, "b")


def test_update_exception2():
    cache = NestedCache(['b'],[[3]])
    with pytest.raises(FlatCacheException) as excinfo:
        cache.update(row=1,location="c",data=5)
    assert excinfo.value.message == "There is nothing to update at c"
    assert 3 == cache.getData(row=1, location="b")


def test_getAsList():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(1).getAsList() == [3]
    assert cache.getRow(2).getAsList() == [4]
    assert cache.getRow(3).getAsList() == [5]


def test_getAsDict():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(1).getAsDict() == {'b': 3}
    assert cache.getRow(2).getAsDict() == {'c': 4}
    assert cache.getRow(3).getAsDict() == {'d': 5}


def test_clear():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    cache.clear()
    assert cache._storage == []


def test_clear2():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    cache.clear()
    assert cache._storage == []


def test_delete():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {'c': 4}
    assert cache.getRow(3).value() == {'d': 5}
    cache.delete(2, "c")
    assert 3 == cache.getData(1, "b")
    assert 5 == cache.getData(3, "d")
    assert None == cache.getData(2, "c")
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {}
    assert cache.getRow(3).value() == {'d': 5}


def test_delete2():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {'c': 4}
    assert cache.getRow(3).value() == {'d': 5}
    cache.delete(row=2, location="c")
    assert 3 == cache.getData(row=1, location="b")
    assert 5 == cache.getData(row=3, location="d")
    assert None == cache.getData(row=2,location="c")
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {}
    assert cache.getRow(3).value() == {'d': 5}


def test_getLocationThatDoesntExist():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    cache.getData(3, "e")


def test_getLocationThatDoesntExist2():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    cache.getData(row=3,location="e")



def test_getRow():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(3) == [5, None, None]

def test_getRow2():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(row=3) == [5, None, None]

def test_getRowAsList():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(row=3, asObj="list") == [5, None, None]


def test_getRowAsDict():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(3, asObj="dict") == {'b': 5, 'c': None, 'd': None}

def test_getRowAsDict2():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    assert cache.getRow(row=3, asObj="dict") == {'b': 5, 'c': None, 'd': None}




def test_unsetRow():
    cache = NestedCache(['b','c'],[[3],[4]])
    cache.unsetRow(2)
    assert cache.getRow(2) == [None, None]

def test_unsetRow2():
    cache = NestedCache(['b','c'],[[3],[4]])
    cache.unsetRow(row=2)
    assert cache.getRow(row=2) == [None, None]

def test_unsetRow_asDict():
    cache = NestedCache(['b','c'],[[3],[4]])
    cache.unsetRow(2)
    assert cache.getRow(2, asObj="dict") == {'b':None, 'c':None}

def test_unsetRow_asDict2():
    cache = NestedCache(['b','c'],[[3],[4]])
    cache.unsetRow(row=2)
    assert cache.getRow(row=2, asObj="dict") == {'b':None, 'c':None}



def test_deleteRow():
    cache = NestedCache(['b','c','d'],[[3],[4],[4]])
    cache.deleteRow(2)
    assert cache.getRow(2) == [4, None, None]

def test_deleteRow_getAsDict():
    cache = NestedCache(['b','c','d'],[[3],[4],[4]])
    cache.deleteRow(2)
    assert cache.getRow(2, asObj="dict") == {'b': 4, 'c': None, 'd': None}


# Adding data to columns that exist should change nothing about the width
def test_width_fromAdds():
    cache = NestedCache(['b','c','d'],[[3]])
    assert 3 == cache.width()
    cache.set(row=1,location="c",data=4)
    assert 3 == cache.width()
    cache.set(row=1,location="d",data=4)
    assert 3 == cache.width()



# adding columns that don't exist should fail gloriously
def test_fail_fromAddingColsThatDontExist():
    # Adding these should change nothing about the width
    cache = NestedCache(['b','c','d'],[[3]])
    with pytest.raises(NestedCacheException) as excinfo:
        cache.set(row=1,location="e",data=4)
    assert excinfo.value.message == "Location 'e' doesn't exist, to add it - addLocation()"


def test_height_fromDeletes():
    cache = NestedCache(['b','c','d'],[[3],[3,4],[5,1,5]])
    with pytest.raises(NestedCacheException) as excinfo:
        cache.set(row=3,location="d",data=4)
    assert excinfo.value.message == "There is already data at row:3 location:d/index:2, to change this data use update(row, location/index, data)"
    
    cache.deleteRow(row=2)
    print(cache.height())
    assert 2 == cache.height()
    cache.deleteRow(row=1)
    assert 1 == cache.height()


def test_addUnrecognizedLocation():
    cache = NestedCache(['b'],[[3]])

    with pytest.raises(NestedCacheException) as excinfo:
        cache.set(row=2, location='c', data=3)
    assert excinfo.value.message == "Row [2] doesn't exist, to add it - append"


# def test_deleteColumn_noIndex():

# def test_deleteColumn_noLocation():

# def test_deleteColumn_noMatchIndexLocation():

# def test_deleteColumn_noLocation():

# def test_deleteRow():

# try to delete row 0
# try to delete item from row 0
