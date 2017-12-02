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
   

A plugin consists of a minimum of three files (without user- and developer documentation):

+--------------------------+----------------------------------------------------------------------+
| File                     | Description                                                          |
+==========================+======================================================================+
| **__init__.py**          | The file containing the Python source code                           | 
+--------------------------+----------------------------------------------------------------------+
| **plugin.yaml**          | The file containing the metadata of the plugin                       |               
+--------------------------+----------------------------------------------------------------------+
| **README.md** or         | A basic documentation file (in English language) - The documentation |
| **README.rst**           | can be written in **markdown** or **restructured text** format       |
+--------------------------+----------------------------------------------------------------------+
| **user_doc.rst** or      | Optional, a user documentation file (in German language). It         |
| **user_doc.rst**         | will be included in the navigation of the user documentation.        |
+--------------------------+----------------------------------------------------------------------+
| **developer_doc.rst** or | Optional, a developer documentation file (in English language).      |
| **developer_doc.rst**    | It will be included in the navigation of the developer documentation |
+--------------------------+----------------------------------------------------------------------+
   
If one of the documentation files (**user_doc.\*** or **developer_doc.\***) should include images or 
other assets, create a directory named **assets** in the plugin directory and put the files in that
directory **../<plugin>/assets**. The documentation files (**user_doc.\*** or **developer_doc.\***) 
need not to be referenced in the metadata file **plugin.yaml**

.. important::

   The first Heading of the **user_doc.rst** / **user_doc.md** or **developer_doc.rst** / **developer_doc.md** 
   MUST be the name of the plugin.
   
   It is used as the entry in the navigation bar of the documentation. Choosing an other top level
   header for these files would make the documentations navigation inconsistent.
   

The plugin may have the following subdirectories:

+--------------------------+----------------------------------------------------------------------+
| Directory                | Description                                                          |
+==========================+======================================================================+
| _pv_<version>            | A directory containing a former version of the plugin (the dots of   |
|                          | the version number are replaced by underline. eg: 1.3.5 -> 1_3_5)    |
+--------------------------+----------------------------------------------------------------------+
| assets                   | Containing files user by the **user_doc** or **developer_doc** files |
+--------------------------+----------------------------------------------------------------------+
| webif                    | Containing the files of a webinterface, if the plugin implements one |
+--------------------------+----------------------------------------------------------------------+


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

   plugins/visu_smartvisu/developer_doc.md
   plugins/visu_websocket/developer_doc.md


