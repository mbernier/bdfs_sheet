
from modules.worksheets.source import Bdfs_Worksheet_Source


class OriginalBdfs_Inventory_Worksheet_Source(Bdfs_Worksheet_Source):
    
    cols_expected = ['Updated Date', 'Title', 'Hardware', 'Published', 'Type', 'On BDFS?', 'Vendor', 
                        'Handle', 'Type', 'Glass', 'SKU', 'SEO Title', 'Tags', 'Sarto SKU', 
                        'Color', 'UnitedPorte URL', 'Image 1 URL', 'Image 1 SEO', 'Image 2 URL', 
                        'Image 2 SEO', 'Image 3 URL', 'Image 3 SEO', 'Image 4 URL', 'Image 4 SEO',
                        'Image 5 URL', 'Image 5 SEO', 'Description']
    
    single_door_cols = ['Cost:18" x 80"', 'Cost:24" x 80"', 'Cost:28" x 80"', 'Cost:30" x 80"', 
                        'Cost:32" x 80"', 'Cost:36" x 80"', 'Cost:42" x 80"', 'Cost:18" x 84"', 'Cost:24" x 84"', 
                        'Cost:28" x 84"', 'Cost:30" x 84"', 'Cost:32" x 84"', 'Cost:36" x 84"', 'Cost:42" x 84"', 
                        'Cost:18" x 96"', 'Cost:24" x 96"', 'Cost:28" x 96"', 'Cost:30" x 96"', 'Cost:32" x 96"', 
                        'Cost:36" x 96"', 'Cost:42" x 96"', 'Price:18" x 80"', 'Price:24" x 80"', 
                        'Price:28" x 80"', 'Price:30" x 80"', 'Price:32" x 80"', 'Price:36" x 80"', 
                        'Price:42" x 80"', 'Price:18" x 84"', 'Price:24" x 84"', 'Price:28" x 84"', 
                        'Price:30" x 84"', 'Price:32" x 84"', 'Price:36" x 84"', 'Price:42" x 84"', 
                        'Price:18" x 96"', 'Price:24" x 96"', 'Price:28" x 96"', 'Price:30" x 96"', 
                        'Price:32" x 96"', 'Price:36" x 96"', 'Price:42" x 96"', 'Profits:18" x 80"',  
                        'Profits:24" x 80"', 'Profits:28" x 80"', 'Profits:30" x 80"', 'Profits:32" x 80"', 
                        'Profits:36" x 80"', 'Profits:42" x 80"', 'Profits:18" x 84"', 'Profits:24" x 84"', 
                        'Profits:28" x 84"', 'Profits:30" x 84"', 'Profits:32" x 84"', 'Profits:36" x 84"', 
                        'Profits:42" x 84"', 'Profits:18" x 96"', 'Profits:24" x 96"', 'Profits:28" x 96"', 
                        'Profits:30" x 96"', 'Profits:32" x 96"', 'Profits:36" x 96"', 'Profits:42" x 96"']

    double_door_cols = ['Cost:36" x 80" (2 @ 18"x80")', 'Cost:48" x 80" (2 @ 24"x80")', 
                        'Cost:36" x 84" (2 @ 18"x84")', 'Cost:48" x 84" (2 @ 24"x84")', 
                        'Cost:56" x 84" (2 @ 28"x84")', 'Cost:60" x 84" (2 @ 30"x84")', 
                        'Cost:56" x 80" (2 @ 28"x80")', 'Cost:60" x 80" (2 @ 30"x80")', 
                        'Cost:64" x 80" (2 @ 32"x80")', 'Cost:72" x 80" (2 @ 36"x80")', 
                        'Cost:84" x 80" (2 @ 42"x80")', 'Cost:64" x 84" (2 @ 32"x84")', 
                        'Cost:72" x 84" (2 @ 36"x84")', 'Cost:84" x 84" (2 @ 42"x84")', 
                        'Cost:36" x 96" (2 @ 18"x96")', 'Cost:48" x 96" (2 @ 24"x96")', 
                        'Cost:56" x 96" (2 @ 28"x96")', 'Cost:60" x 96" (2 @ 30"x96")', 
                        'Cost:64" x 96" (2 @ 32"x96")', 'Cost:72" x 96" (2 @ 36"x96")', 
                        'Cost:84" x 96" (2 @ 42"x96")', 'Price:36" x 80" (2 @ 18"x80")', 
                        'Price:48" x 80" (2 @ 24"x80")', 'Price:56" x 80" (2 @ 28"x80")', 
                        'Price:60" x 80" (2 @ 30"x80")', 'Price:64" x 80" (2 @ 32"x80")', 
                        'Price:72" x 80" (2 @ 36"x80")', 'Price:84" x 80" (2 @ 42"x80")', 
                        'Price:36" x 84" (2 @ 18"x84")', 'Price:48" x 84" (2 @ 24"x84")', 
                        'Price:56" x 84" (2 @ 28"x84")', 'Price:60" x 84" (2 @ 30"x84")', 
                        'Price:64" x 84" (2 @ 32"x84")', 'Price:72" x 84" (2 @ 36"x84")', 
                        'Price:84" x 84" (2 @ 42"x84")', 'Price:36" x 96" (2 @ 18"x96")', 
                        'Price:48" x 96" (2 @ 24"x96")', 'Price:56" x 96" (2 @ 28"x96")', 
                        'Price:60" x 96" (2 @ 30"x96")', 'Price:64" x 96" (2 @ 32"x96")', 
                        'Price:72" x 96" (2 @ 36"x96")', 'Price:84" x 96" (2 @ 42"x96")', 
                        'Profits:36" x 80" (2 @ 18"x80")', 'Profits:48" x 80" (2 @ 24"x80")', 
                        'Profits:56" x 80" (2 @ 28"x80")', 'Profits:60" x 80" (2 @ 30"x80")', 
                        'Profits:64" x 80" (2 @ 32"x80")', 'Profits:72" x 80" (2 @ 36"x80")', 
                        'Profits:84" x 80" (2 @ 42"x80")', 'Profits:36" x 84" (2 @ 18"x84")', 
                        'Profits:48" x 84" (2 @ 24"x84")', 'Profits:56" x 84" (2 @ 28"x84")', 
                        'Profits:60" x 84" (2 @ 30"x84")', 'Profits:64" x 84" (2 @ 32"x84")', 
                        'Profits:72" x 84" (2 @ 36"x84")', 'Profits:84" x 84" (2 @ 42"x84")', 
                        'Profits:36" x 96" (2 @ 18"x96")', 'Profits:48" x 96" (2 @ 24"x96")', 
                        'Profits:56" x 96" (2 @ 28"x96")', 'Profits:60" x 96" (2 @ 30"x96")', 
                        'Profits:64" x 96" (2 @ 32"x96")', 'Profits:72" x 96" (2 @ 36"x96")', 
                        'Profits:84" x 96" (2 @ 42"x96")']

    cols_expected_extra = {'single': single_door_cols,
                            'double': double_door_cols}