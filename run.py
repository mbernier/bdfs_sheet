import sys
from modules.sheetProcessor import SheetProcessor



if __name__ == "__main__":
    run = SheetProcessor()
    run.main(sys.argv[1:])