from modules.helper import Helper

class Doors_Base():
    heights = []
    widths = []
    hasDoubles = False
    map_cols = ['Cost', 'Retail Price']
    cols_expected_extra = {"single":[]}

    def __init__(self):
        widths_inches = Helper.mapCols(self.widths,['"'])
        heights_inches = Helper.mapCols(self.heights,['"'])

        single_sizes = Helper.mapCols(widths_inches, heights_inches, "x")
        single = Helper.mapCols(self.map_cols, single_sizes, ": ")        
        
        self.cols_expected_extra['single'] = single

        if True == self.hasDoubles:
            double_sizes = []
            for width in self.widths:
                for height in heights_inches:
                    # e.g. 36" x 80" (2 @ 18"x80")
                    double_sizes.append(f"{2*int(width)}\"x{height} (2 @ {width}\"x{height})")
            
            double = Helper.mapCols(self.map_cols, double_sizes, ": ")
            self.cols_expected_extra['double'] = double

        


