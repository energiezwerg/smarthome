.. include:: /plugins_doc/plugins_web_header.rst

.. toctree::
   :maxdepth: 2
   :glob:
   :titlesonly:
   :hidden:

   /plugins/alexa/README.md
   /plugins/boxcar/README.md
   /plugins/dwd/README.md
   /plugins/ical/README.md
   /plugins/join/README.md
   /plugins/mail/README.md
   /plugins/mvg_live/README.md
   /plugins/nma/README.md
   /plugins/nokia_health/README.md
   /plugins/odlinfo/README.md
   /plugins/openenergymonitor/README.md
   /plugins/prowl/README.md
   /plugins/pushbullet/README.md
   /plugins/speech/README.md
   /plugins/tankerkoenig/README.md
   /plugins/telegram/README.md
   /plugins/traffic/README.md
   /plugins/webservices/README.md
   /plugins/wettercom/README.md
   /plugins/wunderground/README.md



.. table:: 
   :widths: grid

   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | Plugin            | Description                                                                                                                                                 | Maintainer      | Tester          |
   +===================+===========================================================================================================================================+=================+=================+=================+
   | alexa             | Plugin zur Ansteuerung von SmartHomeNG via Amazon Echo / Alexa, **seit SmartHomeNG                                                                          | hotzen          | psilo909        |
   |                   | v1.3**                                                                                                                                                      |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `alexa support <https://knx-user-forum.de/forum/supportforen/smarthome-py/1021150-amazon-alexa-plugin>`_                                                  |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | boxcar            | Boxcar Notification Service                                                                                                                                 | mode2k          |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | dwd               | Anbindung des FTP Servers des Deutschen Wetterdienstes                                                                                                      | psilo909        | cmalo           |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `dwd additional info <https://github.com/smarthomeNG/smarthome/wiki/DWD>`_                                                                                |                 |                 |
   |                   | - `dwd support <https://knx-user-forum.de/forum/supportforen/smarthome-py/34390-dwd-plugin>`_                                                               |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | ical              | Ermöglicht die Verwendung von Kalendern (ICS)                                                                                                               | cmalo (mknx)    | ohinckel        |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | join              | Ermöglicht die Verwendung der Join API                                                                                                                      | Knx_fan         | psilo909        |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `join support <https://knx-user-forum.de/forum/supportforen/smarthome-py/1113523-neues-plugin-join-tts-sms-phonecall-notification-uvm>`_                  |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | mail              | Integration von E-Mail-Accounts                                                                                                                             | cmalo (mknx)    | psilo909,       |
   |                   |                                                                                                                                                             |                 | onkelandy,      |
   |                   |                                                                                                                                                             |                 | Sandman60       |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | mvg_live          | Abfrage der Abfahrten in Stationen der Münchner Verkehrsbetriebe (MVG)                                                                                      | psilo909        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `mvg_live support <https://knx-user-forum.de/forum/supportforen/smarthome-py/1108867-neues-plugin-mvg_live>`_                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | nma               | Notify My Android Anbindung                                                                                                                                 | ?               |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | nokia_health      | Anbindung der Nokia Health API                                                                                                                              | psilo909        | psilo909        |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `nokia_health support <https://knx-user-forum.de/forum/supportforen/smarthome-py/1141179-nokia-health-plugin>`_                                           |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | odlinfo           | Anbindung der Datenschnittstelle des Bundesamts für Strahlenschutz, **seit                                                                                  | psilo909        | Sandman60       |
   |                   | SmartHomeNG v1.3**                                                                                                                                          |                 |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `odlinfo support <https://knx-user-forum.de/forum/supportforen/smarthome-py/986480-odlinfo-plugin-f&uuml;r-strahlungsdaten>`_                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | openenergymonitor | Upload von Werten zu einer OpenEnergyMonitor Instanz                                                                                                        | ? (ReneHezser)  |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | prowl             | Prowl Unterstützung                                                                                                                                         | Foxi352 (mknx)  |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | pushbullet        | Anbindung des Pushbullet Service                                                                                                                            | ? (lbernau)     | onkelandy,      |
   |                   |                                                                                                                                                             |                 | psilo909,       |
   |                   |                                                                                                                                                             |                 | Sandman60       |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | speech            | Sprach Parser                                                                                                                                               | ?               |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | tankerkoenig      | Benzinpreise                                                                                                                                                | psilo909        | Sandman60       |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `tankerkoenig additional info <https://github.com/smarthomeNG/smarthome/wiki/tankerkoenig>`_                                                              |                 |                 |
   |                   | - `tankerkoenig support <https://knx-user-forum.de/forum/supportforen/smarthome-py/938924-benzinpreis-plugin>`_                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | telegram          | Anbindung des Telegram Service                                                                                                                              | gamade          |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | traffic           | Abfrage der Reisezeit über die Google Directions API                                                                                                        | psilo909        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | webservices       | Implementation of a webservice interface                                                                                                                    | psilo909        |                 |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | wettercom         | Integration von Wetter.COM                                                                                                                                  | ? (Jan N. Klug) | psilo909        |
   |                   |                                                                                                                                                             |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+
   | wunderground      | Get weather data from wunderground.com                                                                                                                      | msinn           |                 |
   |                   |                                                                                                                                                             |                 |                 |
   |                   | - `wunderground support <https://knx-user-forum.de/forum/supportforen/smarthome-py/959964-support-thread-f&uuml;r-das-backend-plugin>`_                     |                 |                 |
   +-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+


.. include:: /plugins_doc/plugins_footer.rst
