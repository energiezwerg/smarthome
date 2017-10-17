:tocdepth: 5

###########
SmartHomeNG
###########

SmartHomeNG is a software that serves a basis for home automation.
It interconnects multiple devices using plugins to access their specific interfaces. 

This documentation reflects the current Release |release|.

What can be done?
The door bell switch triggers a sensor that signals is changed state to SmartHomeNG. In turn the TV set is muted and lights are switched on in the hallway. 
Or being absent an email is sent to the home owner to announce a visitor and a picture or the door camera is attached to it.

The main documentation here within the code and all READMEs are kept in English. The Wiki (https://github.com/smarthomeNG/smarthome/wiki) however mainly contains German documents.

If you are a user with a special problem where you will need a document of this wiki in English
please contact the support forum at KNX-User-Forum (https://knx-user-forum.de/forum/supportforen/smarthome-py) or the chat on gitter.im (https://gitter.im/smarthomeNG/smarthome).
Feel free to contribute in any way you want and can.


.. toctree::
   :maxdepth: 4
   :hidden:
   :titlesonly:
   
   requirements.rst
   install


.. toctree::
   :maxdepth: 5
   :hidden:

   config
   items
   logics
   plugins_all


.. toctree::
   :maxdepth: 4
   :hidden:
   :titlesonly:
   
   logging
   tools
   development_plugins
   development_core
   release

