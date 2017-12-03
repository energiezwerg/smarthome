#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2011-2014 Marcus Popp                          marcus@popp.mx
# Copyright 2016-     Christian Strassburg            c.strassburg@gmx.de
# Copyright 2016-     Martin Sinn                           m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG.
#  https://github.com/smarthomeNG/smarthome
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

#####################################################################
# Check Python Version
#####################################################################
import sys
if sys.hexversion < 0x03030000:
    print("Sorry your python interpreter ({0}.{1}) is too old. Please update to 3.3 or newer.".format(sys.version_info[0], sys.version_info[1]))
    exit()

#####################################################################
# prevent user root
#####################################################################
import os
if not os.name == 'nt':
    # only check if we are not at windows systems
    if os.getegid() == 0:
        print("SmartHomeNG should not run as root")
        # exit()

#####################################################################
# Import Python Core Modules
#####################################################################
import argparse
import datetime
import gc
import locale
import logging
import logging.handlers
import logging.config
import shutil
import re
import signal
import subprocess
import threading
import time
import traceback
import psutil
#####################################################################
# Base
#####################################################################
BASE = os.path.sep.join(os.path.realpath(__file__).split(os.path.sep)[:-2])
sys.path.insert(0, BASE)
PIDFILE= os.path.join(BASE,'var','run','smarthome.pid')
#####################################################################
# Import 3rd Party Modules
#####################################################################
from dateutil.tz import gettz

#####################################################################
# Import SmartHomeNG Modules
#####################################################################
import lib.config
import lib.connection
import lib.daemon
import lib.item
import lib.log
import lib.logic
import lib.module
import lib.plugin
import lib.scene
import lib.scheduler
import lib.tools
import lib.utils
import lib.orb
import lib.shyaml

from lib.constants import (YAML_FILE, CONF_FILE, DEFAULT_FILE)

#####################################################################
# Globals
#####################################################################
import bin.shngversion

MODE = 'default'
TZ = gettz('UTC')
VERSION = bin.shngversion.get_shng_version()


#####################################################################
# Classes
#####################################################################

class _LogHandler(logging.StreamHandler):
    def __init__(self, log):
        logging.StreamHandler.__init__(self)
        self._log = log

    def emit(self, record):
        timestamp = datetime.datetime.fromtimestamp(record.created, TZ)
        self._log.add([timestamp, record.threadName, record.levelname, record.message])


class SmartHome():
    """
    SmartHome ist the main class of SmartHomeNG. All other objects can be addressed relative to
    the main oject, which is an instance of this class. Mostly it is reffered to as ``sh``, ``_sh`` or ``smarthome``.
    """

    _base_dir = BASE
    base_dir = _base_dir     # for external modules using that var (backend, ...?)
    """
    **base_dir** is deprecated. Use method get_basedir() instead.
    """

    _etc_dir = os.path.join(_base_dir, 'etc')
    _var_dir = os.path.join(_base_dir, 'var')
    _lib_dir = os.path.join(_base_dir,'lib')
    _env_dir = os.path.join(_lib_dir, 'env' + os.path.sep)

    _module_conf_basename = os.path.join(_etc_dir,'module')
    _module_conf = ''	# is filled by module.py while reading the configuration file, needed by Backend plugin

    _plugin_conf_basename = os.path.join(_etc_dir,'plugin')
    _plugin_conf = ''	# is filled by plugin.py while reading the configuration file, needed by Backend plugin

    _env_logic_conf_basename = os.path.join( _env_dir ,'logic')
    _items_dir = os.path.join(_base_dir, 'items'+os.path.sep)
    _logic_conf_basename = os.path.join(_etc_dir, 'logic')
    _logic_dir = os.path.join(_base_dir, 'logics'+os.path.sep)
    _cache_dir = os.path.join(_var_dir,'cache'+os.path.sep)
    _log_conf_basename = os.path.join(_etc_dir,'logging')
    _smarthome_conf_basename = None
    _extern_conf_dir = BASE
    _log_buffer = 50
    __logs = {}
    __event_listeners = {}
    __all_listeners = []
    _use_modules = 'True'
    _modules = []
    _moduledict = {}
    _plugins = []
    __items = []
    __children = []
    __item_dict = {}
    _utctz = TZ
    _logger = logging.getLogger(__name__)
    _default_language = 'de'

    plugin_load_complete = False
    item_load_complete = False
    plugin_start_complete = False
    
    def __init__(self, extern_conf_dir=_base_dir):
        # set default timezone to UTC
        self._extern_conf_dir = extern_conf_dir
        global TZ
        self.tz = 'UTC'
        os.environ['TZ'] = self.tz
        self._tzinfo = TZ

        threading.currentThread().name = 'Main'
        self.alive = True
        self.version = VERSION
        self.connections = []

        self._etc_dir = os.path.join(self._extern_conf_dir, 'etc')
        self._items_dir = os.path.join(self._extern_conf_dir, 'items'+os.path.sep)
        self._logic_dir = os.path.join(self._extern_conf_dir, 'logics'+os.path.sep)
        self._smarthome_conf_basename = os.path.join(self._etc_dir,'smarthome')
        self._logic_conf_basename = os.path.join(self._etc_dir, 'logic')
        self._module_conf_basename = os.path.join(self._etc_dir,'module')
        self._plugin_conf_basename = os.path.join(self._etc_dir,'plugin')
        self._log_conf_basename = os.path.join(self._etc_dir,'logging')

        # check config files
        self.checkConfigFiles()

        if MODE == 'unittest':
            return

        # setup logging
        self.initLogging()
        self._logger.info("Using config dir: {}".format(self._extern_conf_dir))

        # Fork process and write pidfile
        if MODE == 'default':
            lib.daemon.daemonize(PIDFILE)

        # Add Signal Handling
        signal.signal(signal.SIGHUP, self.reload_logics)
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        #############################################################
        # Check Time
        while datetime.date.today().isoformat() < '2016-03-16':  # XXX update date
            time.sleep(5)
#            print("Waiting for updated time.")
            self._logger.info("Waiting for updated time.")

        #############################################################
        # Catching Exceptions
        sys.excepthook = self._excepthook

        #############################################################
        # Reading smarthome.yaml

        config = lib.config.parse_basename(self._smarthome_conf_basename, configtype='SmartHomeNG')
        if config != {}:
            for attr in config:
                if not isinstance(config[attr], dict):  # ignore sub items
                    vars(self)['_' + attr] = config[attr]
            del(config)  # clean up
        
        if hasattr(self, '_module_paths'):
            sys.path.extend(self._module_paths if type(self._module_paths) is list else [self._module_paths])

        #############################################################
        # Setting debug level and adding memory handler
        self.initMemLog()

        #############################################################
        # Setting (local) tz if set in smarthome.conf
        if hasattr(self, '_tz'):
            tzinfo = gettz(self._tz)
            if tzinfo is not None:
                TZ = tzinfo
                self.tz = self._tz
                os.environ['TZ'] = self.tz
                self._tzinfo = TZ
            else:
                self._logger.warning("Problem parsing timezone: {}. Using UTC.".format(self._tz))
            del(self._tz, tzinfo)

        self._logger.warning("--------------------   Init SmartHomeNG {0}   --------------------".format(VERSION))
        self._logger.debug("Python {0}".format(sys.version.split()[0]))
        self._starttime = datetime.datetime.now()

        # test if a valid locale is set in the operating system
        try:
            if os.environ['LANG'].find('UTF-8') == -1:
                self._logger.error("Locale for the enviroment is not set to a valid value. Set the LANG environment variable to a value supporting UTF-8")
        except:
            self._logger.error("Locale for the enviroment is not set. Defaulting to en_US.UTF-8")
            os.environ["LANG"] = 'en_US.UTF-8'
            os.environ["LC_ALL"] = 'en_US.UTF-8'
            
        #############################################################
        # Link Tools
        self.tools = lib.tools.Tools()

        #############################################################
        # Link Sun and Moon
        self.sun = False
        self.moon = False
        if lib.orb.ephem is None:
            self._logger.warning("Could not find/use ephem!")
        elif not hasattr(self, '_lon') and hasattr(self, '_lat'):
            self._logger.warning('No latitude/longitude specified => you could not use the sun and moon object.')
        else:
            if not hasattr(self, '_elev'):
                self._elev = None
            self.sun = lib.orb.Orb('sun', self._lon, self._lat, self._elev)
            self.moon = lib.orb.Orb('moon', self._lon, self._lat, self._elev)


    def get_defaultlanguage(self):
        """
        Returns the configured default language of SmartHomeNG
        """
        return self._default_language
        
        
    def set_defaultlanguage(self, language):
        """
        Returns the configured default language of SmartHomeNG
        """
        self._default_language = language
        
        
    def get_basedir(self):
        """
        Function to return the base directory of the running SmartHomeNG installation
        
        :return: Bas directory as an absolute path
        :rtype: str
        """
        return self._base_dir
        
        
    def get_confdir(self):
        """
        Function to return the config directory (that contain 'etc', 'logics' and 'items' subdirectories)
        
        :return: Config directory as an absolute path
        :rtype: str
        """
        return self._extern_conf_dir
        
        
    def getBaseDir(self):
        """
        Function to return the base directory of the running SmartHomeNG installation
        
        **getBaseDir()** is deprecated. Use method get_basedir() instead.

        :return: Bas directory as an absolute path
        :rtype: str
        """
        return self._base_dir
        
        
    def checkConfigFiles(self):
        """
        This function checks if the needed configuration files exist. It checks for CONF and YAML files. 
        If they dont exist, it is checked if a default configuration exist. If so, the default configuration
        is copied to corresponding configuration file.
        
        The check is done for the files that have to exist (with some content) or SmartHomeNG won't start:
        
        - smarthome.yaml / smarthome.conf
        - logging.yaml
        - plugin.yaml / plugin.conf
        - module.yaml / module.conf
        
        """
        configs = ['logging', 'smarthome', 'module', 'plugin']

        for c in configs:
            default = os.path.join(self._base_dir, 'etc', c + YAML_FILE + DEFAULT_FILE)
            conf_basename = os.path.join(self._etc_dir, c)
            if((c == 'logging' and not (os.path.isfile(conf_basename + YAML_FILE))) or
               (c != 'logging' and not (os.path.isfile(conf_basename + YAML_FILE)) and not (os.path.isfile(conf_basename + CONF_FILE)))):
                if os.path.isfile(default):
                    shutil.copy2(default, conf_basename + YAML_FILE)


    def initLogging(self):
        """
        This function initiates the logging for SmartHomeNG.
        """
        
        fo = open(self._log_conf_basename + YAML_FILE, 'r')
        doc = lib.shyaml.yaml_load(self._log_conf_basename + YAML_FILE, False)
        if doc == None:
            print()
            print("ERROR: Invalid logging configuration in file 'logging.yaml'")
            exit(1)
        logging.config.dictConfig(doc)
        fo.close()
        if MODE == 'interactive':  # remove default stream handler
            logging.getLogger().disabled = True
        elif MODE == 'debug':
            logging.getLogger().setLevel(logging.DEBUG)
        elif MODE == 'quiet':
            logging.getLogger().setLevel(logging.WARNING)
#       log_file.doRollover()


    def initMemLog(self):
        """
        This function initializes all needed datastructures to use the (old) memlog plugin
        """
        
        self.log = lib.log.Log(self, 'env.core.log', ['time', 'thread', 'level', 'message'], maxlen=self._log_buffer)
        _logdate = "%Y-%m-%d %H:%M:%S"
        _logformat = "%(asctime)s %(levelname)-8s %(threadName)-12s %(message)s"
        formatter = logging.Formatter(_logformat, _logdate)
        log_mem = _LogHandler(self.log)
        log_mem.setLevel(logging.WARNING)
        log_mem.setFormatter(formatter)
        logging.getLogger('').addHandler(log_mem)


    #################################################################
    # Process Methods
    #################################################################

    def start(self):
        """
        This function starts the threads of the main smarthome object.
        
        The main thread that is beeing started is called ``Main``
        """
        
        threading.currentThread().name = 'Main'

        #############################################################
        # Start Scheduler
        #############################################################
        self.scheduler = lib.scheduler.Scheduler(self)
        self.trigger = self.scheduler.trigger
        self.scheduler.start()

        #############################################################
        # Init Connections
        #############################################################
        self.connections = lib.connection.Connections()

        #############################################################
        # Init and start loadable Modules
        #############################################################
        if not(lib.utils.Utils.to_bool(self._use_modules) == False):
            self._logger.info("Init loadable Modules")
            self._modules = lib.module.Modules(self, configfile=self._module_conf_basename)
            self._modules.start()
        else:
            self._logger.info("Loadable Modules are disabled")

        #############################################################
        # Init Plugins
        #############################################################
        self._logger.info("Init Plugins")
        self._plugins = lib.plugin.Plugins(self, configfile=self._plugin_conf_basename)
        self.plugin_load_complete = True

        #############################################################
        # Init Items
        #############################################################
        self._logger.info("Start initialization of items")
        item_conf = None
        item_conf = lib.config.parse_itemsdir(self._env_dir, item_conf)
        item_conf = lib.config.parse_itemsdir(self._items_dir, item_conf)
        for attr, value in item_conf.items():
            if isinstance(value, dict):
                child_path = attr
                try:
                    child = lib.item.Item(self, self, child_path, value)
                except Exception as e:
                    self._logger.error("Item {}: problem creating: ()".format(child_path, e))
                else:
                    vars(self)[attr] = child
                    self.add_item(child_path, child)
                    self.__children.append(child)
        del(item_conf)  # clean up
        for item in self.return_items():
            item._init_prerun()
        for item in self.return_items():
            item._init_run()
        self.item_count = len(self.__items)
        self._logger.info("Items initialization finished, {} items loaded".format(self.item_count))
        self.item_load_complete = True
        
        #############################################################
        # Init Logics
        #############################################################
        self._logics = lib.logic.Logics(self, self._logic_conf_basename, self._env_logic_conf_basename)

        #############################################################
        # Init Scenes
        #############################################################
        lib.scene.Scenes(self)

        #############################################################
        # Start Connections
        #############################################################
        self.scheduler.add('sh.connections', self.connections.check, cycle=10, offset=0)

        #############################################################
        # Start Plugins
        #############################################################
        self._plugins.start()
        self.plugin_start_complete = True

        #############################################################
        # Execute Maintenance Method
        #############################################################
        self.scheduler.add('sh.garbage_collection', self._maintenance, prio=8, cron=['init', '4 2 * *'], offset=0)

        #############################################################
        # Main Loop
        #############################################################
        while self.alive:
            try:
                self.connections.poll()
            except Exception as e:
                self._logger.exception("Connection polling failed: {}".format(e))

    def stop(self, signum=None, frame=None):
        """
        This function is used to stop SmartHomeNG and all it's threads
        """
        
        self.alive = False
        self._logger.info("stop: Number of Threads: {}".format(threading.activeCount()))

        for item in self.__items:
            self.__item_dict[item]._fading = False
        try:
            self.scheduler.stop()
        except:
            pass

        try:
            self._plugins.stop()
        except:
            pass

        if not(lib.utils.Utils.to_bool(self._use_modules) == False):
            try:
                self._modules.stop()
            except:
                pass
                
        try:
            self.connections.close()
        except:
            pass

        for thread in threading.enumerate():
            if thread.name != 'Main':
                try:
                    thread.join(1)
                except Exception as e:
                    pass
    
        if threading.active_count() > 1:
            header_logged = False
            for thread in threading.enumerate():
                if thread.name != 'Main' and thread.name[0] !=  '_':
                    if not header_logged:
                        self._logger.warning("The following threads have not been terminated propperly by their plugins (please report to the plugin's author):")
                        header_logged = True
                    self._logger.warning("-Thread: {}, still alive".format(thread.name))
            if header_logged:
                self._logger.warning("SmartHomeNG stopped")
        else:
            self._logger.info("SmartHomeNG stopped")

        lib.daemon.remove_pidfile(PIDFILE)

        logging.shutdown()
        exit()


    def list_threads(self, txt):
    
        cp_threads = 0
        http_threads = 0
        for thread in threading.enumerate():
            if thread.name.find("CP Server") == 0:
                cp_threads += 1
            if thread.name.find("HTTPServer") == 0:
                http_threads +=1

        self._logger.info("list_threads: {} - Number of Threads: {} (CP Server={}, HTTPServer={}".format(txt, threading.activeCount(), cp_threads, http_threads))
        for thread in threading.enumerate():
            if thread.name.find("CP Server") != 0 and thread.name.find("HTTPServer") != 0:
                self._logger.info("list_threads: {} - Thread {}".format(txt, thread.name))
        return
        
        
    #################################################################
    # Item Methods
    #################################################################
    def __iter__(self):
        for child in self.__children:
            yield child


    def add_item(self, path, item):
        """
        Function to to add an item to the dictionary of items.
        If the path does not exist, it is created
        
        :param path: Path of the item
        :param item: The item itself
        :type path: str
        :type item: object
        """
        
        if path not in self.__items:
            self.__items.append(path)
        self.__item_dict[path] = item


    def return_item(self, string):
        """
        Function to return the item for a given path
        
        :param string: Path of the item to return
        :type string: str
        
        :return: Item
        :rtype: object
        """
        
        if string in self.__items:
            return self.__item_dict[string]


    def return_items(self):
        """"
        Function to return a list with all items
        
        :return: List of all items
        :rtype: list
        """
        
        for item in self.__items:
            yield self.__item_dict[item]


    def match_items(self, regex):
        """ 
        Function to match items against a regular expresseion
        
        :param regex: Regular expression to match items against
        :type regex: str
        
        :return: List of matching items
        :rtype: list
        """
        
        regex, __, attr = regex.partition(':')
        regex = regex.replace('.', '\.').replace('*', '.*') + '$'
        regex = re.compile(regex)
        attr, __, val = attr.partition('[')
        val = val.rstrip(']')
        if attr != '' and val != '':
            return [self.__item_dict[item] for item in self.__items if regex.match(item) and attr in self.__item_dict[item].conf and ((type(self.__item_dict[item].conf[attr]) in [list,dict] and val in self.__item_dict[item].conf[attr]) or (val == self.__item_dict[item].conf[attr]))]
        elif attr != '':
            return [self.__item_dict[item] for item in self.__items if regex.match(item) and attr in self.__item_dict[item].conf]
        else:
            return [self.__item_dict[item] for item in self.__items if regex.match(item)]


    def find_items(self, conf):
        """"
        Function to find items that match the specified configuration
        
        :param conf: Configuration to look for
        :type conf: str
        
        :return: list of matching items
        :rtype: list
        """
        
        for item in self.__items:
            if conf in self.__item_dict[item].conf:
                yield self.__item_dict[item]


    def find_children(self, parent, conf):
        """
        Function to find children with the specified configuration
        
        :param parent: parent item on which to start the search
        :param conf: Configuration to look for
        :type parent: str
        :type conf: str
        
        :return: list or matching child-items
        :rtype: list
        """
        
        children = []
        for item in parent:
            if conf in item.conf:
                children.append(item)
            children += self.find_children(item, conf)
        return children

    #################################################################
    # Module Methods
    #################################################################
    def return_modules(self):
        """
        Returns a list with the names of all loaded modules

        :return: list of module names
        :rtype: list
        """

#        for module_key in self._modules.key:
#            yield module_key
        l = []
        for module_key in self._moduledict.keys():
            l.append(module_key)
        return l


    def get_module(self, name):
        """
        Returns the module object for the module named by the parameter
        or None, if the named module is not loaded

        :param name: Name of the module to return
        :type name: str
        
        :return: list of module names
        :rtype: object
        """

        return self._moduledict.get(name)

    #################################################################
    # Plugin Methods
    #################################################################
    def return_plugins(self):
        """
        Returns a list with the instances of all loaded plugins

        :return: list of plugin names
        :rtype: list
        """

        for plugin in self._plugins:
            yield plugin

    #################################################################
    # Logic Methods
    #################################################################
    def reload_logics(self, signum=None, frame=None):
        """
        Function to reload all logics

        DEPRECATED - Use Logics.reload_logics() instead
        """
        self._logger.warning("Using deprecated function 'smarthome.reload_logics()', called by {} in class {} - use 'Logics.reload_logics()' instead".format(sys._getframe(1).f_code.co_name, sys._getframe(1).f_locals['self'].__class__.__name__))
        for logic in self._logics:
            self._logics[logic]._generate_bytecode()


    def return_logic(self, name):
        """
        Returns (the object of) one loaded logic with given name 

        DEPRECATED - Use Logics.return_logic() instead
        
        :param name: name of the logic to get
        :type name: str

        :return: object of the logic
        :rtype: object
        """
        self._logger.warning("Using deprecated function 'smarthome.return_logic()', called by {} in class {} - use 'Logics.return_logic()' instead".format(sys._getframe(1).f_code.co_name, sys._getframe(1).f_locals['self'].__class__.__name__))
        return self._logics[name]


    def return_logics(self):
        """
        Returns a list with the names of all loaded logics

        DEPRECATED - Use Logics.return_loaded_logics() instead

        :return: list of logic names
        :rtype: list
        """
        self._logger.warning("Using deprecated function 'smarthome.return_logics()', called by {} in class {} - use 'Logics.return_loaded_logics()' instead".format(sys._getframe(1).f_code.co_name, sys._getframe(1).f_locals['self'].__class__.__name__))
        for logic in self._logics:
            yield logic


    #################################################################
    # Log Methods
    #################################################################
    def add_log(self, name, log):
        """
        Function to add a log to the list of logs (deprecated? -> old logging?)
        
        :param name: Name of log
        :param log: Log object
        :type name: str
        :type log: object
        """
        
        self.__logs[name] = log

    def return_logs(self):
        """
        Function to the list of logs (deprecated? -> old logging?)
        
        :return: List of logs
        :rtype: list
        """
        
        return self.__logs


    #################################################################
    # Event Methods
    #################################################################
    def add_event_listener(self, events, method):
        """
        This Function adds listeners for a list of events. This function is called from
        plugins interfacing with visus (e.g. visu_websocket)
        
        :param events: List of events to add listeners for
        :param method: Method used by the visu-interface
        :type events: list
        :type method: object
        """
        
        for event in events:
            if event in self.__event_listeners:
                self.__event_listeners[event].append(method)
            else:
                self.__event_listeners[event] = [method]
        self.__all_listeners.append(method)


    def return_event_listeners(self, event='all'):
        """
        This function returns the listeners for a specified event.
        
        :param event: Name of the event or 'all' to return all listeners
        :type event: str
        
        :return: List of listeners
        :rtype: list
        """
        
        if event == 'all':
            return self.__all_listeners
        elif event in self.__event_listeners:
            return self.__event_listeners[event]
        else:
            return []


    #################################################################
    # Time Methods
    #################################################################
    def now(self):
        """
        Returns the actual time in a timezone aware format
        
        :return: Actual time for the local timezone
        :rtype: datetime
        """
        
        # tz aware 'localtime'
        return datetime.datetime.now(self._tzinfo)


    def tzinfo(self):
        """
        Returns the info about the actual local timezone
        
        :return: Timezone info
        :rtyye: str
        """

        return self._tzinfo


    def utcnow(self):
        """
        Returns the actual time in GMT
        
        :return: Actual time in GMT
        :rtyye: datetime
        """

        # tz aware utc time
        return datetime.datetime.now(self._utctz)


    def utcinfo(self):
        """
        Returns the info about the GMT timezone
        
        :return: Timezone info
        :rtype: str
        """

        return self._utctz


    def runtime(self):
        """
        Returns the uptime of SmartHomeNG
        
        :return: Uptime in days, hours, minutes and seconds
        :rtype: str
        """

        return datetime.datetime.now() - self._starttime
        

    #################################################################
    # Helper Methods
    #################################################################
    def _maintenance(self):
        self._logger.debug("_maintenace: Started")
        self._garbage_collection()
        references = sum(self._object_refcount().values())
        self._logger.debug("_maintenace: Object references: {}".format(references))

    def _excepthook(self, typ, value, tb):
        mytb = "".join(traceback.format_tb(tb))
        self._logger.error("Unhandled exception: {1}\n{0}\n{2}".format(typ, value, mytb))

    def _garbage_collection(self):
        c = gc.collect()
        self._logger.debug("Garbage collector: collected {0} objects.".format(c))


    # obsolete by utils.
    def string2bool(self, string):
        """
        This function is deprecated. Use ``lib.utils.Utils.to_bool(string)`` instead.
        
        :param string: string to convert
        :type string: str
        
        :return: Parameter converted to bool
        :rtype: bool
        """
        
        try:
            return lib.utils.Utils.to_bool(string)
        except Exception as e:
            return None


    def object_refcount(self):
        """
        Function to return the number of defined objects in SmartHomeNG
        
        :return: Number of objects
        :rtype: int
        """
        
        objects = self._object_refcount()
        objects = [(x[1], x[0]) for x in list(objects.items())]
        objects.sort(reverse=True)
        return objects


    def _object_refcount(self):
        objects = {}
        for module in list(sys.modules.values()):
            for sym in dir(module):
                try:
                    obj = getattr(module, sym)
                    if isinstance(obj, type):
                        objects[obj] = sys.getrefcount(obj)
                except:
                    pass
        return objects


#####################################################################
# Private Methods
#####################################################################

def _reload_logics():
    pid = lib.daemon.read_pidfile(PIDFILE)
    if pid:
        os.kill(pid, signal.SIGHUP)


#####################################################################
# Main
#####################################################################

if __name__ == '__main__':
    try:
        if locale.getdefaultlocale() == (None, None):
            locale.setlocale(locale.LC_ALL, 'C')
        else:
            locale.setlocale(locale.LC_ALL, '')
    except:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    # argument handling
    argparser = argparse.ArgumentParser()
    arggroup = argparser.add_mutually_exclusive_group()
    arggroup.add_argument('-v', '--verbose', help='DEPRECATED use logging.config (verbose (debug output) logging to the logfile)', action='store_true')
    arggroup.add_argument('-d', '--debug', help='stay in the foreground with verbose output', action='store_true')
    arggroup.add_argument('-i', '--interactive', help='open an interactive shell with tab completion and with verbose logging to the logfile', action='store_true')
    arggroup.add_argument('-l', '--logics', help='reload all logics', action='store_true')
    arggroup.add_argument('-s', '--stop', help='stop SmartHomeNG', action='store_true')
    arggroup.add_argument('-q', '--quiet', help='DEPRECATED use logging config (reduce logging to the logfile)', action='store_true')
    arggroup.add_argument('-V', '--version', help='show SmartHomeNG version', action='store_true')
    arggroup.add_argument('--start', help='start SmartHomeNG and detach from console (default)', default=True, action='store_true')
    argparser.add_argument('-c', '--config_dir', help='use external config dir (should contain "etc", "logics" and "items" subdirectories)')
    args = argparser.parse_args()

    extern_conf_dir = BASE
    if args.config_dir is not None:
        extern_conf_dir = os.path.normpath(args.config_dir)

    if args.interactive:
        MODE = 'interactive'
        import code
        import rlcompleter  # noqa
        try:
            import readline
        except:
            print("ERROR: module 'readline' is not installed. Without this module the interactive mode can't be used")
            exit(1)
        import atexit
        # history file
        histfile = os.path.join(os.environ['HOME'], '.history.python')
        try:
            readline.read_history_file(histfile)
        except IOError:
            pass
        atexit.register(readline.write_history_file, histfile)
        readline.parse_and_bind("tab: complete")
        sh = SmartHome(extern_conf_dir=extern_conf_dir)
        _sh_thread = threading.Thread(target=sh.start)
        _sh_thread.start()
        shell = code.InteractiveConsole(locals())
        shell.interact()
        exit(0)
    elif args.logics:
        _reload_logics()
        exit(0)
    elif args.version:
        print("{0}".format(VERSION))
        exit(0)
    elif args.stop:
        lib.daemon.kill(PIDFILE, 30)
        exit(0)
    elif args.debug:
        MODE = 'debug'
    elif args.quiet:
        pass
    elif args.verbose:
        pass

    # check for pid file
    if lib.daemon.check_sh_is_running(PIDFILE):
        print("SmartHomeNG already running with pid {}".format(lib.daemon.read_pidfile(PIDFILE)))
        print("Run 'smarthome.py -s' to stop it.")
        exit()
    if MODE == 'debug':
        lib.daemon.write_pidfile(psutil.Process().pid, PIDFILE)
    # Starting SmartHomeNG
    sh = SmartHome(extern_conf_dir=extern_conf_dir)
    sh.start()
    
