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


class Http():

    version = '1.4.5'
    _shortname = ''
    _longname = 'CherryPy http module for SmartHomeNG'
    
    _applications = OrderedDict()
    _services = OrderedDict()
    
    _port = None
    _servicesport = None

    _hostmap = {}
    _hostmap_webifs = {}
    _hostmap_services = {}

    
    def __init__(self, sh, port=None, servicesport=None, ip='', threads=8, starturl='', 
                       showpluginlist='True', showservicelist='False', showtraceback='False', 
                       user='', password='', hashed_password=''):
        """
        Initialization Routine for the module
        """
        # TO DO: Shortname anders setzen (oder warten bis der Plugin Loader es beim Laden setzt 
        self._shortname = self.__class__.__name__
        self._shortname = self._shortname.lower()
        
        self.logger = logging.getLogger(__name__)
        self._sh = sh
        self.logger.debug("Module '{}': Initializing".format(self._shortname))

        self.logger.debug("Module '{}': Parameters = '{}'".format(self._shortname, str(dict(self._parameters))))


        #================================================================================
        # Checking and converting parameters
        #
        try:
            self._user = self._parameters['user']
            self._password = self._parameters['password']
            self._hashed_password = self._parameters['hashed_password']
            self._realm = 'shng_http_webif'
            self._port = self._parameters['port']

            self._service_user = self._parameters['service_user']
            self._service_password = self._parameters['service_password']
            self._service_hashed_password = self._parameters['service_hashed_password']
            self._service_realm = 'shng_http_service'
            self._servicesport = self._parameters['servicesport']

            self.threads = self._parameters['threads']
            self._showpluginlist = self._parameters['showpluginlist']
            self._showservicelist = self._parameters['showservicelist']
            self._showtraceback = self._parameters['showtraceback']

            self._starturl = self._parameters['starturl']
        except:
            self.logger.critical("Module '{}': Inconsistent module (invalid metadata definition)".format(self._shortname))
            self._init_complete = False
            return
            

        if self._password is not None and self._password != "" and self._hashed_password is not None and self._hashed_password != "":
            self.logger.warning("Module http - Webinterfaces: Both 'password' and 'hashed_password' given. Ignoring 'password' and using 'hashed_password'!")
            self._password = None

        if self._password is not None and self._password != "" and (self._hashed_password is None or self._hashed_password == ""):
            self.logger.warning("Module http - Webinterfaces: Giving plaintext password in configuration is insecure. Consider using 'hashed_password' instead!")
            self._hashed_password = None

        if (self._password is not None and self._password != "") or (self._hashed_password is not None and self._hashed_password != ""):
            self._basic_auth = True
        else:
            self._basic_auth = False


        if self._service_password is not None and self._service_password != "" and self._service_hashed_password is not None and self._service_hashed_password != "":
            self.logger.warning("Module http - Services: Both 'service_password' and 'service_hashed_password' given. Ignoring 'service_password' and using 'service_hashed_password'!")
            self._service_password = None

        if self._service_password is not None and self._service_password != "" and (self._service_hashed_password is None or self._service_hashed_password == ""):
            self.logger.warning("Module http - Services: Giving plaintext service_password in configuration is insecure. Consider using 'service_hashed_password' instead!")
            self._service_hashed_password = None

        if (self._service_password is not None and self._service_password != "") or (self._service_hashed_password is not None and self._service_hashed_password != ""):
            self._service_basic_auth = True
        else:
            self._service_basic_auth = False


        if self._servicesport == 0:
            self._servicesport = self._port

#        self._basic_auth = False
        self._ip = self._get_local_ip_address()

        # ------------------------------------------------------------------------
        # Setting up webinterface environment
        #
        self.webif_dir = os.path.dirname(os.path.abspath(__file__)) + '/webif'

        self.logger.info("Module 'http': ip address = {}, hostname = '{}'".format(self.get_local_ip_address(), self.get_local_hostname()))
        
        self.root = ModuleApp(self, self._starturl)

        global_conf = {
            'global': {
                'engine.autoreload.on': False,
                'error_page.404': self._error_page,
                'error_page.400': self._error_page,
                'error_page.500': self._error_page,
#                'server.socket_host': '127.0.0.1',
#                'server.socket_port': 48080,     
                'server.socket_host': self._ip,
                'server.socket_port': int(self._port),     
            },
        }

        # Update the global CherryPy configuration
        cherrypy.config.update(global_conf)

#        self._server1 = cherrypy._cpserver.Server()
#        self._server1.socket_port=int(self._port)
#        self._server1.socket_host=self._ip
#        self._server1.thread_pool=self.threads
#        self._server1.subscribe()

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
        self.root = ModuleApp(self, self._starturl)

        self.logger.info("module_conf = {}".format(self.module_conf))
        cherrypy.tree.mount(self.root, '/', config = self.msg_conf)

        # Start the CherryPy HTTP server engine
        cherrypy.engine.start()


        # Register the plugins-list app and the services-list app
        self.logger.info("mount '/plugins' - webif_dir = '{}'".format(self.webif_dir))
        config = {
            '/': {
                'tools.auth_basic.on': self._basic_auth,
                'tools.auth_basic.realm': self._realm,
                'tools.auth_basic.checkpassword': self.validate_password,
                'tools.staticdir.root': self.webif_dir,
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static'
            }
        }
        config_services = {
            '/': {
                'tools.auth_basic.on': self._service_basic_auth,
                'tools.auth_basic.realm': self._service_realm,
                'tools.auth_basic.checkpassword': self.validate_service_password,
                'tools.staticdir.root': self.webif_dir,
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static'
            }
        }
        self.logger.info("Module http: config dict: '{}'".format( config ) )
        self.logger.info(" - user '{}', password '{}', hashed_password '{}'".format( self._user, self._password, self._hashed_password ) )
    
        if self._showpluginlist == True:
            # Register the plugin-list as a cherrypy app
            self.root.plugins = _PluginsApp(self)
            self.register_webif(self.root.plugins, 'plugins', config) 
#                               pluginclass='', instance='', description='', webifname='')

        if self._showservicelist == True:
            # Register the service-list as a cherrypy app
            self.root.services = _ServicesApp(self)
            self.register_service(self.root.services, 'services', config) 
#                                  pluginclass='', instance='', description='', servicename='')

        return


    def validate_password(self, realm, username, password):
        """
        """
        if username != self._user or password is None or password == '':
            return False

        if self._hashed_password is not None:
            return Utils.check_hashed_password(password, self._hashed_password)
        elif self._password is not None:
            return password == self._password

        return False


    def validate_service_password(self, realm, username, password):
        """
        """
        if username != self._service_user or password is None or password == '':
            return False

        if self._service_hashed_password is not None:
            return Utils.check_hashed_password(password, self._service_hashed_password)
        elif self._service_password is not None:
            return password == self._service_password

        return False


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
        try:
            return socket.gethostbyaddr(self.get_local_ip_address())[0] # can fail with default /etc/hosts
        except socket.herror:
            try:
                return socket.gethostbyaddr("127.0.1.1")[0]	# in debian based systems hostname is assigned to "127.0.1.1" by default
            except socket.herror:
                try:
                    return socket.gethostbyaddr("127.0.0.1")[0]	# 'localhost' in most cases
                except socket.herror:
                    return "localhost"	# should not happen

 
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
        self.dom3 = self.get_local_hostname().split('.')[0]+'.local'+':'+str(self._port)
        self.dom4 = self.get_local_ip_address()+':'+str(self._servicesport)
        self.dom5 = self.get_local_hostname()+':'+str(self._servicesport)
        self.dom6 = self.get_local_hostname().split('.')[0]+'.local'+':'+str(self._servicesport)
        
        self._hostmap = {}
        if self._port != self._servicesport:
            self._hostmap[self.dom1] = '/plugins'
            self._hostmap[self.dom2] = '/plugins'
            self._hostmap[self.dom3] = '/plugins'
            self._hostmap[self.dom4] = '/services'
            self._hostmap[self.dom5] = '/services'
            self._hostmap[self.dom6] = '/services'
#        self.logger.info("_hostmap = {}".format(self._hostmap))

        self._hostmap_webifs = {}
        self._hostmap_services = {}
        if self._port != self._servicesport:
            self._hostmap_webifs[self.dom1] = '/msg'
            self._hostmap_webifs[self.dom2] = '/msg'
            self._hostmap_webifs[self.dom3] = '/msg'

            self._hostmap_services[self.dom4] = '/msg'
            self._hostmap_services[self.dom5] = '/msg'
            self._hostmap_services[self.dom6] = '/msg'

            self.logger.info("_hostmap_webifs = {}".format(self._hostmap_webifs))
            self.logger.info("_hostmap_services = {}".format(self._hostmap_services))

        
    def get_webifs_for_plugin(self, pluginname):
        """
        Returns infos about the registered webinterfaces for a plugin (specified by shortname)
        
        The information is returned as a list of dicts. One listentry for each registered webinterface.
        The dict for each registered webinterface has the following structure:
        
        webif_dict = {'mount': mount, 
                      'pluginclass': pluginclass, 
                      'webifname': webifname, 
                      'pluginname': pluginname, 
                      'instance': instance, 
                      'conf': conf, 
                      'description': description}

        
        :param pluginname: Shortname of the plugin
        :type pluginname: str
        
        :return: Tnfos about the registered webinterfaces
        :rtype: list of dicts
        """
        result_list = []
        for webif in self._applications.keys():
            if self._applications[webif]['Pluginname'] == pluginname:
                result_list.append(self._applications[webif])
        return result_list
        
    
    def get_services_for_plugin(self, pluginname):
        """
        Returns infos about the registered webservices for a plugin (specified by shortname)
        
        The information is returned as a list of dicts. One listentry for each registered webservice.
        The dict for each registered webinterface has the following structure:
        
        service_dict = {'mount': mount, 
                        'pluginclass': pluginclass, 
                        'servicename': servicename, 
                        'pluginname': pluginname, 
                        'instance': instance, 
                        'conf': conf, 
                        'description': description}


        :param pluginname: Shortname of the plugin
        :type pluginname: str
        
        :return: Tnfos about the registered webservices
        :rtype: list of dicts
        """
        result_list = []
        for service in self._services.keys():
            if self._services[service]['Pluginname'] == pluginname:
                result_list.append(self._services[service])
        return result_list
        
    
    def register_webif(self, app, pluginname, conf, pluginclass='', instance='', description='', webifname='', use_global_basic_auth=True):
        """
        Register an application for CherryPy
        
        This method is called by a plugin to register a webinterface
        
        It should be called like this:

            self.mod_http.register_webif(WebInterface( ... ), 
                               self.get_shortname(), 
                               config, 
                               self.get_classname(), self.get_instance_name(),
                               description,
                               webifname,
                               use_global_basic_auth)


        :param app: Instance of the application object
        :param pluginname: Mount point for the application
        :param conf: Cherrypy application configuration dictionary
        :param pluginclass: Name of the plugin's class
        :param instance: Instance of the plugin (if multi-instance)
        :param description: Description of the functionallity of the webif. If left empty, a generic description will be generated
        :param webifname: Name of the webinterface. If left empty, the pluginname is used
        :param use_global_basic_auth: if True, global basic_auth settings from the http module are used. If False, registering plugin provides its own basic_auth
        :type app: object
        :type pluginname: str
        :type conf: dict
        :type pluginclass: str
        :type istance: str
        :type description: str
        :type webifname: str
        :type: use_global_basic_auth: bool
        
        """
        pluginname = pluginname.lower()
        if webifname == '':
            webifname = pluginname
        mount = '/' + webifname
        if description == '':
           description = 'Webinterface {} of plugin {}'.format(webifname, pluginname)
           
        if use_global_basic_auth:
            conf['/']['tools.auth_basic.on'] = self._basic_auth
            conf['/']['tools.auth_basic.realm'] = self._realm
            conf['/']['tools.auth_basic.checkpassword'] = self.validate_password
            
        self.logger.info("Module http: Registering webinterface '{}' of plugin '{}' from pluginclass '{}' instance '{}'".format( webifname, pluginname, pluginclass, instance ) )
        self.logger.info(" - conf dict: '{}'".format( conf ) )
        if pluginclass != '':
            if instance == '':
                webif_key = webifname
            else:
                webif_key = instance + '@' + webifname
            self._applications[webif_key] = {'Mount': mount, 'Pluginclass': pluginclass, 'Webifname': webifname, 'Pluginname': pluginname, 'Instance': instance, 'Conf': conf, 'Description': description}
            self.logger.info("self._applications['{}'] = {}".format(webif_key, self._applications[webif_key]))
        if len(self._hostmap_services) > 0:
            conf['/']['request.dispatch'] = cherrypy.dispatch.VirtualHost(**self._hostmap_services)

        cherrypy.tree.mount(app, mount, config = conf)
        return
        

    def register_service(self, app, pluginname, conf, pluginclass='', instance='', description='', servicename='', use_global_basic_auth=True):
        """
        Register a service for CherryPy
        
        This method is called by a plugin to register a webservice.
        
        It should be called like this:

            self.mod_http.register_service(Webservice( ... ), 
                                   self.get_shortname(), 
                                   config, 
                                   self.get_classname(), self.get_instance_name(),
                                   description,
                                   servicename,
                                   use_global_basic_auth)


        :param app: Instance of the service object
        :param pluginname: Mount point for the service
        :param conf: Cherrypy application configuration dictionary
        :param pluginclass: Name of the plugin's class
        :param instance: Instance of the plugin (if multi-instance)
        :param description: Description of the functionallity of the webif. If left empty, a generic description will be generated
        :param servicename: Name of the service. I if left empty, the pluginname is used
        :param use_global_basic_auth: if True, global basic_auth settings from the http module are used. If False, registering plugin provides its own basic_auth
        :type app: object
        :type pluginname: str
        :type conf: dict
        :type pluginclass: str
        :type istance: str
        :type description: str
        :type servicename: str
        :type: use_global_basic_auth: bool

        """
        pluginname = pluginname.lower()
        if servicename == '':
            servicename = pluginname
        mount = '/' + servicename
        if description == '':
           description = 'Service {} of plugin {}'.format(servicename, pluginname)

        if use_global_basic_auth:
            conf['/']['tools.auth_basic.on'] = self._service_basic_auth
            conf['/']['tools.auth_basic.realm'] = self._service_realm
            conf['/']['tools.auth_basic.checkpassword'] = self.validate_service_password
            
        self.logger.info("Module http: Registering service '{}' of plugin '{}' from pluginclass '{}' instance '{}'".format( servicename, pluginname, pluginclass, instance ) )
        self.logger.info(" - conf dict: '{}'".format( conf ) )
        if pluginclass != '':
            if instance == '':
                service_key = servicename
            else:
                service_key = instance + '@' + servicename
            self._services[servicename] = {'Mount': mount, 'Pluginclass': pluginclass, 'Servicename': servicename, 'Pluginname': pluginname, 'Instance': instance, 'Conf': conf, 'Description': description}
            self.logger.info("self._services['{}'] = {}".format(service_key, self._services[service_key]))
        if len(self._hostmap_webifs) > 0:
            conf['/']['request.dispatch'] = cherrypy.dispatch.VirtualHost(**self._hostmap_webifs)

        cherrypy.tree.mount(app, mount, config = conf)
        return
        

    def start(self):
        """
        If the module needs to startup threads or uses python modules that create threads,
        put thread creation code or the module startup code here.
        
        Otherwise don't enter code here
        """
#        self.logger.debug("{}: Starting up".format(self._shortname))
        pass


    def stop(self):
        """
        If the module has started threads or uses python modules that created threads,
        put cleanup code here.
        
        Otherwise don't enter code here
        """
        self.logger.info("{}: Shutting down".format(self._shortname))   # should be debug
        cherrypy.engine.exit()
        for thread in threading.enumerate():
            if thread.name == '_TimeoutMonitor':
                thread.join(2)
        self.logger.debug("{}: CherryPy engine exited".format(self._shortname))

    
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
            if self.starturl in self.mod._applications.keys():
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


class _PluginsApp:
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
        result = tmpl.render( webinterfaces=self.mod._applications )
        return result


class _ServicesApp:
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
        result = tmpl.render( services=self.mod._services )
        return result

