#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016-       Martin Sinn                         m.sinn@gmx.de
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
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import logging
import collections
import lib.shyaml as shyaml

logger = logging.getLogger(__name__)


def remove_comments(ydata, level=0):
    '''
    Removes comments from a dict or OrderedDict structure

    :param ydata: configuration (sub)tree to work on
    :param level: optional subtree level (used for recursion)
    '''
    level_keys = list(ydata.keys())
    for key in level_keys:
        if type(ydata[key]).__name__ in ['dict','OrderedDict']:
            remove_comments(ydata[key], level+1)
        else:
            if key.startswith('comment'):
                ydata.pop(key)


def merge(source, destination):
    '''
    Merges an OrderedDict Tree into another one
    
    Run me with nosetests --with-doctest file.py

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    
    
    :param source: OrderedDict tree to be merged into another one
    :param destination: OrderedDict tree, into which the other OrderedDict tree is merged
    :return: The resulting merged OrderedDict tree
    '''
    for key, value in source.items():
        if isinstance(value, collections.OrderedDict):
            # get node or create one
            node = destination.setdefault(key, collections.OrderedDict())
            merge(value, node)
        else:
            if type(value).__name__ == 'list':
                destination[key] = value
            else:
                # convert to string and remove newlines from multiline attributes
                destination[key] = str(value).replace('\n','')

    return destination
    
    
def parse(filename, config=None):
    '''
    Load and parse a yaml configuration file and merge it to the configuration tree

    :param filename: Name of the configuration file
    :param config: Optional OrderedDict tree, into which the configuration should be merged
    :return: The resulting merged OrderedDict tree
    '''
    if config is None:
        config = collections.OrderedDict()

    items = shyaml.yaml_load(filename, ordered=True)
    remove_comments(items)
    
    config = merge(items, config)
    return config
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    conf = parse('dev.conf')
    print(conf)
