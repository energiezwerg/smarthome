.. include:: /plugins_doc/plugins_system_header.rst

.. toctree::
   :maxdepth: 2
   :glob:
   :titlesonly:
   :hidden:

   /plugins/backend/README.md
   /plugins/blockly/README.md
   /plugins/cli/README.md
   /plugins/database/README.md
   /plugins/datalog/README.md
   /plugins/influxdata/README.md
   /plugins/influxdb/README.md
   /plugins/memlog/README.md
   /plugins/operationlog/README.md
   /plugins/rrd/README.md
   /plugins/rtr/README.md
   /plugins/simulation/README.md
   /plugins/sqlite/README.md
   /plugins/sqlite_visu2_8/README.md
   /plugins/uzsu/README.md
   /plugins/visu_smartvisu/README.md
   /plugins/visu_websocket/README.md



.. table:: 
   :widths: grid

   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | Plugin            | Description                                                                                                                                                 | Maintainer      | Tester          |
   +===================+===========================================================================================================================================+=================+=================+=================+
   | backend           | webinterface for displaying system information and SmartHomeNG backend data                                                                                 | psilo909,       | Sandman60       |
   |                   |                                                                                                                                                             | msinn, bmxp     |                 |
   |                   | - `backend support <https://knx-user-forum.de/forum/supportforen/smarthome-py/959964-support-thread-f&uuml;r-das-backend-plugin>`_                          |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | blockly           | Blockly - graphical editor for logics - Still in development, not for use                                                                                   | msinn, psilo909 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | cli               | Commandline interface for SmartHomeNG - Works with SmartHomeNG v1.4 and up                                                                                  | msinn           | onkelandy,      |
   |                   |                                                                                                                                                             |                 | Sandman60,      |
   |                   |                                                                                                                                                             |                 | ohinckel        |
   |                   | - `cli additional info <https://github.com/smarthomeNG/smarthome/wiki/CLI-Plugin>`_                                                                         |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | database          | Database plugin, **since SmartHomeNG v1.3**                                                                                                                 | ohinckel        | psilo909,       |
   |                   |                                                                                                                                                             |                 | onkelandy,      |
   |                   |                                                                                                                                                             |                 | brandst         |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | datalog           | Loggen von Daten in ein anderes Logfile als das Standard Log                                                                                                | ohinckel        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | influxdata        | Ermöglicht Speicherung von Daten in InfluxData TSDB z.B. zur Erzeugung von Graphen                                                                          | rthill          | brandst         |
   |                   | mit Grafana oder Chronograf (Plugin aus 2016)                                                                                                               |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `influxdata additional info <https://github.com/smarthomeNG/smarthome/wiki/Installation-Influx-Grafana>`_                                                 |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | influxdb          | Ermöglicht Speicherung von Item Werten in einer InfluxData time-series Datenbank                                                                            | Kai Meder       |                 |
   |                   | (Plugin aus 2017)                                                                                                                                           |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `influxdb additional info <https://github.com/smarthomeNG/smarthome/wiki/Installation-Influx-Grafana>`_                                                   |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | memlog            | Speicher Logeinträge im Speicher zur Anzeige in der VISU                                                                                                    | ohinckel        | cmalo           |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | operationlog      | Implementierung seperater Logs                                                                                                                              | ? (JanT112)     | Sandman60,      |
   |                   |                                                                                                                                                             |                 | onkelandy       |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | rrd               | Unterstützung für RRD. Kann nicht zusammen mit dem sqlite Plugin genutzt werden.                                                                            | ? (mknx)        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | rtr               | Raum Temperatur Regler                                                                                                                                      | bmxp (TCr82)    |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | simulation        | Aufnahme und Abspielen von Aktionsreihenfolgen                                                                                                              | ggf. cmalo (?)  | psilo909,       |
   |                   |                                                                                                                                                             |                 | Sandman60,      |
   |                   |                                                                                                                                                             |                 | cmalo           |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | sqlite            | Integration einer SQLite Datenbank - kompatibel mit smartVISU 2.7                                                                                           | ?               |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | sqlite_visu2_8    | Integration einer SQLite Datenbank - zu verwenden für smartVISU 2.8                                                                                         | ?               |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | uzsu              | Universal time switch                                                                                                                                       | cmalo (Niko     | Sandman60,      |
   |                   |                                                                                                                                                             | Will)           | cmalo           |
   |                   | - `uzsu additional info <https://github.com/smarthomeNG/smarthome/wiki/UZSU-%28Universelle-Zeitschaltuhr%29>`_                                              |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | visu_smartvisu    | Support for smartVISU: Automatic generation of pages; widget handling                                                                                       | msinn           | psilo909        |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `visu_smartvisu additional info <https://github.com/smarthomeNG/smarthome/wiki/Visu_Unterstuetzung>`_                                                     |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | visu_websocket    | Support for a websocket protocol (for smartVISU, etc.)                                                                                                      | msinn           | psilo909        |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `visu_websocket additional info <https://github.com/smarthomeNG/smarthome/wiki/Visu_Unterstuetzung>`_                                                     |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+


.. include:: /plugins_doc/plugins_footer.rst
