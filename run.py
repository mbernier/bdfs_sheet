import sys
from modules.sheetProcessor import SheetProcessor


from modules.spreadsheets.bdfs_inventory import Bdfs_Spreadsheet
from modules.sheetProcessors.bdfs_inventory import Bdfs_SheetProcessor

if __name__ == "__main__":
    
    # Sheet processor functionality without a specific spreadsheet, this will fail
    # run = SheetProcessor()
    # run.main(sys.argv[1:])

    # Bdfs Sheet Processor functionality
    run = Bdfs_SheetProcessor()
    run.main(sys.argv[1:])

    # For testing the spreadsheet functionality
    # sheet = Bdfs_Spreadsheet()
    # print(sheet.getSpreadsheetId())
