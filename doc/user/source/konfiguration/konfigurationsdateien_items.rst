.. index:: Items; Konfigurationsdateien /items/*.yaml
.. index:: Konfigurationsdateien; /items/*.yaml

items/\*.yaml
=============

.. _`item configuration files`:


---------------------------------------------
Item Definitionen im Verzeichnis **../items**
---------------------------------------------

Die Items repräsentieren das Herz der Konfiguration von SmartHomeNG. Auf ein Item kann von jeder
Logik, jedem Plugin und jedem eval-Ausdruck zugegriffen werden.

Im Verzeichnis **../items** kann eine beliebige Anzahl von Konfigurationsdateien erzeugt werden
und jede Konfigurationsdatei kann eine beliebige Anzahl von Item Definitionen enthalten. Das
Verzeichnis enthält yaml Dateien (oder Dateien im alten .conf Format) mit den Definitionen der
Items, die durch SmartHomeNG genutzt werden sollen. Der Name der yaml Datei kann beliebig sein, 
solange die Extension `.yaml` ist.

Weitere Details zur Konfiguration von Items sind :doc:`hier <items>` zu finden.


