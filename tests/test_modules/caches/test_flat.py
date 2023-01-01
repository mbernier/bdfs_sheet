import pytest, time, pydantic
from modules.caches.flat import UPDATE_TIMESTAMP_KEY, UPDATE_TIMESTAMP_POSTFIX, Flat_Cache
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
    cache = Flat_Cache({'a':None})
    value = cache.select("a")
    assert value == None


def test_empty_cache_select():
    cache = Flat_Cache()
    cache.insert_location('a')
    value = cache.select(position="a")
    assert value == None
 

def test_pass_data_as_list():
    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache = Flat_Cache([1,2,3])
    assert "value is not a valid dict" in  str(excinfo.value)


def test_pass_locations_data():
    cache = Flat_Cache({'a': 1})
    assert 1 == cache.select("a")
    assert 1 == cache.select(0)


def test_cache_insert():
    cache = Flat_Cache({'a':None})
    cache.insert("a", 1)
    value = cache.select("a")
    assert value == 1


def test_cache_set2():
    cache = Flat_Cache({'a':None})
    cache.insert(position="a", data=1)
    value = cache.select("a")
    assert value == 1


def test_cache_set_again():
    cache = Flat_Cache({'a':None})
    assert cache.data.storage['a']['data'] == None
    assert cache.data.storage['a']['position'] == 0
    assert cache.data.storage[0]['data'] == None
    assert cache.data.storage[0]['position'] == 'a'

    cache.insert("a", 2)
    value = cache.select("a")
    assert 2 == value

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert("a", 1)
    assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update()"


def test_cache_set_again2():
    cache = Flat_Cache({'a':None})
    assert cache.data.storage['a']['data'] == None
    assert cache.data.storage['a']['position'] == 0

    assert cache.data.storage[0]['data'] == None
    assert cache.data.storage[0]['position'] == 'a'

    cache.insert(position="a", data=2)
    value = cache.select("a")

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert(position="a", data=1)
    assert excinfo.value.message == "Flat_Cache has '2' at location: a. To update data in the cache, use update()"


def test_insert_dne_location():
    cache = Flat_Cache({'a':None})
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert('b',12345)
    assert excinfo.value.message == "Location 'b' does not exist, try \"insert_location('b')\""


def test_update():
    cache = Flat_Cache({'b':None})
    cache.insert("b",3)
    cache.update("b", 5)
    assert 5 == cache.select("b")


def test_update2():
    cache = Flat_Cache({'b':None})
    cache.insert(position="b", data=3)
    cache.update(position="b", data=5)
    assert 5 == cache.select(position="b")


def test_update_exception():
    cache = Flat_Cache({'b':None})
    cache.insert("b",3)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update("c", 5)
    assert excinfo.value.message == "Location 'c' does not exist, try \"insert_location('c')\""

    assert 3 == cache.select("b")


def test_update_exception2():
    cache = Flat_Cache({'b':None})
    cache.insert(position="b",data=3)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update(position="c", data=5)
    assert excinfo.value.message == "Location 'c' does not exist, try \"insert_location('c')\""

    assert 3 == cache.select(position="b")


def test_select_all():
    cache = Flat_Cache({'b':1, 'c':2})
    keys = cache.getKeys()
    assert keys == ['b', 'c']
    allvalues = cache.select(update_timestamp=False)
    assert allvalues == {'b': 1, 'c': 2}

def test_delete():
    cache = Flat_Cache({'b':None})
    cache.insert("b",3)
    cache.delete("b")
    assert None == cache.select("b")

def test_unset2():
    cache = Flat_Cache({'b':None})
    cache.insert(position="b", data=3)
    cache.delete(position="b")
    assert None == cache.select(position="b")



def test_clear_all():
    cache = Flat_Cache({'b':None,'c':None,'d':None})
    cache.insert("b",3)
    cache.insert("c",4)
    cache.insert("d",5)

    assert cache.select(update_timestamp=False) == {'b': 3, 'c': 4, 'd': 5}

    cache.clear_all()

    assert cache.select(update_timestamp=False) == {'b': None, 'c': None, 'd': None}


def test_delete():
    cache = Flat_Cache({'b':None,'c':None,'d':None})
    cache.insert("b",3)
    cache.insert("c",4)
    cache.insert("d",5)

    assert cache.select(update_timestamp=False) == {'b': 3, 'c': 4, 'd': 5}

    cache.delete("c")

    assert 3 == cache.select("b")
    assert 5 == cache.select("d")
    assert None == cache.select("c")
    assert cache.select(update_timestamp=False) == {'b': 3, 'c': None, 'd': 5}

def test_delete2():
    cache = Flat_Cache({'b':None,'c':None,'d':None})
    cache.insert(position="b",data=3)
    cache.insert(position="c",data=4)
    cache.insert(position="d",data=5)

    assert cache.select(update_timestamp=False) == {'b': 3, 'c': 4, 'd': 5}

    cache.delete(position="c")

    assert 3 == cache.select(position="b")
    assert 5 == cache.select(position="d")
    assert None == cache.select(position="c")
    assert cache.select(update_timestamp=False) == {'b': 3, 'c':None, 'd': 5}

def test_delete_location():
    cache = Flat_Cache({'b':None,'c':None,'d':None})
    cache.insert(position="b",data=3)
    cache.insert(position="c",data=4)
    cache.insert(position="d",data=5)

    assert cache.data.storage['b']['position'] == 0
    assert cache.data.storage['b']['data'] == 3
    assert cache.data.storage[0]['position'] == 'b'
    assert cache.data.storage[0]['data'] == 3
    
    assert cache.data.storage['c']['position'] == 1
    assert cache.data.storage['c']['data'] == 4
    assert cache.data.storage[1]['position'] == 'c'
    assert cache.data.storage[1]['data'] == 4

    assert cache.data.storage['d']['position'] == 2
    assert cache.data.storage['d']['data'] == 5
    assert cache.data.storage[2]['position'] == 'd'
    assert cache.data.storage[2]['data'] == 5

    cache.delete_location('c')

    assert cache.select(update_timestamp=False) == {'b': 3, 'd': 5}    

    assert cache.data.storage['b']['position'] == 0
    assert cache.data.storage['b']['data'] == 3
    assert cache.data.storage[0]['position'] == 'b'
    assert cache.data.storage[0]['data'] == 3
    
    assert not 'c' in cache.data.storage.keys()
    assert not 2 in cache.data.storage.keys()

    assert cache.data.storage['d']['position'] == 1
    assert cache.data.storage['d']['data'] == 5
    assert cache.data.storage[1]['position'] == 'd'
    assert cache.data.storage[1]['data'] == 5



def test_update_location_fail():
    cache = Flat_Cache({'b':None,'c':None,'d':None})
    cache.insert(position="b",data=3)
    cache.insert(position="c",data=4)
    cache.insert(position="d",data=5)

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update_index(2,1)
    assert excinfo.value.message == "Cannot move index:2 to index:1 bc there is already data at index:1"

def test_insert_location_exists():
    cache = Flat_Cache({'b':None,'c':None,'d':None})
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert_location(position='c')
    assert excinfo.value.message == "Position 'c' already exists, you cannot insert a new location to Flat_Cache that already exists"

def test_insert_location_at_index():
    cache = Flat_Cache({'b':None,'c':None,'d':None})
    
    # effectively append
    cache.insert_location(position='e')
    assert cache.select(update_timestamp=False) == {'b': None, 'c':None, 'd': None, 'e': None}
    cache.insert(position="e", data=[1,2,3])
    assert cache.select(update_timestamp=False) == {'b': None, 'c':None, 'd': None, 'e': [1,2,3]}

    # effectively append, but with index at the same size as cache
    cache.insert_location(index=cache.size(), position='f')
    assert cache.select(update_timestamp=False) == {'b': None, 'c':None, 'd': None, 'e': [1,2,3], 'f': None}

    #insert in a location that is greater than the current size
    new_size = cache.size() + 5
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert_location(index=new_size, position='g')
    assert excinfo.value.message == f"index '{new_size}' is much greater than the current size of Flat_Cache: {cache.size()}, try adding items in between {cache.size()} and '{new_size}'"

    #insert in the middle somewhere
    cache.insert_location(index=4, position='g')
    assert cache.select(update_timestamp=False) == {'b': None, 'c':None, 'd': None, 'e': [1,2,3], 'g':None, 'f': None}

    #insert at the beginning
    cache.insert_location(index=0, position='a')
    data = cache.select(update_timestamp=False)
    assert data == {'a':None, 'b': None, 'c':None, 'd': None, 'e': [1,2,3], 'g':None, 'f':None}

def test_timestamp():
    cache = Flat_Cache({'b':None,'c':None,'d':None})

    # effectively append
    cache.insert_location(position='e')
    cache.insert(position="e", data=[1,2,3])
    data = cache.select()
    print(data)
    assert UPDATE_TIMESTAMP_KEY in data.keys()
    assert Flat_Cache.makeTimestampName("b") in data.keys()
    assert Flat_Cache.makeTimestampName("c") in data.keys()
    assert Flat_Cache.makeTimestampName("d") in data.keys()
    assert Flat_Cache.makeTimestampName("e") in data.keys()

    assert data[UPDATE_TIMESTAMP_KEY] != None
    assert data[Flat_Cache.makeTimestampName("b")] != None
    assert data[Flat_Cache.makeTimestampName("c")] != None
    assert data[Flat_Cache.makeTimestampName("d")] != None
    assert data[Flat_Cache.makeTimestampName("e")] != None

    assert type(data[UPDATE_TIMESTAMP_KEY]) is float
    assert type(data[Flat_Cache.makeTimestampName("b")]) is float
    assert type(data[Flat_Cache.makeTimestampName("c")]) is float
    assert type(data[Flat_Cache.makeTimestampName("d")]) is float
    assert type(data[Flat_Cache.makeTimestampName("e")]) is float

    del data[UPDATE_TIMESTAMP_KEY]
    del data[Flat_Cache.makeTimestampName("b")]
    del data[Flat_Cache.makeTimestampName("c")]
    del data[Flat_Cache.makeTimestampName("d")]
    del data[Flat_Cache.makeTimestampName("e")]
    
    assert data == {'b': None, 'c':None, 'd': None, 'e': [1,2,3]}


def test_timestamp_pre_load():
    timestamp = time.time()
    
    cache = Flat_Cache({'b':1,'c':2,'d':3, UPDATE_TIMESTAMP_KEY:timestamp})
    
    assert cache.getUpdateTimestamp(UPDATE_TIMESTAMP_KEY) == timestamp

    # effectively append
    cache.insert_location(position='e')
    cache.insert(position="e", data=[1,2,3])
    data = cache.select()

    del data[UPDATE_TIMESTAMP_KEY]
    del data[Flat_Cache.makeTimestampName("b")]
    del data[Flat_Cache.makeTimestampName("c")]
    del data[Flat_Cache.makeTimestampName("d")]
    del data[Flat_Cache.makeTimestampName("e")]
    
    assert data == {'b': 1, 'c':2, 'd': 3, 'e': [1,2,3]}

def test_getTimestampsAsStr():
    cache = Flat_Cache({'b':1,'c':2,'d':3})
    data = cache.getTimestampsAsStr()

    assert f"'{Flat_Cache.makeTimestampName('b')}" in data
    assert f"'{Flat_Cache.makeTimestampName('c')}" in data
    assert f"'{Flat_Cache.makeTimestampName('d')}" in data
    assert f"{UPDATE_TIMESTAMP_KEY}" in data


def test_getTimestampsAsList():
    cache = Flat_Cache({'b':1,'c':2,'d':3})
    data = cache.getTimestampsAsList()
    assert 4 == len(data)
    assert type(data[0]) == float
    assert type(data[1]) == float
    assert type(data[2]) == float
    assert type(data[3]) == float

def test_getTimestampKeys():
    cache = Flat_Cache({'b':1,'c':2,'d':3})
    data = cache.getTimestampKeys()

    assert data[0] == Flat_Cache.makeTimestampName("b")
    assert data[1] == Flat_Cache.makeTimestampName("c")
    assert data[2] == Flat_Cache.makeTimestampName("d")
    assert data[3] == UPDATE_TIMESTAMP_KEY


def test_getTimestampsAsDict():
    cache = Flat_Cache({'b':1,'c':2,'d':3})
    data = cache.getTimestampsAsDict()

    assert type(data[Flat_Cache.makeTimestampName('b')]) == float
    assert type(data[Flat_Cache.makeTimestampName('c')]) == float
    assert type(data[Flat_Cache.makeTimestampName('d')]) == float
    assert type(data[UPDATE_TIMESTAMP_KEY]) == float

def test_getAsString():
    cache = Flat_Cache({'b':1,'c':2,'d':3})
    data = str(cache)

    assert "Flat_Cache" in data
    assert "'b'" in data
    assert "'c'" in data
    assert "'d'" in data
    assert f"'{Flat_Cache.makeTimestampName('b')}" in data
    assert f"'{Flat_Cache.makeTimestampName('c')}" in data
    assert f"'{Flat_Cache.makeTimestampName('d')}" in data
    assert f"{UPDATE_TIMESTAMP_KEY}" in data

    data = cache.string(update_timestamp=False)
    assert "Flat_Cache" in data
    assert "'b'" in data
    assert "'c'" in data
    assert "'d'" in data
    assert not f"'{Flat_Cache.makeTimestampName('c')}" in data
    assert not f"'{Flat_Cache.makeTimestampName('d')}" in data
    assert not f"{UPDATE_TIMESTAMP_KEY}" in data

def test_getAsList():
    cache = Flat_Cache({'b':1,'c':2,'d':3})
    data = cache.getAsList()
    [1, 2, 3, 1672249755.2532558, 1672249755.2534258, 1672249755.253589, 1672249755.25365]
    assert 7 == len(data)
    assert data[0] == 1
    assert data[1] == 2
    assert data[2] == 3
    assert type(data[3]) == float
    assert type(data[4]) == float
    assert type(data[5]) == float
    assert type(data[6]) == float

    data = cache.getAsList(update_timestamp=False)
    assert data == [1, 2, 3]

def test_getAsDicts():
    cache = Flat_Cache({'b':1,'c':2,'d':3})
    data = cache.getAsDict()
    print(data)
    assert 7 == len(data)
    assert data['b'] == 1
    assert data['c'] == 2
    assert data['d'] == 3
    assert type(data[UPDATE_TIMESTAMP_KEY]) == float
    assert type(data[Flat_Cache.makeTimestampName('b')]) == float
    assert type(data[Flat_Cache.makeTimestampName('c')]) == float
    assert type(data[Flat_Cache.makeTimestampName('d')]) == float

    data = cache.getAsDict(update_timestamp=False)
    assert data == {'b': 1, 'c': 2, 'd': 3}
