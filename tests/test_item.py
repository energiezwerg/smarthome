
import common
import unittest
import lib.plugin
import lib.item
from lib.model.smartplugin import SmartPlugin
import threading

from lib.constants import (CONF_FILE, YAML_FILE)


ITEM_FILE_TYPE = CONF_FILE
#ITEM_FILE_TYPE = YAML_FILE


class TestItem(unittest.TestCase):
    def props(self,cls):   
        return [i for i in cls.__dict__.keys() if i[:1] != '_']

        
    # ===================================================================
    # Following tests are about relative item addressing
    #
    def test_item_relative_references(self):
        """
        Tests various aspects around the handling of relative item references
        """
        sh=MockSmartHome()
        
        #load items
        conf_filename = common.BASE + "/tests/resources/item_items"+ITEM_FILE_TYPE
        item_conf = None
        item_conf = lib.config.parse(conf_filename, item_conf)
        if item_conf == {}:
            print()
            print("config file '"+conf_filename+"' not found")
#        print(item_conf.items())
        for attr, value in item_conf.items():
            if isinstance(value, dict):
                child_path = attr
                try:
                    child = lib.item.Item(sh, sh, child_path, value)
                except Exception as e:
                    self.logger.error("Item {}: problem creating: ()".format(child_path, e))
                else:
                    #vars(sh)[attr] = child
                    sh.add_item(child_path, child)
                    sh.children.append(child)
       
        if 0: self.dump_items(sh)

        # -----------------------------------------------------------------
        
        print()
        it = sh.return_item("item_tree.grandparent.parent.my_item")
        self.assertIsNotNone(it)
        self.assertEqual(it._type, 'bool')
        it = sh.return_item("item_tree.grandparent.parent.my_item.child")
        self.assertIsNotNone(it)
        self.assertEqual(it._type, 'foo')

        print('=== eval_trigger Tests:')
        # Attribute with relative references
        it = sh.return_item("item_tree.grandparent.parent.my_item")
        self.assertEqual(it.get_absolutepath('.', 'eval_trigger'), 'item_tree.grandparent.parent.my_item')
        self.assertEqual(it.get_absolutepath('.self', 'eval_trigger'), 'item_tree.grandparent.parent.my_item')
        self.assertEqual(it.get_absolutepath('.child', 'eval_trigger'), 'item_tree.grandparent.parent.my_item.child')
        self.assertEqual(it.get_absolutepath('.self.child', 'eval_trigger'), 'item_tree.grandparent.parent.my_item.child')
        self.assertEqual(it.get_absolutepath('.child.grandchild', 'eval_trigger'), 'item_tree.grandparent.parent.my_item.child.grandchild')
        self.assertEqual(it.get_absolutepath('..', 'eval_trigger'), 'item_tree.grandparent.parent')
        self.assertEqual(it.get_absolutepath('...', 'eval_trigger'), 'item_tree.grandparent')
        self.assertEqual(it.get_absolutepath('....', 'eval_trigger'), 'item_tree')
        self.assertEqual(it.get_absolutepath('.....', 'eval_trigger'), '')
        self.assertEqual(it.get_absolutepath('......', 'eval_trigger'), '')
        self.assertEqual(it.get_absolutepath('..sister', 'eval_trigger'), 'item_tree.grandparent.parent.sister')

        # Attribute w/o relative references
        self.assertEqual(it.get_absolutepath('item_tree.grandparent.parent.my_item', 'eval_trigger'), 'item_tree.grandparent.parent.my_item')
        self.assertEqual(it.get_absolutepath('abc', 'eval_trigger'), 'abc')

        print('=== eval Tests:')
        it = sh.return_item("item_tree.grandparent.parent.my_item")
        #print(it.get_stringwithabsolutepathes('sh..child()', 'sh.', '(', 'eval'))
        self.assertEqual(it.get_stringwithabsolutepathes('sh..child()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.parent.my_item.child()')
        self.assertEqual(it.get_stringwithabsolutepathes('5*sh..child()', 'sh.', '(', 'eval'), '5*sh.item_tree.grandparent.parent.my_item.child()')
        self.assertEqual(it.get_stringwithabsolutepathes('5 * sh..child() + 4', 'sh.', '(', 'eval'), '5 * sh.item_tree.grandparent.parent.my_item.child() + 4')

        # tests for '.self' implementation
        self.assertEqual(it.get_stringwithabsolutepathes('sh..child.changed_by()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.parent.my_item.child.changed_by()')
        self.assertNotEqual(it.get_stringwithabsolutepathes('sh...changed_by()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.parent.my_item.changed_by()')
        self.assertEqual(it.get_stringwithabsolutepathes('sh.item_tree.grandparent.parent.my_item.changed_by()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.parent.my_item.changed_by()')
        self.assertEqual(it.get_stringwithabsolutepathes('sh..self.changed_by()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.parent.my_item.changed_by()')
        self.assertEqual(it.get_stringwithabsolutepathes('sh...changed_by()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.parent.changed_by()')
        self.assertEqual(it.get_stringwithabsolutepathes('sh...self.changed_by()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.parent.changed_by()')
        self.assertNotEqual(it.get_stringwithabsolutepathes('sh.....changed_by()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.changed_by()')
        self.assertEqual(it.get_stringwithabsolutepathes('sh....self.changed_by()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.changed_by()')

        print('=== plugin-attribute Tests:')
        # Attribute with relative references
        it = sh.return_item("item_tree.grandparent.parent.my_item")
        it.expand_relativepathes('sv_widget', "'", "'")
        self.assertEqual(it.conf['sv_widget'], "{{ basic.switch('id_schreibtischleuchte', 'item_tree.grandparent.parent.my_item.onoff') }}")

        # Attribute w/o relative references
        it = sh.return_item("item_tree.grandparent.parent.my_item.child")
        orig = it.conf['sv_widget']
        it.expand_relativepathes('sv_widget', "'", "'")
        self.assertEqual(it.conf['sv_widget'], orig)
        self.assertEqual(it.conf['sv_widget'], "{{ basic.switch('id_schreibtischleuchte', 'item_tree.grandparent.parent.my_item.child.onoff') }}")

        # Tests for accessing internal attributes of items using relative adressing
        it = sh.return_item("item_tree.grandparent.parent.my_item")
        self.assertEqual(it.get_absolutepath('.child', 'eval_trigger'), 'item_tree.grandparent.parent.my_item.child')



    # ===================================================================
    # Following tests are about the autotimer attribut and value casting
    #
    def test_item_autotimers(self):
        """
        Tests about the autotimer attribut and value casting
        """
        sh=None
        sh=MockSmartHome()
        print()
        
        #load items
        conf_filename = common.BASE + "/tests/resources/item_timers"+ITEM_FILE_TYPE
        item_conf = None
        item_conf = lib.config.parse(conf_filename, item_conf)
        if item_conf == {}:
            print()
            print("config file '"+conf_filename+"' not found")
        print(item_conf)
        for attr, value in item_conf.items():
            if isinstance(value, dict):
                child_path = attr
                try:
                    child = lib.item.Item(sh, sh, child_path, value)
                except Exception as e:
                    self.logger.error("Item {}: problem creating: ()".format(child_path, e))
                else:
                    #vars(sh)[attr] = child
                    sh.add_item(child_path, child)
                    sh.children.append(child)
       
        if 0: self.dump_items(sh)

        # -----------------------------------------------------------------

        #print('== autotimer Tests:')
        
        # Compatibility mode: No value casting for SmartHome v1.2 and older
        it = sh.return_item("item_tree.timertests.test_item01")		# autotimer = 5m = 42 = compat_1.2
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (300, '42'))
        
        it = sh.return_item("item_tree.timertests.test_item02")		# autotimer = 5s = = compat_1.2
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, ''))
        
        it = sh.return_item("item_tree.timertests.test_item03")		# autotimer = 5s = None = compat_1.2
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, 'None'))


        # Compatibility mode: No value casting for SmartHome v1.2 and older -> item-type ist str
        it = sh.return_item("item_tree.timertests.test_item11")		# autotimer = 5m = 42 = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (300, '42'))
        self.assertEqual(it._castvalue_to_itemtype(it._autotimer[0][1], it._autotimer[1]), '42')

        it = sh.return_item("item_tree.timertests.test_item12")		# autotimer = 5s = = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, ''))

        it = sh.return_item("item_tree.timertests.test_item13")		# autotimer = 5s = None = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, 'None'))


        # Compatibility mode: No value casting for SmartHome v1.2 and older -> item-type ist num
        it = sh.return_item("item_tree.timertests.test_item21")		# autotimer = 5m = 42 = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (300, 42))

        it = sh.return_item("item_tree.timertests.test_item22")		# autotimer = 5s = = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, 0))

        it = sh.return_item("item_tree.timertests.test_item23")		# autotimer = 5s = None = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, 0))


        # Compatibility mode: No value casting for SmartHome v1.2 and older -> item-type ist bool
        it = sh.return_item("item_tree.timertests.test_item31")		# autotimer = 5m = 42 = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (300, False))

        it = sh.return_item("item_tree.timertests.test_item32")		# autotimer = 5s = = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, False))

        it = sh.return_item("item_tree.timertests.test_item33")		# autotimer = 5s = None = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, False))

        it = sh.return_item("item_tree.timertests.test_item33")		# autotimer = 5s = 1 = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, False))

        it = sh.return_item("item_tree.timertests.test_item34")		# autotimer = 5s = True = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, True))

        it = sh.return_item("item_tree.timertests.test_item35")		# autotimer = 5s = true = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[0], (5, True))

        # test use of items in attributes
        it = sh.return_item("item_tree.timertests.test_item41")		# sh.item_tree.timertests.test_item41.dauer() = 42 = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[2], 'item_tree.timertests.test_item41.dauer')

        it = sh.return_item("item_tree.timertests.test_item42")		# 5m = sh.item_tree.timertests.test_item42.wert() = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[3], 'item_tree.timertests.test_item42.wert')

        it = sh.return_item("item_tree.timertests.test_item51")		# sh..dauer() = 42 = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[2], 'item_tree.timertests.test_item51.dauer')
        
        it = sh.return_item("item_tree.timertests.test_item52")		# 5m = sh..wert() = latest
        self.assertIsNotNone(it)
        self.assertEqual(it._autotimer[3], 'item_tree.timertests.test_item52.wert')

    def test_cast_str(self):
        with self.assertRaises(ValueError):
            self.assertTrue(lib.item._cast_str(1))
        with self.assertRaises(ValueError):
            self.assertTrue(lib.item._cast_str(["ee","ww"]))

        str = 'qwe'
        self.assertEqual(str, lib.item._cast_str(str))

    def test_cast_list(self):
        with self.assertRaises(ValueError):
            self.assertTrue(lib.item._cast_list(1))
        self.assertIsNotNone(lib.item._cast_list([1,2]))
        with self.assertRaises(ValueError):
            self.assertIsNotNone(lib.item._cast_list({1, 2}))

    def test_cast_dict(self):
        with self.assertRaises(ValueError):
            self.assertTrue(lib.item._cast_dict(1))
        self.assertIsNotNone(lib.item._cast_dict({1:1, 2:2}))
        self.assertIsNotNone(lib.item._cast_dict({'1':1 , '2': 2}))

        with self.assertRaises(ValueError):
            self.assertIsNotNone(lib.item._cast_dict({1, 2}))

    def test_cast_scene(self):
        self.assertEqual(1, lib.item._cast_scene('1'))
        self.assertNotEqual(1, lib.item._cast_scene('2'))
        self.assertEqual(255, lib.item._cast_scene(0xff))

        with self.assertRaises(ValueError):
            self.assertEqual(255, lib.item._cast_scene(""))

        with self.assertRaises(ValueError):
            self.assertEqual(1, lib.item._cast_scene('l'))

    def test_cast_num(self):
        self.assertEqual(0, lib.item._cast_num(''))
        self.assertEqual(0, lib.item._cast_num(' '))
        self.assertEqual(1, lib.item._cast_num(' 1 '))
        self.assertEqual(1, lib.item._cast_num('1'))
        self.assertEqual(1.2, lib.item._cast_num('1.2'))
        self.assertEqual(1.2, lib.item._cast_num(1.2))
        self.assertEqual(1, lib.item._cast_num(int(1.2)))
        self.assertEqual(1.2, lib.item._cast_num(float(1.2)))
        with self.assertRaises(ValueError):
            self.assertEqual(10, lib.item._cast_num(' 0x0a'))

    def test_cast_bool(self):
        """
        ['0', 'false', 'no', 'off', '']:
            return False
        elif value.lower() in ['1', 'true', 'yes', 'on']:
        :return:
        """
        # true string values
        self.assertTrue(lib.item._cast_bool('yes'))
        self.assertTrue(lib.item._cast_bool('true'))
        self.assertTrue(lib.item._cast_bool('1'))
        self.assertTrue(lib.item._cast_bool('on'))
        # true numeric values
        self.assertTrue(lib.item._cast_bool(1))
        self.assertTrue(lib.item._cast_bool(int(1)))
        self.assertTrue(lib.item._cast_bool(float(1)))
        self.assertTrue(lib.item._cast_bool(bool(1)))

        # exceptions
        with self.assertRaises(ValueError):
            self.assertTrue(lib.item._cast_bool(float(99)))
        with self.assertRaises(ValueError):
            self.assertTrue(lib.item._cast_bool(2))
        with self.assertRaises(ValueError):
            self.assertTrue(lib.item._cast_bool(-2))

        with self.assertRaises(TypeError):
            self.assertTrue(lib.item._cast_bool([]))

        with self.assertRaises(TypeError):
            self.assertTrue(lib.item._cast_bool(None))

        #false numeric values
        self.assertFalse(lib.item._cast_bool(0))
        self.assertFalse(lib.item._cast_bool(int(0)))
        self.assertFalse(lib.item._cast_bool(float(0)))
        self.assertFalse(lib.item._cast_bool(bool(0)))
        # false string values
        self.assertFalse(lib.item._cast_bool(""))
        self.assertFalse(lib.item._cast_bool('no'))
        self.assertFalse(lib.item._cast_bool('off'))
        self.assertFalse(lib.item._cast_bool('false'))
        self.assertFalse(lib.item._cast_bool('0'))

    def test_fadejob(self):
        #(item, dest, step, delta):
        sh = MockSmartHome()
        conf = {'test_item01': {'type': 'num', 'autotimer': '5m = 42 = compat_1.2'}}
        item = lib.item.Item(config=conf, parent=sh, smarthome=sh, path='test_item01' )
        item(10)
        item._fading = True
        lib.item._fadejob(item, 0, 5, 1)
        self.assertEqual(10, item._value)
        item._fading = False
        lib.item._fadejob(item,0, 5, 0.1)
        self.assertEqual(0,item._value)

        lib.item._fadejob(item, 10, 5, 0.1)
        self.assertEqual(10, item._value)

        lib.item._fadejob(item, 100, 200, 1)
        self.assertEqual(100, item._value)

    def test_set(self):
        sh = MockSmartHome()
        conf = {'test_item01': {'type': 'num', 'autotimer': '5m = 42 = compat_1.2'}}
        item = lib.item.Item(config=conf, parent=sh, smarthome=sh, path='test_item01')
        item.set(12)

        print(item.cast)
        self.assertEqual(12, item._value)

        item.set(13)
        self.assertEqual(13, item._value)


    def test_split_duration_value_string(self):
        lib.item._split_duration_value_string("")

    def test_join_duration_value_string(self):
        #print(lib.item._join_duration_value_string(12,123))
        #(time, value, compat=''):
        pass
    def testCacheWriteReadJson(self):
        import datetime
        from lib.constants import CACHE_JSON

        self.cache_write_load_value(v = True, f=CACHE_JSON)
        self.cache_write_load_value(v=None, f=CACHE_JSON)
        self.cache_write_load_value(v=1, f=CACHE_JSON)
        self.cache_write_load_value(v=123123123, f=CACHE_JSON)
        self.cache_write_load_value(v="foo", f=CACHE_JSON)
        self.cache_write_load_value(v={'active': True, 'list': [{'active': True, 'rrule': 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU', 'time': 'sunset+30m', 'value': 1}, {'active': True, 'rrule': 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU', 'time': 'sunrise-30m', 'value': 0}]}, f=CACHE_JSON)
        self.cache_write_load_value(v={'active': True}, f=CACHE_JSON)
        self.cache_write_load_value(v=[1,2,3,4,5], f=CACHE_JSON)
        self.cache_write_load_value(v=["a","2","3"], f=CACHE_JSON)
        self.cache_write_load_value(v=["a","2","3",2,3,4,5], f=CACHE_JSON)
        # @TODO: not working : self.cache_write_load_value(v=datetime.datetime.now(), f=CACHE_JSON)
    def testCacheWriteReadPickle(self):
        import datetime
        from lib.constants import CACHE_PICKLE

        self.cache_write_load_value(v = True, f=CACHE_PICKLE)
        self.cache_write_load_value(v=None, f=CACHE_PICKLE)
        self.cache_write_load_value(v=1, f=CACHE_PICKLE)
        self.cache_write_load_value(v=123123123, f=CACHE_PICKLE)
        self.cache_write_load_value(v="foo", f=CACHE_PICKLE)
        self.cache_write_load_value(v={'active': True, 'list': [{'active': True, 'rrule': 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU', 'time': 'sunset+30m', 'value': 1}, {'active': True, 'rrule': 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU', 'time': 'sunrise-30m', 'value': 0}]}, f=CACHE_PICKLE)
        self.cache_write_load_value(v={'active': True}, f=CACHE_PICKLE)
        self.cache_write_load_value(v=[1,2,3,4,5], f=CACHE_PICKLE)
        self.cache_write_load_value(v=["a","2","3"], f=CACHE_PICKLE)
        self.cache_write_load_value(v=["a","2","3",2,3,4,5], f=CACHE_PICKLE)
        self.cache_write_load_value(v=datetime.datetime.now(), f=CACHE_PICKLE)





    def cache_write_load_value(self, v,f):
        from dateutil.tz import gettz

        TZ = gettz('UTC')
        fn = 'test.cache'

        lib.item._cache_write(value=v, filename=fn, cformat=f)

        date = cachedvalue = None
        date, cachedvalue = lib.item._cache_read(filename=fn, tz=TZ, cformat=f)
        #print(type(cachedvalue))
        self.assertEqual(v, cachedvalue)


    def testItemJsonDump(self):
        sh = MockSmartHome()

        # load items
        item_conf = None
        item_conf = lib.config.parse(common.BASE + "/tests/resources/item_dumps.yaml", item_conf)
        for attr, value in item_conf.items():
            if isinstance(value, dict):
                child_path = attr
                try:
                    child = lib.item.Item(sh, sh, child_path, value)
                except Exception as e:
                    self.logger.error("Item {}: problem creating: ()".format(child_path, e))
                else:
                    # vars(sh)[attr] = child
                    sh.add_item(child_path, child)
                    sh.children.append(child)

      #  if 1: self.dump_items(sh)
        #print(item_conf)
        #print(sh.return_item("item1").to_json())
        #print(sh.return_item("item3.item3b.item3b1").to_json())
        #print(sh.return_item("item3").to_json())
        import json
        self.assertEqual(json.loads(sh.return_item("item3").to_json())['name'], sh.return_item("item3")._name)
        self.assertEqual(json.loads(sh.return_item("item3").to_json())['id'], sh.return_item("item3")._path)


class MockSmartHome():
    
    class MockScheduler():
        def add(self, name, obj, prio=3, cron=None, cycle=None, value=None, offset=None, next=None): 
            print(name) 
            if isinstance(obj.__self__, SmartPlugin):
                name = name +'_'+ obj.__self__.get_instance_name()
            print(name)
            print( obj) 
            print(obj.__self__.get_instance_name())
    __logs = {}
    __item_dict = {}
    __items = []
    children = []
    _plugins = []
    scheduler = MockScheduler()
    def add_log(self, name, log):
        self.__logs[name] = log
    def now(self):
        import datetime
        return datetime.datetime.now()
    def add_item(self, path, item):
        if path not in self.__items:
            self.__items.append(path)
        self.__item_dict[path] = item
    def return_item(self, string):
        if string in self.__items:
            return self.__item_dict[string]
    def return_items(self):
        for item in self.__items:
            yield self.__item_dict[item]
    def return_plugins(self):
        for plugin in self._plugins:
            yield plugin   
if __name__ == '__main__':
    unittest.main(verbosity=2)

