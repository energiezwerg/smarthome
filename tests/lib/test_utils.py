#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016 Christian Strassburg  c.strassburg@gmx.de
#########################################################################
# Personal and non-commercial use only, redistribution is prohibited.
#########################################################################

import unittest
from lib.utils import Utils
#from wakeonlan import WakeOnLan
class LibUtilsTest(unittest.TestCase):

    def test_isMAC(self):
        self.assertTrue(True)
        self.assertTrue(Utils.isMAC("11:22:33:44:55:66"))
        self.assertTrue(Utils.isMAC("11-22-33-44-55-66"))
        self.assertTrue(Utils.isMAC("11 22 33 44 55 66"))
        self.assertTrue(Utils.isMAC("112233445566"))
        self.assertTrue(Utils.isMAC("000000000000"))
        self.assertTrue(Utils.isMAC("ffffffffffff"))
        self.assertFalse(Utils.isMAC("1r2233445566"))
        self.assertFalse(Utils.isMAC("gggggggggggg"))
        self.assertFalse(Utils.isMAC("1g:22:33:44:55:66"))
        self.assertFalse(Utils.isMAC(None))
        self.assertFalse(Utils.isMAC(""))
        self.assertFalse(Utils.isMAC(self))

    def test_isIP(self):
        self.assertFalse(Utils.isIP(""))
        self.assertFalse(Utils.isIP(None))
        self.assertFalse(Utils.isIP(self))

        self.assertTrue(Utils.isIP("1.2.3.4"))
        self.assertFalse(Utils.isIP("0.0.0.0"))
        self.assertTrue(Utils.isIP("255.255.255.255"))
        self.assertFalse(Utils.isIP("256.256.256.256"))
        self.assertFalse(Utils.isIP("2561.256.256.256"))
        self.assertFalse(Utils.isIP("561.256.256.256"))
        self.assertFalse(Utils.isIP("161.256.256"))

    def test_toBool(self):
        with self.assertRaises(Exception):
            Utils.toBool("161.256.256")
        
       # with self.assertRaises(Exception):
       #     Utils.toBool(self)
        self.assertFalse(Utils.toBool(None))
        self.assertFalse(Utils.toBool(False))
        self.assertFalse(Utils.toBool("No"))
        self.assertFalse(Utils.toBool("0"))
        self.assertFalse(Utils.toBool(""))
        self.assertFalse(Utils.toBool("n"))
        self.assertFalse(Utils.toBool("false"))
        self.assertFalse(Utils.toBool("f"))
        self.assertFalse(Utils.toBool(0))

        self.assertTrue(Utils.toBool(1.2))
        self.assertTrue(Utils.toBool(True))
        self.assertTrue(Utils.toBool("yes"))
        self.assertTrue(Utils.toBool("1"))
        self.assertTrue(Utils.toBool("y"))
        self.assertTrue(Utils.toBool("true"))
        self.assertTrue(Utils.toBool("t"))
        self.assertTrue(Utils.toBool(1))

if __name__ == '__main__':
    unittest.main(verbosity=2)
