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


# TO DO
# - consolidate with plugin.py


"""
This library implements loading and starting of core modules of SmartHomeNG.


:Warning: This library is part of the core of SmartHomeNG. It **should not be called directly** from plugins!

"""
import logging
#import threading
import inspect
import os

import lib.config
#from lib.model.smartplugin import SmartPlugin
from lib.constants import (KEY_CLASS_NAME, KEY_CLASS_PATH, KEY_INSTANCE,CONF_FILE)
#from lib.utils import Utils
from lib.metadata import Metadata

logger = logging.getLogger(__name__)


class Modules():
    """
    Module loader class. Parses config file and creates an instance for each module.
    To start the modules, the start() method has to be called.
    
    :param smarthome: Instance of the smarthome master-object
    :param configfile: Basename of the module configuration file
    :type samrthome: object
    :type configfile: str
    """
    
    _modules = []
    _moduledict = {}
    
    def __init__(self, smarthome, configfile):
        self._sh = smarthome
        self._sh._moduledict = {}

        # read module configuration (from etc/module.yaml)
        _conf = lib.config.parse_basename(configfile, configtype='module')
        if _conf == {}:
            return
            
        for module in _conf:
            logger.debug("Modules, section: {}".format(module))
            module_name, self.meta = self._get_modulename_and_metadata(_conf[module])
            if self.meta.test_shngcompatibility():
                args = self._get_conf_args(_conf[module])
                classname, classpath = self._get_classname_and_classpath(_conf[module], module_name)
                if not self._test_duplicate_configuration(module, classname):
                    try:
                        self._load_module(module, classname, classpath, args)
                    except Exception as e:
                        logger.exception("Module {0} exception: {1}".format(module, e))

        self._sh._moduledict = self._moduledict
        logger.warning('Loaded Modules: {}'.format( str( self._sh.return_modules() ) ) )

        # clean up (module configuration from module.yaml)
        del(_conf)  # clean up
        
        return


    def _get_modulename_and_metadata(self, mod_conf):
        """
        Return the actual module name and the metadata instance
        
        :param mod_conf: loaded section of the module.yaml for the actual module
        :type mod_conf: dict
        
        :return: module_name and metadata_instance
        :rtype: string, object
        """
        module_name = mod_conf.get('module_name','').lower()
        if module_name != '':
            meta = Metadata(self._sh, module_name, 'module')
        else:
            classpath = mod_conf.get(KEY_CLASS_PATH,'')
            if classpath != '':
                module_name = classpath.split('.')[len(classpath.split('.'))-1].lower()
            logger.info("Modules: module_name '{}' was extracted from classpath '{}'".format(module_name, classpath))
            meta = Metadata(self._sh, module_name, 'module', classpath)
        return (module_name, meta)
        

    def _get_conf_args(self, mod_conf):
        """
        Return the parameters/values for the actual module as args-dict
        
        :param mod_conf: loaded section of the module.yaml for the actual module
        :type mod_conf: dict
        
        :return: args = specified parameters and their values
        :rtype: dict
        """
        args = {}
        for arg in mod_conf:
            if arg != KEY_CLASS_NAME and arg != KEY_CLASS_PATH and arg != KEY_INSTANCE:
                value = mod_conf[arg]
                if isinstance(value, str):
                    value = "'{0}'".format(value)
                args[arg] = value
        return args


    def _get_classname_and_classpath(self, mod_conf, module_name):
        """
        Returns the classname and the classpath for the actual module
        
        :param mod_conf: loaded section of the module.yaml for the actual module
        :param module_name: Module name (to be used, for building classpass, if it is not specified in the configuration
        :type mod_conf: dict
        :type module_name: str
        
        :return: classname, classpass
        :rtype: str, str
        """
        classname = self.meta.get_string('classname')
        if classname == '':
            classname = mod_conf.get(KEY_CLASS_NAME,'')
        try:
            classpath = mod_conf[KEY_CLASS_PATH]
        except:
            classpath = 'modules.' + module_name
        return (classname, classpath)
        

    def _test_duplicate_configuration(self, module, classname):
        """
        Returns True, if a module instance of the classname is already loaded by another configuration section
        
        :param module: Name of the configuration
        :param classname: Name of the class to check
        :type module: str
        :type classname: str
        
        :return: True, if module is already loaded
        :rtype: bool
        """
        # give a warning if a module uses the same class twice
        duplicate = False
        for m in self._modules:
            if m.__class__.__name__ == classname:
                duplicate = True
                logger.warning("Modules, section '{}': Multiple module instances of class '{}' detected, additional instance not initialized".format(module, classname))
        return duplicate
        
        
    def _load_module(self, name, classname, classpath, args):
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
        logger.debug('_load_module: Section {}, Module {}, classpath {}'.format( name, classname, classpath ))
        
        # Load an instance of the module
        try:
            exec("import {0}".format(classpath))
        except Exception as e:
            logger.exception("Module '{0}' exception during import of __init__.py: {1}".format(name, e))
            return None
        exec("self.loadedmodule = {0}.{1}.__new__({0}.{1})".format(classpath, classname))
                
        # get arguments defined in __init__ of module's class to self.args
        exec("self.args = inspect.getargspec({0}.{1}.__init__)[0][1:]".format(classpath, classname))

        # get list of argument used names, if they are defined in the module's class
        logger.debug("Module '{}': args = '{}'".format(classname, str(args)))
        arglist = [name for name in self.args if name in args]
        argstring = ",".join(["{}={}".format(name, args[name]) for name in arglist])

        self.loadedmodule._init_complete = False
        (module_params, params_ok) = self.meta.check_parameters(args)
        if params_ok == True:
            if module_params != {}:
                # initialize parameters the old way
                argstring = ",".join(["{}={}".format(name, "'"+str(module_params.get(name,''))+"'") for name in arglist])
            # initialize parameters the new way: Define a dict within the instance
            self.loadedmodule._parameters = module_params
            self.loadedmodule._metadata = self.meta

            # initialize the loaded instance of the module
            self.loadedmodule._init_complete = True   # set to false by module, if an initalization error occurs
            exec("self.loadedmodule.__init__(self._sh{0}{1})".format("," if len(arglist) else "", argstring))
            
        if self.loadedmodule._init_complete == True:
            try:
                code_version = self.loadedmodule.version
            except:
                code_version = None    # if module code without version
            if self.meta.test_version(code_version):
                 logger.info("Modules: Loaded module '{}' (class '{}') v{}: {}".format( name, str(self.loadedmodule.__class__.__name__), self.meta.get_version(), self.meta.get_mlstring('description') ) )
                 self._moduledict[name] = self.loadedmodule
                 self._modules.append(self._moduledict[name])
                 return self.loadedmodule
            else:
                return None
        else:
            logger.error("Modules: Module '{}' initialization failed, module not loaded".format(classpath.split('.')[1]))
            return None

        
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

