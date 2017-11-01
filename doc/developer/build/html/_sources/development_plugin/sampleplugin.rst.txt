Sample Plugin
=============

On this page you find files for writing a new plugin. The plugin consist of a file with Python
code (__init__.py), a metadata fila (plugin.yaml) and a documentation file (README.md). 
A skeleton of the three files is shown below.

A formatted version of the sample README.md can be found here:

.. toctree::
   :maxdepth: 1
   :glob:
   :titlesonly:

   /dev/sample_plugin/README.md

A raw version of the README.md for copy and paste can be found below the Python source code.


The meta data file:

.. literalinclude:: /dev/sample_plugin/plugin.yaml
    :caption: plugin.yaml


The source code:

.. literalinclude:: /dev/sample_plugin/__init__.py
    :caption: __init__.py


The following file outlines the minimum documentation a plugin should have. This README file
should be written in English.

.. literalinclude:: /dev/sample_plugin/README.md
    :caption: README.md


