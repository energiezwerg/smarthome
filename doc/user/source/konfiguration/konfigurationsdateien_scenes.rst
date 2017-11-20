scenes/*.yaml
#############


.. _`scene configuration files`:


Szenen Definitionen im Verzeichnis **../scenes**
================================================

Im Verzeichnis **../scenes** kann eine beliebige Anzahl von Konfigurationsdateien für Szenen
erzeugt werden. Jede Konfigurationsdatei kann dabei nur die Konfiguration einer Szene enthalten. 
Das Verzeichnis enthält yaml Dateien (oder Dateien im alten .conf Format) mit den Definitionen 
der Szenen, die durch SmartHomeNG genutzt werden sollen. Der Name der yaml Datei kann beliebig sein, 
solange die Extension `.yaml` ist.

.. note:: 

   Das alte Format der Konfigurationsdateien für Szenen trägt zwar die Extension .conf. Das 
   Dateiformat weicht jedoch vom Dateiformat der anderen .conf Dateien ab.


Weitere Details zur Konfiguration von Items als Szenen sind :doc:`hier <items>` zu finden.



Szenen
------

Für die Verwendung von Szenen ist eine Konfigurationsdatei für jedes 'Szenenobjekt' im Szenenverzeichnis 
erforderlich. Diese Dateien können im alten Szenen-Conf Format (Endung '.conf') oder im 
yaml Format (Endung '.yaml') erstellt werden und müssen als Dateinamen den Item-Path des Items
tragen in dem die Szene definiert ist und über das der Status der Szene gesteuert wird.


altes Konfigurationsformat
--------------------------

Die Szenenkonfigurationsdatei besteht aus Zeilen mit jeweils drei durch Leerzeichen getrennten 
Werten. Jede Zeile bestimmt ein Zielitem(Logik), das verändert werden soll, wenn die Szene einen
bestimmten Status annimmt. Jede Zeile enthält folgende Informationen:

+-----------------+----------------------------------------------------------------------------------------------------------+
| Szenen-Status   | Wert, den das Szenen Item annehmen muss, damit die definierte Zuweisung durchgeführt wird (Wert 0 - 63)  | 
+-----------------+----------------------------------------------------------------------------------------------------------+
| Ziel-Item/Logic | Item-Pfad des Items, dass den definierten Wert zugewiesen bekommen soll (oder Logik, die gestartet /     |
|                 | gestoppt werden soll).                                                                                   |
+-----------------+----------------------------------------------------------------------------------------------------------+
| Wert            | Wert der dem Item zugewiesen werden soll (oder run/stop, falls eine Logik angegeben wurde).              | 
+-----------------+----------------------------------------------------------------------------------------------------------+


.. code::

   # items/example.conf
   [example]
       type = scene
   [otheritem]
       type = num

.. code::

   # scenes/example.conf
   0 otheritem 2
   1 otheritem 20
   1 LogicName run
   2 otheritem 55
   3 LogicName stop


Neuerungen ab SmartHomeNG v1.4
------------------------------

Mit SmartHomeNG v1.4 kommen folgende neue Features hinzu:

- Es werden Konfigurationsdateien im yaml Format unterstützt.
- Für Szenen Stati können im neuen Dateiformat Namen vergeben werden.
- Der Ziel Item-Pfad einer Szenenaktion kann als relative Referenz angegeben werden.
- Anstelle eines Wertes kann auch ein **eval** Ausdruck angegeben werden. In diesem Ausdruck sind auch relative Item Referenzen möglich.
- Für Szenen Aktionen in denen ein absoluter Wert angegeben wird, wird bei Verwendung des neuen Dateiformats das Lernen (analog zu KNX Szenen) unterstützt

