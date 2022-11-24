import pytest

from modules.caches.nested import NestedCache
from modules.caches.exception import NestedCacheException
from modules.caches.exception import FlatCacheException

def test_cache_creation():
     cache = NestedCache()
     assert cache != None

     assert cache._storage == []


def test_empty_cache_get():
    cache = NestedCache()
    value = cache.get(row=1,location="test")
    assert value == None

def test_empty_cache_get():
    cache = NestedCache()
    value = cache.get(1, "test")
    assert value == None


def test_cache_set():
    cache = NestedCache()
    cache.set(1, "a", 1)
    value = cache.get(1, "a")
    assert value == 1

def test_cache_set():
    cache = NestedCache()
    cache.set(row=1, location="a", data=1)
    value = cache.get(1, "a")
    assert value == 1


def test_cache_set_again():
    cache = NestedCache()
    assert cache._storage == []
    cache.set(1, "a", 2)
    value = cache.get(1, "a")

    with pytest.raises(NestedCacheException) as excinfo:
        cache.set(1, "a", 1)
    assert excinfo.value.message == "Cache has 2 at 1:a. To update data in the cache, use update()"

def test_cache_set_again2():
    cache = NestedCache()
    assert cache._storage == []
    cache.set(row=1, location="a", data=2)
    value = cache.get(location="a", row=1)

    with pytest.raises(NestedCacheException) as excinfo:
        cache.set(row=1, location="a", data=1)
    # assert excinfo.value.message == "NestedCache has 2 at a. To update data in the cache, use update()"
    assert excinfo.value.message == "Cache has 2 at 1:a. To update data in the cache, use update()"

def test_unset():
    cache = NestedCache()
    cache.set(1,"b",3)
    cache.unset(1, "b")
    assert None == cache.get(1, "b")

def test_unset2():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    cache.unset(row=1, location="b")
    assert None == cache.get(row=1, location="b")


def test_unset_fail():
    cache = NestedCache()
    cache.set(1, "b",3)
    cache.unset(1, "c")
    assert 3 == cache.get(1, "b")

def test_unset_fail():
    cache = NestedCache()
    cache.set(row=1, location="b",data=3)
    cache.unset(row=1, location="c")
    assert 3 == cache.get(row=1, location="b")


def test_update():
    cache = NestedCache()
    cache.set(1, "b",3)
    cache.update(1, "b", 5)

    assert 5 == cache.get(1, "b")


def test_update2():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    cache.update(row=1,location="b",data=5)

    assert 5 == cache.get(row=1, location="b")


def test_update_exception():
    cache = NestedCache()
    cache.set(1, "b",3)
    with pytest.raises(FlatCacheException) as excinfo:
        cache.update(1, "c", 5)
    assert excinfo.value.message == "There is nothing to update at c"
    assert 3 == cache.get(1, "b")

def test_update_exception2():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    with pytest.raises(FlatCacheException) as excinfo:
        cache.update(row=1,location="c",data=5)
    assert excinfo.value.message == "There is nothing to update at c"
    assert 3 == cache.get(row=1, location="b")


def test_clear():
    cache = NestedCache()
    cache.set(1,"b",3)
    cache.set(2,"c",4)
    cache.set(3,"d",5)
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {'c': 4}
    assert cache.getRow(3).value() == {'d': 5}
    cache.clear()
    assert cache._storage == []


def test_clear2():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    cache.set(row=2,location="c",data=4)
    cache.set(row=3,location="d",data=5)
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {'c': 4}
    assert cache.getRow(3).value() == {'d': 5}
    cache.clear()
    assert cache._storage == []


def test_delete():
    cache = NestedCache()
    cache.set(1,"b",3)
    cache.set(2,"c",4)
    cache.set(3,"d",5)
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {'c': 4}
    assert cache.getRow(3).value() == {'d': 5}
    cache.delete(2, "c")
    assert 3 == cache.get(1, "b")
    assert 5 == cache.get(3, "d")
    assert None == cache.get(2, "c")
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {}
    assert cache.getRow(3).value() == {'d': 5}


def test_delete2():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    cache.set(row=2,location="c",data=4)
    cache.set(row=3,location="d",data=5)
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {'c': 4}
    assert cache.getRow(3).value() == {'d': 5}
    cache.delete(row=2, location="c")
    assert 3 == cache.get(row=1, location="b")
    assert 5 == cache.get(row=3, location="d")
    assert None == cache.get(row=2,location="c")
    assert cache.getRow(1).value() == {'b': 3}
    assert cache.getRow(2).value() == {}
    assert cache.getRow(3).value() == {'d': 5}

def test_getRow():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    cache.set(row=2,location="c",data=4)
    cache.set(row=3,location="d",data=5)
    cache.set(row=3,location="e",data=6)
    assert cache.getRow(3).value() == {'d': 5, 'e': 6}

def test_getRow2():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    cache.set(row=2,location="c",data=4)
    cache.set(row=3,location="d",data=5)
    cache.set(row=3,location="e",data=6)
    assert cache.getRow(row=3).value() == {'d': 5, 'e': 6}


def test_unsetRow():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    cache.set(row=2,location="c",data=4)
    cache.unsetRow(2)
    assert cache.getRow(2).value() == {}

def test_unsetRow2():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    cache.set(row=2,location="c",data=4)
    cache.unsetRow(row=2)
    assert cache.getRow(row=2).value() == {}


def test_deleteRow():
    cache = NestedCache()
    cache.set(row=1,location="b",data=3)
    cache.set(row=2,location="c",data=4)
    cache.set(row=3,location="d",data=4)
    cache.deleteRow(2)
    assert cache.getRow(2).value() == {'d':4}
