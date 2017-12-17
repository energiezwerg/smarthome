.. index:: module

module.yaml
###########

Module sind eine Erweiterung des Cores und stellen den Plugins zusätzliche Funktionalitäten 
zur Verfügung stehen. Sie bilden also eine erweiterte API für Plugin Entwickler.

Da diese Funktionalitäten einen größeren Ressourcen Bedarf haben, sind sie nicht fest in den
Programmcode des Cores aufgenommen worden, sondern als ladbare Module ausgeführt. Dadurch ist 
es möglich auf leistungsschwachen Systemen SmartHomeNG einzusetzen. Man muss nur auf den Einsatz 
der ladbaren Module verzichten.

Die ladbaren Module werden in der Datei **../etc/module.yaml** konfiguriert.

Details bitte dem Abschnitt **Konfiguration/Module** dieser Dokumentation entnehmen.

