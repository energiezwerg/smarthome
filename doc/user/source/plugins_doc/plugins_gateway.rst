.. include:: /plugins_doc/plugins_gateway_header.rst

.. toctree::
   :maxdepth: 2
   :glob:
   :titlesonly:
   :hidden:

   /plugins/artnet/README.md
   /plugins/dashbutton/README.md
   /plugins/dmx/README.md
   /plugins/ecmd/README.md
   /plugins/elro/README.md
   /plugins/enocean/README.md
   /plugins/hue/README.md
   /plugins/iaqstick/README.md
   /plugins/knx/README.md
   /plugins/lirc/README.md
   /plugins/milight/README.md
   /plugins/mlgw/README.md
   /plugins/mpd/README.md
   /plugins/onewire/README.md
   /plugins/raumfeld/README.md
   /plugins/rcswitch/README.md
   /plugins/smawb/README.md
   /plugins/snom/README.md
   /plugins/sonos/README.md
   /plugins/squeezebox/README.md
   /plugins/tellstick/README.md



.. table:: 
   :widths: grid

   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | Plugin            | Beschreibung                                                                                                                                                | Maintainer      | Tester          |
   +===================+===========================================================================================================================================+=================+=================+=================+
   | artnet            | Ansteuerung der meisten USB DMX Adapter                                                                                                                     | mode2k          | ohinckel        |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | dashbutton        | Amazon Dashbutton plugin, **seit SmartHomeNG v1.3**                                                                                                         | pfischi         | psilo909        |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `dashbutton Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/1005266-plugin-amazon-dashbutton>`_                                  |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | dmx               | Unterstützt die DMX Interfaces NanoDMX und DMXking (RS-232)                                                                                                 | ? (mknx)        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | ecmd              | Anbindung eines AVRMicrocontrollers. Das Protokoll gibt Zugriff auf 1wire Sensoren                                                                          | ? (Dirk         |                 |
   |                   | DS1820                                                                                                                                                      | Wallmeier)      |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | elro              | Unterstützt elro-basierter Remote-Control-Switches                                                                                                          | ? (Brootux)     |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | enocean           | Enocean Unterstützung                                                                                                                                       | ? (Robert Budde |                 |
   |                   |                                                                                                                                                             | / aschwith)     |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | hue               | Anbindung einer oder mehrerer Philips HUE Bridges                                                                                                           | mworion, msinn  | Sandman60       |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `hue Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/41379-philips-hue-plugin-neu-v1-0-released>`_                               |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | iaqstick          | Unterstützung für Applied Sensor iAQ Stick und Voltcraft CO-20                                                                                              | ? (Robert Budde |                 |
   |                   |                                                                                                                                                             | )               |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | knx               | Anbindung von KNX Bussystemen via EIBD/KNXD                                                                                                                 | cmalo           | psilo909,       |
   |                   |                                                                                                                                                             |                 | onkelandy,      |
   |                   |                                                                                                                                                             |                 | Sandman60,      |
   |                   |                                                                                                                                                             |                 | brandst         |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | lirc              | Sendet Kommandos an lircd das wiederum IR-Signale an Geräte mit IR-Schnittstelle                                                                            | E3EAT           |                 |
   |                   | versendet                                                                                                                                                   |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | milight           | Unterstützung von MiLight Leuchtmitteln                                                                                                                     | ? (Stephan      |                 |
   |                   |                                                                                                                                                             | Schaade)        |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | mlgw              | Bang & Olufsen Masterlink Gateway                                                                                                                           | msinn           |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | mpd               | Music Player Deamon (MPD) Unterstützung                                                                                                                     | ? (mknx)        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | onewire           | 1-Wire Unterstützung über owserver                                                                                                                          | cmalo (mknx)    |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | raumfeld          | Prototyp einer einfachen Anbindung von Teufel Raumfeld                                                                                                      | ? (hholle)      |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | rcswitch          | Schalten von 433 MHz Funksteckdosen **seit SmartHomeNG v1.3**                                                                                               | dafra           |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `rcswitch Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/39094-logic-und-howto-f&uuml;r-433mhz-steckdosen>`_                    |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | smawb             | Anbindung einer oder mehrerer SMA-Sunny-WebBox(en)                                                                                                          | ? (Brootux)     |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | snom              | Telefonbuch Anbindung für Snom Telefone                                                                                                                     | ? (mknx)        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | sonos             | Anbindung von Sonos Lautsprechern                                                                                                                           | pfischi         | pfischi         |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `sonos zusätzliche Infos <https://knx-user-forum.de/forum/supportforen/smarthome-py/35587-immer-aktuell-sonos-broker-und-sonos-plugin-howto>`_            |                 |                 |
   |                   | - `sonos Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/25151-sonos-anbindung>`_                                                  |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | squeezebox        | Anbindung von Squeezebox Devices. Eine laufender Logitech Media Server wird benötigt.                                                                       | Robert          | onkelandy,      |
   |                   |                                                                                                                                                             |                 | Sandman60,      |
   |                   |                                                                                                                                                             |                 | cmalo, brandst  |
   |                   | - `squeezebox Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/28692-√-neues-plugin-logitech-squeezebox-anregungen>`_               |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | tellstick         | Unterstützung für TellStick und TellStick Duo RF Transmitter                                                                                                | ? (Matthieu     |                 |
   |                   |                                                                                                                                                             | Gaigniere)      |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+


.. include:: /plugins_doc/plugins_footer.rst
