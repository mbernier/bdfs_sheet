import pytest, pydantic

from modules import caches
from modules.caches.flat import Flat_Cache
from modules.caches.nested import Nested_Cache
from modules.caches.exception import Nested_Cache_Exception
from modules.caches.exception import Flat_Cache_Exception

def test_cache_creation():
     cache = Nested_Cache([], [])
     assert cache != None
     assert cache.getAsListOfLists() == []


def test_empty_cache_select():
    cache = Nested_Cache([], [])
    with pytest.raises(Nested_Cache_Exception) as excinfo:
        value = cache.select(row=0,position="test")
    assert excinfo.value.message == "Row 0 doesn't exist, to add it use insert(rowData)"

def test_empty_cache_select2():
    cache = Nested_Cache([], [])

    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.insert([1])
    assert excinfo.value.message == "Location '0' does not exist, try \"insert_location('0')\""

    cache.insert_location("test")

    assert cache.height() == 0
    
    cache.insert([1])

    cache.select(0, "test")

    value = cache.select(0, "test")
    


def test_cache_trySetOnNewRow():
    cache = Nested_Cache(['a'],[[1]])

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.insert(1, position="a", data=1)
    assert "unexpected keyword arguments: 'position', 'data' (type=type_error)" in str(excinfo.value)

    value = cache.select(0, "a")

    assert value == 1


def test_cache_trysetOnNewRow2():
    cache = Nested_Cache(['a'],[[1]])

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.insert(row=1, position="a", data=1)
    assert "unexpected keyword arguments: 'row', 'position', 'data' (type=type_error)" in str(excinfo.value)
    
    cache.insert([1])

    value = cache.select(1, "a")
    assert value == 1


def test_cache_set_again():
    cache = Nested_Cache(['a'],[[2]])
    value = cache.select(0, "a")

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.insert(0, "a", 1)
    assert "2 positional arguments expected but 4 given (type=type_error)" in str(excinfo.value)


def test_cache_set_again2():
    cache = Nested_Cache(["a"],[[2]])
    value = cache.select(position="a", row=0)

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.insert(row=0, position="a", data=1)
    # assert excinfo.value.message == "Nested_Cache has 2 at a. To update data in the cache, use update()"
    assert "unexpected keyword arguments: 'row', 'position', 'data' (type=type_error)" in str(excinfo.value)


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
    assert excinfo.value.message == "Location '2' does not exist, try \"insert_location('2')\""
    assert 3 == cache.select(0, "b")


def test_update_exception2():
    cache = Nested_Cache(['b'],[[3]])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        cache.update(row=0,position="c",data=5)
    assert excinfo.value.message == "Location 'c' does not exist, try \"insert_location('c')\""
    assert 3 == cache.select(row=0, position="b")


def test_getAsDict():
    cache = Nested_Cache(['b','c','d'],[[3],[None, 4, None],[None, None, 5]])
    assert cache.select(0, updated_timestamp=False) == {'b': 3, 'c': None, 'd': None}
    assert cache.select(1, updated_timestamp=False) == {'b': None, 'c': 4, 'd': None}
    assert cache.select(2, updated_timestamp=False) == {'b': None, 'c': None, 'd': 5}


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
    assert excinfo.value.message == "Location 'e' does not exist, try \"insert_location('e')\""


def test_getLocationThatDoesntExist2():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        assert cache.select(row=2,position="e") == None
    assert excinfo.value.message == "Location 'e' does not exist, try \"insert_location('e')\""

    




def test_select():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.select(2, updated_timestamp=False) == {'b': 5, 'c': None, 'd': None}

def test_select2():
    cache = Nested_Cache(['b','c','d'],[[3],[4],[5]])
    assert cache.select(row=2, updated_timestamp=False) == {'b': 5, 'c': None, 'd': None}



# Adding data to columns that exist should change nothing about the width
def test_width_fromAdds():
    cache = Nested_Cache(['b','c','d'],[[3]])
    assert 3 == cache.width()

    rowItem = cache.select(row=0, position='c')
    assert None == rowItem
    
    cache.update(row=0, position="c", data=4)
    assert 3 == cache.width()
    
    cache.update(row=0, position="d", data=4)
    assert 3 == cache.width()

def test_delete_column():
    cache = Nested_Cache(['b','c','d'],[[3]])
    
    cache.deleteColumn('c')
    assert cache.select(0, updated_timestamp=False) == {'b': 3, 'd': None}

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.deleteColumn(1)
    assert "str type expected" in str(excinfo.value)

def test_delete_columns():
    cache = Nested_Cache(['b','c','d','e','f'],[[3,4,5,6,7]])
    
    cache.deleteColumns(['c','d','e'])
    assert cache.select(0, updated_timestamp=False) == {'b': 3, 'f': 7}


def test_delete_columns_check_first_row():
    cache = Nested_Cache(['b','c','d','e','f'],[[3,4,5,6,7]])

    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.deleteColumns([1,2,3])
    assert "str type expected" in str(excinfo.value)


def test_delete_columns_check_multi_rows():
    cache = Nested_Cache(['b','c','d','e','f'],[[3,4,5,6,7],[1,2,3,4,5]])
    
    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        cache.deleteColumns([1,2,3])
    assert "str type expected" in str(excinfo.value)

    cache.deleteColumns(['c','d','e'])

    assert cache.select(0, updated_timestamp=False) == {'b': 3, 'f': 7}
    assert cache.select(1, updated_timestamp=False) == {'b': 1, 'f': 5}

def test_updateRow():
    cache = Nested_Cache(['b','c','d','e','f'],[[3,4,5,6,7],[1,2,3,4,5]])
    cache.updateRow(1, [10,20,30,40,50])

    assert cache.select(0, updated_timestamp=False) == {'b': 3, 'c': 4,'d': 5,'e': 6,'f': 7}
    assert cache.select(1, updated_timestamp=False) == {'b': 10, 'c': 20,'d': 30,'e': 40,'f': 50}

def test_reorderColumns():
    cache = Nested_Cache(['b','c','d','e','f'],[[3,4,5,6,7],[1,2,3,4,5]])
    cache.reorderColumns(['f','b','d','c','e'])
    assert cache.select(0, updated_timestamp=False) == {'f': 7, 'b': 3, 'd': 5, 'c': 4, 'e': 6}
    assert cache.select(1, updated_timestamp=False) == {'f': 5, 'b': 1, 'd': 3, 'c': 2, 'e': 4}