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
- ``parameters:`` - Definition of the parameters that can bei used in ``/etc/plugin.yaml`` to configure the plugin
- ``item_attributes:`` - In the future: Definition of the additional attributes for items, defined by this plugin

:Note: After the completion of the implementation of metadata for plugins, the following variables in the Python code of SmartPlugins need not be set anymore. They are read from the global metadata and are automatically set in the instance of the plugin:

    - ALLOW_MULTIINSTANCE
    - PLUGIN_VERSION

    The variable PLUGIN_VERSION should be set (even if it is not needed). If it is set, the version numbers defined in __init__.py and plugin.yaml are compared to ensure they match. If they don't match, an error is logged and the plugin is not loaded.


.. include:: /metadata/plugin_global.rst

.. include:: /metadata/parameters.rst

.. include:: /metadata/item_attributes.rst

