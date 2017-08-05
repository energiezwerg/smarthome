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

"""
This library implements loading and starting of plugins within SmartHomeNG.


:Warning: This library is part of the core of SmartHomeNG. It **should not be called directly** from plugins!

"""
import logging
import threading
import inspect
import os.path		# until Backend is modified

import lib.config
from lib.model.smartplugin import SmartPlugin
from lib.constants import (KEY_CLASS_NAME, KEY_CLASS_PATH, KEY_INSTANCE,YAML_FILE,CONF_FILE)

logger = logging.getLogger(__name__)


class Plugins():
    """
    Plugin loader class. Parses config file and creates a worker thread for each plugin
    """
    
    _plugins = []
    _threads = []
    
    def __init__(self, smarthome, configfile):

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
            logger.debug("Plugin: {0}".format(plugin))
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
                self._threads.append(plugin_thread)
                self._plugins.append(plugin_thread.plugin)
            except Exception as e:
                logger.exception("Plugin {0} exception: {1}".format(plugin, e))
        del(_conf)  # clean up

    def __iter__(self):
        for plugin in self._plugins:
            yield plugin

    def start(self):
        """
        Start all plugins
        """
        logger.info('Start Plugins')
        for plugin in self._threads:
            logger.debug('Starting {} Plugin'.format(plugin.name))
            plugin.start()

    def stop(self):
        """
        Stop all plugins
        """
        logger.info('Stop Plugins')
        for plugin in self._threads:
            logger.debug('Stopping {} Plugin'.format(plugin.name))
            plugin.stop()
    
    def get_plugin(self, name):
        """
        Returns (the thread of) one plugin with given name 

        :param name: name of the plugin to get
        :type name: str
        
        :return: Thread of the plugin
        :rtype: thread
        """

        for thread in self._threads:
            if thread.name == name:
               return thread
        return None


class PluginWrapper(threading.Thread):
    """
    Plugin wrapper class. Wraps around the loaded plugin code and defines the interface to the plugin.
    """

    def __init__(self, smarthome, name, classname, classpath, args, instance):
        threading.Thread.__init__(self, name=name)

        exec("import {0}".format(classpath))

        #exec("self.plugin = {0}.{1}(smarthome{2})".format(classpath, classname, args))
        exec("self.plugin = {0}.{1}.__new__({0}.{1})".format(classpath, classname))
        setattr(smarthome, self.name, self.plugin)
        if isinstance(self.get_implementation(), SmartPlugin):
            if instance != '':
                logger.debug("set plugin {0} instance to {1}".format(name, instance ))
                self.get_implementation().set_instance_name(instance)
            self.get_implementation().set_sh(smarthome)

        exec("self.args = inspect.getargspec({0}.{1}.__init__)[0][1:]".format(classpath, classname))

        arglist = [name for name in self.args if name in args]
        argstring = ",".join(["{}={}".format(name, args[name]) for name in arglist])
        logger.debug("Using arguments {}".format(arglist))

        exec("self.plugin.__init__(smarthome{0}{1})".format("," if len(arglist) else "", argstring))

    def run(self):
        """
        Starts this plugin instance
        """
        self.plugin.run()

    def stop(self):
        """
        Stops this plugin instance
        """
        self.plugin.stop()
    
    def get_name(self):
        """
        Get the name of the current plugin instance
        
        :return: name of the plugin instance
        :rtype: str 
        """
        return self.name

    def get_ident(self):
        """
        Get the thread identifier of the current plugin instance
        
        :return: thread identifier of current plugin instance
        :rtype: int
        """
        return self.ident
    
    def get_implementation(self):
        """
        Get the implementation of the current plugin instance
        
        :return: implementation of current plugin instance
        :rtype: object of plugin
        """
        return self.plugin
