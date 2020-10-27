import tableprop
import unittest
from lark import Tree

class notStatement(unittest.TestCase):
    def setUp(self):
        self.generator = tableprop.PropTextGenerator()
    def test_parse_no_error_not_call(self):
        # test if no error is thrown
        self.generator.parse("not p")
    def test_parse_not_call_get_variable_list(self):
        self.generator.parse("not p")
        self.assertTrue(len(self.generator.get_variables()) == 1)

if __name__ == '__main__':
    unittest.main()