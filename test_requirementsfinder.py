import unittest
import requirementsfinder

EXAMPLE_PATH  = 'example'
class TablibTestCase(unittest.TestCase):
    def setUp(self):
        self.example_path = EXAMPLE_PATH
    def tearDown(self):
        self.example_path = None
    def test_make_freeze(self):
        """test that make freeze gives the expected output"""
        expected = ['Flask==0.10.1','requests==2.7.0']
        self.assertEqual(expected,unittest.make_freeze(self.example_path))