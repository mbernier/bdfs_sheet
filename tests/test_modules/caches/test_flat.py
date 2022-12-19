import pytest

from modules.caches.flat import Flat_Cache
from modules.caches.exception import Flat_Cache_Exception


def test_cache_creation():
     cache = Flat_Cache()
     assert cache != None
     assert cache.data.storage == {}


def test_empty_cache_select():
    cache = Flat_Cache()
    cache.insert_location('a')
    value = cache.select("a")
    assert value == None


def test_empty_cache_select():
    cache = Flat_Cache(['a'])
    value = cache.select("a")
    assert value == None


def test_empty_cache_select():
    cache = Flat_Cache()
    cache.insert_location('a')
    value = cache.select(position="a")
    assert value == None
 

def test_pass_data_no_locations():
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache = Flat_Cache(locations=None, data=[1,2,3])
    assert excinfo.value.message == "Need locations in order to load data to Flat_Cache"


def test_pass_locations_data():
    cache = Flat_Cache(['a'],[1])
    assert 1 == cache.select("a")
    assert 1 == cache.select(0)


def test_pass_extra_locations():
    cache = Flat_Cache(['a'], [1])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.load_locations(["two","three"])
    assert excinfo.value.message == "Locations are already loaded, to add new keys use insert_location(location)"


def test_cache_insert():
    cache = Flat_Cache(['a'])
    cache.insert("a", 1)
    value = cache.select("a")
    assert value == 1


def test_cache_set2():
    cache = Flat_Cache(['a'])
    cache.insert(position="a", data=1)
    value = cache.select("a")
    assert value == 1


def test_cache_set_again():
    cache = Flat_Cache(['a'])
    assert cache.data.storage == {'a': {'data': None, 'position': 0}, 0: {'data': None, 'position': 'a'}}
    cache.insert("a", 2)
    value = cache.select("a")
    assert 2 == value

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert("a", 1)
    assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update()"


def test_cache_set_again2():
    cache = Flat_Cache(['a'])
    assert cache.data.storage == {'a': {'data': None, 'position': 0}, 0: {'data': None, 'position': 'a'}}
    cache.insert(position="a", data=2)
    value = cache.select("a")

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert(position="a", data=1)
    assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update()"


def test_insert_dne_location():
    cache = Flat_Cache(['a'])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert('b',12345)
    assert excinfo.value.message == "Location 'b' does not exist, try \"insert_location('b')\""


def test_update():
    cache = Flat_Cache(['b'])
    cache.insert("b",3)
    cache.update("b", 5)
    assert 5 == cache.select("b")


def test_update2():
    cache = Flat_Cache(['b'])
    cache.insert(position="b", data=3)
    cache.update(position="b", data=5)
    assert 5 == cache.select(position="b")


def test_update_exception():
    cache = Flat_Cache(['b'])
    cache.insert("b",3)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update("c", 5)
    assert excinfo.value.message == "Location 'c' does not exist, try \"insert_location('c')\""

    assert 3 == cache.select("b")


def test_update_exception2():
    cache = Flat_Cache(['b'])
    cache.insert(position="b",data=3)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update(position="c", data=5)
    assert excinfo.value.message == "Location 'c' does not exist, try \"insert_location('c')\""

    assert 3 == cache.select(position="b")


def test_select_all():
    cache = Flat_Cache(['b','c'], [1,2])
    keys = cache.getKeys()
    assert keys == ['b', 'c']
    allvalues = cache.select()
    assert allvalues == {'b': 1, 'c': 2}

def test_delete():
    cache = Flat_Cache(['b'])
    cache.insert("b",3)
    cache.delete("b")
    assert None == cache.select("b")

def test_unset2():
    cache = Flat_Cache(['b'])
    cache.insert(position="b", data=3)
    cache.delete(position="b")
    assert None == cache.select(position="b")



def test_clear_all():
    cache = Flat_Cache(['b','c','d'])
    cache.insert("b",3)
    cache.insert("c",4)
    cache.insert("d",5)

    assert cache.select() == {'b': 3, 'c': 4, 'd': 5}

    cache.clear_all()

    assert cache.select() == {'b': None, 'c': None, 'd': None}


def test_delete():
    cache = Flat_Cache(['b','c','d'])
    cache.insert("b",3)
    cache.insert("c",4)
    cache.insert("d",5)

    assert cache.select() == {'b': 3, 'c': 4, 'd': 5}

    cache.delete("c")

    assert 3 == cache.select("b")
    assert 5 == cache.select("d")
    assert None == cache.select("c")
    assert cache.select() == {'b': 3, 'c': None, 'd': 5}

def test_delete2():
    cache = Flat_Cache(['b','c','d'])
    cache.insert(position="b",data=3)
    cache.insert(position="c",data=4)
    cache.insert(position="d",data=5)

    assert cache.select() == {'b': 3, 'c': 4, 'd': 5}

    cache.delete(position="c")

    assert 3 == cache.select(position="b")
    assert 5 == cache.select(position="d")
    assert None == cache.select(position="c")
    assert cache.select() == {'b': 3, 'c':None, 'd': 5}

def test_remove_location():
    cache = Flat_Cache(['b','c','d'])
    cache.insert(position="b",data=3)
    cache.insert(position="c",data=4)
    cache.insert(position="d",data=5)

    assert cache.data.storage == {'b': {'position': 0, 'data': 3}, 0: {'position': 'b', 'data': 3}, 'c': {'position': 1, 'data': 4}, 1: {'position': 'c', 'data': 4}, 'd': {'position': 2, 'data': 5}, 2: {'position': 'd', 'data': 5}}

    cache.delete_location('c')

    assert cache.select() == {'b': 3, 'd': 5}    

    assert cache.data.storage == {'b': {'position': 0, 'data': 3}, 0: {'position': 'b', 'data': 3}, 'd': {'position': 1, 'data': 5}, 1: {'position': 'd', 'data': 5}}

def test_update_location_fail():
    cache = Flat_Cache(['b','c','d'])
    cache.insert(position="b",data=3)
    cache.insert(position="c",data=4)
    cache.insert(position="d",data=5)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update_index(2,1)
    assert excinfo.value.message == "Cannot move index:2 to index:1 bc there is already data at index:1"

def test_insert_location_exists():
    cache = Flat_Cache(['b','c','d'])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert_location(position='c')
    assert excinfo.value.message == "Position 'c' already exists, you cannot insert a new location to Flat_Cache that already exists"

def test_insert_location_at_index():
    cache = Flat_Cache(['b','c','d'])
    
    # effectively append
    cache.insert_location(position='e')
    assert cache.select() == {'b': None, 'c':None, 'd': None, 'e': None}
    cache.insert(position="e", data=[1,2,3])
    assert cache.select() == {'b': None, 'c':None, 'd': None, 'e': [1,2,3]}

    # effectively append, but with index at the same size as cache
    print(f"insert 'f' at {cache.size()}")
    cache.insert_location(index=cache.size(), position='f')
    assert cache.select() == {'b': None, 'c':None, 'd': None, 'e': [1,2,3], 'f': None}

    #insert in a location that is greater than the current size
    new_size = cache.size() + 5
    print(f"fail to insert 'g' at {new_size}")
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert_location(index=new_size, position='g')
    assert excinfo.value.message == f"index '{new_size}' is much greater than the current size of Flat_Cache: {cache.size()}, try adding items in between {cache.size()} and '{new_size}'"

    #insert in the middle somewhere
    print(f"success insert 'g' at 4")
    cache.insert_location(index=4, position='g')
    print("\n")
    print(cache.select())
    assert cache.select() == {'b': None, 'c':None, 'd': None, 'e': [1,2,3], 'g':None, 'f': None}

    #insert at the beginning
    print(f"insert 'a' at 0")
    cache.insert_location(index=0, position='a')
    print("\n")
    print(cache.select())
    assert cache.select() == {'a':None, 'b': None, 'c':None, 'd': None, 'e': [1,2,3], 'g':None, 'f':None}
