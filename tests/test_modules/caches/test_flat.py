import pytest

from modules.caches.flat import Flat_Cache
from modules.caches.exception import Flat_Cache_Exception


def test_cache_creation():
     cache = Flat_Cache()
     assert cache != None
     assert cache.data.storage == {}


def test_empty_cache_get_at_location():
    cache = Flat_Cache()
    value = cache.get_at_location("a")
    assert value == None

def test_empty_cache_get_at_location():
    cache = Flat_Cache()
    value = cache.get_at_location(location="a")
    assert value == None


def test_cache_set_at_location():
    cache = Flat_Cache()
    cache.set_at_location("a", 1)
    value = cache.get_at_location("a")
    assert value == 1

def test_cache_set2():
    cache = Flat_Cache()
    cache.set_at_location(location="a", data=1)
    value = cache.get_at_location("a")
    assert value == 1

def test_cache_set_again():
    cache = Flat_Cache()
    assert cache.data.storage == {}
    cache.set_at_location("a", 2)
    value = cache.get_at_location("a")

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.set_at_location("a", 1)
    assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update_at_location()"

def test_cache_set_again2():
    cache = Flat_Cache()
    assert cache.data.storage == {}
    cache.set_at_location(location="a", data=2)
    value = cache.get_at_location("a")

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.set_at_location(location="a", data=1)
    assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update_at_location()"


def test_unset_at_location():
    cache = Flat_Cache()
    cache.set_at_location("b",3)
    cache.unset_at_location("b")
    assert None == cache.get_at_location("b")

def test_unset2():
    cache = Flat_Cache()
    cache.set_at_location(location="b", data=3)
    cache.unset_at_location(location="b")
    assert None == cache.get_at_location(location="b")


def test_unset_fail():
    cache = Flat_Cache()
    cache.set_at_location("b",3)
    cache.unset_at_location("c")
    assert 3 == cache.get_at_location("b")

def test_unset_fail2():
    cache = Flat_Cache()
    cache.set_at_location(location="b",data=3)
    cache.unset_at_location(location="c")
    assert 3 == cache.get_at_location(location="b")


def test_update_at_location():
    cache = Flat_Cache()
    cache.set_at_location("b",3)
    cache.update_at_location("b", 5)
    assert 5 == cache.get_at_location("b")

def test_update2():
    cache = Flat_Cache()
    cache.set_at_location(location="b", data=3)
    cache.update_at_location(location="b", data=5)
    assert 5 == cache.get_at_location(location="b")


def test_update_exception():
    cache = Flat_Cache()
    cache.set_at_location("b",3)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update_at_location("c", 5)
    assert excinfo.value.message == "There is nothing to update at position 'c' consider using set"

    assert 3 == cache.get_at_location("b")

def test_update_exception2():
    cache = Flat_Cache()
    cache.set_at_location(location="b",data=3)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update_at_location(location="c", data=5)
    assert excinfo.value.message == "There is nothing to update at position 'c' consider using set"

    assert 3 == cache.get_at_location(location="b")


def test_clear_all():
    cache = Flat_Cache()
    cache.set_at_location("b",3)
    cache.set_at_location("c",4)
    cache.set_at_location("d",5)

    assert cache.data.storage == {'b': 3, 'c': 4, 'd': 5}

    cache.clear_all()

    assert cache.data.storage == {}


def test_delete_at_location():
    cache = Flat_Cache()
    cache.set_at_location("b",3)
    cache.set_at_location("c",4)
    cache.set_at_location("d",5)

    assert cache.data.storage == {'b': 3, 'c': 4, 'd': 5}

    cache.delete_at_location("c")

    assert 3 == cache.get_at_location("b")
    assert 5 == cache.get_at_location("d")
    assert None == cache.get_at_location("c")
    assert cache.data.storage == {'b': 3, 'd': 5}

def test_delete2():
    cache = Flat_Cache()
    cache.set_at_location(location="b",data=3)
    cache.set_at_location(location="c",data=4)
    cache.set_at_location(location="d",data=5)

    assert cache.data.storage == {'b': 3, 'c': 4, 'd': 5}

    cache.delete_at_location(location="c")

    assert 3 == cache.get_at_location(location="b")
    assert 5 == cache.get_at_location(location="d")
    assert None == cache.get_at_location(location="c")
    assert cache.data.storage == {'b': 3, 'd': 5}