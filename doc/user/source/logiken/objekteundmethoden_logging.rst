Logging
=======

logger und sh.log
-----------------

Das **logger** Objekt ist nützlich, um Protokollnachrichten zu generieren. Es bietet fünf 
verschiedene Protokollierungsebenen: *debug*, *info*, *warning*, *error* und *critical*. 
Anwendung: **logger.<ebene>(str)** (z.B. **logger.info('42')**. 
Die Lognachrichten werden in einer Logdatei gespeichert (Details sind im Abschnitt
:doc:`Konfiguration/Logging <../konfiguration/konfigurationsdateien_logging>` dieser Dokumentation nachzulesen).

Außerdem sind die letzten 50 Einträge auch unter **sh.log** verfügbar. So ist es möglich, 
über Plugins (z.B. Visu) und Logiken auf die Log-Nachrichten zuzugreifen. 

.. note::

   Die Datum / Uhrzeit Angabe in jedem Protokolleintrag ist bezogen auf die lokale Zeitzone der SamrtHomeNG Installation.

.. code-block:: python
   :caption: Eine einfache Schleife über die Log Einträg

   # a simple loop over the log messages
   for entry in sh.log:
       print(entry)       # remark: if SmartHome.py is run in daemon mode output by 'print' is not visible.


