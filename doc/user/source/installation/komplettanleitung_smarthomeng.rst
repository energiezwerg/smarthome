
.. role:: bluesup

##########################################
SmartHomeNG installieren :bluesup:`update`
##########################################

- Schritte der Installation:
    - [zusätzliche Pakete installieren](#zusätzliche-pakete-installieren-1)
    - [Quellcode laden](#quellcode-laden)
    - [Erstmalige Konfiguration erstellen](#erstmalige-konfiguration-erstellen)
    - [Zusätzliche Python Module](#zusätzliche-python-module)
    - [SmartHomeNG starten](#smarthomeng-starten)
    - [Backend Plugin nutzen](#backend-plugin-nutzen)


zusätzliche Pakete installieren
-------------------------------

Zunächst müssen einige zusätzlichen Pakete erfüllt werden:

.. code-block:: bash

   sudo apt-get -y install dialog python3 python3-dev python3-setuptools unzip build-essential
   sudo apt-get install python3-pip


Dann noch Pythons Paketmanager PIP auf den neuesten Stand bringen:

.. code-block:: bash

   sudo python3 -m pip install --upgrade pip


Quellcode laden
---------------

SmartHomeNG Dateien vom github holen:

Die folgenden Kommandos am besten mit dem User Account (smarthome) durchführen unter dem später SmartHomeNG laufen soll.

.. code-block:: bash

   cd /usr/local
   sudo mkdir smarthome
   sudo chown -R smarthome:smarthome /usr/local/smarthome

   cd smarthome
   git clone git://github.com/smarthomeNG/smarthome.git .

   mkdir plugins
   cd plugins
   git clone git://github.com/smarthomeNG/plugins.git .


Bitte auf den Punkt am Ende der **git clone** Kommandos achten!


Erstmalige Konfiguration erstellen
----------------------------------

smarthome.yaml
~~~~~~~~~~~~~~

In der **smarthome.yaml** stehen die allgemeinen Konfigurationseinstellungen der SmartHomeNG Installation, wie z.B. die
Koordinaten des Standortes. Die Koordinaten werden benötigt um unter anderem Sonnenaufgang / -untergang zu berechnen.
Die Koordinaten für einen Standort kann man z.B. auf http://www.mapcoordinates.net/de ermitteln.

Wenn keine Datei **smarthome.yaml** existiert, wird beim ersten Start von SmartHomeNG die mitgelieferte Datei **smarthome.yaml.default**
kopiert. Anschießend kann **smarthome.yaml** bearbeitet werden. Damit die Änderungen wirksam werden, muss SmartHomeNG im
Anschluß neu gestartet werden.

Der Inhalt von **smarthome.yaml** sollte mit einem Editor (z.B. **nano**) angepasst werden. Bei anderen Editoren ist darauf
zu achten, dass sie die Datei im UTF-8 Format schreiben.


plugin.yaml
~~~~~~~~~~~

In der **plugin.yaml** stehen die Plugins die verwendet werden sollen, sowie ihre Konfigurationsparameter.

Wenn keine Datei **plugin.yaml** existiert, wird beim ersten Start von SmartHomeNG die mitgelieferte Datei **plugin.yaml.default**
kopiert. In dieser Datei ist ein minimaler Set von Plugins konfiguriert, so dass z.B. per Browser oder mit der smartVISU auf die
SmartHomeNG Instanz zugegriffen werden kann.

.. code-block:: yaml

   %YAML 1.1
   ---
   BackendServer:
       plugin_name: backend
       #updates_allowed: False

   cli:
       plugin_name: cli
       ip: 0.0.0.0
       #port: 2323
       update: True
       #hashed_password: 1245a9633edf47b7091f37c4d294b5be5a9936c81c5359b16d1c48337$

   # Bereitstellung eines Websockets zur Kommunikation zwischen SmartVISU und SmartHomeNG
   websocket:
       plugin_name: visu_websocket
       #ip: 0.0.0.0
       #port: 2424
       #tls: no
       #wsproto: 4
       #acl: rw


Die Konfiguration weitere Plugins ist auskommentiert vorhanden, um die Nutzung dieser Plugins möglichst einfach zu
gestalten.


Zusätzliche Python Module
-------------------------

Für den ersten Start müssen noch einige Module nachgeladen werden, dazu wird für den Core die mitgelieferte **requirements/base.txt** genutzt:

.. code-block:: bash

   cd /usr/local/smarthome
   sudo pip3 install -r requirements/base.txt


Jedes Plugin kann weitere Abhängigkeiten mit sich bringen. Diese sind einzeln zu installieren mit

.. code-block:: bash

   sudo pip3 install -r plugins/<plugin-name-hier-einsetzen>/requirements.txt


oder aber alternativ kann man auch sämtliche von allen Plugins benötigten Module nachladen über

.. code-block:: bash

   sudo pip3 install -r requirements/all.txt


SmartHomeNG starten
-------------------

Erstmalig bietet es sich an, SmartHomeNG im Verbose-Modus zu starten um zu sehen was passiert und ob Fehler auftauchen.
Dafür ausführen:

.. code-block:: bash

   cd /usr/local/smarthome/bin
   python3 ./smarthome.py -v


Jetzt sollten jede Menge Logging-Meldungen über den Bildschirm laufen, die sehen in etwa so aus:

.. code-block:: text

   2017-08-05  00:00:07 DEBUG    M:lib.scheduler  T:Scheduler    IT.SwitchB next time: 2017-01-05 00:02:07+01:00
   2017-08-05  00:00:14 WARNING  M:plugins.dlms   T:DLMS         update is alrady running, maybe it really takes very long or you should use longer query interval time
   2017-08-05  00:00:14 DEBUG    M:lib.scheduler  T:Scheduler    DLMS next time: 2017-01-05 00:01:44+01:00


Vorne steht Datum und Uhrzeit, dann der Loglevel (DEBUG, ERROR, WARNING, INFO), dann je nach Setup in der Datei logging.yaml
noch Modul, Thread und ein Meldungstext der den Logeintrag beschreibt.

Wir schauen nach ERROR und WARNING und versuchen diese zu vermeiden.
ToDo: Erweitern.


Backend Plugin nutzen
---------------------

Wenn jetzt erstmal SmartHomeNG am Laufen ist, sollte auch das Backend funktionieren. Dazu prüfen wir im Browser unter der
Adresse **http://<IP vom SmartHomeNG>:8383** den Zugriff.

Initial ist SmartHomeNG ohne Benutzer Anmeldung konfiguriert. Wenn ein Zugriff nur mit User/Password möglich sein soll,
muss dieses im Abschnitt **http:** in **../etc/module.yaml** konfiguriert werden.

Der Backendserver ist unabhängig von der smartVISU und funktioniert auch dann, wenn kein visu Plugin geladen ist.

Hier sind ein paar Bilder vom Backendserver, um einen Eindruck zu vermitteln:

Der Item-Tree:

.. image:: assets/Backend_Items.png

Die Dienste/Tools Seite:

.. image:: assets/Backend_Dienste.jpg

Die Logik-Liste:

.. image:: assets/Backend_Logiken.jpg

Die Szenen Übersicht:

.. image:: assets/Backend_Szenen.jpg



 ----------------------------------------

Der Item-Tree:
![Backend Items](assets/Backend_Items.png)

Die Dienste/Tools Seite:
![Backend Dienste](assets/Backend_Dienste.jpg)

Die Logik-Liste:
![Backend Logiken](assets/Backend_Logiken.jpg)

Die Szenen Übersicht:
![Backend Logiken](assets/Backend_Szenen.jpg)
