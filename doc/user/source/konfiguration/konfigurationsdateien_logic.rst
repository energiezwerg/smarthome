
.. _`logic.yaml`:

logic.yaml
==========

Logiken in SmartHomeNG sind Python Skripte (wie der Core auch). Diese Skripte werden im 
Verzeichnis `/usr/local/smarthome/logics` abgelegt. Um SmartHomeNG wissen zu lassen, wann eine 
Logik gestartet werden soll und welches Python Skript dann genutzt werden soll, muss jede Logik
in der Datei `logic.yaml` konfiguriert werden:

.. code-block:: yaml
   :caption: logic.yaml
   
   MyLogic:
       filename: logic.py
       crontab: init
       watch_item: mydoorcontact

.. code-block:: ini
   :caption: logic.conf (deprecated)
   
   # /usr/local/smarthome/etc/plugin.conf (deprecated)
   [MyLogic]
       filename = logic.py
       crontab = init
       watch_item = mydoorcontact

Mit dem Beispiel oben, würde SmartHomeNG in ``/usr/local/smarthome/logics/`` nach der Datei
``logic.py`` suchen. Die Logik würde einmal beim Start von SmartHomeNG ausgeführt und wenn sich 
der Wert des Items `watch_item` ändert.

