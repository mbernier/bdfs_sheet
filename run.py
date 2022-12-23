import sys, logging
from modules.spreadsheets.sources.simple_sheet import Simple_Spreadsheet_Source
from modules.spreadsheets.destinations.simple_sheet import Simple_Spreadsheet_Destination


if __name__ == "__main__":

    # Create a test script with the Simple Sheet:
    # 1. Setup: 
    #     1. Delete any old destination worksheets (calculated and summary)
    #     1. For missing worksheets:
    #         a. Option1: In Spreadsheet class - add list of expected worksheets? add them if missing?
    #         a. Option2: Update method for getWorksheet() to have "Add if not found"
    # 1. Test1
    #     1. Spin up the Source Sheet
    sourceSpreadsheet = Simple_Spreadsheet_Source()
    sourceWorksheet = sourceSpreadsheet.getWorksheet("demo_worksheet")
    
    newWorksheetName = "test_payroll"
    #     1. Spin up the Destination Sheet
    destinationSpreadsheet = Simple_Spreadsheet_Destination()

    # # since this is a test script, delete the old one, so we can have a clean run here
    # try:
    #     destinationSpreadsheet.deleteWorksheet(newWorksheetName)
    # except Bdfs_Spreadsheet_Destination_Exception as err:
    #     pass #ignore, bc we were just cleaning this up just in case

    # # create the new worksheet if it doesn't exist
    # destinationWorksheet = destinationSpreadsheet.insertWorksheet(newWorksheetName)

    # # The columns we have in the source
    # source_actualCols = sourceWorksheet.getColumns()

    # # The columns we have in the destination
    # destination_actualCols = destinationWorksheet.getColumns()

    # # The columns we will write to the destination
    # destination_expectedCols = destinationWorksheet.getExpectedColumns()

    # # Columns that we need to add to the destination
    # missingFromActual = list(set(destination_expectedCols) - set(destination_actualCols))
    
    # # Columns we will remove from the destination
    # extraInDestination = list(set(destination_actualCols) - set(destination_expectedCols))

    # # Make sure the local data has what we need
    # #     1. Create some columns that should be there in the Destination
    # #         1. Hourly pay
    # #         2. Total Pay
    # destinationWorksheet.alignToColumns(destination_expectedCols)

    # # verify that what we expected to happen in the previous step, actually did
    # assert destination_expectedCols == destinationWorksheet.getColumns()

    # #     1. Modify/Add some data in the Destination
    # #         1. Calculate Hourly pay = yearly salary / 2008
    # #         2. Calculate Total Pay = hourly pay * hours worked

    # for row in destinationWorksheet.height():
    #     salary = destinationWorksheet.select(row, "Yearly Salary")
        
    #     hourly = salary / 2008

    #     destinationWorksheet.update(row, "Hourly Pay", hourly)
        
    #     total_hours = destinationWorksheet.select(row, "Hours Worked")
        
    #     total_pay = total_hours * hourly

    #     destinationWorksheet.update(row, "Total Pay", total_pay)

    # #     1. Commit the changes
    # #     1. Test the changes were committed

    # destinationWorksheet.commit()

    # # 1. Test2: Create a summary sheet from data in the calculated sheet
    # #     1. Setup Source Spreadsheet + source Worksheet from test1
    # #     1. Setup destination spreadsheet + summary worksheet
    # #     1. Data to put in Summary
    # #         1. Number of Employees
    # #         2. Total hours worked
    # #         3. Total pay sent
    # #         4. Average Hourly Pay

    # destinationWorksheet.commit()
    
