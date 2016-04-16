#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2016 <AUTHOR>                                        <EMAIL>
#########################################################################
#  This file is part of SmartHomeNG.py.   
#
#  SmartHomeNG.py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHome.py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeiNG.py. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import logging

class FooClass:

    def __init__(self, smarthome):
        self.logger = logging.getLogger(__name__)
        self.sh = smarthome

    def run(self):
        self.logger.debug("run method called")
        self.alive = True

    def stop(self):
        self.alive = False
        self.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    FooClass(None).run()
