
import common
import unittest

from lib.model.smartplugin import SmartPlugin

from tests.mock.core import MockSmartHome

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.sh = MockSmartHome()
        self.modules = self.sh.with_modules_from(common.BASE + "/tests/resources/module")

    def test_module_is_registered(self):
        self.assertIsNotNone(self.sh.get_module("http"))

    def test_plugin_not_registered(self):
        self.assertIsNone(self.sh.get_module("httpX"))

    def test_modules_loaded(self):
        self.assertEqual(self.sh.return_modules(),['http'])

 

if __name__ == '__main__':
    unittest.main(verbosity=2)

