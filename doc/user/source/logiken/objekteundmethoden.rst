Verfügbare Objekte und Methoden
===============================

Neben dem **sh** Objekt, gibt es andere wichtige vordefinierte Objekte:


logic
-----

Dieses Objekt bietet Zugriff auf das aktuelle Logikobjekt. Es ist möglich, während der Laufzeit 
logische Attribute (crontab, cycle, ...) zu ändern. Diese Änderungen gehen nach dem Neustart 
von SmartHomeNG verloren. 

Vordefinierte Attribute/Funktionen des Logikobjekts:

- logic.name: mit dem Namen der Logik wie in **../etc/logic.yaml** angegeben
- logic.last_time(): Diese Funktion liefert den letzten Lauf dieser Logik (vor aktuellen Lauf)
- logic.prio: liest und setzt die aktuelle Priorität dieser Logik.
- logic.trigger[]: Ein Python-Dictionary, welches im Folgenden beschreiben wird.
- logic.disable(): Konfigurierte Logiken sind standardmäßig aktiv und werden entsprechend der Konfiguration ausgeführt. Diese Methode deaktiviert die Logik, sodass deren Ausführung unterbunden wird.  (Ab SmartHomeNG v1.3)
- logic.enable(): Eine bereits deaktivierte Logik kann mit dieser Methode wieder aktiviert werden. (Ab SmartHomeNG v1.3)


trigger
-------

trigger ist ein Python-Dictionary, welches als Laufzeitumgebung einige Informationen über das 
Ereignis liefert, das die Logik ausgelöst hat.

Das Dictionary enthält folgende Informationen: 

- trigger['by']
- trigger['source']
- trigger['dest']
- trigger['value']


logger und sh.log
-----------------

Das **logger** Objekt ist nützlich, um Protokollnachrichten zu generieren. Es bietet fünf 
verschiedene Protokollierungsebenen: *debug*, *info*, *warning*, *error* und *critical*. 
Anwendung: **logger.<ebene>(str)** (z.B. logger.info('42')**. 
Die Lognachrichten werden in einer Logdatei gespeichert (Details sind im Abschnitt
:doc:**Konfiguration/Logging** <./logging>' dieser Dokumentation nachzulesen).

Außerdem sind die letzten 50 Einträge auch unter **sh.log** verfügbar. So ist es möglich, 
über Plugins (z.B. Visu) und Logiken auf die Log-Nachrichten zuzugreifen. 

.. note::

Die Datum / Uhrzeit Angabe in jedem Protokolleintrag ist bezogen auf die lokale Zeitzone der SamrtHomeNG Installation.

.. code:: python
   :caption: Eine einfache Schleife über die Log Einträg

   # a simple loop over the log messages
   for entry in sh.log:
       print(entry)       # remark: if SmartHome.py is run in daemon mode output by 'print' is not visible.


sh.now und sh.utcnow
--------------------

Diese beiden Funktionen geben din aktuellen Zeitpunkt in einem datetime-Objekt zurück. **sh.now** verwendet
die lokale Zeitzone, während **sh.utcnow** den Zeitpunkt in GMT zurück liefert.

Es ist möglich, mit verschiedenen Zeitzonen zu rechnen. Die Funktionen **sh.tzinfo()** und 
**sh.utcinfo()** liefern die Namen der jeweiligen Zeitzonen zurück.


sh.sun
------

Dieses Objekt bietet Zugriff auf Parameter der Sonne. Um dieses Objekt zu verwenden, ist es 
erforderlich, den Breitengrad (latitude, z.B. lat: 53.5989481) und den Längegrad (longitude z.B. lon: 10.0459898),
sowie dir Höhe über dem Meeresspiegel (elevation z.B.: elev: 20) in der Datei **../etc/smarthome.yaml** anzugeben.

.. code:: python
   :caption: Beispiele zur Sonnenstandsberechnung

   # sh.sun.pos(offset)   hierbei gibt offset die Differenz in Zeit-Minuten zur aktuellen Zeit an
   azimut, altitude = sh.sun.pos()   # liefert die aktuelle Position der Sonne
   azimut, altitude = sh.sun.pos(30) # liefert die Position, welche die Sonne in 30 Minuten haben wird

   # sh.sun.set(offset)   hierbei gibt offset die Differenz in Grad zum nächsten Sonnenuntergang an
   sunset = sh.sun.set()      # liefert den utc-basierten Zeitpunkt des nächsten Sonnenuntergangs
   sunset_tw = sh.sun.set(-6) # liefert den utc-basierten Zeitpunkt zu dem die Sonne 6° unter dem Horizont
                              # steht. (Ende der bürgerlichen Abenddämmerung)

   # sh.sun.rise(offset)  hierbei gibt offset die Differenz in Grad zum nächsten Sonnenaufganges an
   sunrise = sh.sun.rise()      # liefert den utc-basierten Zeitpunkt des nächsten Sonnenaufganges
   sunrise_tw = sh.sun.rise(-6) # liefert den utc-basierten Zeitpunkt zu dem die Sonne wieder 6° unter 
                              # dem Horizont steht. (Beginn der nächsten bürgerlichen Morgendämmerung)


sh.moon
-------

Neben den drei Funktionen (sh.moon.pos, sh.moon.set, sh.moon.rise) stehen zwei weitere zur Verfügung. 
**sh.moon.light(offset)** liefert einen Wert von 0 bis 100 der beleuchteten Fläche zur aktuellen Zeit + Offset. 
**sh.moon.phase(offset)** gibt die Mondphase als ganze Zahl (0 bis 7) zurück, wobei: 0 = Neumond, 4 = Vollmond, 6 = abnehmender Halbmond


Item Methoden
-------------

Die grundsätzlichen Methoden, die jedes Item hat, sind unter **Items** beschrieben. Darüber
hinaus stehen folgende Methoden zum Handling von Items zur Verfügung:

sh.return_item(path)
^^^^^^^^^^^^^^^^^^^^

Liefert das Item Objekt für den angegebenen Pfad zurück. 

.. code:: python

   sh.return_item('erdgeschoss.flur')


sh.return_items()
^^^^^^^^^^^^^^^^^

Liefert alle Item Objekte zurück. 

.. code:: python

   for item in sh.return_items():     
       logger.info(item.id())


sh.match_items(regex)
^^^^^^^^^^^^^^^^^^^^^

Liefert alle Items zurück, die der Regular Expression, dem Pfad und dem optionalen Attribut entsprechen. 

.. code:: python

   for item in sh.match_items('*.licht'):
       # Selektiere alle Items, deren Pfad mit 'licht' endet
       logger.info(item.id())
       
   for item in sh.match_items('*.licht:special'):
       # Selektiere alle Items, deren Pfad mit 'licht' endet und die das Attribut 'special' haben     
       logger.info(item.id())


sh.find_items(configattribute)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Liefert alle Items zurück, die über das angegebene spezielle Attribut verfügen.

.. code:: python

   for item in sh.find_items('my_special_attribute'):
       logger.info(item.id())


find_children(parentitem, configattribute)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Liefert alle untergeordneten Items zurück, die über das angegebene Konfigurations-Attribut verfügen.


...

<Allgemeine Informationen Erstellung von Logiken>

...

Details zur Konfiguration von Logiken finden sich :doc:`hier <../konfiguration/logiken>` .

