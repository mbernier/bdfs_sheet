import sys
from modules.spreadsheets.sources.bdfs_test import BdfsInventory_Test_Spreadsheet_Source

sheet = BdfsInventory_Test_Spreadsheet_Source()

def test_getWorksheetKeeperPattern():
    assert "test" == sheet.getWorksheetKeeperPattern()

def test_getSpreadsheetId():
    assert "1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8" == sheet.getSpreadsheetId()


def test_getWorksheetClassName():
    assert "BdfsInventory_Test_Worksheet_Source" == sheet.getWorksheetClassName()


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