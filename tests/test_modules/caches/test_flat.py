import pytest

from modules.caches.flat import Flat_Cache
from modules.caches.exception import Flat_Cache_Exception


def test_cache_creation():
     cache = Flat_Cache()
     assert cache != None
     assert cache._storage == {}


def test_empty_cache_get():
    cache = Flat_Cache()
    value = cache.get("a")
    assert value == None

def test_empty_cache_get2():
    cache = Flat_Cache()
    value = cache.get(location="a")
    assert value == None


def test_cache_set():
    cache = Flat_Cache()
    cache.set("a", 1)
    value = cache.get("a")
    assert value == 1

def test_cache_set2():
    cache = Flat_Cache()
    cache.set(location="a", data=1)
    value = cache.get("a")
    assert value == 1

def test_cache_set_again():
    cache = Flat_Cache()
    assert cache._storage == {}
    cache.set("a", 2)
    value = cache.get("a")

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.set("a", 1)
    assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update()"

def test_cache_set_again2():
    cache = Flat_Cache()
    assert cache._storage == {}
    cache.set(location="a", data=2)
    value = cache.get("a")

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.set(location="a", data=1)
    assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update()"


def test_unset():
    cache = Flat_Cache()
    cache.set("b",3)
    cache.unset("b")
    assert None == cache.get("b")

def test_unset2():
    cache = Flat_Cache()
    cache.set(location="b", data=3)
    cache.unset(location="b")
    assert None == cache.get(location="b")


def test_unset_fail():
    cache = Flat_Cache()
    cache.set("b",3)
    cache.unset("c")
    assert 3 == cache.get("b")

def test_unset_fail2():
    cache = Flat_Cache()
    cache.set(location="b",data=3)
    cache.unset(location="c")
    assert 3 == cache.get(location="b")


def test_update():
    cache = Flat_Cache()
    cache.set("b",3)
    cache.update("b", 5)
    assert 5 == cache.get("b")

def test_update2():
    cache = Flat_Cache()
    cache.set(location="b", data=3)
    cache.update(location="b", data=5)
    assert 5 == cache.get(location="b")


def test_update_exception():
    cache = Flat_Cache()
    cache.set("b",3)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update("c", 5)
    assert excinfo.value.message == "There is nothing to update at position 'c' consider using set"

    assert 3 == cache.get("b")

def test_update_exception2():
    cache = Flat_Cache()
    cache.set(location="b",data=3)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update(location="c", data=5)
    assert excinfo.value.message == "There is nothing to update at position 'c' consider using set"

    assert 3 == cache.get(location="b")


def test_clear():
    cache = Flat_Cache()
    cache.set("b",3)
    cache.set("c",4)
    cache.set("d",5)

    assert cache._storage == {'b': 3, 'c': 4, 'd': 5}

    cache.clear()

    assert cache._storage == {}


def test_delete():
    cache = Flat_Cache()
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
    cache = Flat_Cache()
    cache.set(location="b",data=3)
    cache.set(location="c",data=4)
    cache.set(location="d",data=5)

    assert cache._storage == {'b': 3, 'c': 4, 'd': 5}

    cache.delete(location="c")

    assert 3 == cache.get(location="b")
    assert 5 == cache.get(location="d")
    assert None == cache.get(location="c")
    assert cache._storage == {'b': 3, 'd': 5}