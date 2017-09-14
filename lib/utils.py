#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016 Christian Strassburg  c.strassburg@gmx.de
#########################################################################
#  This file is part of SmartHomeNG
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
#  along with SmartHomeNG  If not, see <http://www.gnu.org/licenses/>.
#########################################################################

"""
This library contails the Utile-class for SmartHomeNG.

New helper-functions are going to be implemented in this library.

"""

import re
import hashlib

IP_REGEX = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}|0
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}|0
            |
              0x0*[0-9a-f]{1,2}
            )
          ){0,3}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)

TIMEFRAME_REGEX = re.compile(r'^(\d+)([ihdwmy]?)$', re.VERBOSE | re.IGNORECASE)

class Utils(object):

    @staticmethod
    def is_mac(mac):
        """
        Validates a MAC address

        :param mac: MAC address
        :type string: str
        
        :return: True if value is a MAC
        :rtype: bool
        """
        
        mac = str(mac)
        if len(mac) == 12:
            for c in mac:
                try:
                    if int(c, 16) > 15:
                        return False
                except:
                    return False
            return True

        octets = re.split('[\:\-\ ]', mac)
        if len(octets) != 6:
            return False
        for i in octets:
            try:
                if int(i, 16) > 255:
                    return False
            except:
                return False
        return True

    @staticmethod
    def is_ip(string):
        """
        Checks if a string is a valid ip-address (v4)
        
        The ip-address has is checked to have the format with four decimal numbers divided by three dots (example: 10.0.0.250)
        
        :param string: String to check
        :type string: str
        
        :return: True if an ip, false otherwise.
        :rtype: bool
        """
        
        try:
            return bool(IP_REGEX.search(string))
        except TypeError:
            return False

    @staticmethod
    def is_hostname(string):
        """
        Checks if a string is a valid hostname
        
        The hostname has is checked to have a valid format
        
        :param string: String to check
        :type string: str
        
        :return: True if a hostname, false otherwise.
        :rtype: bool
        """
        
        try:
            return bool(re.match("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$", string))
        except TypeError:
            return False

    @staticmethod
    def is_timeframe(string):
        """
        Checks if a string is a timeframe. A timeframe consists of a
        number and an optional unit identifier (e.g. 2h, 30m, ...).
        Unit identifiers are: i for minutes, h for hours, d for days,
        w for weeks, m for months, y for years. If omitted milliseconds
        are assumed.
        
        :param string: String to check.
        :type string: str

        :return: True if a timeframe can be recognized, false otherwise.
        :rtype: bool
        """

        try:
            return bool(TIMEFRAME_REGEX.search(string))
        except TypeError:
            return False

    @staticmethod
    def is_knx_groupaddress(groupaddress):
        """
        Checks if the passed string is a valid knx goup address
        
        The checked format is:
           main group (0-31 = 5 bits)
           middle group (0-7 = 3 bits)
           subgroup (0-255 = 8 bits)
        
        :param groupaddress: String to check
        :type groupaddress: str

        :return: True if a groupaddress can be recognized, false otherwise.
        :rtype: bool
        """
        g = groupaddress.split('/')
        if len(g) != 3:
            return False
        if not( Utils.is_int(g[0]) and Utils.is_int(g[1]) and Utils.is_int(g[2]) ):
            return False
        if (int(g[0]) < 0) or (int(g[0]) > 31):
            return False
        if (int(g[1]) < 0) or (int(g[1]) > 7):
            return False
        if (int(g[2]) < 0) or (int(g[2]) > 255):
            return False
        return True
    
    @staticmethod
    def to_timeframe(value):
        """
        Converts a timeframe value to milliseconds. See is_timeframe() method.
        The special value 'now' is supported for the current time.

        :param value : value to convert
        :type value: str, int, ...

        :return: True if cant be converted and is true, False otherwise.
        :rtype: bool
        """
        
        minute = 60 * 1000
        hour = 60 * minute
        day = 24 * hour
        week = 7 * day
        month = 30 * day
        year = 365 * day
        frames = {'i': minute, 'h': hour, 'd': day, 'w': week, 'm': month, 'y': year}

        if value == 'now':
            value = '0'

        if not Utils.is_timeframe(value):
            raise Exception('Invalid value for boolean conversion: ' + value)

        amount, unit = TIMEFRAME_REGEX.match(value).groups()
        if unit in frames:
            return int(float(amount) * frames[unit])
        else:
            return int(amount)

    @staticmethod
    def is_int(string):
        """
        Checks if a string is a integer.
        
        :param string: String to check.
        :type string: str
        
        :return: True if a cast to int works, false otherwise.
        :rtype: bool
        """
        
        try:
            int(string)
            return True
        except ValueError:
            return False
        except TypeError:
            return False

    @staticmethod
    def is_float(string):
        """
        Checks if a string is a float.
        
        :param string: String to check.
        :type string: str

        :return: True if a cast to float works, false otherwise.
        :rtype: bool
        """

        try:
            float(string)
            return True
        except ValueError:
            return False
        except TypeError:
            return False

    @staticmethod
    def to_bool(value, default='exception'):
        """
        Converts a value to boolean.
        
        Raises exception if value is a string and can't be converted and if no default value is given
        Case is ignored. These string values are allowed:
        - True: 'True', "1", "true", "yes", "y", "t", "on"
        - False: "", "0", "faLse", "no", "n", "f", "off"
        Non-string values are passed to bool constructor.
        
        :param value : value to convert
        :param default: optional, value to return if value can not be parsed, if default is not set this method throws an exception
        :type value: str, object, int, ...
        :type value: str, object, int, ...
        
        :return: True if cant be converted and is true, False otherwise.
        :rtype: bool
        """
        # -> should it be possible to cast strings: 0 -> False and non-0 -> True (analog to integer values)?
        if type(value) == type(''):
            if value.lower() in ("yes", "y", "true",  "t", "1","on"):
                return True
            if value.lower() in ("no",  "n", "false", "f", "0", "off", ""):
                return False
            if default=='exception':
                raise Exception('Invalid value for boolean conversion: ' + value)
            else:
                return default
        return bool(value)

    @staticmethod
    def create_hash(plaintext):
        """
        Create hash (currently sha512) for given plaintext value
        
        :param plaintext: plaintext
        :type plaintext: str
        
        :return: hash of plaintext, lowercase letters
        :rtype: str
        """

        hashfunc = hashlib.sha512()
        hashfunc.update(plaintext.encode())
        return "".join(format(b, "02x") for b in hashfunc.digest())

    @staticmethod
    def is_hash(value):
        """
        Check if value is a valid hash (currently sha512) value
        
        :param value: value to check
        :type value: str
        
        :return: True: given value can be a sha512 hash, False: given value can not be a sha512 hash
        :rtype: bool
        """

        # a valid sha512 hash is a 128 charcter long string value
        if value is None or not isinstance(value, str) or len(value) != 128:
            return False

        # and its a hexedecimal value
        try:
            int(value, 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_hashed_password(pwd_to_check, hashed_pwd):
        """
        Check if given plaintext password matches the hashed password
        An empty password is always rejected
        
        :param pwd_to_check: plaintext password to check
        :type pwd_to_check: str
        :param hashed_pwd: hashed password
        :type hashed_pwd: str

        :return: True: password matches, False: password does not match
        :rtype: bool
        """

        if pwd_to_check is None or pwd_to_check == '':
            # No password given -> return "not matching"
            return False

        # todo: check pwd_to_check for minimum length?

        return Utils.create_hash(pwd_to_check) == hashed_pwd.lower()

    @staticmethod
    def strip_quotes(string):
        """
        If a string contains quotes as first and last character, this function
        returns the string without quotes, otherwise the string is returned unchanged
        
        :param string: string to check for quotes
        :type string: str

        :return: sting with quotes stripped
        :rtype: str
        """
        if type(string) is str:
            string = string.strip()
            if len(string) >= 2:
                if string[0] in ['"', "'"]:  # check if string starts with ' or "
                    if string[0] == string[-1]:  # and end with it
                        if string.count(string[0]) == 2:  # if they are the only one
                            string = string[1:-1]  # remove them
        return string
