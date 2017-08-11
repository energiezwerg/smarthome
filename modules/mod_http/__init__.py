#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2016-2017  Martin Sinn                       m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG.
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
#  along with SmartHomeNG.  If not, see <http://www.gnu.org/licenses/>.
#########################################################################


import logging

class mod_http():

    version = '1.4.0'
    shortname = ''
    longname = 'CherryPy http module for SmartHomeNG'
    
    def __init__(self, sh, port):
        self.shortname = self.__class__.__name__
        self.logger = logging.getLogger(__name__)
        
#        self.logger.warning('Module mod_http: Initializing module {} v{}: {}'.format( str(self.shortname), str(self.version), str(self.longname) ) )
#        self.logger.warning('Module mod_http: Argument {}={}'.format( str('port'), str(port) ) )

