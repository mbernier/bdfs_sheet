import pytest
from modules.spreadsheets.destinations.simple_sheet import Simple_Spreadsheet_Destination
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Destination_Exception

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
    worksheets = sheet.setupWorksheets(use_cache=False)
    worksheets2 = sheet.getWorksheets()
    assert worksheets == worksheets2
    assert 'test_DONTMOVE' in worksheets.keys()


def test_fail_delete_Worksheet():
    worksheetName = "test_destination_dne"

    worksheetList = sheet.getWorksheets()
    assert not worksheetName in worksheetList

    with pytest.raises(Bdfs_Spreadsheet_Destination_Exception) as excinfo:
        sheet.deleteWorksheet(worksheetName)
    assert excinfo.value.message == "Worksheet 'test_destination_dne' is not in the spreadsheet, cannot be deleted"


def test_create_delete_Worksheet():
    worksheetName = "test_destination"
    # just in case a previous test failed, lets do some cleanup
    #   this passed a previous test, so ?ok to use here?
    if worksheetName in sheet.getWorksheets():
       sheet.deleteWorksheet(worksheetName)

    sheet.insertWorksheet(worksheetName,10,10,0)
    # cause the worksheets to be re-fetched
    worksheetList = sheet.getWorksheets()
    assert worksheetName in worksheetList

    sheet.deleteWorksheet(worksheetName)
    # cause the worksheets to be re-fetched
    worksheetList = sheet.getWorksheets()
    assert not worksheetName in worksheetList