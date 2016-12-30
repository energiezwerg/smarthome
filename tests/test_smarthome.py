#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016 Christian Strassburg  c.strassburg@gmx.de
#########################################################################
#  This file is part of SmartHomeNG
#  https://github.com/smarthomeNG/smarthome
#  http://knx-user-forum.de/
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG If not, see <http://www.gnu.org/licenses/>.
#########################################################################
import common
import unittest
import bin.smarthome


class SmarthomeTest(unittest.TestCase):
    def test_to_bool(self):

        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, None))
        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, False))
        self.assertIsNone(bin.smarthome.SmartHome.string2bool(self, "werwer"))
        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, "No"))
        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, "0"))
        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, ""))
        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, "n"))
        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, "false"))
        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, "False"))
        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, "f"))
        self.assertFalse(bin.smarthome.SmartHome.string2bool(self, 0))

        self.assertTrue(bin.smarthome.SmartHome.string2bool(self,1.2))
        self.assertTrue(bin.smarthome.SmartHome.string2bool(self,True))
        self.assertTrue(bin.smarthome.SmartHome.string2bool(self,"yes"))
        self.assertTrue(bin.smarthome.SmartHome.string2bool(self,"1"))
        self.assertTrue(bin.smarthome.SmartHome.string2bool(self,"y"))
        self.assertTrue(bin.smarthome.SmartHome.string2bool(self,"true"))
        self.assertTrue(bin.smarthome.SmartHome.string2bool(self,"True"))
        self.assertTrue(bin.smarthome.SmartHome.string2bool(self,"t"))
        # self.assertTrue(bin.smarthome.SmartHome.string2bool(self,1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
