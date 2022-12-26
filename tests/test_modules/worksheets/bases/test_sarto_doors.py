from modules.worksheets.bases.sarto_doors import Sarto_Inventory_Base

def test_default():
    base = Sarto_Inventory_Base()

    assert base.cols_expected == ['URL', 'URL_key', 'Title', 'Type', 'Glass', 'Lites', 'Color', 'Hardware', 'SKU', 'Model', 'Image 1 URL', 'Image 2 URL', 'Image 3 URL', 'Image 4 URL', 'Image 5 URL', 'Image 6 URL', 'Image 7 URL', 'Image 8 URL', 'Image 9 URL', 'Image 10 URL', 'Description']
    assert base.cols_expected_extra == {'single': ['Cost: 18"x80"', 'Cost: 18"x84"', 'Cost: 18"x96"', 'Cost: 24"x80"', 'Cost: 24"x84"', 'Cost: 24"x96"', 'Cost: 28"x80"', 'Cost: 28"x84"', 'Cost: 28"x96"', 'Cost: 30"x80"', 'Cost: 30"x84"', 'Cost: 30"x96"', 'Cost: 32"x80"', 'Cost: 32"x84"', 'Cost: 32"x96"', 'Cost: 36"x80"', 'Cost: 36"x84"', 'Cost: 36"x96"', 'Cost: 42"x80"', 'Cost: 42"x84"', 'Cost: 42"x96"', 'Retail Price: 18"x80"', 'Retail Price: 18"x84"', 'Retail Price: 18"x96"', 'Retail Price: 24"x80"', 'Retail Price: 24"x84"', 'Retail Price: 24"x96"', 'Retail Price: 28"x80"', 'Retail Price: 28"x84"', 'Retail Price: 28"x96"', 'Retail Price: 30"x80"', 'Retail Price: 30"x84"', 'Retail Price: 30"x96"', 'Retail Price: 32"x80"', 'Retail Price: 32"x84"', 'Retail Price: 32"x96"', 'Retail Price: 36"x80"', 'Retail Price: 36"x84"', 'Retail Price: 36"x96"', 'Retail Price: 42"x80"', 'Retail Price: 42"x84"', 'Retail Price: 42"x96"'], 'double': ['Cost: 36"x80" (2 @ 18"x80")', 'Cost: 36"x84" (2 @ 18"x84")', 'Cost: 36"x96" (2 @ 18"x96")', 'Cost: 48"x80" (2 @ 24"x80")', 'Cost: 48"x84" (2 @ 24"x84")', 'Cost: 48"x96" (2 @ 24"x96")', 'Cost: 56"x80" (2 @ 28"x80")', 'Cost: 56"x84" (2 @ 28"x84")', 'Cost: 56"x96" (2 @ 28"x96")', 'Cost: 60"x80" (2 @ 30"x80")', 'Cost: 60"x84" (2 @ 30"x84")', 'Cost: 60"x96" (2 @ 30"x96")', 'Cost: 64"x80" (2 @ 32"x80")', 'Cost: 64"x84" (2 @ 32"x84")', 'Cost: 64"x96" (2 @ 32"x96")', 'Cost: 72"x80" (2 @ 36"x80")', 'Cost: 72"x84" (2 @ 36"x84")', 'Cost: 72"x96" (2 @ 36"x96")', 'Cost: 84"x80" (2 @ 42"x80")', 'Cost: 84"x84" (2 @ 42"x84")', 'Cost: 84"x96" (2 @ 42"x96")', 'Retail Price: 36"x80" (2 @ 18"x80")', 'Retail Price: 36"x84" (2 @ 18"x84")', 'Retail Price: 36"x96" (2 @ 18"x96")', 'Retail Price: 48"x80" (2 @ 24"x80")', 'Retail Price: 48"x84" (2 @ 24"x84")', 'Retail Price: 48"x96" (2 @ 24"x96")', 'Retail Price: 56"x80" (2 @ 28"x80")', 'Retail Price: 56"x84" (2 @ 28"x84")', 'Retail Price: 56"x96" (2 @ 28"x96")', 'Retail Price: 60"x80" (2 @ 30"x80")', 'Retail Price: 60"x84" (2 @ 30"x84")', 'Retail Price: 60"x96" (2 @ 30"x96")', 'Retail Price: 64"x80" (2 @ 32"x80")', 'Retail Price: 64"x84" (2 @ 32"x84")', 'Retail Price: 64"x96" (2 @ 32"x96")', 'Retail Price: 72"x80" (2 @ 36"x80")', 'Retail Price: 72"x84" (2 @ 36"x84")', 'Retail Price: 72"x96" (2 @ 36"x96")', 'Retail Price: 84"x80" (2 @ 42"x80")', 'Retail Price: 84"x84" (2 @ 42"x84")', 'Retail Price: 84"x96" (2 @ 42"x96")']}