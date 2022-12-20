import sys
from modules.spreadsheets.destinations.simple_sheet import Simple_Spreadsheet_Destination

sheet = Simple_Spreadsheet_Destination()


def test_getWorksheetKeeperPattern():
    assert "test" == sheet.getWorksheetKeeperPattern()

def test_getSpreadsheetId():
    assert "1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI" == sheet.getSpreadsheetId()


def test_getWorksheetClassName():
    assert "Simple_Worksheet_Destination" == sheet.getWorksheetClassName()


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
