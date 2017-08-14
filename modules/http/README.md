# Module http

This module allows plugins to implement a web interface. The API is described below. The first plugin to utilize this API is teh backend plugin.

> Note: To write a plugin that utilizes this module, you have to be familiar with CherryPy. 


## Requirements

This module is running under SmmartHomeNG versions beyond v1.3. It requires Python >= 3.4 as well as the lib **cherrypy**. You can install the libraries (python modules) with:

```
(sudo apt-get install python-cherrypy)
sudo pip3 install cherrypy
```

And please pay attention that the lib(s) are installed for Python3 and not an older Python 2.7 that is probably installed on your system. Be carefull to use `pip3` and nor `pip`.

> Note: This module needs the module handling in SmartHomeNG to be activated. Make sure, that `use_modules`in `etc/smarthome.yaml` is **not** set to False!


## Configuration

### etc/module.yaml


```yaml
# etc/module.yaml
http:
    class_name: http
    class_path: modules.http
#    port: '1234'
#    starturl: backend

```

#### port (optional)
The port on which the html interface listens. By default port **`8383`** is used.

####  threads (optional)

Number of worker threads to start by cherrypy (default 8, which may be too much for slow CPUs)

#### starturl (optional)

The name of the plugin that is started when calling url `smarthomeNG.local:8383` without further detailing that url. If you want to startup the **backend** plugin for example: You set `starturl: backend`. That results in a redirect which redirects `smarthomeNG.local:8383` to `smarthomeNG.local:8383/backend`.

if `starturl` is not specified or point to an url that does not exist, a redirect to `smarthomeNG.local:8383/plugins` will take place. It points to a page that lists all plugins that have registered a html interface and allows you to start those interfaces.

> Note: If you have redirected to a specific plugin, you can always get to the page with the list of all plugins that have registered a html interface, by entering the url `smarthomeNG.local:8383/plugins`.


## API of module http

### Test if module http is loaded

`http` is a loadlable module. Therefore there is no guarantiee that it is present in every system. Before you can use this module, you have to make sure ist is loaded. You can do it by calling a method of the main smarthome object. Do it like this:

```
self.classname = self.__class__.__name__

try:
    self.mod_http = self._sh.get_module('http')
except:
    self.mod_http = None
    
if self.mod_http == None:
    # Do what is necessary if you can't start a web interface
    # for your plugin. For example:
    self.logger.error('{}: Module ''http'' not loaded - Abort loading of plugin {0}'.format(self.classname))
    return
```

### Registering a web application/interface

For registering a web interface (or a web application in CherryPy terminology) you first have to define an application configuration for cherrypy.

> Note: Be careful not to include a CherryPy ``global`` configuration.

An application configuration for CherryPy can look like this;

```
app_config = {
    '/': {
        'tools.staticdir.root': current_dir,
        'tools.auth_basic.on': self._basic_auth,
        'tools.auth_basic.realm': 'earth',
        'tools.auth_basic.checkpassword': self.validate_password,
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'static')
    }
}
```

> Note: The `tools.auth_basic`entries in this example are for implementing a basic logon security. If you don`t want/need login security, delete those enties.

For registering a web application/interface you have to call the `register_app` of module `http`:

```
register_app(app_object, 
             appname, 
             app_config, 
             pluginclass, instance,
             description)
```

For example:

```
appname = 'backend'    # Name of the plugin
pluginclass = self.__class__.__name__
instance = self.get_instance_name()

self.mod_http.register_app(Backend(self, self.updates_allowed, language, self.developer_mode, self.pypi_timeout), 
                          appname, 
                          app_config, 
                          pluginclass, instance,
                          description='Administration interface for SmartHomeNG')
```

## Implementing a web interface for you plugin

For details about implementing a web interface (CherryPy application) for your plugin, refer to the CherryPy documentation.

The documentation will tell you how to expose parts of your python code to be availabe through CheryPy`s http-server.
