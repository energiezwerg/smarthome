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
This library implements loading and starting of core modules of SmartHomeNG.


:Warning: This library is part of the core of SmartHomeNG. It **should not be called directly** from plugins!

"""
import logging
import threading
import inspect
import os.path		# until Backend is modified

import lib.config
#from lib.model.smartplugin import SmartPlugin
from lib.constants import (KEY_CLASS_NAME, KEY_CLASS_PATH, KEY_INSTANCE,YAML_FILE,CONF_FILE)

logger = logging.getLogger(__name__)


class Modules():
    """
    Module loader class. Parses config file and creates a worker thread for each module
    """
    
    _modules = []
    _threads = []
    
    def __init__(self, smarthome, configfile):

        # until Backend plugin is modified
        if os.path.isfile(configfile+ YAML_FILE):
            smarthome._module_conf = configfile + YAML_FILE
        else:
            smarthome._module_conf = configfile + CONF_FILE


        _conf = lib.config.parse_basename(configfile, configtype='module')
        if _conf == {}:
            return
            
        for module in _conf:
            args = {}
            logger.warning("Module: {0}".format(module))   #ex debug
            for arg in _conf[module]:
                if arg != KEY_CLASS_NAME and arg != KEY_CLASS_PATH and arg != KEY_INSTANCE:
                    value = _conf[module][arg]
                    if isinstance(value, str):
                        value = "'{0}'".format(value)
                    args[arg] = value
            classname = _conf[module][KEY_CLASS_NAME]
            classpath = _conf[module][KEY_CLASS_PATH]
            
            instance = ''
            if KEY_INSTANCE in _conf[module]:
                instance = _conf[module][KEY_INSTANCE].strip()
                if instance == 'default': 
                    instance = ''

            # give a warning if a module uses the same class twice
            for m in self._modules:
                if m.__class__.__name__ == classname:
                    logger.warning("Multiple module instances of class '{}' detected".format(classname))

            try:
                module_thread = ModuleWrapper(smarthome, module, classname, classpath, args, instance)
                self._threads.append(module_thread)
                self._modules.append(module_thread.module)
            except Exception as e:
                logger.error("Module '{}' configuration error: Module '{}' not found or class '{}' not found in module file".format(module, classpath, classname))
#                logger.exception("Module {0} exception: {1}".format(module, e))
        del(_conf)  # clean up

    def __iter__(self):
        for module in self._modules:
            yield module

    def start(self):
        """
        Start all modules
        """
        logger.warning('Start Modules')
        for module in self._threads:
            logger.warning('Starting {} Module'.format(module.name))   # ex debug
            module.start()

    def stop(self):
        """
        Stop all modules
        """
        logger.warning('Stop Modules')
        for module in self._threads:
            logger.debug('Stopping {} Module'.format(module.name))
            module.stop()
    
    def get_module(self, name):
        """
        Returns (the thread of) one module with given name 

        :param name: name of the module to get
        :type name: str
        
        :return: Thread of the module
        :rtype: thread
        """

        for thread in self._threads:
            if thread.name == name:
               return thread
        return None


class ModuleWrapper(threading.Thread):
    """
    Module wrapper class. Wraps around the loaded module code and defines the interface to the module.
    """

    def __init__(self, smarthome, name, classname, classpath, args, instance):
        threading.Thread.__init__(self, name=name)

        exec("import {0}".format(classpath))

        #exec("self.module = {0}.{1}(smarthome{2})".format(classpath, classname, args))
        exec("self.module = {0}.{1}.__new__({0}.{1})".format(classpath, classname))
        setattr(smarthome, self.name, self.module)

        exec("self.args = inspect.getargspec({0}.{1}.__init__)[0][1:]".format(classpath, classname))

        arglist = [name for name in self.args if name in args]
        argstring = ",".join(["{}={}".format(name, args[name]) for name in arglist])
        logger.debug("Using arguments {}".format(arglist))

        exec("self.module.__init__(smarthome{0}{1})".format("," if len(arglist) else "", argstring))

    def run(self):
        """
        Starts this module instance
        """
        self.module.run()

    def stop(self):
        """
        Stops this module instance
        """
        self.module.stop()
    
    def get_name(self):
        """
        Get the name of the current module instance
        
        :return: name of the module instance
        :rtype: str 
        """
        return self.name

    def get_ident(self):
        """
        Get the thread identifier of the current module instance
        
        :return: thread identifier of current module instance
        :rtype: int
        """
        return self.ident
    
    def get_implementation(self):
        """
        Get the implementation of the current module instance
        
        :return: implementation of current module instance
        :rtype: object of module
        """
        return self.module
