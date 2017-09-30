#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2011-2013   Marcus Popp                        marcus@popp.mx
# Copyright 2016-       Martin Sinn                         m.sinn@gmx.de
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
##########################################################################

"""
This library implements logics in SmartHomeNG. 

The main class ``Logics`` implements the handling for all logics. This class has a couple
of static methods. These methods implement the API for handling logics from within SmartHomeNG and from plugins.
This API enables plugins to configure new logics or change the configuration of existing plugins.

Each logic is represented by an instance of the class ``Logic``.


:Warning: This library is part of the core of SmartHomeNG. **Only the static methods** should be called directly from plugins!

"""
import logging
import os

import ast

import lib.config
import lib.shyaml as shyaml
from lib.constants import PLUGIN_PARSE_LOGIC
from lib.constants import (YAML_FILE, CONF_FILE)

logger = logging.getLogger(__name__)


_smarthome = None
_logics_instance = None
_config_type = None


class Logics():
    """
    This is the main class for the implementation og logics in SmartHomeNG. It implements the API for the
    handling of those logics.
    """
    
    def __init__(self, smarthome, userlogicconf, envlogicconf):
        logger.info('Start Logics')
        self._sh = smarthome
        self._userlogicconf = userlogicconf
        self._env_dir = smarthome._env_dir
        self._envlogicconf = envlogicconf
        self._logic_dir = smarthome._logic_dir
        self._workers = []
        self._logics = {}
        self._bytecode = {}
        self.alive = True
        global _smarthome
        _smarthome = smarthome
        global _logics_instance
        _logics_instance = self
        _config = {}
        _config.update(self._read_logics(envlogicconf, self._env_dir))
        _config.update(self._read_logics(userlogicconf, self._logic_dir))

        for name in _config:
            self._load_logic(name, _config)


    def _read_logics(self, filename, directory):
        """
        Read the logics configuration file
        
        :param filename: name of the logics configurtion file
        :param directory: directory where the logics are stored
        """
        logger.debug("Reading Logics from {}.*".format(filename))
        config = lib.config.parse_basename(filename, configtype='logics')
        if config != {}:
            global _config_type
            if os.path.isfile(filename+YAML_FILE):
                _config_type = YAML_FILE
            else:
                _config_type = CONF_FILE

            for name in config:
                if 'filename' in config[name]:
                    config[name]['filename'] = directory + config[name]['filename']
        return config


    def _load_logic(self, name, config):
        """
        Load a logic, specified by section name in config
        """
        logger.debug("_load_logic: Logics.is_logic_loaded(name) = {}.".format( str(Logics.is_logic_loaded(name)) ))
        if Logics.is_logic_loaded(name):
            return False
        logger.debug("Logic: {}".format(name))
        logic = Logic(self._sh, name, config[name])
        if hasattr(logic, 'bytecode'):
            self._logics[name] = logic
            self._sh.scheduler.add(name, logic, logic.prio, logic.crontab, logic.cycle)
        else:
            return False
        # plugin hook
        for plugin in self._sh._plugins:
            if hasattr(plugin, PLUGIN_PARSE_LOGIC):
                update = plugin.parse_logic(logic)
                if update:
                    logic.add_method_trigger(update)
        # item hook
        if hasattr(logic, 'watch_item'):
            if isinstance(logic.watch_item, str):
                logic.watch_item = [logic.watch_item]
            for entry in logic.watch_item:
                for item in self._sh.match_items(entry):
                    item.add_logic_trigger(logic)
        return True
        
    
    def __iter__(self):
        for logic in self._logics:
            yield logic

    def __getitem__(self, name):
        if name in self._logics:
            return self._logics[name]

    def _delete_logic(self, name):
        if name in self._logics:
            del self._logics[name]


    def _return_logics(self):
        """
        Returns a list with the names of all loaded logics

        :return: list of logic names
        :rtype: list
        """
        for logic in _logics_instance:
            yield logic


    @staticmethod
    def reload_logics():
        """
        Function to reload all logics
        
        It generates new bytecode for every logic that is loaded. The configured triggers 
        are not loaded from the configuration, so the triggers that where active before the
        reload remain active.
        """
        for logic in self._logics:
            _logics_instance[logic]._generate_bytecode()


    @staticmethod
    def is_logic_loaded(name):
        """
        Test if a logic is loaded. Given is the name of the section in /etc/logic.yaml
    
        :param name: logic name (name of the configuration section section)
        :type name: str
    
        :return: True: Logic is loaded
        :rtype: bool
        """
        if _smarthome == None:
            logger.critical("is_logic_loaded: _smarthome is not initialized")
            return False
        
        if Logics.return_logic(name) == None:
            return False
        else:
            return True


    @staticmethod
    def return_logic(name):
        """
        Returns (the object of) one loaded logic with given name 

        :param name: name of the logic to get
        :type name: str

        :return: object of the logic
        :rtype: object
        """
        
        return _logics_instance[name]


    @staticmethod
    def unload_logic(name):
        """
        Unload a specified logic
        
        This function unloads a logic. Before unloading, it remove defined schedules and triggers for ``watch_item``s.
        
        :param name: Name of the section that defines the logic in the configuration file
        :type name: str
        """
        if _smarthome == None:
            logger.critical("unload_logic: _smarthome is not initialized")
            return False

        logger.info("lib.logic: unload_logic: logic = '{}'".format(name))
        mylogic = Logics.return_logic(name)
        if mylogic == None:
            return False
        
        mylogic.enabled = False
        mylogic.cycle = None
        mylogic.crontab = None

        # Scheduler entfernen
        _smarthome.scheduler.remove(name)
    
        # watch_items entfernen
        if hasattr(mylogic, 'watch_item'):
            if isinstance(mylogic.watch_item, str):
                mylogic.watch_item = [mylogic.watch_item]
            for entry in mylogic.watch_item:
                # item hook
                for item in _smarthome.match_items(entry):
                    try:
                        item.remove_logic_trigger(mylogic)
                    except:
                        logger.error("lib.logic: unload_logic: logic = '{}' - cannot remove logic_triggers".format(name))
        mylogic.watch_item = []
        _logics_instance._delete_logic(name)
        return True


    @staticmethod
    def load_logic(name):
        """
        Load a specified logic
        
        Load a logic as defined in the configuration section. After loading the logic's code,
        the defined schedules and/or triggers adre set.
        
        :param name: Name of the logic (name of the configuration section)
        :type name: str
        
        :return: Success
        :rtype: bool
        """
        _config = _logics_instance._read_logics(_smarthome._logic_conf_basename, _smarthome._logic_dir)
        logger.info("lib.logic: try load_logic ({}): _config = {}".format( name, str(_config) ))
        if not (name in _config):
            return False
    
        logger.info("lib.logic: load_logic ({}): _config = {}".format( name, str(_config) ))
        return _logics_instance._load_logic(name, _config)


    @staticmethod
    def return_logictype(name):
        """
        Returns the type of a specified logic (Python, Blockly, None)
        
        :param name: Name of the logic (name of the configuration section)
        :type name: str
        
        :return: Logic type ('Python', 'Blockly' or None)
        :rtype: str or None
        """
        # load /etc/logic.yaml
        conf_filename = os.path.join(_smarthome._etc_dir, 'logic') 
        config = shyaml.yaml_load_roundtrip(conf_filename)

        filename = config[name]['filename']
        blocklyname = os.path.splitext(os.path.basename(filename))[0]+'.xml'
        logic_type = 'None'
        if os.path.isfile(os.path.join(_smarthome._logic_dir, filename)):
            logic_type = 'Python'
            if os.path.isfile(os.path.join(_smarthome._logic_dir, blocklyname)):
                logic_type = 'Blockly'
        logger.info("lib.logic: return_logictype: name '{}', logic_type '{}'".format(name, logic_type))
        return logic_type
        

    @staticmethod
    def return_defined_logics(withtype=False):
        """
        Returns the names of defined logics from file /etc/logic.yaml as a list
        
        If ``withtype`` is specified and set to True, the function returns a dict with names and
        logictypes ('Python', 'Blockly')

        :param withtype: If specified and set to True, the function will additionally return the logic types
        :type withtype: bool
        
        :return: list of defined logics or dict of defined logics with type
        :rtype: list or dict
        """
        if withtype:
            logic_list = {}
        else:
            logic_list = []
        if _smarthome == None:
            logger.critical("update_config_section: _smarthome is not initialized")
            return logic_list
        
        # load /etc/logic.yaml
        conf_filename = os.path.join(_smarthome._etc_dir, 'logic') 
        config = shyaml.yaml_load_roundtrip(conf_filename)

        for section in config:
            logic_dict = {}
            filename = config[section]['filename']
            blocklyname = os.path.splitext(os.path.basename(filename))[0]+'.xml'
            logic_type = 'None'
            if os.path.isfile(os.path.join(_smarthome._logic_dir, filename)):
                logic_type = 'Python'
                if os.path.isfile(os.path.join(_smarthome._logic_dir, blocklyname)):
                    logic_type = 'Blockly'
            logger.info("lib.logic: get_defined_logics: section '{}', logic_type '{}'".format(section, logic_type))
            
            if withtype:
                logic_list[section] = logic_type
            else:
                logic_list.append(section)

        return logic_list
        

    @staticmethod
    def return_loaded_logics():
        """
        Returns a list with the names of all logics that are currently loaded

        :return: list of logic names
        :rtype: list
        """

        logic_list = []
        for logic in _logics_instance._logics:
            logic_list.append(logic)
        return logic_list


    @staticmethod
    def return_config_type():
        """
        Return the used config type 
        
        After initialization this function returns '.conf', if the used logic configuration file in /etc
        is in the old file format or '.yaml' if the used configuration file is in YAML format.
        
        To use the following functions for reading and manipulating the logic configuration, the
        configuration file **has to be** in YAML format. Otherwise the functions will not work/return empty results.
    
        :return: '.yaml', '.conf' or None
        :rtype: str or None
        """
        return _config_type


    @staticmethod
    def read_config_section(section):
        """
        Read a section from /etc/logic.yaml
        
        This funtion returns the data from one section of the configuration file as a list of
        configuration entries. A configuration entry is a list with three items:
          - key      configuration key
          - value    configuration value (string or list)
          - comment  comment for the value (string or list)
          
        :param section: Name of the logic (section)
        :type section: str
        
        :return: config_list: list of configuration entries. Each entry of this list is a list with three string entries: ['key', 'value', 'comment']
        :rtype: list of lists
        """
        if Logics.return_config_type() != YAML_FILE:
            logger.error("update_config_section: Editing of configuration only possible with new (yaml) config format")
            return False
            
        if _smarthome == None:
            logger.critical("update_config_section: _smarthome is not initialized")
            return False
        
        # load /etc/logic.yaml
        conf_filename = os.path.join(_smarthome._etc_dir, 'logic') 
        conf = shyaml.yaml_load_roundtrip(conf_filename)

        config_list = []
        section_dict = conf.get(section, {})
#        logger.warning("read_config_section: read_config_section('{}') = {}".format(section, str(section_dict) ))
        for key in section_dict:
            if isinstance(section_dict[key], list):
                value = section_dict[key]
                comment = []            # 'Comment 6: ' + loaded['a']['c'].ca.items[0][0].value      'Comment 7: ' + loaded['a']['c'].ca.items[1][0].value
                for i in range(len(value)):
                    c = section_dict[key].ca.items[i][0].value
                    if c[0] == '#':
                        c = c[1:]
                    
                    comment.append(c.strip())
            else:
                value = section_dict[key]
                c = section_dict.ca.items[key][2].value    # if not list: loaded['a'].ca.items['b'][2].value 
                if c[0] == '#':
                        c = c[1:]
                comment = c.strip()
            
#            logger.warning("-> read_config_section: section_dict['{}'] = {}, comment = '{}'".format(key, str(section_dict[key]), comment ))
            config_list.append([key, value, comment])
        return config_list
        
        
    @staticmethod
    def update_config_section(active, section, config_list):
        """
        Update file /etc/logic.yaml
    
        This method creates/updates a section in /etc/logic.yaml. If the section exist, it is cleared
        before new configuration imformation is written to the section
    
        :param active: True: logic is/should be active
        :param section: name of section to configure in logics configurationfile
        :param config_list: list of configuration entries. Each entry of this list is a list with three string entries: ['key', 'value', 'comment']
        :type active: bool
        :type section: str
        :type config_list: list of lists
        """
        if Logics.return_config_type() != YAML_FILE:
            logger.error("update_config_section: Editing of configuration only possible with new (yaml) config format")
            return False
            
        if _smarthome == None:
            logger.critical("update_config_section: _smarthome is not initialized")
            return False
        
        # load /etc/logic.yaml
        conf_filename = os.path.join(_smarthome._etc_dir, 'logic') 
        conf = shyaml.yaml_load_roundtrip(conf_filename)

        # empty section
        conf[section] = shyaml.get_emptynode()

        if active:
            # add entries to section
            for c in config_list:
                # process config entries
                key = c[0].strip()
                value = c[1]
                comment = c[2]

                if isinstance(value, str):
                    value = value.strip()
                    comment = comment.strip()
                    if value[0] == '[' and value[-1] == ']':
                        # convert a list of triggers to list, if given as a string
                        value = ast.literal_eval(value)
                        comment = ast.literal_eval(comment)
                    else:
                        # process single trigger
                        conf[section][key] = value
                        conf[section].yaml_add_eol_comment(comment, key, column=50)

                if isinstance(value, list):
                    # process a list of triggers
                    conf[section][key] = shyaml.get_commentedseq(value)
                    listvalue = True
                    for i in range(len(value)):
                        if comment[i] != '':
                            conf[section][key].yaml_add_eol_comment(comment[i], i, column=50)

        if conf[section] == shyaml.get_emptynode():
            conf[section] = None
        shyaml.yaml_save_roundtrip(conf_filename, conf, True)


class Logic():
    """
    Class for the representation of a loaded logic
    """
    def __init__(self, smarthome, name, attributes):
        self._sh = smarthome
        self.name = name
        self.enabled = True if 'enabled' not in attributes else bool(attributes['enabled'])
        self.crontab = None
        self.cycle = None
        self.prio = 3
        self.last = None
        self.conf = attributes
        self.__methods_to_trigger = []
        if attributes != 'None':
            for attribute in attributes:
                vars(self)[attribute] = attributes[attribute]
            self.prio = int(self.prio)
            self._generate_bytecode()
        else:
            logger.error("Logic {} is not configured correctly (configuration has no attibutes)".format(self.name))
        

    def id(self):
        """
        Returns the id of the loaded logic
        """
        return self.name

    def __str__(self):
        return self.name

    def __call__(self, caller='Logic', source=None, value=None, dest=None, dt=None):
        if self.enabled:
            self._sh.scheduler.trigger(self.name, self, prio=self.prio, by=caller, source=source, dest=dest, value=value, dt=dt)

    def enable(self):
        """
        Enables the loaded logic
        """
        self.enabled =True

    def disable(self):
        """
        Disables the loaded logic
        """
        self.enabled = False

    def trigger(self, by='Logic', source=None, value=None, dest=None, dt=None):
        if self.enabled:
            self._sh.scheduler.trigger(self.name, self, prio=self.prio, by=by, source=source, dest=dest, value=value, dt=dt)

    def _generate_bytecode(self):
        if hasattr(self, 'filename'):
            if not os.access(self.filename, os.R_OK):
                logger.warning("{}: Could not access logic file ({}) => ignoring.".format(self.name, self.filename))
                return
            try:
#                code = open(self.filename, encoding='UTF-8').read()
                f = open(self.filename, encoding='UTF-8')
                code = f.read()
                f.close()
                code = code.lstrip('\ufeff')  # remove BOM
                self.bytecode = compile(code, self.filename, 'exec')
            except Exception as e:
                logger.exception("Exception: {}".format(e))
        else:
            logger.warning("{}: No filename specified => ignoring.".format(self.name))

    def add_method_trigger(self, method):
        self.__methods_to_trigger.append(method)

    def get_method_triggers(self):
        return self.__methods_to_trigger


