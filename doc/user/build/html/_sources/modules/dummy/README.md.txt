# Module dummy

This module allows plugins to implement nothing.

> Note: To write a plugin that utilizes this module, you have to be familiar with CherryPy. 


## Requirements

This module is running under SmmartHomeNG versions beyond v1.3. It requires Python >= 3.4 as well as ... . You can install the libraries (python modules) with:

```
(sudo apt-get install ...)
sudo pip3 install ...
```

And please pay attention that the lib(s) are installed for Python3 and not an older Python 2.7 that is probably installed on your system. Be carefull to use `pip3` and nor `pip`.

> Note: This module needs the module handling in SmartHomeNG to be activated. Make sure, that `use_modules`in `etc/smarthome.yaml` is **not** set to False!


## Configuration

### etc/module.yaml


```yaml
# etc/module.yaml
dummy:
    class_name: Dummy
    class_path: modules.dummy

```


## API of module dummy

### Test if module dummy is loaded

`dummy` is a loadlable module. Therefore there is no guarantiee that it is present in every system. Before you can use this module, you have to make sure ist is loaded. You can do it by calling a method of the main smarthome object. Do it like this:

```
self.classname = self.__class__.__name__

try:
    self.mod_dummy = self._sh.get_module('dummy')
except:
    self.mod_dummy = None
    
if self.mod_dummy == None:
    # Do what is necessary if you can't start a web interface
    # for your plugin. For example:
    self.logger.error('{}: Module ''dummy'' not loaded - Abort loading of plugin {0}'.format(self.classname))
    return
```

