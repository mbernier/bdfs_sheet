from modules.worksheets.bases.doors import Doors_Base

class simpleDoors_single(Doors_Base):
        cols_expected = ['URL', 'Title', 'Description']
        widths = [18, 24]
        heights = [80, 84]
        hasDoubles = False


class simpleDoors_double(Doors_Base):
        cols_expected = ['URL', 'Title', 'Description']
        widths = [18, 24]
        heights = [80, 84]
        hasDoubles = True


def test_single():
    base = simpleDoors_single()
    assert base.cols_expected == ['URL', 'Title', 'Description']
    assert base.cols_expected_extra['single'] == ['Cost: 18"x80"', 'Cost: 18"x84"', 'Cost: 24"x80"', 'Cost: 24"x84"', 'Retail Price: 18"x80"', 'Retail Price: 18"x84"', 'Retail Price: 24"x80"', 'Retail Price: 24"x84"']


def test_double():
    base = simpleDoors_double()
    assert base.cols_expected == ['URL', 'Title', 'Description']
    assert base.cols_expected_extra['double'] == ['Cost: 36"x80" (2 @ 18"x80")', 'Cost: 36"x84" (2 @ 18"x84")', 'Cost: 48"x80" (2 @ 24"x80")', 'Cost: 48"x84" (2 @ 24"x84")', 'Retail Price: 36"x80" (2 @ 18"x80")', 'Retail Price: 36"x84" (2 @ 18"x84")', 'Retail Price: 48"x80" (2 @ 24"x80")', 'Retail Price: 48"x84" (2 @ 24"x84")']