from modules.worksheets.destination import Bdfs_Worksheet_Destination


class Simple_Worksheet_Destination(Bdfs_Worksheet_Destination):
    # hourly Pay and total Pay will be added in testing
    cols_expected = ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Hourly Pay', 'Total Pay']

    cols_expected_extra = {}