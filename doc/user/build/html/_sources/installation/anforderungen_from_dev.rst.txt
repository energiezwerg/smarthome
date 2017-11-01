#############
Anforderungen
#############

********
Hardware
********

Ein beliebiger Rechner mit x86 or x64 CPU sollte funktionieren, genauso wie Rechner mit einer
ARM CPU wie Raspberry.

Häufig verwendete Hardware ist:

- Raspberry 1, Raspberry 2, Raspberry 3 (der Letztere wird aufgrund der besseren Hardware **unbedingt empfohlen**)
  Der Großteil der Nutzer verwendet diese Hardware, Siehe `Umfrage <https://knx-user-forum.de/forum/supportforen/smarthome-py/1112952-welche-hardware-nutzt-ihr-f%C3%BCr-euer-smarthomeng>`_
- Intel NUC (Empfohlen für Stabilität und Geschwindigkeit, auch wenn diese Rechner mehr Leistung haben, als benötigt wird. Unterstützt normale SATA Festplatten, was ein Vorteil gegenüber den Raspberry Pis mit ihren SD-Karten ist)
- ODroid
- Banana Pi
- Beagle Bone
- Virtuelle Maschine, die z.B. auf einem NAS gehostet wird
- Docker Container

**************
Betriebssystem
**************

Ein beliebiges Linux oder Unix System (mit Shell Zugang um die Requirements und SmartHomeNG zu installieren) sollte funktionieren. 
SmartHomeNG ist mindestend getestet auf Raspbian und Debian Jessie (amd64)

Wenn eine Hardware ohne gepufferte Realtime Clock genutzt wird, ist der Einsatz eines NTP Deamons notwendig, 
um die Zeit über das Internet zu beziehen. Sonst wird SmartHomeNG aufgrund der fehlenden Zeitinformation nicht starten.

Einige Libraries in SmartHomeNG benutzen noch Bibliotheken, die ein Unix-artiges Betriebssystem voraussetzen.
Daher läuft SmartHomeNG nicht auf Windows und z.Zt. nicht unter MacOS.
