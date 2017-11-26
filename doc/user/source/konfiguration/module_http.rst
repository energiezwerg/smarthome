..index:: http

###########
Module http
###########

Dieses Modul erlaubt es Plugins eine Webschnittstelle zu implementieren. Die API wird weiter 
unten beschrieben. Das erste Plugin zur Nutzung dieser API ist das Backend-Plugin.


Voraussetzungen
===============

Dieses Modul läuft unter SmmartHomeNG-Versionen jenseits von Version 1.3. Es benötigt 
Python >= 3.4, sowie das Python Package  **cherrypy**. Sie können die Python-Module folgendermaßen 
installieren:

.. code-block:: python

   sudo pip3 install cherrypy

Und bitte beachten Sie, dass die lib (s) für Python3 installiert sind und nicht ein älteres Python 2.7, 
das wahrscheinlich auf Ihrem System installiert ist. Achten Sie darauf, `pip3` und nicht` pip` zu verwenden.

.. note::

   Für dieses Modul muss die Modulhandhabung in SmartHomeNG aktiviert sein. Stellen Sie sicher, 
   dass `use_modules` in **../etc/smarthome.yaml** auf **nicht** auf **True** gesetzt ist!
   

Konfiguration
=============

--------------------------
Datei *../etc/module.yaml*
--------------------------

.. code-block:: yaml

   # etc/module.yaml
   http:
   module_name: http
   #    port: 8383
   #    servicesport: 8384
   #    showpluginlist: False
       showservicelist: True
   #    starturl: backend
   #    threads: 8
   #    showtraceback: True


+----------------+------------------------------------------------------------------------------------------------------+
| **Parameter**  | **Bemerkung**                                                                                        |
+----------------+------------------------------------------------------------------------------------------------------+
| port           | **Optional**: Der Port auf welchem das html Interface lauscht. Standard Port ist **8383** is.        |
+----------------+------------------------------------------------------------------------------------------------------+
| serviceport    | **Optional**: Der Port auf welchem das html Interface lauscht. Standard Port ist **8384** is.        |
+----------------+------------------------------------------------------------------------------------------------------+
| showpluginlist | Falls der Parameter auf **False** gesetzt wird, wird unter **http://smarthomeNG.local:8383/plugins** |
|                | keine Liste der geladenen Plugins mit Web Interface gezeigt. **showpluginlist** ist standardmäßig    |
|                | **True**.                                                                                            |
+----------------+------------------------------------------------------------------------------------------------------+
| starturl       | **Optional**: Wenn **starturl** auf den Namen eines geladenen Plugins gesetzt ist, wird beim Aufruf  |
|                | von http://smarthomeNG.local:8383/ auf dieses Plugin weitergeleitet, statt auf die Übersichtsseite.  |
|                | Wenn z.B. standardmäßig das Backend Plugin aufgerufen werden soll, muss ``starturl: backend``        |
|                | gesetzt werden.                                                                                      |
+----------------+------------------------------------------------------------------------------------------------------+
| threads        | **Optional**: Die Anzahl der Threads, die CherryPy für jeden Port startet, auf dem es lauscht.       |
|                | Default ist 8, was für leistungsschwächere CPUs zu viel sein kann                                    |
+----------------+------------------------------------------------------------------------------------------------------+
| showtraceback  | Falls dieser Parameter auf  **True** gesetzt wird, zeigen Fehlerseiten (außer Fehler bei 404) einen  | 
|                | Python Fehler-Trace an. Normalerweise wird dieser Trace nur im **smarthome.log** aufgezeichnet       |
+----------------+------------------------------------------------------------------------------------------------------+


.. note::

   Wenn über den Parameter **starturl** die Weiterleitung auf ein spezifisches Plugin aktiviert ist,
   kann trotzdem die Übersichtsseite mit der Liste aller geledenen Plugins, die ein Webinterface registriert
   haben über **http://smarthomeNG.local:8383/plugins** angezeigt werden. Außer, man hat über
   ``showpluginlist: False`` diese Übersichtsseite deaktiviert.
   

