import pytest
from modules.caches.nested_cache.row import Nested_Cache_Row
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.validations.exception import Validation_Exception


testData = [1,2,3,4,5]

####
#
# Create Nested_Cache_Rows_Location
#
####

# test creation without data
def test_creation_without_data():
    row = Nested_Cache_Row()
    
# create then load

def test_creation_then_load_data():
    row = Nested_Cache_Row()
    row.load(testData)

# create passing data on instantiate
def test_creation_with_data_on_create():
    row = Nested_Cache_Row(testData)

####
#
# Width
#
####

# test width
def test_width():
    row = Nested_Cache_Row(testData)
    assert 5 == row.width()

####
#
# Add
#
####

# add a location that doesn't exist
def test_add_location_does_not_exist():
    row = Nested_Cache_Row(testData)
    row.add(7,"seven")

# add an index that exists
def test_add_index_that_does_exist():
    row = Nested_Cache_Row(testData)
    with pytest.raises(Nested_Cache_Row_Exception) as excinfo:
        row.add(1, 500)
    assert "Flat_Cache has '2' at location: 1. To update data in the cache, use updateData()" in excinfo.value.message


# add something that isn't a string
def test_add_not_string_as_location():
    row = Nested_Cache_Row(testData)
    with pytest.raises(Validation_Exception) as excinfo:
        row.add([1,2,4],400)
    assert excinfo.value.message == "index was expected to be type int, but <class 'list'> was found for method add"

####
#
# Get
#
####

# get data from index

def test_get_by_index():
    row = Nested_Cache_Row(testData)
    assert 2 == row.get(1)

# get data from index that doesn't exist
def test_get_by_index_dne():
    row = Nested_Cache_Row(testData)
    assert None == row.get(17)

####
#
# Set
#
####

# set a location that exists
def test_set_by_index_exists():
    row = Nested_Cache_Row(testData)
    with pytest.raises(Nested_Cache_Row_Exception) as excinfo:
        row.setData(1, "banana")
    assert "Flat_Cache has '2' at location: 1. To update data in the cache, use updateData()" in excinfo.value.message


# set a location that doesn't exists
def test_get_by_index_dne():
    row = Nested_Cache_Row(testData)
    row.setData(17, "banana")

    assert "banana" == row.get(17)

####
#
# Update
#
####

# update successful
def test_update_by_index_exists():
    row = Nested_Cache_Row(testData)
    row.updateData(1, "banana")


# update fail (location doesn't exist, try add)
def test_update_by_index_dne():
    row = Nested_Cache_Row(testData)

    with pytest.raises(Nested_Cache_Row_Exception) as excinfo:
        row.updateData(17, "banana")
    assert "There is nothing to update at position '17' consider using set" in excinfo.value.message