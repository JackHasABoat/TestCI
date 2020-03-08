import unittest
from myapp import add_function


class MyTestCases(unittest.TestCase):
    def test_add_function(self):
        self.assertEqual(add_function(1,2), 3)

    def test_add_function_false_case(self):
        self.assertNotEqual(add_function(4,5),6)

if __name__ == '__main__':
    unittest.main()
    print("Jack: ok my ci works")
