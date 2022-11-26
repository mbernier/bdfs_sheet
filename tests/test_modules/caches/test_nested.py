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

def test_getRow():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    cache.set(3, "e", 6)
    assert cache.getRow(3).value() == {'d': 5, 'e': 6}

def test_getRow2():
    cache = NestedCache(['b','c','d'],[[3],[4],[5]])
    cache.set(row=3,location="e",data=6)
    assert cache.getRow(row=3).value() == {'d': 5, 'e': 6}


def test_unsetRow():
    cache = NestedCache(['b','c'],[[3],[4]])
    cache.unsetRow(2)
    assert cache.getRow(2).value() == {}

def test_unsetRow2():
    cache = NestedCache(['b','c'],[[3],[4]])
    cache.unsetRow(row=2)
    assert cache.getRow(row=2).value() == {}


def test_deleteRow():
    cache = NestedCache(['b','c','d'],[[3],[4],[4]])
    cache.deleteRow(2)
    assert cache.getRow(2).value() == {'d':4}


def test_width_fromAdds():
    cache = NestedCache(['b','c','d'],[[3]])
    assert 1 == cache.width()
    cache.set(row=2,location="c",data=4)
    assert 2 == cache.width()
    cache.set(row=3,location="d",data=4)
    assert 3 == cache.width()


def test_width_fromDeletes():
    cache = NestedCache(['b','c','d'],[[3],[3,4],[5,1,5]])
    with pytest.raises(NestedCacheException) as excinfo:
        cache.set(row=3,location="d",data=4)
    assert excinfo.value.message == "There is already data at row:3 location:d/index:2, to change this data use update(row, location/index, data)"
    
    cache.delete(row=2, location="c")
    assert 2 == cache.width()
    cache.delete(row=1, location="c")
    assert 1 == cache.width()



# def test_height():

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
