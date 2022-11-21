from __future__ import print_function

import os.path

from modules.sheet.bdfs_sheet import Bdfs_sheet

def main():

    try:
        bdfs_sheet = Bdfs_sheet()
        bdfs_sheet.read_sheet()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()