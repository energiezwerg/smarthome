=====================
 Installation
=====================

Requirements
============

System
------

-  OS: Any Linux or Unix System should be fine. SmartHomeNG is tested
   on Debian Jessie (amd64) and several flavors of Ubuntu.
   So the specific installation commands may differ from this guide.
-  NTP: A running NTP daemon is recommended:
   ``# apt-get install openntpd``

Python
------

Python 3.2 or higher is mandatory. Python 2.x is not supported
``$ sudo apt-get install python3 python3-dev python3-setuptools``

Calculating of sunset/sunrise in triggers,requires installation of
**ephem** as well.

.. raw:: html

   <pre>
   <code>
   $ sudo easy_install3 pip
   $ sudo pip-3.2 install ephem
   </code>
   </pre>

User
~~~~

A dedicated user for SmartHomeNG could be created with:

.. raw:: html

   <pre>
   <code>
   $ sudo adduser smarthome
   </code>
   </pre>

Installation
============

Stable Release
--------------

Download
~~~~~~~~

At
`https://github.com/smarthomeNG/smarthome/releases <https://github.com/smarthomeNG/smarthome/releases>`_
you find the latest release.

Installation of the latest release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <pre>
   <code>
   $ cd /usr/local
   $ sudo tar --owner=smarthome xvzf path-to-tgz/smarthome-X.X.tgz
   </code>
   </pre>

Everything is extracted to /usr/local/smarthome/. It is possible to use
another path.

Development
------------

To install the recent development version of SmartHomeNG for user **smarthome**:

.. raw:: html

   <pre>
   <code>
   $ sudo mkdir -p /usr/local/smarthome
   $ sudo chown -R smarthome /usr/local/smarthome/
   $ cd /usr/local
   $ git clone https://github.com/smarthomeNG/smarthome.git -b develop 
   </code>
   </pre>

To get the latest updates:

.. raw:: html

   <pre>
   <code>
   $ cd /usr/local/smarthome
   $ git pull
   </code>
   </pre>

Structure
=========

Structure of the SmartHomeNG directory, e.g. /usr/local/smarthome/:

-  bin/: contains the core smarthome.py
-  dev/ development files
-  etc/: should contain the basic configuration files (smarthome.conf,
   plugin.conf, logic.conf)
-  examples/: contains some example files for the configuration and the
   visu plugin
-  items/: should contain one or more item configuration files
-  lib/: contains the core libraries of SmartHomeNG
-  logics/: should contain the logic scripts
-  plugins/: contains the available plugins, one subdirectory for each plugin
-  scenes/: scene files
-  tools/: contains little programms helping to maintain and setup SmartHomeNG
-  var/cache/: contains cached item values
-  var/db/: contains the SQLite3 Database
-  var/log/: contains the logfiles
-  var/rrd/: contains the Round Robin Databases

Configuration
=============

`There is a dedicated page for the configuration. <config.html>`_

Plugins
=======

Every `plugin <plugin.html>`_ has it's own installation section.


Running SmartHomeNG
====================

Arguments for running SmartHomeNG

.. raw:: html

   <pre>
   <code>
   $ /usr/local/smarthome/bin/smarthome.py -h
   --help show this help message and exit 
   -v, --verbose verbose (debug output) logging to the logfile
   -d, --debug stay in the foreground with verbose output
   -i, --interactive open an interactive shell with tab completion and with verbose logging to the logfile
   -l, --logics reload all logics
   -s, --stop stop SmartHomeNG
   -q, --quiet reduce logging to the logfile
   -V, --version show SmartHomeNG version
   --start start SmartHomeNG and detach from console (default)
   </code>
   </pre>

