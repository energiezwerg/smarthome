Verfügbare Objekte und Methoden
===============================


.. toctree::
   :maxdepth: 3
   :hidden:
   :titlesonly:
   
   objekteundmethoden_logging
   objekteundmethoden_zeit_sonne_mond
   objekteundmethoden_item_methoden
   objekteundmethoden_scheduler
   objekteundmethoden_tools


Neben dem **sh** Objekt, gibt es andere wichtige vordefinierte Objekte:


logic
-----

Dieses Objekt bietet Zugriff auf das aktuelle Logikobjekt. Es ist möglich, während der Laufzeit 
logische Attribute (crontab, cycle, ...) zu ändern. Diese Änderungen gehen nach dem Neustart 
von SmartHomeNG verloren. 

Vordefinierte Attribute/Funktionen des Logikobjekts:

+-------------------+--------------------------------------------------------------------------------------------------------+
| Attribut/Funktion | Erläuterung                                                                                            |
+===================+========================================================================================================+
| logic.name        | mit dem Namen der Logik wie in **../etc/logic.yaml** angegeben.                                        |
+-------------------+--------------------------------------------------------------------------------------------------------+
| logic.last_time() | Diese Funktion liefert den letzten Lauf dieser Logik (vor aktuellen Lauf).                             |
+-------------------+--------------------------------------------------------------------------------------------------------+
| logic.prio        | liest und setzt die aktuelle Priorität dieser Logik.                                                   |
+-------------------+--------------------------------------------------------------------------------------------------------+
| logic.trigger[]   | Ein Python-Dictionary, welches im Folgenden beschreiben wird.                                          |
+-------------------+--------------------------------------------------------------------------------------------------------+
| logic.disable()   | Konfigurierte Logiken sind standardmäßig aktiv und werden entsprechend der Konfiguration ausgeführt.   |
|                   | Diese Methode deaktiviert die Logik, sodass deren Ausführung unterbunden wird.  (Ab SmartHomeNG v1.3)  |
+-------------------+--------------------------------------------------------------------------------------------------------+
| logic.enable()    | Eine bereits deaktivierte Logik kann mit dieser Methode wieder aktiviert werden. (Ab SmartHomeNG v1.3) |
+-------------------+--------------------------------------------------------------------------------------------------------+


trigger
-------

trigger ist ein Python-Dictionary, welches als Laufzeitumgebung einige Informationen über das 
Ereignis liefert, das die Logik ausgelöst hat.

Das Dictionary enthält folgende Informationen: 

- trigger['by']
- trigger['source']
- trigger['dest']
- trigger['value']


Geladene Python Module
----------------------

Im Logik Environment sind diverse Python Module bereits geladen:

- sys
- os
- time
- datetime
- ephem
- random
- Queue
- subprocess


Konfiguration
-------------

Details zur Konfiguration von Logiken finden sich :doc:`hier <../konfiguration/logiken>` .

