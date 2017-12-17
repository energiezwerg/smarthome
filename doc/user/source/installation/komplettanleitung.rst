#################
Komplettanleitung
#################

.. Aus dem Wiki übernommen: 11. November 2017 von Seite https://github.com/smarthomeNG/smarthome/wiki/Komplettanleitung

Ziel dieser Anleitung
=====================

Diese Anleitung beschreibt ein komplettes Installieren von **SmartHomeNG 1.3** inklusive knxd, 1-Wire 
und SmartVISU auf einem Debian 8.x (Jessie) oder Debian 9.x (Stretch) Linux Betriebssystem.

Debian > 8.x nutzt als init System den Systemd. Das hat den Effekt, das die Scripte zum Start 
der Services wegfallen und stattdessen nur Konfig-Dateien genutzt werden. Für einige optionale Module 
wie den knxd, ofws sind bereits entsprechende config-Dateien in den Paketen enthalten.

Es bietet sich an die allererste Installation einfach in einer virtuellen Maschine (VirtualBox, VMWare, etc.) 
durchzuführen um den Ablauf einmal gesehen und erlebt zu haben. Beim Installieren als VM solltet Ihr darauf 
achten, das die neue VM auch eine IP aus dem internen Netzwerk bekommt. Bei VirtualBox geht das z.B. über 
den Verbindungsmodus "bridged".


.. toctree::
   :maxdepth: 5
   :hidden:

   komplettanleitung_debian.md
   komplettanleitung_knx.md
   komplettanleitung_smarthomeng.md
   komplettanleitung_smartvisu.md
   komplettanleitung_onewire.md
   komplettanleitung_samba.md
   komplettanleitung_abschluss.md

