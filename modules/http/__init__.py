#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2016-2017  Martin Sinn                       m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG.
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
#  along with SmartHomeNG.  If not, see <http://www.gnu.org/licenses/>.
#########################################################################


import logging
import os
from collections import OrderedDict

import cherrypy
from jinja2 import Environment, FileSystemLoader

from lib.utils import Utils


class http():

    version = '1.4.2'
    shortname = ''
    longname = 'CherryPy http module for SmartHomeNG'
    
    applications = OrderedDict()
    services = OrderedDict()
    
    _port = None
    _servicesport = None

    
    def __init__(self, sh, port=None, servicesport=None, ip='', showpluginlist='True', showservicelist='False', showtraceback='False', threads=8, starturl=''):
        """
        Initialization Routine for the module
        """
        self.shortname = self.__class__.__name__
        self.logger = logging.getLogger(__name__)
        self._sh = sh
        self.logger.debug("{}: Initializing".format(self.shortname))
        
        self.logger.debug("Module '{}': Parameters = '{}'".format(self.shortname, str(self._parameters)))

        # ------------------------------------------------------------------------
        # Testing parameter values
        #
        if Utils.is_int(port):
            self._port = int(port)
        else:
            self._port = 8383
            if port is not None:
                self.logger.error("Module http: Invalid value '"+str(port)+"' configured for attribute 'port' in module.yaml, using '"+str(self._port)+"' instead")

        if Utils.is_int(servicesport):
            self._servicesport = int(servicesport)
        else:
            self._servicesport = 8384
            if servicesport is not None:
                self.logger.error("Module http: Invalid value '"+str(servicesport)+"' configured for attribute 'servicesport' in module.yaml, using '"+str(self._servicesport)+"' instead")

        if ip == '':
            self._ip = self._get_local_ip_address()
        else:
            if not self.is_ip(ip):
                self._ip = self._get_local_ip_address()
                self.logger.error("module http: Invalid value '"+str(ip)+"' configured for attribute ip in module.yaml, using '"+str(self._ip)+"' instead")
            else:
                self._ip = self._get_local_ip_address()
                self.logger.warning("module http: Setting of ip address is not yet supported, using '"+str(self._ip)+"' instead")
        self.logger.debug("Module http: Using local ip address '{0}'".format(self._ip))

        if Utils.is_int(threads):
            self.threads = int(threads)
        else:
            self.threads = 8
            self.logger.error("Module http: Invalid value '"+str(threads)+"' configured for attribute 'thread' in module.yaml, using '"+str(self.threads)+"' instead")

        self._basic_auth = False

        self._showpluginlist = Utils.to_bool(showpluginlist, default=True)
        self._showservicelist = Utils.to_bool(showservicelist, default=False)
        self._showtraceback = Utils.to_bool(showtraceback, default=False)

        # ------------------------------------------------------------------------
        # Setting up webinterface environment
        #
        self.webif_dir = os.path.dirname(os.path.abspath(__file__)) + '/webif'

        self.logger.info("Module http: ip address = {}, hostname = '{}'".format(self.get_local_ip_address(), self.get_local_hostname()))
        
        self.root = ModuleApp(self, starturl)

        global_conf = {
            'global': {
                'engine.autoreload.on': False,
                'error_page.404': self._error_page,
                'error_page.500': self._error_page,
            },
        }

        # Update the global CherryPy configuration
        cherrypy.config.update(global_conf)

        self._server1 = cherrypy._cpserver.Server()
        self._server1.socket_port=int(self._port)
        self._server1.socket_host=self._ip
        self._server1.thread_pool=self.threads
        self._server1.subscribe()

        if self._port != self._servicesport:
            self._server2 = cherrypy._cpserver.Server()
            self._server2.socket_port=int(self._servicesport)
            self._server2.socket_host=self._ip
            self._server2.thread_pool=self.threads
            self._server2.subscribe()

        self._build_hostmaps()
        
        self.tplenv = Environment(loader=FileSystemLoader(os.path.join( self.webif_dir, 'templates' ) ))

        self.module_conf = {
            '/': {
                'tools.staticdir.root': self.webif_dir,
                'tools.staticdir.debug': True,
                'tools.trailing_slash.on': False,
                'log.screen': False,
                'request.dispatch': cherrypy.dispatch.VirtualHost(**self._hostmap),
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static',
            },
        }

        self.msg_conf = {
            '/': {
                'tools.staticdir.root': self.webif_dir,
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static'
            }
        }

        # mount the application on the '/' base path (Creating an app-instance on the way)
        self.root = ModuleApp(self, starturl)

        self.logger.info("module_conf = {}".format(self.module_conf))
        cherrypy.tree.mount(self.root, '/', config = self.msg_conf)

        # Start the CherryPy HTTP server engine
        cherrypy.engine.start()


        # Register the plugins-list app and the services-list app
        self.logger.info("mount '/plugins' - webif_dir = '{}'".format(self.webif_dir))
        config = {
            '/': {
                'tools.staticdir.root': self.webif_dir,
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static'
            }
        }
    
        if self._showpluginlist == True:
            # Register the plugin-list as a cherrypy app
            self.root.plugins = PluginsApp(self)
            self.register_app(self.root.plugins, 'plugins', config) 
#                              pluginclass='', instance='', description='')

        if self._showservicelist == True:
            # Register the service-list as a cherrypy app
            self.root.services = ServicesApp(self)
            self.register_service(self.root.services, 'services', config) 
#                                  pluginclass='', instance='', description='')

        return


    def _error_page(self, status, message, traceback, version):
        """
        Generate html page for errors

        :param status: error number and description
        :param message: detailed error description
        :param traceback: traceback that lead to the error
        :param version: CherryPy version
        :type status: str
        :type message: str
        :type traceback: str
        :type version: str

        :return: html error page
        :rtype: str
        
        """
        tmpl = self.tplenv.get_template('error_page.html')
        errno = status.split()[0]
        if (self._showtraceback == False) or (errno == '404'):
            traceback = ''
        else:
            traceback = traceback.replace('\n', '<br>&nbsp;&nbsp;')
            traceback = traceback.replace(' ', '&nbsp;&nbsp;')
            traceback = '&nbsp;&nbsp;' + traceback
        return tmpl.render( errno=errno, errmsg=message, traceback=traceback, cpversion=version )
        

    def _get_local_ip_address(self):
        """
        Detemine the local ip address used for the network connection
        
        :return: ip address
        :rtype: str
        """
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.10.10.10", 80))
        return s.getsockname()[0]

 
    def get_local_ip_address(self):
        """
        Returns the local ip address under which the webinterface can be reached
        
        :return: ip address
        :rtype: str
        """
        return self._ip

 
    def get_local_hostname(self):
        """
        Returns the local hostname under which the webinterface can be reached
        
        :return: fully qualified hostname 
        :rtype: str
        """
        import socket
        return socket.gethostbyaddr(self.get_local_ip_address())[0]

 
    def get_local_port(self):
        """
        Returns the local port under which the webinterface can be reached
        
        :return: port number
        :rtype: int
        """
        return self._port

 
    def get_local_servicesport(self):
        """
        Returns the local port under which the webservices can be reached
        
        :return: port number
        :rtype: int
        """
        return self._servicesport

 
    def _build_hostmaps(self):
        """
        Build hostmaps for working with two different ports for web interfaces and services
        """
        self._hostmap = {}
        self._hostmap_webifs = {}
        self._hostmap_services = {}

        self.dom1 = self.get_local_ip_address()+':'+str(self._port)
        self.dom2 = self.get_local_hostname()+':'+str(self._port)
        self.dom3 = self.get_local_ip_address()+':'+str(self._servicesport)
        self.dom4 = self.get_local_hostname()+':'+str(self._servicesport)
        
        self._hostmap = {}
        if self._port != self._servicesport:
            self._hostmap[self.dom1] = '/plugins'
            self._hostmap[self.dom2] = '/plugins'
            self._hostmap[self.dom3] = '/services'
            self._hostmap[self.dom4] = '/services'
        self.logger.info("_hostmap = {}".format(self._hostmap))

        self._hostmap_webifs = {}
        self._hostmap_services = {}
        if self._port != self._servicesport:
            self._hostmap_webifs[self.dom1] = '/msg'
            self._hostmap_webifs[self.dom2] = '/msg'

            self._hostmap_services[self.dom3] = '/msg'
            self._hostmap_services[self.dom4] = '/msg'

            self.logger.info("_hostmap_webifs = {}".format(self._hostmap_webifs))
            self.logger.info("_hostmap_services = {}".format(self._hostmap_services))

        
    def register_app(self, app, pluginname, conf, pluginclass='', instance='', description=''):
        """
        Register an application for CherryPy
        
        This method is called by a plugin to register a webinterface
        
        :param app: Instance of the application object
        :param pluginname: Mount point for the application
        :param conf: Cherrypy application configuration dictionary
        :param plugin: Name of the plugin's class
        :param instance: Instance of the plugin (if multi-instance)
        :param description: Description of the functionallity of the plugin / cherrypy app
        :type app: object
        :type mount: str
        :type conf: dict
        :type plugin: str
        :type istance: str
        :type description: str
        
        """
        pluginname = pluginname.lower()
        mount = '/' + pluginname
        
        if description == '':
           description = 'Webinterface of plugin ' + pluginname
           
        self.logger.info("Module http: Registering application/plugin '{}' from pluginclass '{}' instance '{}'".format( pluginname, pluginclass, instance ) )
        if pluginclass != '':
            self.applications[pluginname] = {'mount': mount, 'Plugin': pluginclass, 'Instance': instance, 'conf': conf, 'Description': description}

        if len(self._hostmap_services) > 0:
            conf['/']['request.dispatch'] = cherrypy.dispatch.VirtualHost(**self._hostmap_services)

        cherrypy.tree.mount(app, mount, config = conf)
        return
        

    def register_service(self, service, servicename, conf, pluginclass='', instance='', description=''):
        """
        Register a service for CherryPy
        
        This method is called by a plugin to register a webinterface
        
        :param service: Instance of the service object
        :param servicename: Mount point for the service
        :param conf: Cherrypy application configuration dictionary
        :param plugin: Name of the plugin's class
        :param instance: Instance of the plugin (if multi-instance)
        :param description: Description of the functionallity of the plugin / cherrypy app
        :type service: object
        :type servicename: str
        :type conf: dict
        :type plugin: str
        :type istance: str
        :type description: str
        
        """
        servicename = servicename.lower()
        mount = '/' + servicename
        
        if description == '':
           description = 'Service of plugin ' + servicename
           
        self.logger.info("Module http: Registering service/plugin '{}' from pluginclass '{}' instance '{}'".format( servicename, pluginclass, instance ) )
        if pluginclass != '':
            self.services[servicename] = {'mount': mount, 'Plugin': pluginclass, 'Instance': instance, 'conf': conf, 'Description': description}

        if len(self._hostmap_webifs) > 0:
            conf['/']['request.dispatch'] = cherrypy.dispatch.VirtualHost(**self._hostmap_webifs)

        cherrypy.tree.mount(service, mount, config = conf)
        return
        

    def start(self):
        """
        If the module needs to startup threads or uses python modules that create threads,
        put thread creation code or the module startup code here.
        
        Otherwise don't enter code here
        """
#        self.logger.debug("{}: Starting up".format(self.shortname))
        pass


    def stop(self):
        """
        If the module has started threads or uses python modules that created threads,
        put cleanup code here.
        
        Otherwise don't enter code here
        """
        self.logger.info("{}: Shutting down".format(self.shortname))   # should be debug
        cherrypy.engine.exit()
        self.logger.debug("{}: CherryPy engine exited".format(self.shortname))

    
class ModuleApp:
    """
    The module http implements it's own webinterface.
    This WebApp implements the entrypoint for the webinterface of the module 'http'.

    Depenting on the configuration of the 'http' module, it redirects to the webinterface of a 
    specified plugin or it redirects to a chooser which allows the start of the differnt webinterfaces of the plugins.
    
    This webinterface is mounted to CherryPy as '/'
    """

    def __init__(self, mod, starturl):
        self.mod = mod
        self.starturl = starturl    
    

    @cherrypy.expose
    def index(self):
        """
        This method is exposed to CherryPy. It implements the page 'index.html'
        """
        self.mod.logger.info("ModuleApp: local.name '{}', local.port '{}'".format(cherrypy.request.local.name, cherrypy.request.local.port))
        if cherrypy.request.local.port == self.mod._port:
            if self.starturl in self.mod.applications.keys():
                result = self.starturl
            else:
                if self.mod._showpluginlist == True:
                    result = 'plugins'
                else:
                    return ''
        else:
            if self.mod._showservicelist == True:
                result = 'services'
            else:
                return ''
        result = '<html><meta http-equiv="refresh" content="0; URL=/' + result + '"></html>'
        return result


class PluginsApp:
    """
    The module 'http' implements it's own webinterface.
    This WebApp implements the chooser which allows the start of the differnt webinterfaces of the plugins.
    
    This webinterface is mounted to CherryPy as '/plugins'
    """

    def __init__(self, mod):
        self.mod = mod
        
    @cherrypy.expose
    def index(self):
        """
        This method is exposed to CherryPy. It implements the page 'plugins/index.html'
        """

        tmpl = self.mod.tplenv.get_template('plugins.html')
        result = tmpl.render( webinterfaces=self.mod.applications )
        return result


class ServicesApp:
    """
    The module 'http' implements it's own webservice.
    This WebApp implements the chooser which allows the start of the differnt services of the plugins.
    
    This webinterface is mounted to CherryPy as '/services'
    """

    def __init__(self, mod):
        self.mod = mod

    @cherrypy.expose
    def index(self):
        """
        This method is exposed to CherryPy. It implements the page 'services/index.html'
        """

        tmpl = self.mod.tplenv.get_template('services.html')
        result = tmpl.render( services=self.mod.services )
        return result

