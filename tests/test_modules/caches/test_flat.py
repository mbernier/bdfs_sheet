import pytest

from modules.caches.flat import Flat_Cache
from modules.caches.exception import Flat_Cache_Exception


def test_cache_creation():
     cache = Flat_Cache()
     assert cache != None
     assert cache.data.storage == {}


def test_empty_cache_select():
    cache = Flat_Cache()
    cache.add_location('a')
    value = cache.select("a")
    assert value == None

def test_empty_cache_select():
    cache = Flat_Cache(['a'])
    value = cache.select("a")
    assert value == None


# def test_empty_cache_select():
#     cache = Flat_Cache()
#     cache.add_location('a')
#     value = cache.select(location="a")
#     assert value == None
 

# def test_cache_insert():
#     cache = Flat_Cache()
#     cache.insert("a", 1)
#     value = cache.select("a")
#     assert value == 1

# def test_cache_set2():
#     cache = Flat_Cache()
#     cache.insert(location="a", data=1)
#     value = cache.select("a")
#     assert value == 1

# def test_cache_set_again():
#     cache = Flat_Cache()
#     assert cache.data.storage == {}
#     cache.insert("a", 2)
#     value = cache.select("a")

#     with pytest.raises(Flat_Cache_Exception) as excinfo:
#         cache.insert("a", 1)
#     assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update()"

# def test_cache_set_again2():
#     cache = Flat_Cache()
#     assert cache.data.storage == {}
#     cache.insert(location="a", data=2)
#     value = cache.select("a")

#     with pytest.raises(Flat_Cache_Exception) as excinfo:
#         cache.insert(location="a", data=1)
#     assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update()"


# def test_delete():
#     cache = Flat_Cache()
#     cache.insert("b",3)
#     cache.delete("b")
#     assert None == cache.select("b")

# def test_unset2():
#     cache = Flat_Cache()
#     cache.insert(location="b", data=3)
#     cache.delete(location="b")
#     assert None == cache.select(location="b")


# def test_unset_fail():
#     cache = Flat_Cache()
#     cache.insert("b",3)
#     cache.delete("c")
#     assert 3 == cache.select("b")

# def test_unset_fail2():
#     cache = Flat_Cache()
#     cache.insert(location="b",data=3)
#     cache.delete(location="c")
#     assert 3 == cache.select(location="b")


# def test_update():
#     cache = Flat_Cache()
#     cache.insert("b",3)
#     cache.update("b", 5)
#     assert 5 == cache.select("b")

# def test_update2():
#     cache = Flat_Cache()
#     cache.insert(location="b", data=3)
#     cache.update(location="b", data=5)
#     assert 5 == cache.select(location="b")


# def test_update_exception():
#     cache = Flat_Cache()
#     cache.insert("b",3)

#     with pytest.raises(Flat_Cache_Exception) as excinfo:
#         cache.update("c", 5)
#     assert excinfo.value.message == "There is nothing to update at position 'c' consider using set"

#     assert 3 == cache.select("b")

# def test_update_exception2():
#     cache = Flat_Cache()
#     cache.add_location('b')
#     cache.insert(location="b",data=3)

#     with pytest.raises(Flat_Cache_Exception) as excinfo:
#         cache.update(location="c", data=5)
#     assert excinfo.value.message == "Location 'c' does not exist, try \"add_location('c')\""

#     assert 3 == cache.select(location="b")


# def test_clear_all():
#     cache = Flat_Cache()
#     cache.insert("b",3)
#     cache.insert("c",4)
#     cache.insert("d",5)

#     assert cache.data.storage == {'b': 3, 'c': 4, 'd': 5}

#     cache.clear_all()

#     assert cache.data.storage == {}


# def test_delete():
#     cache = Flat_Cache()
#     cache.insert("b",3)
#     cache.insert("c",4)
#     cache.insert("d",5)

#     assert cache.data.storage == {'b': 3, 'c': 4, 'd': 5}

#     cache.delete("c")

#     assert 3 == cache.select("b")
#     assert 5 == cache.select("d")
#     assert None == cache.select("c")
#     assert cache.data.storage == {'b': 3, 'c': None, 'd': 5}

# def test_delete2():
#     cache = Flat_Cache()
#     cache.insert(location="b",data=3)
#     cache.insert(location="c",data=4)
#     cache.insert(location="d",data=5)

#     assert cache.data.storage == {'b': 3, 'c': 4, 'd': 5}

#     cache.delete(location="c")

#     assert 3 == cache.select(location="b")
#     assert 5 == cache.select(location="d")
#     assert None == cache.select(location="c")
#     assert cache.data.storage == {'b': 3, 'c':None, 'd': 5}


# def test_delete():
#     cache = Flat_Cache()
#     cache.insert("b",3)
#     cache.insert("c",4)
#     cache.insert("d",5)

#     assert cache.data.storage == {'b': 3, 'c': 4, 'd': 5}

#     cache.remove_location("c")

#     assert 3 == cache.select("b")
#     assert 5 == cache.select("d")
#     assert None == cache.select("c")
#     assert cache.data.storage == {'b': 3, 'd': 5}

# def test_delete2():
#     cache = Flat_Cache()
#     cache.insert(location="b",data=3)
#     cache.insert(location="c",data=4)
#     cache.insert(location="d",data=5)

#     assert cache.data.storage == {'b': 3, 'c': 4, 'd': 5}

#     cache.remove_location(location="c")

#     assert 3 == cache.select(location="b")
#     assert 5 == cache.select(location="d")
#     assert None == cache.select(location="c")
#     assert cache.data.storage == {'b': 3, 'd': 5}