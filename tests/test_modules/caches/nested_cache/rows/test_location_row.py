import sys, pytest
from collections import OrderedDict
from modules.caches.nested_cache.rows.location import Nested_Cache_Rows_Location
from modules.caches.exception import Nested_Cache_Rows_Location_Exception
from modules.validations.exception import Validation_Exception



testData = ["one", "two", "three", "four"]


####
#
# Create Nested_Cache_Rows_Location
#
####

# test creation without data
def test_creation_without_data():
    row = Nested_Cache_Rows_Location()
    
# create then load
def test_creation_then_load_data():
    row = Nested_Cache_Rows_Location()
    row.load(testData)

# create passing data on instantiate
def test_creation_and_load_data():
    row = Nested_Cache_Rows_Location(testData)

####
#
# Width
#
####

# test width
def test_width():
    row = Nested_Cache_Rows_Location(testData)
    assert 4 == row.width()

####
#
# Add
#
####

# add a location that doesn't exist
def test_add():
    row = Nested_Cache_Rows_Location(testData)
    row.add("anotherHeader")
    assert 5 == row.width()


# add a location that exists
def test_add_location_that_exists():
    row = Nested_Cache_Rows_Location(testData)
    with pytest.raises(Nested_Cache_Rows_Location_Exception) as excinfo:
        row.add("two")
    assert "Flat_Cache has '1' at location: two. To update data in the cache, use updateData()" in excinfo.value.message


# add something that isn't a string
def test_add_not_string():
    row = Nested_Cache_Rows_Location(testData)
    with pytest.raises(Validation_Exception) as excinfo:
        row.add([1,2,3])
    assert "location was expected to be type str, but <class 'list'> was found for method add" in excinfo.value.message

####
#
# Get
#
####

# get a location from index
def test_get_index_by_location():
    row = Nested_Cache_Rows_Location(testData)
    assert 0 == row.get("one")

# get an index from location
def test_get_location_by_index():
    row = Nested_Cache_Rows_Location(testData)
    assert "one" == row.get(0)

####
#
# Get location index
#
####

# get both by location
def test_get_locationIndex():
    row = Nested_Cache_Rows_Location(testData)
    assert ("one", 0) == row.getLocationIndex("one")

# get both by index
def test_get_locationIndex2():
    row = Nested_Cache_Rows_Location(testData)
    assert ("two", 1) == row.getLocationIndex(1)

####
#
# Set
#
####

# set a location that exists
def test_set_existing_location():
    row = Nested_Cache_Rows_Location(testData)
    with pytest.raises(Nested_Cache_Rows_Location_Exception) as excinfo:
        row.setData(0,"zero")
    assert "Flat_Cache has 'one' at location: 0. To update data in the cache, use updateData()" in excinfo.value.message


# set a location that doesn't exists
def test_set_dne_location():
    row = Nested_Cache_Rows_Location(testData)
    row.setData(5,"five")
    assert ['one', 'two', 'three', 'four', 'five'] == row.getAsList()
    assert OrderedDict([('one', 0), ('two', 1), ('three', 2), ('four', 3), ('five', 5)]) == row.getAsDict()

    row.setData("six", 6)
    assert ['one', 'two', 'three', 'four', 'five', 'six'] == row.getAsList()
    assert OrderedDict([('one', 0), ('two', 1), ('three', 2), ('four', 3), ('five', 5), ('six', 6)]) == row.getAsDict()


####
#
# Update
#
####

# update successful
# def test_updateData():
#     row = Nested_Cache_Rows_Location(testData)
#     row.updateData("one", 7)
#     row.updateData(5, "seventeen")
#     print(row.getAsList())

# # update fail (location doesn't exist, try add)
# def test_update_fail():
#     row = Nested_Cache_Rows_Location(testData)
#     row.updateData("one", 7)
#     print(row.getAsList())


####
#
# Get Location Keys
#
####

# get location keys
def test_get_locationKeys():
    row = Nested_Cache_Rows_Location(testData)
    assert testData == row.getLocationKeys()
