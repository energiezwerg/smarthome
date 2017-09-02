
import common
import unittest

from lib.model.smartplugin import SmartPlugin

from tests.mock.core import MockSmartHome

class TestModule(unittest.TestCase):

#    def setUp(self):
#        self.sh = MockSmartHome()
#        self.modules = self.sh.with_modules_from(common.BASE + "/tests/resources/module")

    def test_module_is_registered(self):
        print()
        print('=== module Tests:')
        self.sh = MockSmartHome()
        self.modules = self.sh.with_modules_from(common.BASE + "/tests/resources/module")
        self.assertIsNotNone(self.sh.get_module("dummy"))    # Test module is not registered
        self.assertIsNone(self.sh.get_module("dummyX"))      # Test plugin ist not registered
        self.assertEqual(self.sh.return_modules(),['dummy']) # Test modules loaded

#    def test_plugin_not_registered(self):
#        self.assertIsNone(self.sh.get_module("dummyX"))

#    def test_modules_loaded(self):
#        self.assertEqual(self.sh.return_modules(),['dummy'])

 

if __name__ == '__main__':
    unittest.main(verbosity=2)

