#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2011-2013   Marcus Popp                        marcus@popp.mx
# Copyright 2016-       Christian Strassburg 
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

import logging
import threading
import inspect
import os.path		# until Backend is modified

import lib.config
from lib.model.smartplugin import SmartPlugin
from lib.constants import (KEY_CLASS_NAME, KEY_CLASS_PATH, KEY_INSTANCE,YAML_FILE,CONF_FILE)
from lib.utils import Utils

logger = logging.getLogger(__name__)


class Plugins():
    """
    Plugin loader Class. Parses config file and creates a worker thread for each plugin
    
    :param smarthome: Instance of the smarthome master-object
    :param configfile: Basename of the plugin configuration file
    :type samrthome: object
    :type configfile: str

    """
    _plugins = []
    _threads = []
    
    def __init__(self, smarthome, configfile):
        self._sh = smarthome

        try:
            self._debug_plugins = Utils.to_bool(self._sh._debug_plugins)
        except:
            self._debug_plugins = False
        if self._debug_plugins:
            logger.warning('Plugins: Debugging of plugins is enabled. Exceptions are not caught outside of the plugin(s)' )

        # until Backend plugin is modified
        if os.path.isfile(configfile+ YAML_FILE):
            smarthome._plugin_conf = configfile + YAML_FILE
        else:
            smarthome._plugin_conf = configfile + CONF_FILE


        _conf = lib.config.parse_basename(configfile, configtype='plugin')
        if _conf == {}:
            return
            
        for plugin in _conf:
            args = {}
            logger.debug("Section: {0}".format(plugin))
            for arg in _conf[plugin]:
                if arg != KEY_CLASS_NAME and arg != KEY_CLASS_PATH and arg != KEY_INSTANCE:
                    value = _conf[plugin][arg]
                    if isinstance(value, str):
                        value = "'{0}'".format(value)
                    args[arg] = value
            classname = _conf[plugin][KEY_CLASS_NAME]
            classpath = _conf[plugin][KEY_CLASS_PATH]
            
            instance = ''
            if KEY_INSTANCE in _conf[plugin]:
                instance = _conf[plugin][KEY_INSTANCE].strip()
                if instance == 'default': 
                    instance = ''

            # give a warning if either a classic plugin uses the same class twice
            # or if a SmartPlugin uses the same class and instance twice (due to a copy & paste error)
            for p in self._plugins:
                if isinstance(p, SmartPlugin):
                    if p.get_instance_name() == instance:
                        for t in self._threads:
                            if t.plugin == p:
                                if t.plugin.__class__.__name__ == classname:
                                    prev_plugin = t._name
                                    logger.warning("Plugin '{}' uses same class '{}' and instance '{}' as plugin '{}'".format(plugin, p.__class__.__name__, 'default' if instance == '' else instance, prev_plugin))
                                    break

                elif p.__class__.__name__ == classname:
                    logger.warning("Multiple classic plugin instances of class '{}' detected".format(classname))

            try:
                plugin_thread = PluginWrapper(smarthome, plugin, classname, classpath, args, instance)
                try:
                    self._plugins.append(plugin_thread.plugin)
                    self._threads.append(plugin_thread)
                    if instance == '':
                        logger.info("Loaded plugin '{}' from from section '{}'".format( str(classpath).split('.')[1], plugin ) )
                    else:
                        logger.info("Loaded plugin '{}' instance '{}' from from section '{}'".format( str(classpath).split('.')[1], instance, plugin ) )
                except:
                    logger.warning("Plugin '{}' from from section '{}' not loaded".format( str(classpath).split('.')[1], plugin ) )
            except Exception as e:
                logger.exception("Plugin '{}' from section '{}' exception: {}".format(str(classpath).split('.')[1], plugin, e))

        del(_conf)  # clean up

    def __iter__(self):
        for plugin in self._plugins:
            yield plugin

    def start(self):
        logger.info('Start Plugins')
        for plugin in self._threads:
            try:
                instance = plugin.get_implementation().get_instance_name()
                if instance != '':
                    instance = ", instance '"+instance+"'"
                logger.debug("Starting plugin '{}'{}".format(plugin.get_implementation().get_shortname(), instance))
            except:
                logger.debug("Starting classic-plugin from section '{}'".format(plugin.name))
            plugin.start()

    def stop(self):
        logger.info('Stop Plugins')
        for plugin in self._threads:
            try:
                instance = plugin.get_implementation().get_instance_name()
                if instance != '':
                    instance = ", instance '"+instance+"'"
                logger.debug("Stopping plugin '{}'{}".format(plugin.get_implementation().get_shortname(), instance))
            except:
                logger.debug("Stopping classic-plugin from section '{}'".format(plugin.name))
            plugin.stop()
    
    def get_plugin(self, name):
        """
           returns one plugin with given name 
        """
        for thread in self._threads:
            if thread.name == name:
               return thread
        return None


class PluginWrapper(threading.Thread):
    def __init__(self, smarthome, name, classname, classpath, args, instance):
        threading.Thread.__init__(self, name=name)

        try:
            exec("import {0}".format(classpath))
        except Exception as e:
            logger.exception("Plugin '{0}' exception during import of __init__.py: {1}".format(name, e))
            return
            
        #exec("self.plugin = {0}.{1}(smarthome{2})".format(classpath, classname, args))
        exec("self.plugin = {0}.{1}.__new__({0}.{1})".format(classpath, classname))
        setattr(smarthome, self.name, self.plugin)
        if isinstance(self.get_implementation(), SmartPlugin):
            self.get_implementation()._set_shortname(str(classpath).split('.')[1])
            self.get_implementation()._set_classname(classname)
            if instance != '':
                logger.debug("set plugin {0} instance to {1}".format(name, instance ))
                self.get_implementation()._set_instance_name(instance)
            self.get_implementation()._set_sh(smarthome)
            self.get_implementation()._set_plugin_dir( os.path.join( os.path.dirname( os.path.dirname(os.path.abspath(__file__)) ), classpath.replace('.',os.sep) ) )

        exec("self.args = inspect.getargspec({0}.{1}.__init__)[0][1:]".format(classpath, classname))

        arglist = [name for name in self.args if name in args]
        argstring = ",".join(["{}={}".format(name, args[name]) for name in arglist])
        logger.debug("Plugin '{}' using arguments {}".format(str(classpath).split('.')[1], arglist))

        exec("self.plugin.__init__(smarthome{0}{1})".format("," if len(arglist) else "", argstring))

    def run(self):
        """
            starts this plugin instance
        """
        self.plugin.run()

    def stop(self):
        """
            stops this plugin instance
        """
        self.plugin.stop()
    
    def get_name(self):
        """
            returns the name of current plugin instance
            :rtype: str 
        """
        return self.name

    def get_ident(self):
        """
            returns the thread ident of current plugin instance
            :rtype: int
        """
        return self.ident
    
    def get_implementation(self):
        """
            returns the implementation of current plugin instance
            :rtype: object of plugin
        """
        return self.plugin
    