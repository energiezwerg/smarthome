======================
Development of Plugins
======================


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
   - A basic documentation file ``README.md`` or ``README.rst`` (in English language)
   - Optional, a user documentation file ``user_doc.rst`` or ``user_doc.rst`` (in German language) it will be included in the navigation of the user documentation.
   - Optional, a developer documentation file ``developer_doc.rst`` or ``developer_doc.rst`` (in English language) it will be included in the navigation of the developer documentation
   
If one of the documentation files (``user_doc.*`` or ``developer_doc.*``) should include images or 
other assets, create a directory named ``assets`` in the plugin directory and put the files in that
directory. The documentation files (``user_doc.*`` or ``developer_doc.*``) need not to be referenced 
in the metadata file ``plugin.yaml``


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


