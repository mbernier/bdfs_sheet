import pytest, pydantic
from modules.caches.nested_cache.row import Nested_Cache_Row
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.validations.exception import Validation_Exception

testHeaders = ["one", "two", "three", "four", "five"]
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
    row = Nested_Cache_Row(testHeaders, testData)
    print(row.width())
    assert 5 == row.width()

####
#
# Add
#
####

# add an index that exists
def test_add_index_that_does_exist():
    row = Nested_Cache_Row(testHeaders, testData)
    with pytest.raises(Nested_Cache_Row_Exception) as excinfo:
        row.insert(1, 500)
    assert "Flat_Cache has '2' at location: 1. To update data in the cache, use update()" in excinfo.value.message


# add something that isn't a string
def test_add_not_string_as_location():
    row = Nested_Cache_Row(testHeaders, testData)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as excinfo:
        row.insert([1,2,4],400)
    assert "value is not a valid integer" in str(excinfo.value)

####
#
# Get
#
####

# get data from index

def test_get_by_index():
    row = Nested_Cache_Row(testHeaders, testData)
    assert 2 == row.select(1)

# get data from index that doesn't exist
def test_get_by_index_dne():
    row = Nested_Cache_Row(testHeaders, testData)
    with pytest.raises(Flat_Cache_Exception) as excinfo:
        row.select(17)
    assert "Location '17' does not exist, try \"add_location('17')\"" in excinfo.value.message

####
#
# Set
#
####

# set a location that exists
def test_set_by_index_exists():
    row = Nested_Cache_Row(testHeaders, testData)
    row.update(1, "banana")

####
#
# Update
#
####

# update successful
def test_update_by_index_exists():
    row = Nested_Cache_Row(testHeaders, testData)
    row.update(1, "banana")


# update fail (location doesn't exist, try add)
def test_update_by_index_dne():
    row = Nested_Cache_Row(testHeaders, testData)

    with pytest.raises(Nested_Cache_Row_Exception) as excinfo:
        row.update(17, "banana")
    assert "Location '17' does not exist, try \"add_location('17')\"" in excinfo.value.message


