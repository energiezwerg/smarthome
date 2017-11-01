# Hard- u. Software Anforderungen

Um SmartHomeNG nutzen zu können, braucht es nicht viel. Für jemanden, der erstmalig SmartHomeNG installiert bietet es sich an zum Kennenlernen eine virtuelle Maschine zu erstellen und dort als Betriebssystem ein aktuelles Debian Jessie (>= 8.3) oder Ubuntu (>= 15.x) zu verwenden.

Da SmartHomeNG in den meisten Fällen im Hintergrund laufen wird, benötigt das System keine grafische Benutzeroberfläche und kann entsprechend schlank installiert werden.

## Hardware

### Virtuelle Maschine

Eine brauchbare Grundlage um SmartHomeNG auszuprobieren ist eine Virtuelle Maschine mit 512MB RAM und zwischen 20GB und 60GB Plattenplatz.

### Raspberry Pi 1, 2 oder 3, jeweils Modell B oder B+
#### Vorteile: 
* recht günstig im Einstieg, auch gebraucht zu bekommen
* weit verbreitet
* fertiges [Image](https://knx-user-forum.de/forum/supportforen/smarthome-py/979095-smarthomeng-image-file) von Onkelandy verfügbar

#### Nachteile: 
* Standardmäßig wird nur eine SD-Karte als Massenspeicher unterstützt - Hochwertige SD-Karte wird dringend empfohlen
  aufgrund der häufigen Schreibzyklen (Alternativ ist eine [Auslagerung der Dateien](https://knx-user-forum.de/forum/supportforen/smarthome-py/862047-wie-sqlite-auf-schnelleres-medium-verlagern) auf einen USB-Stick möglich
* Empfindlich, braucht eine **sehr stabile Spannungsversorgung**
* ARM Plattform, es gibt nicht für alles fertige Pakete zum Download

### Intel NUC (z.B. DN2820FYKH0) oder vergleichbar
#### Vorteile:
* verschiedene Hardwareausstattungen möglich
* niedriger Verbrauch
* Normale SSD kann verwendet werden (60GB oder 120GB macht Sinn)
* Installation über Docker-Container leicht möglich

#### Nachteile:
* teurer (z.B. bei 4GB RAM, 60GB SSD um 250 EUR)

### NAS wie z.B. Synology, QNAP

#### Vorteile:
* zumeist bereits vorhanden
* Leistung reicht für SmartHomeNG meist aus
* Installation über Docker-Container leicht möglich

#### Nachteile:
* Es sind nicht immer alle Pakete verfügbar, abhängig von der Plattform und vom Prozessortyp
* Bei Systemsoftware Updates des NAS werden zusätzliche Einstellungen oft wieder überschrieben

### Weitere Einplatinencomputer (Banana PI, ODroid, BeagleBone, etc.)

#### Vorteile: 
* recht günstig im Einstieg
* teilweise mit SATA Anschluß für Festplatte/SSD

#### Nachteile: 
* es hängt sehr von der Plattform ab ob sich Nachteile ergeben

## Software

Die aktuelle Version 1.3 von SmartHomeNG setzt Python der Version 3.3 oder neuer voraus.

Die Grundregel nach der sich der Support für Python Versionen richten soll ist folgende:

> **Unterstützt werden die bei Enwicklungsstart einer SmartHomeNG Version aktuelle Python Version und die zwei Vorgängerversionen.**

Zur Verdeutlichung:

```
| SmartHomeNG    | akt. Python zu Entwicklungsstart | unterstützte Python Versionen |
| -------------- | -------------------------------- | ----------------------------- |
| v1.2 und davor | diverse                          | Python 3.2, 3.3, 3.4          |
| v1.3           | Python 3.5                       | Python 3.3, 3.4, 3.5          |
| v1.4           | Python 3.6                       | Python 3.4, 3.5, 3.6          |
```

Das bedeutet nich automatisch, dass SmartHomeNG auf älteren Versionen von Python nicht mehr funktioniert. Die Entwicklung wird nur nicht mehr gegen die älteren Versionen getestet.