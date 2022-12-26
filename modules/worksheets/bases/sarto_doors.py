from modules.helper import Helper
from modules.worksheets.bases.doors import Doors_Base

class Sarto_Inventory_Base(Doors_Base):
        
        cols_expected = ['URL', 'URL_key', 'Title', 'Type', 'Glass', 'Lites', 'Color', 'Hardware', 'SKU', 'Model', 
                        'Image 1 URL', 'Image 2 URL', 'Image 3 URL', 'Image 4 URL', 'Image 5 URL', 
                        'Image 6 URL', 'Image 7 URL', 'Image 8 URL', 'Image 9 URL', 'Image 10 URL', 
                        'Description']
        
        # cols_expected_extra are created in Doors_Base from widths, heights, and hasDoubles vars

        widths = [18, 24, 28, 30, 32, 36, 42]
        heights = [80, 84, 96]
        hasDoubles = True

        uniqueKey = 'url_key'