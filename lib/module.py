#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2017-       Martin Sinn                         m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG
#
#  SmartHomeNG is free software: you can redistribute it and/or modifyNode.js Design Patterns - Second Edition
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
#import threading
import inspect

import lib.config
#from lib.model.smartplugin import SmartPlugin
from lib.constants import (KEY_CLASS_NAME, KEY_CLASS_PATH, KEY_INSTANCE,YAML_FILE,CONF_FILE)
from lib.utils import Utils

logger = logging.getLogger(__name__)


class Modules():
    """
    Module loader class. Parses config file and creates a worker thread for each module
    
    :param smarthome: Instance of the smarthome master-object
    :param configfile: Basename of the module configuration file
    :type samrthome: object
    :type configfile: str
    """
    
    _modules = []
    _moduledict = {}
    
    def __init__(self, smarthome, configfile):
        self._sh = smarthome

        try:
            self._debug_modules = Utils.to_bool(self._sh._debug_modules)
        except:
            self._debug_modules = False
        if self._debug_modules:
            logger.warning('Modules: Debugging of modules is enabled. Exceptions are not caught outside of the module(s)' )

        # read module configuration (from module.yaml)
        _conf = lib.config.parse_basename(configfile, configtype='module')
        if _conf == {}:
            return
            
        for module in _conf:
            logger.debug("Modules, section: {}".format(module))
            args = {}
            for arg in _conf[module]:
                if arg != KEY_CLASS_NAME and arg != KEY_CLASS_PATH and arg != KEY_INSTANCE:
                    value = _conf[module][arg]
                    if isinstance(value, str):
                        value = "'{0}'".format(value)
                    args[arg] = value
            classname = _conf[module][KEY_CLASS_NAME]
            try:
                classpath = _conf[module][KEY_CLASS_PATH]
            except:
                classpath = 'modules.' + classname
                        
            # give a warning if a module uses the same class twice
            double = False
            for m in self._modules:
                if m.__class__.__name__ == classname:
                    double = True
                    logger.warning("Modules, section '{}': Multiple module instances of class '{}' detected, additional instance not initialized".format(module, classname))

            if not double:
                if self._debug_modules == True:
                    self._LoadModule(module, classname, classpath, args)
                else:
                    try:
                        self._LoadModule(module, classname, classpath, args)
                    except Exception as e:
#                        logger.error("Modules, section '{}' configuration error: Module '{}' not found or class '{}' not found in module file".format(module, classpath, classname))
                        logger.exception("Module {0} exception: {1}".format(module, e))

        self._sh._moduledict = self._moduledict
        logger.warning('Loaded Modules: {}'.format( str( self._sh.return_modules() ) ) )

        # clean up (module configuration from module.yaml)
        del(_conf)  # clean up
        
        return


    def _LoadModule(self, name, classname, classpath, args):
        """
        Module Loader. Loads one module defined by the parameters classname and classpath.
        Parameters defined in the configuration file are passed to this function as 'args'
        
        :param name: Section name in module configuration file (etc/module.yaml)
        :param classname: Name of the (main) class in the module
        :param classpath: Path to the Python file containing the class
        :param args: Parameter as specified in the configuration file (etc/module.yaml)
        :type name: str
        :type classname: str
        :type classpath: str
        :type args: dict
        
        :return: loaded module
        :rtype: object
        """

        exec("import {0}".format(classpath))
        exec("self.loadedmodule = {0}.{1}.__new__({0}.{1})".format(classpath, classname))
        
        logger.debug('_LoadModule: Section {}, Module {}, classpath {}'.format( name, classname, classpath ))
        
        exec("self.args = inspect.getargspec({0}.{1}.__init__)[0][1:]".format(classpath, classname))

        arglist = [name for name in self.args if name in args]
        argstring = ",".join(["{}={}".format(name, args[name]) for name in arglist])
        logger.debug('_LoadModule: Using arguments {}'.format(arglist))    # ex debug
        
        exec("self.loadedmodule.__init__(self._sh{0}{1})".format("," if len(arglist) else "", argstring))

        self._moduledict[classname] = self.loadedmodule
        self._modules.append(self._moduledict[classname])
        logger.info('Modules: Loaded module {} v{}: {}'.format( str(self._moduledict[classname].__class__.__name__), str(self._moduledict[classname].version), str(self._moduledict[classname].longname) ) )
        return

        
    def start(self):
        """
        Start all modules

        Call start routine of module in case the module wants to start any threads
        """
        logger.info('Start Modules')

        for module in self._sh.return_modules():
            logger.debug('Starting {} Module'.format(module))
            self.m = self._sh.get_module(module)
            self.m.start()


    def stop(self):
        """
        Stop all modules
        
        Call stop routine of module to clean up in case the module has started any threads
        """
        logger.warning('Stop Modules')
    
        for module in self._sh.return_modules():
            logger.debug('Stopping {} Module'.format(module))
            self.m = self._sh.get_module(module)
            self.m.stop()

