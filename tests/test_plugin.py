
import common
import unittest
import lib.plugin

class TestConfig(unittest.TestCase):

    def test_plugins(self):
        plugins = lib.plugin.Plugins(MockSmartHome(), "resources/plugin.conf")
        self.assertIsNone(plugins.get_plugin("wol1") )
        print(plugins) 
        print(plugins._plugins) 
        self.assertIsNotNone(plugins._plugins )

        wolplug= plugins.get_plugin("wol") 

        self.assertIsNotNone(wolplug )
        print(wolplug.get_name() )
        self.assertEqual(wolplug.name,"wol" )
        print(wolplug.ident )
        print(wolplug.get_ident() )
        self.assertIsNone(wolplug.ident )
        plugins.start()
        
        print(wolplug.get_ident() )
        self.assertEqual(wolplug.ident,wolplug.get_ident())
        print(wolplug.get_implementation() )
        self.assertEqual(wolplug.plugin, wolplug.get_implementation())

        self.assertIsNotNone(wolplug.get_ident() )

        plugins.stop()
#        print(plugins.get_plugin("wol").get_ident() )

class MockSmartHome():
    __logs = {}
    def add_log(self, name, log):
        self.__logs[name] = log

   
if __name__ == '__main__':
    unittest.main(verbosity=2)

