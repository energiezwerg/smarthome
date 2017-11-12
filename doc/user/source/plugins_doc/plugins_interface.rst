.. include:: /plugins_doc/plugins_interface_header.rst

.. toctree::
   :maxdepth: 2
   :glob:
   :titlesonly:
   :hidden:

   /plugins/apcups/README.md
   /plugins/asterisk/README.md
   /plugins/avdevice/README.md
   /plugins/avm/README.md
   /plugins/buderus/README.md
   /plugins/comfoair/README.md
   /plugins/dlms/README.md
   /plugins/drexelundweiss/README.md
   /plugins/easymeter/README.md
   /plugins/ebus/README.md
   /plugins/enigma2/README.md
   /plugins/eta_pu/README.md
   /plugins/gpio/README.md
   /plugins/harmony/README.md
   /plugins/helios/README.md
   /plugins/homematic/README.md
   /plugins/intercom_2n/README.md
   /plugins/kathrein/README.md
   /plugins/kostal/README.md
   /plugins/logo/README.md
   /plugins/luxtronic2/README.md
   /plugins/netio230b/README.md
   /plugins/nuki/README.md
   /plugins/nut/README.md
   /plugins/plex/README.md
   /plugins/pluggit/README.md
   /plugins/roomba/README.md
   /plugins/russound/README.md
   /plugins/sma/README.md
   /plugins/sma_em/README.md
   /plugins/smarttv/README.md
   /plugins/sml/README.md
   /plugins/solarlog/README.md
   /plugins/systemair/README.md
   /plugins/volkszaehler/README.md
   /plugins/vr100/README.md
   /plugins/xbmc/README.md
   /plugins/xiaomi/README.md
   /plugins/yamaha/README.md



.. table:: 
   :widths: grid

   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | Plugin            | Beschreibung                                                                                                                                                | Maintainer      | Tester          |
   +===================+===========================================================================================================================================+=================+=================+=================+
   | apcups            | Unterstützung für smartUPS Geräte der Firma APC                                                                                                             | cmalo           | Sandman60       |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | asterisk          | Ansteuerung einer Asterisk Telefonanlage                                                                                                                    | ? (mknx)        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | avdevice          | Steuerung von diversen AV Geräten über TCP/IP und RS232 Schnittstelle, **seit                                                                               | onkelandy       | Foxi352         |
   |                   | SmartHomeNG v1.3**                                                                                                                                          |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `avdevice Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/1097870-neues-plugin-av-device-f%C3%BCr-yamaha-pioneer-denon-etc>`_    |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | avm               | Ansteuerung von AVM FRITZ!Boxen, WLAN-Repeatern, DECT Steckdosen, etc.                                                                                      | psilo909        | Sandman60,      |
   |                   |                                                                                                                                                             |                 | cmalo           |
   |                   | - `avm Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/934835-avm-plugin>`_                                                        |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | buderus           | Steuerung von Buderus Heizkesseln über ein Logamatic web KM200 Modul (noch in der                                                                           | rthill          |                 |
   |                   | Entwicklung), **seit SmartHomeNG v1.3**                                                                                                                     |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | comfoair          | Unterstützung für Zehnder ComfoAir 350 & 500 KWL                                                                                                            | ? (SvStefan)    | ohinckel        |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `comfoair zusätzliche Infos <https://github.com/smarthomeNG/smarthome/wiki/Comfoair-Plugin>`_                                                             |                 |                 |
   |                   | - `comfoair Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/31291-neues-plugin-comfoair-kwl-wohnrauml&uuml;ftung-zehnder-paul-wern |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | dlms              | Unterstützung für Smartmeter, die DLMS (Device Language Message Specification, IEC                                                                          | bmxp (JuMi2006) |                 |
   |                   | 62056-21) nutzen und OBIS codes liefern                                                                                                                     |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | drexelundweiss    | Unterstützt Drexel & Weiss USB Devices                                                                                                                      | ?               | onkelandy,      |
   |                   |                                                                                                                                                             |                 | brandst         |
   |                   | - `drexelundweiss Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/34582-drexel-weiss-plugin>`_                                     |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | easymeter         | Easymeter Q3D Unterstützung                                                                                                                                 | ?               |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | ebus              | Unterstützt eBus Heizungen (Vailant, Wolf, Kromschroeder)                                                                                                   | ?               | Sandman60       |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | enigma2           | Plugin zur Einbindung von Enigma2 kompatiblen Sat-Receivern mit openwebif                                                                                   | psilo909        | Sandman60,      |
   |                   |                                                                                                                                                             |                 | cmalo           |
   |                   | - `enigma2 Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/943871-enigma2-plugin>`_                                                |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | eta_pu            | Anbindung der REST-Schnittstelle von ETA Heizungen                                                                                                          | ? (Brootux)     | psilo909, ?     |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | gpio              | GPIO Unterstützung für Rasberry Pi, **seit SmartHomeNG v1.3**                                                                                               | onkelandy       | cmalo, ohinckel |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | harmony           | Harmony Hub plugin, **seit SmartHomeNG v1.3**                                                                                                               | pfischi         |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `harmony Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/1046500-harmony-hub-plugin>`_                                           |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | helios            | Helios EC x00 Pro / Vallox SE KWL Plugin (Modellserien bis 2014)                                                                                            | mtiews, Tom-    |                 |
   |                   |                                                                                                                                                             | Bom-badil       |                 |
   |                   | - `helios zusätzliche Infos <https://github.com/Tom-Bom-badil/helios/wiki>`_                                                                                |                 |                 |
   |                   | - `helios Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/40092-erweiterung-helios-vallox-plugin>`_                                |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | homematic         | Steuerung von Buderus Heizkesseln über ein Logamatic web KM200 Modul (noch in der                                                                           | rthill          |                 |
   |                   | Entwicklung)                                                                                                                                                |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | intercom_2n       | Integration von 2N SIP-Türsprechanlagen                                                                                                                     | pfischi         |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `intercom_2n Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/1030539-plugin-2n-intercom>`_                                       |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | kathrein          | Kathrein Receiver                                                                                                                                           | ? (Johannes     |                 |
   |                   |                                                                                                                                                             | Mayr)           |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | kostal            | Anbindung eines KOSTAL-Wechselrichters                                                                                                                      | ohinckel        | ohinckel,       |
   |                   |                                                                                                                                                             |                 | datenschuft     |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | logo              | Ansteuerung einer Siemens LOGO PLC                                                                                                                          | ?               |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | luxtronic2        | Integration von Systemen die eine Luxtronic-Steuerung haben (z.B Heizungen)                                                                                 | ? (2ndsky)      | ohinckel        |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | netio230b         | Unterstützt KOUKAAM NETIO230B Hardware, eine über Ethernet schaltbare 4-fach-                                                                               | ?               |                 |
   |                   | Steckdose                                                                                                                                                   |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | nuki              | Unterstützung für ein Nuki Smart-Lock                                                                                                                       | fuppy, pfischi  |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `nuki Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/1052437-nuki-smartlock-plugin-support-thread>`_                            |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | nut               | Anbindung an eine UPS über den NUT deamon                                                                                                                   | 4d4mu           |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | plex              | Erlaubt das Senden von Notifications an Plex Clients (wie RasPlex), **seit                                                                                  | rthill          |                 |
   |                   | SmartHomeNG v1.3**                                                                                                                                          |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | pluggit           | Anbindung einer KWL Pluggit AP310 über das Modbus Protokoll                                                                                                 | ? (Henning      |                 |
   |                   |                                                                                                                                                             | Behrend /       |                 |
   |                   |                                                                                                                                                             | ratzi82)        |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | roomba            | Anbindung von iRobot Roomba Staubsaugern                                                                                                                    | ? (Mirko        | Sandman60       |
   |                   |                                                                                                                                                             | Hirsch)         |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | russound          | Anbindung von Russound Audio Geräten                                                                                                                        | ?               |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | sma               | Unterstützung für SMA Inverter SunnyBoy 5000TL-21, Sunny Tripower 8000TL-10, Sunny                                                                          | ? (Robert       | psilo909        |
   |                   | Tripower 12000TL-10                                                                                                                                         | Budde)          |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | sma_em            | Auslesen des SMA Energy Meter Netzwerk Multicasts                                                                                                           | psilo909        | psilo909        |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | smarttv           | Anbdindung (Remote Control) von SmartTV Geräten                                                                                                             | ? (2ndsky)      | psilo909        |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | sml               | Auslesen von Stromzählern via SML-Protokoll                                                                                                                 | ohinckel        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | solarlog          | Auslesen der Web-Seite eines SolarLog                                                                                                                       | ? (2ndsky)      |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | systemair         | Unterstützung für Systemair residential air units über Modbus.                                                                                              | pfischi         |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `systemair Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/939623-systemair-modbus-plugin-zentrale-l&uuml;ftungsanlage>`_        |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | volkszaehler      | Auslesen von Energiemessern und Sensoren, die das S0 Protokoll unterstützen                                                                                 | ? (st0ne)       | brandst         |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | vr100             | Anbindung eines Vorwerk Kobold VR100 Staubsaugers. Der Kobold muss mit einem                                                                                | ? (Robert       |                 |
   |                   | Bluetooth Modul ausgerüstet sein                                                                                                                            | Budde)          |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | xbmc              | Anbindung von XBMC v12 (Frodo) oder neuer                                                                                                                   | ggf. cmalo      | onkelandy       |
   |                   |                                                                                                                                                             | (mknx)          |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | xiaomi            | Auslesen von Xiaomi Mi Flora Pflanzensensoren, **seit SmartHomeNG v1.3**                                                                                    | psilo909        | Sandman60       |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `xiaomi Unterstützung <https://knx-user-forum.de/forum/supportforen/smarthome-py/1027133-plugin-xiaomi-mi-plant-flowers-tester-light-monitor>`_           |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | yamaha            | Plugin um Yamaha RX-V und RX-S Receiver zu kontrollieren, **seit SmartHomeNG v1.3**                                                                         | rthill          | Sandman60       |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+


.. include:: /plugins_doc/plugins_footer.rst
