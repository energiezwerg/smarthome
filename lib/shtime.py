#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016-       Martin Sinn                         m.sinn@gmx.de
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
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#########################################################################


import datetime
import logging


logger = logging.getLogger(__name__)

_shtime_instance = None    # Pointer to the initialized instance of the shtime class (for use by static methods)


class Shtime:

    _tzinfo = None
    _utctz = None
    _starttime = None
    
    
    def __init__(self, smarthome):
        global _shtime_instance
        _shtime_instance = self
        
        self._starttime = datetime.datetime.now()


    # -------------------------------------------------------------------------------------------
    #   Following (static) method of the class Scheduler implement the API for schedulers in shNG
    # -------------------------------------------------------------------------------------------

    @staticmethod
    def get_instance():
        """
        Returns the instance of the Shtime class, to be used to access the shtime-API

       .. code-block:: python

           from lib.shtime import Shtime
           shtime = Shtime.get_instance()

           # to access a method (eg. to get timezone info):
           shtime.tzinfo()


        :return: shinfo instance
        :rtype: object or None
        """
        if _shtime_instance == None:
            return None
        else:
            return _shtime_instance


    def set_tzinfo(self, tzinfo):
        """
        Set the timezone info
        """
        self._tzinfo = tzinfo
        return
        
        
    #################################################################
    # Time Methods
    #################################################################
    def now(self):
        """
        Returns the actual time in a timezone aware format
        
        :return: Actual time for the local timezone
        :rtype: datetime
        """
        
        if self._tzinfo is None:
            self._tzinfo = tz.gettz('UTC')
        # tz aware 'localtime'
        return datetime.datetime.now(self._tzinfo)


    def tzinfo(self):
        """
        Returns the info about the actual local timezone

        :return: Timezone info
        :rtype: str
        """

        return self._tzinfo


    def utcnow(self):
        """
        Returns the actual time in GMT

        :return: Actual time in GMT
        :rtype: datetime
        """

        # tz aware utc time
        if self._utctz is None:
            self._utctz = tz.gettz('UTC')
        return datetime.datetime.now(self._utctz)


    def utcinfo(self):
        """
        Returns the info about the GMT timezone

        :return: Timezone info
        :rtype: str
        """

        return self._utctz


    def runtime(self):
        """
        Returns the uptime of SmartHomeNG

        :return: Uptime in days, hours, minutes and seconds
        :rtype: str
        """

        return datetime.datetime.now() - self._starttime


