import gspread, pytest
from modules.spreadsheets.bdfs_test import BdfsInventory_Test_Spreadsheet
from modules.worksheets.exception import Bdfs_Worksheet_Exception

worksheetName = "test_easy_data"
renameWorksheetName = "test_easy_data_new_title"
copyFromWorksheetName = "demo_worksheet"


####
#
# Setup the sheet for testing, creates these spreadsheets out of the scope of the Bdfs functionality
#   so when this is run, you have to re-setup Bdfs_Spreadsheet otherwise, it doens't know about the 
#   new sheets
#
####
print(" Running setup") #for some reason pytest chops the first character of this statement...
sheet = BdfsInventory_Test_Spreadsheet()
spreadsheet = sheet.setupSpreadsheet()

# see if the sheetName 
try:
    testWorksheetExists = spreadsheet.worksheet(worksheetName)
    print(f"Worksheet: {worksheetName} found, deleting it")
    spreadsheet.del_worksheet(testWorksheetExists)

except gspread.exceptions.WorksheetNotFound:
    print(f"Worksheet: {worksheetName} isn't found, creating it")

try:
    testWorksheetExists = spreadsheet.worksheet(renameWorksheetName)
    print(f"Worksheet: {renameWorksheetName} found, deleting it")
    spreadsheet.del_worksheet(testWorksheetExists)

except gspread.exceptions.WorksheetNotFound:
    print(f"Worksheet: {renameWorksheetName} wasn't found, isn't that nice!")

worksheet1 = spreadsheet.worksheet(copyFromWorksheetName)
worksheet2 = worksheet1.duplicate(1, None, worksheetName)

del sheet
del spreadsheet
del worksheet1
del worksheet2


####
#
# Create a spreadsheet for the tests to run on
#
####
sheet = BdfsInventory_Test_Spreadsheet() 
test_worksheet = sheet.getWorksheet(worksheetName)

####
#
# Not Implemented, raises Exceptions
#
####

def test_removeColumns():
    with pytest.raises(Bdfs_Worksheet_Exception) as excinfo:
        test_worksheet.changed("whatever")
    assert excinfo.value.message == f"there is no 'whatever' in data.changes keys, add it to __setup() to track it"

####
#
# Implemented
#
####


def test_changed_isChanged():
    with pytest.raises(Bdfs_Worksheet_Exception) as excinfo:
        test_worksheet.changed("whatever")
    assert excinfo.value.message == f"there is no 'whatever' in data.changes keys, add it to __setup() to track it"
    
    test_worksheet.changed("data")
    assert True == test_worksheet.isChanged("data")
    
    test_worksheet.changed("data", False)
    assert False == test_worksheet.isChanged("data")

def test_getTitle():
    title = test_worksheet.getTitle()
    assert worksheetName == title

def test_setTitle_to_same_title():
    #if the titles are the same, we don't set the flag or the uncommitted title
    title = test_worksheet.getTitle()

    newTitle = test_worksheet.getTitle()

    test_worksheet.setTitle(newTitle)

    assert title == test_worksheet.getTitle()
    assert title == test_worksheet.getOriginalTitle()
    assert test_worksheet.isChanged('title') == False


def test_setTitle():
    title = test_worksheet.getTitle()

    newTitle = "test_easy_data_new_title"

    test_worksheet.setTitle(newTitle)

    assert newTitle == test_worksheet.getTitle()
    assert title == test_worksheet.getOriginalTitle()
    assert test_worksheet.isChanged('title') == True


def test_getA1():
    assert "A1" == test_worksheet.getA1(1,1)
    assert "E5" == test_worksheet.getA1(5,5)


def test_getDataRange():
    dataRange = test_worksheet.getDataRange()
    assert dataRange == "A1:C4" #this counts the header row as row 1, where normally we don't do that in the code, bc gspread counts header row as row 1


def test_getExpectedColumns():
    cols = test_worksheet.getExpectedColumns()
    assert cols == ['Updated Date', 'Title', 'Hardware', 'Published', 'Type', 'On BDFS?', 'Vendor', 'Handle', 'Type', 'Glass', 'SKU', 'SEO Title', 'Tags', 'Sarto SKU', 'Color', 'UnitedPorte URL', 'Image 1 URL', 'Image 1 SEO', 'Image 2 URL', 'Image 2 SEO', 'Image 3 URL', 'Image 3 SEO', 'Image 4 URL', 'Image 4 SEO', 'Image 5 URL', 'Image 5 SEO', 'Description']


def test_getColumns():
    cols = test_worksheet.getColumns()
    assert cols == ['Name', 'Birthday', 'Email']
  

def test_getColumnCounts():
    counts = test_worksheet.getColumnCounts()
    # also tests the gspread_worksheet_resize_to_data, bc if the data width is the same we got it right
    # not setting to a specific number, bc we don't care what the width is, just that they are the same
    assert counts['data'] == counts['gspread_worksheet'] 


def test_addColumns():
    test_worksheet.addColumn("newColumn1")
    assert test_worksheet.getColumns() == ['Name', 'Birthday','Email', 'newColumn1']

    test_worksheet.addColumn(name="newColumn3", index=3)
    assert test_worksheet.getColumns() == ['Name', 'Birthday','Email', 'newColumn3', 'newColumn1']
    

def test_commit():
    #pushes all the changes we have make to the sheet
    test_worksheet.commit()

    print("\n\n\nNeed to add tests to verify that the data was setup correctly in the gspread sheet\n\n\n")

def test_commit_with_larger_data():
    # the worksheet is only 5 columns wide right now, let's see what happens if we add a lot more data
    test_worksheet.addColumn("newColumn4")
    test_worksheet.addColumn("newColumn5")
    test_worksheet.addColumn("newColumn6")
    test_worksheet.commit()