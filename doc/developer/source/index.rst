:tocdepth: 5

###########
SmartHomeNG
###########

Developer Documentation
=======================

SmartHomeNG is a software that serves a basis for home automation.
It interconnects multiple devices using plugins to access their specific interfaces. 

This documentation reflects the current Release |release|.

What can be done?
The door bell switch triggers a sensor that signals is changed state to SmartHomeNG. In turn 
the TV set is muted and lights are switched on in the hallway. Or being absent an email is sent 
to the home owner to announce a visitor and a picture or the door camera is attached to it.

The main documentation here within the code and all READMEs are kept in English. 
`The SmarthomeNG Wiki <https://github.com/smarthomeNG/smarthome/wiki>`_ however mainly contains German documents.

If you are a user with a special problem where you will need a document of this wiki in English
please contact the `support forum at KNX-User-Forum <https://knx-user-forum.de/forum/supportforen/smarthome-py>`_ 
or the `chat on gitter.im <https://gitter.im/smarthomeNG/smarthome>`_ . Feel free to contribute in 
any way you want and can.

.. note::

   Place **remarks** und **wishes for changes** regarding this developer documentation on 
   `this wiki page <https://github.com/smarthomeNG/smarthome/wiki/Developer-Documentation---Comments>`_ .



.. toctree::
   :maxdepth: 4
   :hidden:
   :titlesonly:
   
   user_doc.rst
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
   genindex
