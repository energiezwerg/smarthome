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
import os

import lib.config
#from lib.model.smartplugin import SmartPlugin
from lib.constants import (KEY_CLASS_NAME, KEY_CLASS_PATH, KEY_INSTANCE,YAML_FILE,CONF_FILE)
from lib.utils import Utils
import lib.shyaml as shyaml

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

#        try:
#            self._debug_modules = Utils.to_bool(self._sh._debug_modules)
#        except:
#            self._debug_modules = False
#        if self._debug_modules:
#            logger.warning('Modules: Debugging of modules is enabled. Exceptions are not caught outside of the module(s)' )

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
                if False:  # if self._debug_modules == True:
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
        
        # get arguments defined in __init__ of module's class to self.args
        exec("self.args = inspect.getargspec({0}.{1}.__init__)[0][1:]".format(classpath, classname))

        # get list of argument used names, if they are defined in the module's class
        arglist = [name for name in self.args if name in args]
        argstring = ",".join(["{}={}".format(name, args[name]) for name in arglist])
        logger.debug('_LoadModule: Using arguments {}'.format(arglist))    # ex debug
# -----
        logger.info("Module '{}': args = '{}'".format(classname, str(args)))
        logger.info("Module '{}': argstring = '{}'".format(classname, str(argstring)))
        meta = CheckParameters(self._sh, classname)
        module_params = meta.test(args)
        if module_params != {}:
            argstring = ",".join(["{}={}".format(name, "'"+str(module_params[name])+"'") for name in arglist])
            logger.info("Module '{}': argstring(neu) = '{}'".format(classname, str(argstring)))

        self.loadedmodule._parameters = module_params
     
# -----
        
        exec("self.loadedmodule.__init__(self._sh{0}{1})".format("," if len(arglist) else "", argstring))

        self._moduledict[classname] = self.loadedmodule
        self._modules.append(self._moduledict[classname])
        logger.info("Modules: Loaded module '{}' v{}: {}".format( str(self._moduledict[classname].__class__.__name__), str(self._moduledict[classname].version), str(self._moduledict[classname].longname) ) )
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

# -------------------------------------------------------------------------------------

class CheckParameters():

    def __init__(self, sh, module):
        self._sh = sh
        self._module = module

        basedir = self._sh.getBaseDir()
        filename = os.path.join( self._sh.getBaseDir(), 'modules', self._module, 'module.yaml' )
        self.meta = shyaml.yaml_load(filename, ordered=True)
        self._paramlist = []
        if self.meta != None:
            self.parameters = self.meta.get('parameters')
            if self.parameters != None:
                self._paramlist = list(self.parameters.keys())
#        logger.info("Module '{}' metadata: paramlist = '{}'".format( self._module, str(self._paramlist) ) )

        # Test parameter definitions for validity
        for param in self._paramlist:
            typ = str(self.parameters[param].get('type', 'foo')).lower()
            # to be implemented: timeframe
            if not (typ in ['bool', 'int', 'pint', 'float', 'pfloat', 'str', 'list', 'dict', 'ip', 'mac', 'foo']):
                logger.error("Modules: Invalid definition in metadata file '{}': type '{}' for parameter '{}' -> using type 'foo' instead".format( os.path.join( 'modules', self._module, 'module.yaml' ), typ, param ) )
                self.parameters[param]['type'] = 'foo'

    
    def _strip_quotes(self, string):
        if type(string) is str:
            string = string.strip()
            if len(string) >= 2:
                if string[0] in ['"', "'"]:  # check if string starts with ' or "
                    if string[0] == string[-1]:  # and end with it
                        if string.count(string[0]) == 2:  # if they are the only one
                            string = string[1:-1]  # remove them
        return string


    def get_type(self, param):
        return str(self.parameters[param].get('type', 'foo')).lower()
        
    
    def test_value(self, param, value):
        if param in self._paramlist:
            typ = self.get_type(param)
            if typ == 'bool':
                return (Utils.to_bool(value, default='?') != '?')
            elif typ == 'int':
                return Utils.is_int(value)
            elif typ == 'pint':
                if Utils.is_int(value):
                    return (int(value) >= 0)
                else:
                    return False
            elif typ == 'float':
                return Utils.is_float(value)
            elif typ == 'pfloat':
                if Utils.is_float(value):
                    return (float(value) >= 0.0)
                else:
                    return False
            elif typ == 'str':
                return (type(value) is str)
            elif typ == 'list':
                return (type(value) is list)
            elif typ == 'dict':
                return (type(value) is dict)
            elif typ == 'ip':
                return Utils.is_ip(value)
            elif typ == 'mac':
                return Utils.is_mac(value)
            elif typ == 'foo':
                return True
        return False
    

    def convert_valuetotype(self, param, value):
        if param in self._paramlist:
            typ = self.get_type(param)
            if typ == 'bool':
                return Utils.to_bool(value)
            elif typ in ['int', 'pint']:
                return int(value)
            elif typ in ['float', 'pfloat']:
                return float(value)
            elif typ == 'str':
                return str(value)
            elif typ == 'list':
                return list(value)
            elif typ == 'dict':
                return dict(value)
            elif typ in ['ip', 'mac']:
                return str(value)
            elif typ == 'foo':
                return value
        return False
    

    def test_validity(self, param, value):
        valid_list = self.parameters[param].get('valid_list')
        if (valid_list == None) or (len(valid_list) == 0):
            return value
        else:
            if value in valid_list:
                return value
            else:
                return valid_list[0]


    def get_default_if_none(self, typ):
        if typ == 'bool':
            value = False
        elif typ in ['int', 'pint']:
            value = 0
        elif typ in ['float', 'pfloat']:
            value = 0.0
        elif typ == 'str':
            value = ''
        elif typ == 'ip':
            value = '0.0.0.0'
        elif typ == 'mac':
            value = '00:00:00:00:00:00'
        else:
            value = None
        return value
        
    
    def get_defaultvalue(self, param):
        value = None
        if param in self._paramlist:
            value = self.parameters[param].get('default')
            typ = self.get_type(param)
            if value == None:
                value = self.get_default_if_none(typ)
            if not self.test_value(param, value):
                # Für non-default Prüfung nur Warning
                logger.error("Module '{}': Invalid data for type '{}' in metadata file '{}': default '{}' for parameter '{}' -> using '{}' instead".format( self._module, self.parameters[param].get('type'), os.path.join( 'modules', self._module, 'module.yaml' ), value, param, self.get_default_if_none(typ) ) )
                value = None
            if value == None:
                value = self.get_default_if_none(typ)
            
            orig_value = value
            value = self.test_validity(param, value)
            if value != orig_value:
                # Für non-default Prüfung nur Warning
                logger.error("Invalid default '{}' in metadata file '{}' for parameter '{}' -> using '{}' instead".format( orig_value, os.path.join( 'modules', self._module, 'module.yaml' ), param, value ) )

        return value


    def test(self, args):
        module_params = {}
        if self.meta == None:
            logger.info("No metadata found for module '{}'".format( str(self._module) ) )
            return module_params
        if self.parameters == None:
            logger.info("No parameter definitions in metadata found for module '{}'".format( str(self._module) ) )
            return module_params
            
        module_params = {}
        for param in self._paramlist:
            value = self._strip_quotes(args.get(param))
            if value == None:
                module_params[param] = self.get_defaultvalue(param)
                logger.debug("Module '{}': '{}' not found in /etc/module.yaml, using default value '{}'".format(self._module, param, module_params[param]))
            else:
                if self.test_value(param, value):
                    module_params[param] = self.convert_valuetotype(param, value)
                    logger.debug("Module '{}': Found '{}' with value '{}' in /etc/module.yaml".format(self._module, param, value))
                else:
                    module_params[param] = self.get_defaultvalue(param)
                    logger.error("Module '{}': Found invalid value '{}' for parameter '{}' in /etc/module.yaml, using default value '{}' instead".format(self._module, value, param, str(module_params[param])))

        return module_params
        
    