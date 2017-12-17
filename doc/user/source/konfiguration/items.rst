Items
#####

.. Aus dem Wiki übernommen: 11. November 2017 von Seite https://github.com/smarthomeNG/smarthome/wiki/Items


.. toctree::
   :maxdepth: 4
   :hidden:

   initiale_itemkonfiguration.md
   items_standard_attribute.rst
   items_attributes_relative_referenzen.rst
   items_attributes_eval_ausdruecke.rst
   items_funktionen.rst


Überblick
---------

Das einfachste Item ist eines nur mit dem Itemnamen:


.. code-block:: yaml

    # myitem.yaml
    One:

.. code-block:: ini

    # myitem.conf (altes Dateiformat)
    [One]



Für den Itemnamen sollten nur die Zeichen **A-Z** und **a-z** verwendet werden. Ein **Unterstrich** 
oder eine Ziffer **0-9** darf _innerhalb_ des Itemnamens vorkommen. Einen Itemname 
wie `[1w_Bus]`, `[42]` oder `[_Bus]` sind nicht zulässig. Außerdem ist es unzulässig für Itemnamen
reservierte Worte der Programmiersprache Python zu verwenden.

.. attention::

   Bei Items wird zwischen Groß- und Kleinschreibung unterschieden.

Items können Hierarchisch aufgebaut sein, ein Item kann Kinder-Items haben, die ihrerseits wiederum 
Kinder-Items haben können. Zur Kennzeichnung der Hierarchieebene wird im yaml Dateiformat eine
Einrücklung verwendet. 

Im alten .CONF Dateiformat werden eckige Klammern um den Itemnamen gesetzt. Dabei werden Kinder-Items 
aber immer mit ihrem vollen Pfad angesprochen. Beispiel:

.. code-block:: yaml

    # myitem.yaml
    Opa:
       Papa:
          Kind:

.. code-block:: ini

    # myitem.conf (altes Dateiformat)
    [Opa]
       [[Papa]]
          [[[Kind]]]


Die richtige Referenzierung der Items wäre hier ``Opa``, ``Opa.Papa`` und ``Opa.Papa.Kind``

So wie die Items oben stehen, erfüllen Sie noch keine Funktion außer einer gewissen Gliederung. 
Aus diesem Grund kann man den Items Attribute zuweisen. 


Namensvergabe
-------------

Bei der Wahl von Itemnamen ist folgendes zu beachten:

Plugin-Instanzen und Items der obersten Ebene (Top-Level) teilen sich den Namensraum. Es sollte 
vermieden werden, Top-Level Items einen Namen zu geben, der in **../etc/plugin.yaml** (bzw. **../etc/plugin.conf**) 
bereits für eine Plugin-Instanz gewählt wurde. Dieses kann zu unvorhergesehenen Problemen führen. 

z.B.: Wenn ein Plugin Funktionen implementiert hat, wird dies beim Aufruf dieser Funktionen zu 
Problemen führen, da SmartHomeNG dann versucht auf eine (nicht existierende) Methode des Items 
zuzugreifen, statt auf das Plugin.


Attribute 
---------

Attribute eines Items werden in der Konfigurationsdatei in der Form 

.. code-block:: yaml

    # myitem.yaml
    <Attribut-Name>: <Attribut-Wert>
    
bzw. 

.. code-block:: ini

    # myitem.conf  (altes Dateiformat)
    <Attribut-Name> = <Attribut-Wert>

angegeben. Normalerweise sind Attribut-Werte einzeilig. Es wird alles bis zum Zeilenende oder bis 
zum Beginn eines Kommentars (`#`) angenommen. (Seit dem Release 1.3 werden auch mehrzeilige Attribute 
unterstützt.)

.. hint::

   **Ab SmartHomeNG v1.3** wird ein neues Dateiformat für Konfigurationsdateien 
   unterstützt. Das bisherige Format der Konfigurationsdateien wird vorerst weiter unterstützt. 

   Informationen zum :doc:`neuen Dateiformat <./konfigurationsdateien_aufbau>` 
   finden Sie :doc:`hier <./konfigurationsdateien_aufbau>`.

