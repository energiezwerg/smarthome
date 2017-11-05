#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016-2017   Martin Sinn                         m.sinn@gmx.de
# Copyright 2013-2013   Marcus Popp                        marcus@popp.mx
#########################################################################
#  This file is part of SmartHomeNG.    https://github.com/smarthomeNG//
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

"""
This file implements scenes in SmartHomeNG
"""

import logging
import os.path
import csv

from lib.logic import Logics
import lib.shyaml as yaml

logger = logging.getLogger(__name__)


_scenes_instance = None    # Pointer to the initialized instance of the Plugins class (for use by static methods)


class Scenes():
    """
    This class loads all scene definitions from /scenes folder and adds the necessary triggers
    for the scenes to function.

    :Note: The scene definitions are stored in /scenes files with the extension .conf but don't follow the file format for conf-files of smarthome.py!

    :param smarthome: Main SmartHomeNG object
    :type smarthome: object
    """

    def __init__(self, smarthome):
        self._sh = smarthome
        global _scenes_instance
        _scenes_instance = self
        self._scenes = {}
        self._scenes_dir = smarthome.base_dir + '/scenes/'
        if not os.path.isdir(self._scenes_dir):
            logger.warning("Directory scenes not found. Ignoring scenes.".format(self._scenes_dir))
            return

        for item in smarthome.return_items():
            if item.type() == 'scene':
                scene_file = os.path.join(self._scenes_dir, item.id())

                scene_file_yaml = yaml.yaml_load(scene_file+'.yaml', ordered=False, ignore_notfound=True)
                if scene_file_yaml is not None:
                    # Reading yaml file with scene definition
                    for scene_no in scene_file_yaml:
                        if isinstance(scene_file_yaml[scene_no], str):
                            scene_file_yaml[scene_no] = [ scene_file_yaml[scene_no] ]
                        for scene_lo_list in scene_file_yaml[scene_no]:
                            scene_lo_list_out = scene_lo_list.split('=')
                            scene_lo_list_out.insert(0, str(scene_no))
                            scene_lo_list_out[1] = scene_lo_list_out[1].strip()
                            scene_lo_list_out[2] = scene_lo_list_out[2].strip()
                            self._add_scene_entry(item, scene_lo_list_out)
                    logger.info("Loading scene definition from file = {}".format(scene_file+'.yaml'))
                else:
                    # Trying to read conf file with scene definition
                    scene_conf_file = scene_file + '.conf'
                    try:
                        with open(scene_conf_file, 'r', encoding='UTF-8') as f:
                            reader = csv.reader(f, delimiter=' ')
                            for row in reader:
                                if row == []:  # ignore empty lines
                                    continue
                                if row[0][0] == '#':  # ignore comments
                                    continue
                                self._add_scene_entry(item, row)
                    except Exception as e:
                        logger.warning("Problem reading scene file {0}: {1}".format(scene_file, e))
                        continue
                    logger.info("Loading scene definition from file = {}".format(scene_conf_file))
                item.add_method_trigger(self._trigger)


    def _trigger(self, item, caller, source, dest):
        """
        Trigger a scene
        """
        if not item.id() in self._scenes:
            return
        if str(item()) in self._scenes[item.id()]:
            logger.info("Triggered scene {} with value {}:".format(item.id(), item()))
            for ditem, value in self._scenes[item.id()][str(item())]:
                sh = self._sh  # noqa
                try:
                    rvalue = eval(value)
                except Exception as e:
                    logger.warning(" - Problem evaluating: {} - {}".format(value, e))
                else:
                    if rvalue is not None:
                        # set item
                        if str(rvalue) == str(value):
                            logger.info(" - Item {} set to {}".format(ditem, rvalue))
                        else:
                            logger.info(" - Item {} set to {} ( from {} )".format(ditem, rvalue, value))
                        try:
                            ditem(value=rvalue, caller='Scene', source=item.id())
                        except Exception as e:
                            logger.warning(" - ditem '{}', value '{}', exception {}".format(ditem, rvalue, e))


    def _add_scene_entry(self, item, row):
        """
        Adds a single assignement entry to the loaded scenes
        
        :param item:
        :param row: list of: scene number, item to assign to, value to assign to item 
        :type item: item object
        :type row: list (with 3 entries)
        """
        logger.debug("_add_scene_entry: item = {}, row = {}".format(item, row))
        row[2] = item.get_stringwithabsolutepathes(row[2], 'sh.', '(', 'scene')
        ditem = self._sh.return_item(row[1])
        if ditem is None:
#            ditem = smarthome.return_logic(row[1])
            ditem = Logics.return_logic(row[1])
            if ditem is None:
                logger.warning("Could not find item or logic '{}' specified in {}".format(row[1], scene_file))
                return

        if item.id() in self._scenes:
            if row[0] in self._scenes[item.id()]:
                self._scenes[item.id()][row[0]].append([ditem, row[2]])
            else:
                self._scenes[item.id()][row[0]] = [[ditem, row[2]]]
        else:
            self._scenes[item.id()] = {row[0]: [[ditem, row[2]]]}
        return
        
        
    # ------------------------------------------------------------------------------------
    #   Following (static) methods of the class Plugins implement the API for plugins in shNG
    # ------------------------------------------------------------------------------------

    @staticmethod
    def get_instance():
        """
        Returns the instance of the Scenes class, to be used to access the scene-api
        
        Use it the following way to access the api:
        
        .. code-block:: python

            from lib.scene import Scenes
            scenes = Scenes.get_instance()
            
            # to access a method (eg. xxx()):
            scenes.xxx()

        
        :return: logics instance
        :rtype: object of None
        """
        if _scenes_instance == None:
            return None
        else:
            return _scenes_instance


    def get_loaded_scenes(self):
        """
        Returns a list with the names of all scenes that are currently loaded

        :return: list of scene names
        :rtype: list
        """

        scene_list = []
        for scene in self._scenes:
            scene_list.append(scene)
        return sorted(scene_list)


    def get_scene_values(self, name):
        """
        Returns a list with the the defined values for a scene

        :return: list of scene values
        :rtype: list
        """

        value_list = []
        for value in self._scenes[name]:
            value_list.append(int(value))
        value_list = sorted(value_list)
        value_list2 = []
        for value in value_list:
            value_list2.append(str(value))
        return value_list2


    def return_scene_value_actions(self, name, value):
        """
        Returns a list with the the defined actions for value of a a scene

        :return: list of value actions (item name, value to set)
        :rtype: list
        """

        action_list = []
        for action in self._scenes[name][value]:
            return_action = [ str(action[0]), action[1] ]
            action_list.append(return_action)

        return action_list

