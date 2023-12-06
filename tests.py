import unittest

from main import DataCapture


class TestDataCapture(unittest.TestCase):

    def setUp(self):
        self.dc = DataCapture()

    def test_attributes(self):
        """
        > Expected results: attributes must be present and if they are variables, they must be of certain types.
        """
        self.assertTrue(hasattr(self.dc, "add"))
        self.assertTrue(hasattr(self.dc, "between"))
        self.assertTrue(hasattr(self.dc, "build_stats"))
        self.assertTrue(hasattr(self.dc, "less"))
        self.assertTrue(hasattr(self.dc, "greater"))
        self.assertTrue(hasattr(self.dc, "numbers"))
        self.assertTrue(isinstance(self.dc.numbers, list))
        self.assertTrue(hasattr(self.dc, "stats"))
        self.assertTrue(isinstance(self.dc.stats, dict))  # 'dict' is the parent class of 'defaultdict'

    def test_input_validation(self):
        """
        > Expected results: all mentioned exceptions must be successfully raised.
        """
        self.assertRaises(TypeError, self.dc.build_stats)
        self.assertRaises(TypeError, self.dc.add, "0")
        self.assertRaises(ValueError, self.dc.add, 0)
        self.assertRaises(ValueError, self.dc.add, 1200)
        self.dc.add(4)
        self.dc.add(6)
        self.dc.add(3)
        self.dc.add(9)
        self.dc.add(1)
        self.assertRaises(TypeError, self.dc.less, "5")
        self.assertRaises(ValueError, self.dc.less, 5)
        self.assertRaises(TypeError, self.dc.greater, "2")
        self.assertRaises(ValueError, self.dc.greater, 2)
        self.assertRaises(TypeError, self.dc.between, "1", 5)
        self.assertRaises(ValueError, self.dc.between, 1, 5)

    def test_less_with_one_number(self):
        """
        > Expected result: empty list of lesser numbers, when there's only "a single input"
        """
        x = 2
        self.dc.add(x)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.less(x=x), second=[])

    def test_less_with_five_numbers(self):
        """
        > Expected result: list of positive numbers lesser than "x"
        """
        x = 7
        for n in (3, 9, 7, 5):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.less(x=x), second=[3, 5])

    def test_less_with_ten_numbers(self):
        """
        > Expected result: list of positive numbers lesser than "x"
        """
        x = 6
        for n in (2, 1, 1, 3, 9, 5, 2, 6, 4):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.less(x=x), second=[1, 1, 2, 2, 3, 4, 5])

    def test_greater_with_one_number(self):
        """
        > Expected result: empty list of lesser numbers, when there's only "a single input"
        """
        x = 4
        self.dc.add(x)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.greater(x=x), second=[])

    def test_greater_with_five_numbers(self):
        """
        > Expected result: list of positive numbers greater than "x"
        """
        x = 2
        for n in (2, 1, 8, 5, 8):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.greater(x=x), second=[5, 8, 8])

    def test_greater_with_ten_numbers(self):
        """
        > Expected result: list of positive numbers greater than "x"
        """
        x = 3
        for n in (5, 2, 9, 3, 3, 7, 1, 2, 5, 6):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.greater(x=x), second=[5, 5, 6, 7, 9])

    def test_between_with_seven_numbers(self):
        """
        > Expected result: list of positive numbers between "start" and "end"
        """
        for n in (4, 3, 6, 4, 12, 6, 9):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.between(start=4, end=9), second=[4, 4, 6, 6, 9])

    def test_between_with_ten_numbers(self):
        """
        > Expected result: list of positive numbers between "start" and "end"
        """
        for n in (3, 9, 5, 5, 5, 12, 5, 6, 1, 25):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.between(start=3, end=9), second=[3, 5, 5, 5, 5, 6, 9])


if __name__ == '__main__':
    unittest.main()
