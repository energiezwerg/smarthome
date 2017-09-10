=====================
Development - Plugins
=====================


Information about writing a plugin and getting it included in SmartHomeNG can be found here: 

.. toctree::
   :maxdepth: 1
   :titlesonly:

   /dev/README.md


More info upon the functions and their parameters can be found here. The core which resides in bin/smarthome.py is the heart of the system.
It is accessible via ``sh``-Object. The libraries provide extra functionality like scheduling, database access, connections etc.

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :hidden:
   
   development_plugin/plugin_in5minutes.md
   

A plugin consists of a minimum of three files:

   - A Python source code file ``__init__``
   - A metadata file ``plugin.yaml``
   - A documentation file ``README.md``
   

The plugin code is a class based on the class SmartPlugin. The methods of SmartPlugin are documented here.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   development_plugin/smartplugin


.. toctree::
   :maxdepth: 3
   :titlesonly:
   :hidden:
   
   development_plugin/plugin_metadata
   development_plugin/sampleplugins
   modules_doc/modules_plugins
   modules_doc/modules_readmes
   development_plugin/libraries_plugins



Some very specific info upon some plugins can be found here:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plugins/visu_smartvisu/README_for_developers.md
   plugins/visu_websocket/README_for_visu_developers.md


