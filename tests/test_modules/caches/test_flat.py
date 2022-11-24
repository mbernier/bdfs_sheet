import pytest

from modules.caches.flat import FlatCache
from modules.caches.exception import FlatCacheException


def test_cache_creation():
     cache = FlatCache()
     assert cache != None
     assert cache._storage == {}


def test_empty_cache_get():
    cache = FlatCache()
    value = cache.get("a")
    assert value == None

def test_empty_cache_get2():
    cache = FlatCache()
    value = cache.get(location="a")
    assert value == None


def test_cache_set():
    cache = FlatCache()
    cache.set("a", 1)
    value = cache.get("a")
    assert value == 1

def test_cache_set2():
    cache = FlatCache()
    cache.set(location="a", data=1)
    value = cache.get("a")
    assert value == 1

def test_cache_set_again():
    cache = FlatCache()
    assert cache._storage == {}
    cache.set("a", 2)
    value = cache.get("a")

    with pytest.raises(FlatCacheException) as excinfo:
        cache.set("a", 1)
    assert excinfo.value.message == "FlatCache has 2 at a. To update data in the cache, use update()"

def test_cache_set_again2():
    cache = FlatCache()
    assert cache._storage == {}
    cache.set(location="a", data=2)
    value = cache.get("a")

    with pytest.raises(FlatCacheException) as excinfo:
        cache.set(location="a", data=1)
    assert excinfo.value.message == "FlatCache has 2 at a. To update data in the cache, use update()"


def test_unset():
    cache = FlatCache()
    cache.set("b",3)
    cache.unset("b")
    assert None == cache.get("b")

def test_unset2():
    cache = FlatCache()
    cache.set(location="b", data=3)
    cache.unset(location="b")
    assert None == cache.get(location="b")


def test_unset_fail():
    cache = FlatCache()
    cache.set("b",3)
    cache.unset("c")
    assert 3 == cache.get("b")

def test_unset_fail2():
    cache = FlatCache()
    cache.set(location="b",data=3)
    cache.unset(location="c")
    assert 3 == cache.get(location="b")


def test_update():
    cache = FlatCache()
    cache.set("b",3)
    cache.update("b", 5)
    assert 5 == cache.get("b")

def test_update2():
    cache = FlatCache()
    cache.set(location="b", data=3)
    cache.update(location="b", data=5)
    assert 5 == cache.get(location="b")


def test_update_exception():
    cache = FlatCache()
    cache.set("b",3)

    with pytest.raises(FlatCacheException) as excinfo:
        cache.update("c", 5)
    assert excinfo.value.message == "There is nothing to update at c"

    assert 3 == cache.get("b")

def test_update_exception2():
    cache = FlatCache()
    cache.set(location="b",data=3)

    with pytest.raises(FlatCacheException) as excinfo:
        cache.update(location="c", data=5)
    assert excinfo.value.message == "There is nothing to update at c"

    assert 3 == cache.get(location="b")


def test_clear():
    cache = FlatCache()
    cache.set("b",3)
    cache.set("c",4)
    cache.set("d",5)

    assert cache._storage == {'b': 3, 'c': 4, 'd': 5}

    cache.clear()

    assert cache._storage == {}


def test_delete():
    cache = FlatCache()
    cache.set("b",3)
    cache.set("c",4)
    cache.set("d",5)

    assert cache._storage == {'b': 3, 'c': 4, 'd': 5}

    cache.delete("c")

    assert 3 == cache.get("b")
    assert 5 == cache.get("d")
    assert None == cache.get("c")
    assert cache._storage == {'b': 3, 'd': 5}

def test_delete2():
    cache = FlatCache()
    cache.set(location="b",data=3)
    cache.set(location="c",data=4)
    cache.set(location="d",data=5)

    assert cache._storage == {'b': 3, 'c': 4, 'd': 5}

    cache.delete(location="c")

    assert 3 == cache.get(location="b")
    assert 5 == cache.get(location="d")
    assert None == cache.get(location="c")
    assert cache._storage == {'b': 3, 'd': 5}