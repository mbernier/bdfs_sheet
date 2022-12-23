from modules.decorator import Debugger
from modules.worksheets.exception import Bdfs_Worksheet_Source_Exception
from modules.worksheet import Bdfs_Worksheet

#
# Rules; 
#   This ONLY reads data, it cannot write - any writing methods from Bdfs_Worksheet will raise an exception
#
class Bdfs_Worksheet_Source(Bdfs_Worksheet):

    # allows the class to barf if used incorrectly
    @Debugger
    def modifiesData(self):
        raise Bdfs_Worksheet_Source_Exception("Source Worksheets are not allowed to modify data")