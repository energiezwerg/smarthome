Plugin Metadata
===============

Plugins are configured in ``etc/plugin.yaml``. The parameters are described in the README.md
files of the plugins.


A plugin is made up of three files:

- The program code: __init__.py
- The metadata: plugin.yaml
- A short documentation: README.md

All three files reside in a folder within the ``/plugins`` folder. The name of the folder reflects
the name of the plugin.


The **metadata** file is named ``/plugins/<name of the plugin>/plugin.yaml``. It has three main sections:

- ``plugin:`` - Global metadata of the plugin
  The data defined in this section is used to check if the plugin works with the running version of SmartHomeNG, and defines how the plugin is loaded.
  The ``description:`` data is used to generate the plugin documentation pages within this documentation. Since this documentation is in english, the english description is read. If no english description is found, the german description is used.

- ``parameters:`` - Definition of the parameters that can bei used in ``/etc/plugin.yaml`` to configure the plugin
  The data defined in this section is used to check if configured parameters are valid.
  The `description:`` data is going to be used **in the future**: 
  - for generating documentation pages (that way the parameter descriptions will not be needed in the README.md file)
  - for guiding users in a graphical configuration utility
  
- ``item_attributes:`` - **In the future**: Definition of the additional attributes for items, defined by this plugin
  The data defined in this section is used to check if configured item attributes are valid.
  The `description:`` data is going to be used **in the future**: 
  - for generating documentation pages (that way the item attribute descriptions will not be needed in the README.md file)
  - for guiding users in a graphical configuration utility




:Note: After the completion of the implementation of metadata for plugins, the following variables in the Python code of SmartPlugins need not be set anymore. They are read from the global metadata and are automatically set in the instance of the plugin:

    - ALLOW_MULTIINSTANCE
    - PLUGIN_VERSION

    The variable PLUGIN_VERSION should be set (even if it is not needed). If it is set, the version numbers defined in __init__.py and plugin.yaml are compared to ensure they match. If they don't match, an error is logged and the plugin is not loaded.


.. include:: /metadata/plugin_global.rst

.. include:: /metadata/parameters.rst

.. include:: /metadata/item_attributes.rst

