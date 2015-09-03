import unittest
import requirementsfinder
import os
from subprocess import check_output

EXAMPLE_PATH  = 'example'
class TablibTestCase(unittest.TestCase):
    def setUp(self):
        self.example_path = EXAMPLE_PATH

    def tearDown(self):
        self.example_path = None

    def test_make_freeze(self):
        """test that make freeze gives the expected output"""
        expected = ['Flask==0.10.1','requests==2.7.0']
        self.assertEqual(expected,requirementsfinder.make_freeze(self.example_path))

    def test_command_line_default(self):
        expected_output = 'setuptools==12.2\npip==7.1.2\nrequirementsfinder==0.1\nrequests==2.4.3\n'
        output = check_output('requirementsfinder', cwd = os.getcwd())
        self.assertEqual(expected_output, output)
    def test_command_line_with_dir(self):
        expected_output = 'Flask==0.10.1\nrequests==2.4.3\n'
        output = check_output(['requirementsfinder',self.example_path], cwd = os.getcwd())
        self.assertEqual(expected_output, output)