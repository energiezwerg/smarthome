========================
Development - Plugin API
========================

More info upon the functions and their parameters can be found here. The core which resides in bin/smarthome.py is the heart of the system.
It is accessible via ``sh``-Object. The libraries provide extra functionality like scheduling, database access, connections etc.

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :hidden:
   
   development_plugin/plugin_in5minutes.md
   libraries_plugins
   

A plugin is a class based on the class SmartPlugin. The methods of SmartPlugin are documented here.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   /lib/model/smartplugin


.. toctree::
   :maxdepth: 1
   :titlesonly:
   :hidden:
   
   libraries_plugins


Some very specific info upon some plugins can be found here:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plugins/visu_smartvisu/README_for_developers.md
   plugins/visu_websocket/README_for_visu_developers.md
   