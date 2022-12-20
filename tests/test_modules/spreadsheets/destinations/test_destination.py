import sys
from modules.spreadsheets.destinations.bdfs_test import BdfsInventory_Test_Spreadsheet_Destination

sheet = BdfsInventory_Test_Spreadsheet_Destination()


def test_getWorksheetKeeperPattern():
    assert "test" == sheet.getWorksheetKeeperPattern()

def test_getSpreadsheetId():
    assert "1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8" == sheet.getSpreadsheetId()


def test_getWorksheetClassName():
    assert "BdfsInventory_Test_Worksheet_Destination" == sheet.getWorksheetClassName()


def test_setupServiceAccount():
    assert "Client" == sheet.setupServiceAccount().__class__.__name__


def test_setupSpreadsheet():
    assert "Spreadsheet" == sheet.setupSpreadsheet().__class__.__name__

#proves the workflow from setupWorksheets, setWorksheet and getWorksheets
def test_setupWorksheets():
    # can't compare, bc ID will change here
    # {'test_DONTMOVE': {'Worksheet': <Worksheet 'test_DONTMOVE' id:796438040>}}
    worksheets = sheet.setupWorksheets()
    worksheets2 = sheet.getWorksheets()
    assert worksheets == worksheets2
    assert 'test_DONTMOVE' in worksheets.keys()






# def test_getWorksheets():
#     assert ["test_DONTMOVE"] == sheet.getWorksheets()

# def test_getWorksheet():

#     worksheetClassName = sheet.getWorksheetClassName()
#     assert "BdfsInventory_Test_Worksheet" == worksheetClassName

#     worksheetclass = sheet.getWorksheetClass()
#     assert worksheetclass.__name__ == "BdfsInventory_Test_Worksheet"

#     worksheet = sheet.getWorksheet("test_DONTMOVE")
#     assert worksheet.__class__.__name__ == "BdfsInventory_Test_Worksheet"




