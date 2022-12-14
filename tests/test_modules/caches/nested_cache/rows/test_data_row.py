
import sys, pydantic, pytest
from modules.caches.nested_cache.rows.data import Nested_Cache_Rows_Data
from modules.caches.exception import Nested_Cache_Rows_Data_Exception


def test_createDataDicts():
    row = Nested_Cache_Rows_Data()
    locationData, indexData = row.createDataDicts("one", 1, "some data")

    assert locationData == {"position": 1, "data": "some data"}
    assert indexData == {"position": "one", "data": "some data"}

def test_add_at():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")

    locationDict, indexDict = row.getBothDicts("one")
    assert locationDict == {"position": 1, "data": "some data"}
    assert indexDict == {"position": "one", "data": "some data"}

    locationDict, indexDict = row.getBothDicts(1)
    assert locationDict == {"position": 1, "data": "some data"}
    assert indexDict == {"position": "one", "data": "some data"}


    locationPosition, indexPosition = row.getOtherPosition("one")
    assert locationPosition == "one"
    assert indexPosition == 1

    locationPosition, indexPosition = row.getOtherPosition(1)    
    assert locationPosition == "one"
    assert indexPosition == 1

    with pytest.raises(Nested_Cache_Rows_Data_Exception) as excinfo:
        row.add_at("one", 567)
    assert "Flat_Cache has '{'position': 1, 'data': 'some data'}' at location: one. To update data in the cache, use update_at_location()" in excinfo.value.message

    
def test_add_at_location():
    row = Nested_Cache_Rows_Data()
    with pytest.raises(Nested_Cache_Rows_Data_Exception) as excinfo:
        row.add_at_location("one", 567)
    assert "add_at_location DNE for Nested_Cache_Rows_Data, use add_at()" in excinfo.value.message


def test_set_at():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")
    row.set_at("two", 2, 'some other data')
    with pytest.raises(Nested_Cache_Rows_Data_Exception) as excinfo:
        row.set_at("one", 567)
    assert "Flat_Cache has '{'position': 1, 'data': 'some data'}' at location: one. To update data in the cache, use update_at_location()" in excinfo.value.message


def test_set_at_location():
    row = Nested_Cache_Rows_Data()
    with pytest.raises(Nested_Cache_Rows_Data_Exception) as excinfo:
        row.set_at_location("one", 567)
    assert "set_at_location DNE for Nested_Cache_Rows_Data, use set_at()" in excinfo.value.message    


def test_get_at():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")
    data = row.get_at("one")
    assert data == "some data"

    data = row.get_at(1)
    assert data == "some data"

def test_get_at_location():
    row = Nested_Cache_Rows_Data()
    with pytest.raises(Nested_Cache_Rows_Data_Exception) as excinfo:
        row.get_at_location("one", 567)
    assert "get_at_location DNE for Nested_Cache_Rows_Data, use get_at()" in excinfo.value.message    


def test_unset_at():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")
    row.unset_at("one")
    data = row.get_at("one")
    assert data == None
    data = row.get_at(1)
    assert data == None    

def test_unset_at_location():
    row = Nested_Cache_Rows_Data()
    with pytest.raises(Nested_Cache_Rows_Data_Exception) as excinfo:
        row.unset_at_location("one", 567)
    assert "unset_at_location DNE for Nested_Cache_Rows_Data, use unset_at()" in excinfo.value.message    


# def test_remove_position():
#     row = Nested_Cache_Rows_Data()
#     row.add_at("one", 1, "some new data")
#     row.remove_position(1)
#     data = row.get_at("one")
#     assert data == None

#     data = row.get_at(1)
#     assert data == None

def test_remove_location():
    row = Nested_Cache_Rows_Data()
    with pytest.raises(Nested_Cache_Rows_Data_Exception) as excinfo:
        row.remove_location("one")
    assert "remove_location DNE for Nested_Cache_Rows_Data, use remove_position()" in excinfo.value.message    


def test_clear_all():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")
    row.add_at("two", 2, "some other data")
    row.clear_all()

    data = row.get_at("one")
    assert data == None
    data = row.get_at(1)
    assert data == None    

    data = row.get_at("two")
    assert data == None
    data = row.get_at(2)
    assert data == None 

def test_str():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")

    string = str(row)
    assert "Nested_Cache_Rows_Data" in string
    assert "one: some data" in string

def test_getAsStringRaw():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")

    string = row.getAsStringRaw()
    assert "Nested_Cache_Rows_Data:\n OrderedDict([('one', 'some data'), (1, 'some data')])" == string


def test_getAsList():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")

    string = row.getAsList()
    assert ['some data'] == string

def test_getAsDict():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")

    string = row.getAsDict()
    assert {'one': 'some data'} == string

def test_getAsListRaw():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")

    with pytest.raises(Nested_Cache_Rows_Data_Exception) as excinfo:
        string = row.getAsListRaw()
    assert "Raw list doesn't make sense for Nested_Cache_Rows_Data, bc we have the same data in a string and an int position in storage, use getAsDictRaw" in excinfo.value.message
   
def test_getAsDictRaw():
    row = Nested_Cache_Rows_Data()
    row.add_at("one", 1, "some data")    
    string = row.getAsDictRaw()
    assert {'one': 'some data', 1: 'some data'} == string