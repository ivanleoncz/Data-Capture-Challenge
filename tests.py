import unittest

from main import DataCapture


class TestDataCapture(unittest.TestCase):

    def setUp(self):
        self.dc = DataCapture()

    def test_attributes(self):
        """
        > Expected attributes and if they are variables, they must be of certain types.
        """
        self.assertTrue(hasattr(self.dc, "add"), msg="add() method is missing")
        self.assertTrue(hasattr(self.dc, "between"), msg="between() method is missing")
        self.assertTrue(hasattr(self.dc, "build_stats"), msg="build_stats() method is missing")
        self.assertTrue(hasattr(self.dc, "less"), msg="less() method is missing")
        self.assertTrue(hasattr(self.dc, "greater"), msg="greater() method is missing")
        self.assertTrue(hasattr(self.dc, "numbers"), msg="numbers variable is missing")
        self.assertTrue(isinstance(self.dc.numbers, list), msg="numbers must be of type 'list'")
        self.assertTrue(hasattr(self.dc, "stats"), msg="stats variable is missing")
        self.assertTrue(isinstance(self.dc.stats, dict), msg="numbers must be of type 'dict'")

    def test_input_validation(self):
        """
        > Expected exceptions must be raised.
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
        self.assertRaises(TypeError, self.dc.greater, "2")
        self.assertRaises(TypeError, self.dc.between, "1", 5)
        self.assertRaises(ValueError, self.dc.less, 5)
        self.assertRaises(ValueError, self.dc.greater, 2)
        self.assertRaises(ValueError, self.dc.between, 1, 5)
        self.assertRaises(ValueError, self.dc.between, 9, 1)

    def test_less_with_one_number(self):
        """
        > Expected result: empty list of lesser numbers, when there's only "a single input"
        """
        x = 2
        self.dc.add(x)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.less(x=x), second=0,
                         msg=f"there must be no value lesser than {x}, since it's the only value processed")

    def test_less_with_five_numbers(self):
        """
        > Expected result: list of positive numbers lesser than "x"
        """
        x = 7
        for n in (3, 9, 7, 5):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.less(x=x), second=2,
                         msg=f"amount of numbers lesser than {x}, surpasses the expected amount")

    def test_less_with_ten_numbers(self):
        """
        > Expected result: list of positive numbers lesser than "x"
        """
        x = 6
        for n in (2, 1, 1, 3, 9, 5, 2, 6, 4):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.less(x=x), second=7,
                         msg=f"amount of numbers lesser than {x}, surpasses the expected amount")

    def test_greater_with_one_number(self):
        """
        > Expected result: empty list of lesser numbers, when there's only "a single input"
        """
        x = 4
        self.dc.add(x)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.greater(x=x), second=0)

    def test_greater_with_five_numbers(self):
        """
        > Expected result: list of positive numbers greater than "x"
        """
        x = 2
        for n in (2, 1, 8, 5, 8):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.greater(x=x), second=3,
                         msg=f"amount of numbers greater than {x}, surpasses the expected amount")

    def test_greater_with_ten_numbers(self):
        """
        > Expected result: list of positive numbers greater than "x"
        """
        x = 3
        for n in (5, 2, 9, 3, 3, 7, 1, 2, 5, 6):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        self.assertEqual(first=self.stats.greater(x=x), second=5,
                         msg=f"amount of numbers greater than {x}, surpasses the expected amount")

    def test_between_with_seven_numbers(self):
        """
        > Expected result: list of positive numbers between "start" and "end"
        """
        start, end = 4, 9
        for n in (4, 3, 6, 4, 12, 6, 9):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        result, amount_expected = self.stats.between(start=start, end=end), 5
        self.assertEqual(first=result, second=amount_expected,
                         msg=f"result: {result} / amount expected: {amount_expected}")

    def test_between_with_ten_numbers(self):
        """
        > Expected result: list of positive numbers between "start" and "end"
        """
        start, end = 3, 9
        for n in (3, 9, 5, 5, 5, 12, 5, 6, 1, 25):
            self.dc.add(n)
        self.stats = self.dc.build_stats()
        result, amount_expected = self.stats.between(start=start, end=end), 7
        self.assertEqual(first=result, second=amount_expected,
                         msg=f"result: {result} / amount expected: {amount_expected}")


if __name__ == '__main__':
    unittest.main()
