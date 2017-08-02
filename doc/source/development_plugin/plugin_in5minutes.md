# How to write a Plugin 

Plugins are additions to the SmartHomeNG code that enable additional functions. Plugins are written in Python. To add a plugin you need the plugin code itself and an additional entry in the plugin.conf file. 
A good basis for your own plugin is found in ``dev/sample_plugin/__init__.py``

## Plugin description

### The plugin configuration file
The file plugin.conf is normally located in the subdirectory ``etc`` of SmartHomeNG base directory. It tells SmartHomeNG which plugins to load and where to find them. The following box is a typical entry for your new plugin in that file (old configuration file format.

```
    # etc/plugin.conf
    [myplugin]
        class_name = Myplugin
        class_path = plugins.myplugin
        Parameter1 = 42
```

In the new configuration file format (yaml) the entry looks like this:

```yaml
    # etc/plugin.yaml
    myplugin:
        class_name: Myplugin
        class_path: plugins.myplugin
        Parameter1: 42
```

Let's look at the parameters:

`[myplugin]`

This is the name you give to the plugin. You can choose whatever you like. This is the name of the plugin instance when running SmartHomeNG. If you are running multiple instances of the plugin: This name you distinguish the instances.

`class_name`

The Parameter class_name is of course the class name you give to the new python class in the plugin. It has to match the class name in your python code as described in the following section.

`class_path`

The class_path parameter tells SmartHomeNG where to find the python code of the plugin. The example in the box means that your code is in the file ``plugins/myplugin/__init__.py`` where ``plugins`` is a subdirectory of SmartHomeNG base directory and ``myplugin`` is the directory where all files of the plugin reside. It is also the name of the plugin. The name of the directory has to be lower case.

`Parameter1`

You can add several parameters to the init file that are passed to your plugin during initialization. You can use them to set it up in a proper way.

### The file plugins/myplugin/__init__.py:

The next thing you need is the plugin itself. The main code is in the file …/plugins/myplugin/__init__.py. All plugins have the same structure. There are several functions that need to exist which are called by SmartHomeNG at certain events. For ease of use you can find an empty plugin at ``dev/sample_plugin/__init__.py``.

The name of the directory where the plugin files reside **in has to be in lower case**!

In addition you need to write your own functions for the plugin. Normally those functions are executed by the sharthome.py scheduler. You can program the scheduler to call your functions at specified times or cycles. See chapter “The Scheduler” for more information.

```python
#!/usr/bin/env python3

import logging
from lib.model.smartplugin import SmartPlugin
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class Myplugin(SmartPlugin):

ALLOW_MULTIINSTANCE = False
PLUGIN_VERSION = "a.b.c"

def __init__(self, smarthome, Parameter1= False):
    logger.info('Init MyPlugin')
self._sh=smarthome
    # …

def run(self):
    self.alive = True

def stop(self):
    self.alive = False

def parse_item(self, item):
    if 'my_parameter' in item.conf:
        value = item.conf['my_parameter']
        return self.update_item
    else:
        return None

def parse_logic(self, logic):
    if 'xxx' in logic.conf:
        return self.run_logic

def update_item(self, item, caller=None, source=None, dest=None):
    # …

def run_logic(self, logic, caller=None, source=None, dest=None):
    # …

def bla(self):
    logger.info("bla")
```

First you import certain things you need and get acess to the logger. The logger allows you to log output of your plugin into the smarthome.log file. Then you start you class. The classname has to match the classname parameter in the plugin.conf file. Afterwards you define the required functions.

```python
def __init__(self, smarthome, Parameter1 = False):
```

The function __init__ is called once when SmartHomeNG initializes before the items are loaded. Here you place the code that is needed to initialize you plugin. For example you can open a serial port if you need to communicate to an external device, open files, initialize other variables you need and so on.
The function receives the parameter “smarthome” which gives access to the SmartHomeNG functions. You should save the value in a variable for later use like in the example above.
Other parameter values are received from the file plugin.conf. You can default values for the case that the parameter is not defined in the plugin.conf file. It is a good practice to log your plugin name to the smarthome.log file.

```python
def run(self):
```

The function run is called once when SmartHomeNG starts. Run is executed after all items are loaded. You need to set the variable self.alive=True here.

```python
def stop(self):
```

This is called when SmartHomeNG shuts down. This is the right place to close files and data connections. You need to set the variable self.alive=False here.

```python
def parse_item(self, item):
```

This function is called for each item during startup when SmartHomeNG reads the item.conf file. You can access item parameters and start according action here. For example you have the following item defined in …/items/xxx.conf

```
    # items/xxx.conf
    [upstairs]
        [[lamp]]
            type = bool
            visu_acl = rw
            ivalue = 1
            knx_dpt = 1
            …
```

Using the new configuration file format the configuration looks like this:

```yaml
    # items/xxx.yaml
    upstairs:
        lamp:
            type: bool
            visu_acl: rw
            ivalue: 1
            knx_dpt: 1
            …
```

You can access the parameter ivalue using the following code:

```python
    if 'ivalue' in item.conf:
        ad=item.conf['ivalue']
        return self.update_item
    else:
        return None
```

Here you check if the parameter ivalue is defined in the item. It case it is, the variable ad is set to the parameter value and the function update_item is returned. The function update_item is called each time when the item changes. Each time the lamp is switched on or off by KNX or something else, the function update_item is called.
The paramter values are always string values. Even if you set ivalue=1 in the plugin.conv your code
will receive the string '1'. If you need a number you must convert it on your own.
If the parameter ivalue is not in the item definition, nothing is done and a change of the item does not affect you plugin at all.

```python
def parse_logic(self, logic):    # (version>=1.3)
```

This function called for each logic during startup when SmartHomeNG reads the logic.conf file. You can access logic parameters and start according action here. For example you have the following logic defined in …/etc/logic.conf

```
    etc/logic.conf
    [jalousie_up]
        filename = jalousie-up.py
        crontab = sunrise+20m
        some_plugin_setting = send-notify
```

Using the new configuration fiel format, the configuration looks like this:

```yaml
    etc/logic.yaml
    jalousie_up:
        filename: jalousie-up.py
        crontab: sunrise+20m
        some_plugin_setting: send-notify
```

A plugin can now check the `some_plugin_setting` to find logics where the execution is interesting for it. The following implementation could be used to register a hook for such logics:

```python
    if 'some_plugin_setting' in logic.conf:
        return self.run_logic
    else:
        return None
```

```python
def update_item(self, item, caller=None, source=None, dest=None):
```

This function is called each time an item changes. It receives several parameters:

`caller`

This is a string that identifies the one who changed the item. It’s value is e.g. KNX if the item has been changed by the KNX plugin.

`source`

…

`dest`

…

```python
def run_logic(self, logic, caller=None, source=None, dest=None):    # (version>=1.3)
```

This is like the `update_item()` method except that it is called on logic execution.

Besides those pre-defined functions you can define additional functions that are needed for your plugin.

## SmartHomeNG functions

### The Scheduler

The scheduler is one of the most important functions of SmartHomeNG It is the main time machine that starts functions at specified times. In order for your own functions to be executed you need to propagate them to the scheduler. You do this by calling certain scheduler functions. The scheduler is part of SmartHomeNG, so you need to access it using the variable you defined in the __init__ function. The most important function is add:

#### Add

```python
    self._sh.scheduler.add('name',
                           obj,
                           prio=3,
                           cron=None,
                           cycle=None,
                           value=None,
                           offset=None,
                           next=None)
```

scheduler.add adds an entry to the scheduler. You need to call it with at least three parameters, the name, object and one timing parameter. 

`name=string`

This is a string value which is the name you give to the scheduler entry. You need the name in case you want to remove the entry from the scheduler.

`obj=function`

Obj is a function that has been defined in your plugin. This function will be called by the scheduler. If you want to pass arguments to the function use **kwargs (see description of parameter value below).

`cron`

…

`cycle=int`

Cycle is an integer value of seconds. It tells the scheduler to call your function defined by obj regularly. If you set cycles to 60 your function will be called each 60 seconds as long as long as SmartHomeNG is up.

`value`

The parameter value allows you to pass parameters to the function that is called be the scheduler. You can use a keyworded variable list of parameters. Define you function in the following way:

```python
    _bla(self, **kwargs):
        if 'heinz' in kwargs:
            logger.info("found")
            em = kwargs['heinz']
```

In that case you should call the scheduler with a value list:

```python
    self._sh.scheduler.add('name',
                           self._bla,
                           value={'heinz': bla, 'tom': 10},
                           next=_ndate)
```

> **Warning**: Passing values via the scheduler only works when the scheduler is called with one single trigger time using the “next” parameter. When the scheduler is called with cycle, no parameters are passed to the called function.

`offset=int`

Offset is a value in seconds that works together with cycle. It defines the delay of the first trigger after the plugin is initialized. For example: You set offset to 20 and cycle to 10. The scheduler will trigger the first time 20 seconds after initialization and then each 10 seconds. If you do not define offset or set it to none, SmartHomeNG will choose a random value between 10 and 15 seconds.

`next=dateobject`

Next is a time object that tells the scheduler to trigger once at a specified time. It is a date object that you create e.g. using datetime like here:

```python
    nd=datetime.strptime('Jan 14 2015 8:09PM','%b %d %Y %I:%M%p').replace(tzinfo=self._sh.tzinfo())
```

Important: It is important to include the time zone info in the object. Otherwise the scheduler will crash. Here we use the time zone info from SmartHomeNG.

#### Remove

```python
    self._sh.scheduler.remove(name)
```

The function remove removes an entry from the scheduler.

`Name=string`

Name is a string value with the name of the entry.

## Finding Items

```python
    sh.return_item(item_path)
```

Return_item allows you to find an item by its name.

`item_path=string`

The path of the item as defined in the items configuration file e.g. Floor1.Room1.Lamp1.
The function returns the item object which can be called to modify the value or access other
properties.

### Modifiy Items
An item can be modified by calling it like a function.

```python
item(value, caller)
```

`value`

The value that the item is set to. For a binary item is it True or False. 

`caller=string`

A name you choose the names the one who made the change to the item. This is passed caller argument of the function update_item.

## Summary

![Summary](https://github.com/smarthomeNG/smarthome/wiki/assets/pluginsummary.png)
