import unittest
import requirementsfinder
import os
import subprocess

##this next bit taken from stackoverflow.com/questions/4814970/subprocess-check-output-doesnt-seem-to-exist-python-2-6-5
##which is in turn taken from the python2.7 source
if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

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
        output = subprocess.check_output('requirementsfinder', cwd = os.getcwd())
        self.assertEqual(expected_output, output)
    def test_command_line_with_dir(self):
        expected_output = 'Flask==0.10.1\nrequests==2.4.3\n'
        output = subprocess.check_output(['requirementsfinder',self.example_path], cwd = os.getcwd())
        self.assertEqual(expected_output, output)

if __name__ == '__main__':
    unittest.main()