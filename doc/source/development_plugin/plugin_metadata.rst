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
- ``item_attributes:`` - n the future: Definition of the additional attributes for items, defined by this plugin

.. include:: /metadata/plugin_global.rst

.. include:: /metadata/parameters.rst

.. include:: /metadata/item_attributes.rst

