Sample Plugin v1.5
==================

This documentation is valid vor SmartHomeNG verseions beyond v1.4.2. Id does not work on v1.4.2
and below.

On this page you find files for writing a new plugin. The plugin consist of a file with Python
code (__init__.py), a metadata fila (plugin.yaml) and a documentation file (README.md). 
A skeleton of the three files is shown below.

A formatted version of the sample README.md can be found here:

.. toctree::
   :maxdepth: 1
   :glob:
   :titlesonly:

   /dev/sample_plugin_1_5/README.md

A raw version of the README.md for copy and paste can be found below the Python source code.


The meta data file:

.. literalinclude:: /dev/sample_plugin_1_5/plugin.yaml
    :caption: plugin.yaml


The source code:

.. literalinclude:: /dev/sample_plugin_1_5/__init__.py
    :caption: __init__.py


The Web interface (template file):

The template file has up to five content blocks to be filled with data of the plugin.

   1. Data for the heading on the right side ``{% block headtable %}``
   2. Tab 1 of the body of the page ``{% block bodytab1 %}``
   3. Tab 2 of the body of the page ``{% block bodytab2 %}``
   4. Tab 3 of the body of the page ``{% block bodytab3 %}``
   5. Tab 4 of the body of the page ``{% block bodytab4 %}``
 
The number of bodytab blocks that is to be displayed is defined by the template statement
``{% set tabcount = 4 %}``
 
.. literalinclude:: /dev/sample_plugin_1_5/webif/templates/index.html
    :tab-width: 4
    :caption: templates/index.html


The multi-language support file:

.. literalinclude:: /dev/sample_plugin_1_5/locale.yaml
    :caption: locale.yaml


The following file outlines the minimum documentation a plugin should have. This README file
should be written in English.

.. literalinclude:: /dev/sample_plugin_1_5/README.md
    :caption: README.md


