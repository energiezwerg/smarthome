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
import cherrypy
from collections import OrderedDict

from lib.utils import Utils


class http():

    version = '1.4.0'
    shortname = ''
    longname = 'CherryPy http module for SmartHomeNG'
    
    applications = {}
    
    
    def __init__(self, sh, port=None, ip='', threads=8, starturl=''):
        """
        Initialization Routine for the module
        """
        self.shortname = self.__class__.__name__
        self.logger = logging.getLogger(__name__)
        self._sh = sh
        self.logger.debug("{}: Initializing".format(self.shortname))
        
        #
        # Testing parameter values
        #
        if Utils.is_int(port):
            self.port = int(port)
        else:
            self.port = 8383
            if port is not None:
                self.logger.error("Module http: Invalid value '"+str(port)+"' configured for attribute 'port' in module.yaml, using '"+str(self.port)+"' instead")

        if ip == '':
            ip = self.get_local_ip_address()
            self.logger.debug("Module http: Using local ip address '{0}'".format(ip))
        else:
            pass
        #    if not self.is_ip(ip):
        #         self.logger.error("module http: Invalid value '"+str(ip)+"' configured for attribute ip in module.yaml, using '"+str('0.0.0.0')+"' instead")
        #         ip = '0.0.0.0'

        if Utils.is_int(threads):
            self.threads = int(threads)
        else:
            self.threads = 8
            self.logger.error("Module http: Invalid value '"+str(threads)+"' configured for attribute 'thread' in module.yaml, using '"+str(self.threads)+"' instead")

        self._basic_auth = False

        current_dir = os.path.dirname(os.path.abspath(__file__))

        #
        # Setting global configuration for CherryPy
        #
        global_conf = {'global': {
            'engine.autoreload.on': False,
            'server.socket_host': ip,
            'server.socket_port': int(self.port),
#            'tools.staticdir.debug': True,
#            'tools.trailing_slash.on': False,
#            'log.screen': False,
            }
        }
        
        application_conf = {
            '/': {
#                'tools.staticfile.root': current_dir,
                'tools.staticdir.root': current_dir,
                'tools.staticdir.debug': True,
                'tools.trailing_slash.on': False,
                'log.screen': False,
            },
#            '/logo_big.png': {
#                'tools.staticfile.on': True,
#                'tools.staticfile.filename': 'static/logo_big.png',
#            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static',
            },
        }
        
        # Update the global CherryPy configuration
        cherrypy.config.update(global_conf)

        # mount the application on the '/' base path (Creating an app-instance on the way)
        cherrypy.tree.mount(ModuleApp(self._sh, self, starturl), '/', config = application_conf)
        cherrypy.tree.mount(PluginsApp(self), '/plugins', config = application_conf)

        # Start the CherryPy HTTP server engine
        cherrypy.engine.start()



# aus dem Backend: --------------------------------------------
#
#         self._server.thread_pool = self.threads
# 


    def get_local_ip_address(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.10.10.10", 80))
        return s.getsockname()[0]

 
    def register_app(self, app, pluginname, conf, pluginclass, instance='', description=''):
        """
        Register an application for CherryPy
        
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
        
        self.applications[pluginname] = {'mount': mount, 'Plugin': pluginclass, 'Instance': instance, 'conf': conf, 'Description': description}

        cherrypy.tree.mount(app, mount, config = conf)
#        cherrypy.engine.start()

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
        self.logger.warning("{}: Shutting down".format(self.shortname))   # should be debug
        cherrypy.engine.exit()
        self.logger.warning("{}: engine exited".format(self.shortname))   # should be debug

    
class ModuleApp:


    def __init__(self, sh, mod, starturl):
        self._sh = sh
        self.mod = mod
        self.starturl = starturl    
    
    #<meta http-equiv="refresh" content="5; URL=http://wiki.selfhtml.org/">

    part1 = '<html><meta http-equiv="refresh" content="0; URL=/'

    part2 = '"></html>'

    @cherrypy.expose
    def index(self):
        result = self.part1
        if self.starturl in self.mod.applications.keys():
            result += self.starturl
        else:
            result += 'plugins'
        result += self.part2
        return result



class PluginsApp:


    def __init__(self, mod):
        self.mod = mod
        
    part1 = """<html>
<head>
    <link rel="stylesheet" href="static/css/font-awesome.min.css" type="text/css"/>
    <link rel="stylesheet" href="static/css/bootstrap.min.css" type="text/css"/>
    <link rel="icon" href="static/img/favicon.ico" type="image/png">
</head>

<body>
<div class="container">
	<br>
	<br>
	<br>
	<br>
	<br>
	<br>
    <div class="row">
        <div align="center" class="col-md-7 col-md-offset-2 panel panel-default">
			<h1 class="margin-base-vertical">
			<img src="static/img/logo_big.png" width="150" height="75">
	    	&nbsp; SmartHomeNG</h1>
	    	
            <p align="center">
                Willkommen bei SmartHomeNG.
            </p>
			<br>
"""

    part2 = """<br>
        <br>
        <br>
        </div><!-- //main content -->
    </div><!-- //row -->
</div> <!-- //container -->
</body>
</html>"""

    @cherrypy.expose
    def index(self):
        result = self.part1
        result += '<h3>Plugins:</h3>'
        applist = list(self.mod.applications.keys())
        applist.sort()
        for app in applist:
            href = app + ' - ' + str(self.mod.applications[app]['Description'])
            href = '<li class="nav-item"><a href="/' + app + '">' + href + '</a></li>'
            result += '<br>' + href
        result += self.part2
        return result

