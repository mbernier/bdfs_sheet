from modules.helper import Helper
from modules.worksheets.bases.doors import Doors_Base

class Shopify_Barndoor_Base(Doors_Base): 

    cols_expected = ['Title', 'Type', 'SEO Title', 'Description', 'Item Count', 
                        'Image 1 URL', 'Image 1 SEO', 'Image 2 URL', 'Image 2 SEO', 
                        'Image 3 URL', 'Image 3 SEO', 'Image 4 URL', 'Image 4 SEO', 
                        'Image 5 URL', 'Image 5 SEO', 'Image 6 URL', 'Image 6 SEO', 
                        'Image 7 URL', 'Image 7 SEO', 'Image 8 URL', 'Image 8 SEO', 
                        'Image 9 URL', 'Image 9 SEO', 'Image 10 URL', 'Image 10 SEO',
                        'Vendor Name', 'Vendor Unique ID', 'Vendor SKU', 'Vendor Model Name',
                        'Shipping Cost', 'Shipping Method', 'Discount'
                        'Has Glass', 'Glass Type', 'Glass Lites',
                        'Has Hardware', 'Hardware Type', 'Hardware Color'
                        'Shopify URL', 'Shopify Handle', 'Tags',
                        'Publish To Store', 'Publish To Google',
                        'Publish to Pinterest', 'Publish To Facebook & Instagram', 
                        'Publish to Microsoft', 'Publish to Shop']

    # cols_expected_extra are created in Doors_Base from widths, heights, and hasDoubles vars

    widths = [18, 24, 28, 30, 32, 36, 42]
    heights = [80, 84, 96]
    
    hasDoubles = True

    uniqueField = 'Handle'