#######
Plugins
#######

Das Grundsystem von SmartHomeNG kann durch den Einsatz von Plugins erweitert werden. Ein Plugin 
ist ein Zusatzmodul in einem Unterverzeichnis unterhalb des Verzeichnisses **../plugins**. 
Um ein Plugin in SmartHomeNG zu verwenden (eine Instanz des Plugins zu laden) muß eine Sektion 
für das gewünschte Plugin in der Datei **etc/plugin.conf** erstellt werden. 

Für das oft benutzte KNX-Plugin sieht das z.B. so aus:

.. code::

   # etc/plugin.conf
   [knx]
      class_name = KNX
      class_path = plugins.knx
   #   host = 127.0.0.1
   #   port = 6720
      send_time = 600 # update date/time every 600 seconds, default none
      time_ga = 8/0/0
      date_ga = 8/0/1


bzw. im neuen Format:

.. code:: yaml

   # etc/plugin.yaml
   knx:
       class_name: KNX
       class_path: plugins.knx
   #    host: 127.0.0.1
   #    port: 6720
       send_time: 600    # update date/time every 600 seconds, default none
       time_ga: 8/0/0
       date_ga: 8/0/1


Dabei kann der Name der **Plugin-Instanz** (Name der Sektion in eckigen Klammern) frei gewählt 
werden. Es muss nur darauf geachtet werden, dass er eindeutig ist, also nur einmal vorkommt. 
Der name der Instanz sollte auch so gewählt werden, dass es zu keiner Namensgleichheit mit 
Top-Level Items kommt.

Die Parameter/Attribute **class_name** und **class_path** müssen angegeben werden. Dabei ist 
**class_name** immer der Python Klassenname und **class_path** immer der Pfad vom SmartHomeNG 
Basisverzeichnis zum Plugin. Diese beiden Einträge müssen exakt so übernommen werden, wie sie 
in der README.md Datei des jeweiligen Plugins beschrieben sind.

Die weiteren Einträge sind Plugin spezifisch. Welche Parameter/Attribute ein Plugin kennt ist 
auch der README.md des Plugins zu entnehmen. Je nach Plugin können sie verpflichtend oder 
optional sein. Im obigen Beispiel sind sie alle optional. Diese Parameter/Attribute werden 
beim Start von SmartHomeNG an das Plugin übergeben.

Ein **#** wirkt wie auch bei den Konfigurationsdateien der Items als Beginn eines Kommentars.


Liste der verfügbaren Plugins
-----------------------------

Details zu den :doc:`existierenden Plugins <../../plugins_all>` finden sich :doc:`hier <../../plugins_all>` .
