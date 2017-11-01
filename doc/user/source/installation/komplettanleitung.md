# Komplettanleitung

### Ziel dieser Anleitung

Diese Anleitung beschreibt ein komplettes Installieren von **SmartHomeNG 1.3** inklusive knxd, 1-Wire und SmartVISU auf einem Debian 8.x (Jessie) oder Debian 9.x (Stretch).
Debian > 8.x nutzt als init System den Systemd. Das hat den Effekt, das die Scripte zum Start der Services wegfallen und stattdessen nur Konfig-Dateien genutzt werden. 
Für einige optionale Module wie den knxd, ofws sind bereits entsprechende config-Dateien in den Paketen enthalten.
Es bietet sich an die allererste Installation einfach in einer virtuellen Maschine (VirtualBox, VMWare, etc.) durchzuführen um den Ablauf einmal gesehen und erlebt zu haben. 
Beim Installieren als VM solltet Ihr darauf achten, das die neue VM auch eine IP aus dem internen Netzwerk bekommt.
Bei VirtualBox geht das z.B. über den Verbindungsmodus "bridged".

- [Debian](#debian)
    - [Softwareauswahl](#softwareauswahl)
    - [Einloggen via SSH  oder an der Konsole](#einloggen-via-ssh--oder-an-der-konsole)
    - [Systemaktualisierung](#systemaktualisierung)
    - [Restarbeiten am System](#restarbeiten-am-system)
- [knxd installieren](#knxd-installieren)
    - [zusätzliche Pakete installieren](#zusätzliche-pakete-installieren)
    - [Quellcode laden, compilieren und ein Paket schnüren](#quellcode-laden-compilieren-und-ein-paket-schnüren)
    - [knxd konfigurieren](#knxd-konfigurieren)
    - [knxd und systemd](#knxd-und-systemd)
- [SmartHomeNG installieren](#smarthomeng-installieren)
    - [zusätzliche Pakete installieren](#zusätzliche-pakete-installieren-1)
    - [Quellcode laden](#quellcode-laden)
    - [Erstmalige Konfiguration erstellen](#erstmalige-konfiguration-erstellen)
    - [Zusätzliche Python Module](#zusätzliche-python-module)
    - [SmartHomeNG starten](#smarthomeng-starten)
    - [Backend Plugin nutzen](#backend-plugin-nutzen)
- [SmartVISU installieren](#smartvisu-installieren)
    - [zusätzliche Pakete installieren](#zusätzliche-pakete-installieren-2)
    - [SmartVISU Quellcode laden](#smartvisu-quellcode-laden)
- [Onewire installieren](#onewire-installieren)
    - [zusätzliche Pakete installieren](#zusätzliche-pakete-installieren-3)
    - [owfs konfigurieren](#owfs-konfigurieren)
- [Samba installieren](#samba-installieren)
- [Abschlussarbeiten](#abschlussarbeiten)
    - [Weitere Konfiguration](#weitere-konfiguration)
    - [Mehr Komfort via SSH Zugriff](#mehr-komfort-via-ssh-zugriff)
    - [SmartHomeNG als Dienst einrichten](#smarthomeng-als-dienst-einrichten)


## Debian
Die genaue Step-by-Step Installation des Betriebsystemes wird hier nicht beschrieben, das hier ist der falsche Ort dafür. 
Jedoch werden als Referenz die Paketauswahlen während der Installation hier beschrieben. 
Am kompaktesten ist die Netinstall ISO-Datei. Wenn ihr auf einem externen Rechner (z.B. NUC o.ä.) installiert, 
kann die ISO-Datei mit Tools wie z.B. [Linux Live USB Creator](http://www.linuxliveusb.com/), [Universal-USB-Installer](http://www.pendrivelinux.com/universal-usb-installer-easy-as-1-2-3/) 
oder [UNetbootin](https://unetbootin.github.io/) auf einen USB Stick übertragen werden.

Wer SmarthomeNG auf einem Raspberry Pi betreiben möchte, startet am besten mit dem aktuellsten [Raspbian Image](https://www.raspberrypi.org/downloads/raspbian/) von der raspberrypi.org Seite. Dieses Image kann mittels [Etcher](https://etcher.io/) oder [Win32Diskimager](https://sourceforge.net/projects/win32diskimager/) auf eine SD-Karte "gebrannt" werden. Die unten stehenden Schritte bis "Einloggen via SSH" entfallen. Es ist allerdings notwendig, sich beim ersten Start direkt am Raspberry Pi einzuloggen (User: pi, Passwort: raspberry - Achtung, englische Tastatur!) und mittels 
```
sudo systemctl start ssh
sudo systemctl enable ssh
```
das SSH Service zu starten und für zukünftige Neustarts automatisch zu aktivieren.

Im allgemeinen braucht ein Server keine grafische Benutzeroberfläche, also ganz normale Installation wählen. Einige Einstellungen die jetzt vorgenommen werden sind
* Sprache, Tastaturlayout 
* Rechnername z.B. sh
* Das root Passwort bitte leer lassen.
* Benutzer "smarthome" anlegen
* Zeitzone (z.B. Berlin)
* Festplatte geführt partitionieren und alles verwenden, Änderungen auf Platten schreiben

Jetzt erfolgt die Grundinstallation des Systems aus dem Netinst Basispaket. Anschließend wird aufgrund der Landesvorwahl der Spiegelserver für die weiteren Dateien festgelegt. 
Nach der Festlegung konfiguriert das System apt und lädt Pakete aus dem Spiegelserver nach. Das ist die Gelegenheit sich ein Heiß- oder Kaltgetränk nach Wahl zu holen da der Vorgang je nach Hardware und Netzwerkgeschwindigkeit  zwischen 4 und 8 Minuten dauert.
Die Rückmeldung des Systems an die Entwicklung darf abgelehnt werden.

### Softwareauswahl

Wenn ihre keine grafische Benutzeroberfläche braucht, dann bitte **abwählen**:

* Debian Desktop Environment 

**abwählen**:

* Druckserver 

**auswählen**:

* Web Server
* SSH Server (wird für SSH z.B. via PuTTY oder Bitvise SSH client benötigt)
* Standard-Systemwerkzeuge

Nun ist es Zeit für das nächste Getränk, das nachladen der zu installierenden Pakete dauert jetzt wiederum 5 bis 20 Minuten. 
Die angebotene  Installation von GRUB wird akzeptiert und anschließend neu gestartet.

### Einloggen via SSH  oder an der Konsole

Mit einem **SSH Client** jetzt auf den frisch installierten smarthome Server einloggen:
Unter OSX dazu einfach eine Kommandozeile öffnen und folgendes eintippen: `ssh <ip_des_servers>`.  
Unter Linux genau das gleiche, Kommandozeile öffnen und folgendes eintippen: `ssh <ip_des_servers>`.  
Unter Windows gibt es Putty als SSH Client, [download hier](http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe). 
Noch komfortabler ist [Kitty](http://www.9bis.net/kitty/?page=Download). 
Einfach zunächst Putty installieren und umbenennen in Putty.exe.bak. Dann Kitty ins Verzeichnis vom Putty schreiben und umbenennen als Putty.exe.
Natürlich `<ip_des_servers>` ersetzen durch die IP Adresse oder den Namen des neuen smarthome Servers.

Oder alternativ direkt an der **Konsole** anmelden.

Benutzer zum Anmelden ist "smarthome" und das weiter oben erstellte Passwort für diesen User. Wurde kein Passwort angegeben und möchte man SSH so konfigurieren, dass man sich mit einem leeren Passwort einloggen kann, sind folgende Operationen notwendig:
```
sudo sed -i -e 's/#PermitEmptyPasswords no/PermitEmptyPasswords yes/g' /etc/ssh/sshd_config
sudo sed -i -e '/console/s/.*/&\nssh/' /etc/securetty
sudo systemctl restart sshd
```

Generell wird aber empfohlen, den SSH-Zugang mit Zertifikaten abzusichern und ein Einloggen mittels Username/Passwort zu unterbinden. Informationen zum [Erstellen von Zertifikaten](https://www.thomas-krenn.com/de/wiki/SSH_Key_Login) gibt es zB bei Thomas Krenn. 


### Systemaktualisierung

Nach der Anmeldung ist zunächst mit 

```
sudo apt-get update
sudo apt-get upgrade
```

das frisch installierte System mit den neuesten Systemupdates zu versorgen. Eigentlich sollte dabei nix zu installieren sein aber sicher ist sicher.

Für den Fall einer virtuellen Maschine ist jetzt eine gute Gelegenheit einen Snapshot zu erstellen um einen definierten Punkt 
zur Rückkehr zu haben falls im weiteren etwas schiefläuft. Alternativ kann der Snapshot auch nach Abschluß der Restarbeiten weiter unten ausgeführt werden.

#### Optional: Einstellen von Tastaturlayout, Sprache, etc.

Hat man das Image auf einem Raspberry Pi installiert, können nach dem ersten Start sämtliche Einstellungen über ein übersichtliches Menü getätigt werden. Es empfiehlt sich, die Sprache auf de_DE.UTF-8 und das Tastaturlayout auf Deutsch umzustellen. Außerdem können hier diverse Services aktiviert und das Filesystem auf die Größe der SD-Karte erweitert werden. 

```
sudo raspi-config
```

#### Optional: System herunterfahren für Snapshop

```
sudo poweroff
```

#### Optional: alternative Netzwerk Konfiguration für feste IP
Hierfür sei [auf diese Seite verwiesen](https://wiki.debian.org/NetworkConfiguration)

#### Optional: Installation der Open VM Tools bei Verwendung als virtuelle Maschine unter VMWare Workstation oder ESXi

Wenn die Installation virtuelle Maschine erfolgt ist, wird von [VMWare empfohlen](https://kb.vmware.com/kb/2073803) die Open VM Tools zu installieren:

Für die reine Servervariante vom Debian geht das über

```
sudo apt-get install open-vm-tools
```

bei Vorhandensein einer GUI dann alternativ mit 

```
sudo apt-get install open-vm-tools-desktop
```

Die automatische Anpassung der Bildschirmgröße funktioniert erst nach einem Neustart.


#### Optional: Installation der Gästeerweiterungen bei Verwendung als virtuelle Maschine unter Oracle VM VirtualBox

Um die Gästeerweiterungen zu installieren zuerst unter **Geräte** -> **Gästeerweiterungen einlegen** anklicken. Diese nun via Terminal/Shell ausführen und den Anweisungen folgen: 

```
sudo sh /media/cdrom/VBoxLinuxAdditions.run
```

Nach einem Neustart passt sich nun bspw. bei Verwendung einer GUI die Auflösung dynamisch an.

### Restarbeiten am System

Wenn kein Passwort für root vergeben wurde, dann wird der bei der Installation erstellte User (hier: smarthome) automatisch in die Gruppe für sudo aufgenommen.

Falls man einen anderen Benutzernamen bei der Installation gewählt hat, muss man den User smarthome zunächst erstellen:
```
sudo  adduser smarthome --disabled-password --gecos "First Last,RoomNumber,WorkPhone,HomePhone" 
```

Den Benutzer **smarthome** in die **www-data** und **sudo** Gruppe hinzufügen:

```
sudo usermod -aG www-data,sudo smarthome
```
Auch wenn der Benutzer smarthome schon existiert muss er in die Gruppe www-data mit folgendem Befehl eingetragen werden.
```
sudo usermod -aG www-data smarthome
```

Der Benutzer **smarthome** muß nun abgemeldet und neu angemeldet werden, damit die Rechte neu eingelesen werden. Dies ist eine gute Gelegenheit 
um einen alternativen Snapshop zu erstellen. Dazu dann wiederum das System ausschalten mit:

```
sudo poweroff
```


## knxd installieren

Der knxd implementiert Zugriffe auf verschiedenste Schnittstellen zum KNX Bus (z.B. IP-Router, IP-Schnittstelle, USB-Schnittstelle, etc.) und bietet dafür eine dokumentierte Softwareschnittstelle für Programme an.
SmartHomeNG nutzt den knxd über seine tcp Schnittstelle um Daten auf den KNX Bus zu schreiben oder zu lesen.

Wer keinen KNX-Bus einsetzt, kann diesen Installationsschritt überspringen. Für den Fall, das die knxd Installation ausgelassen wird, kann es sein, das für weitere Module wie SmartHomeNG einige Pakete fehlen. Diese müßten dann per **sudo apt-get install paketname** nachinstalliert werden.

Grundsätzlich findet sich auf der [knxd-Seite](https://github.com/knxd/knxd) die Anleitung für die Installation.
Auf der Github Seite kann unter **Code** immer der Branch ausgewählt werden. Jeder Branch hat sein eigenes Read.me.

> **Wichtig:** 
> Der knxd wird derzeit aktiv weiterentwickelt. Ab Version 0.12.x ist pthsem nicht mehr notwendig und es wird libev eingesetzt.
> Wer genügend Wissen zum Testen hat ist herzlich eingeladen hier mitzuhelfen oder zu spenden.
> Auch bitte **vor** der Installation hier noch einen Blick auf [knxd-Seite](https://github.com/knxd/knxd)
> werfen um aktuelles nicht zu verpassen.
> 
> Diese Anleitung wird zwar in regelmäßigen Abständen aktualisiert aber eben nicht unbedingt wöchentlich oder gar täglich.

Die folgenden Installationsschritte beziehen sich auf Version **0.14**.

### zusätzliche Pakete installieren

Zunächst müssen für den Bau einige grundlegende Tools installiert werden:

```
sudo apt-get install git-core build-essential
```

<!-- Die Installation auf einem frischen Jessie zeigt 
folgende nicht erfüllte Bauabhängigkeiten:
debhelper (>= 7.0.0)
autotools-dev
autoconf
automake
libtool
libusb-1.0-0-dev (>= 1.0.9) pkg-config
libsystemd-dev (>= 228) | libsystemd-daemon-dev (>= 200) | base-files (<< 8)
dh-systemd | base-files (<< 8) libev-dev

Diese Abhängigkeiten werden mit den nachfolgenden Paketinstallationen aufgelöst.
Wenn sich **dpkg-buildpackage** über weitere fehlende Pakete beschweren sollte,
("Unmet build dependencies"): dann sollten sie nachinstalliert
(``sudo apt-get install …``) und ein neuer Versuch gestartet werden.<br>
Wenn **x | y** gefordert wird, erstmal nur **x** installieren.
Wenn das nicht funktioniert, kann auch **y** installiert werden<br>
Bei Beschwerden über inkompatible Pakete können diese ggf. entfernt werden.
Bitte in obigem Fall die Komplettanleitung anpassen !!!
-->

debhelper-Erweiterung zur Behandlung von systemd-Dateien

```
sudo apt-get install dh-systemd
```


Erstellt automatisch configure-Skripte

```
sudo apt-get install autoconf
```

Generisches Skript zur Unterstützung von Bibliotheken

```
sudo apt-get install libtool
```

Bibliothek zum Programmieren von USB-Anwendungen ohne Kenntnis der Linux-Kernel-Interna

```
sudo apt-get install libusb-1.0-0-dev
```

Pkg-config ist ein System zur Verwaltung von Schaltern für die Übersetzung und Verknüpfung von Bibliotheken,
das mit automake und autoconf arbeitet.

```
sudo apt-get install pkg-config
```

Die Bibliothek sd-daemon stellt eine Referenzimplementierung mehrerer APIs für neuartige Daemons bereit,
wie sie vom Initialisierungssystem systemd implementiert werden

Für Debian Jessie wird benötigt:
```
sudo apt-get install libsystemd-daemon-dev
```

Für Debian Stretch wird benötigt:
```
sudo apt-get install libsystemd-dev
```

Nun noch libev-dev installieren
```
sudo apt-get install libev-dev
```

Und es wird noch das cmake tool benötigt
```
sudo apt-get install cmake
```

### Quellcode laden, compilieren und ein Paket schnüren

Zunächst den Quellcode für den knxd vom github laden und sicherstellen, das der 0.14 branch gewählt wird:

```
git clone https://github.com/knxd/knxd.git
cd knxd
git checkout v0.14
```

Im Unterverzeichnis ```tools```findet sich ein Skript was benötigt wird um libfmt herunterzuladen und zu bauen

```
tools/get_libfmt
```

Dann übersetzen und das Paket schnüren:

```
dpkg-buildpackage -b -uc
```

Wichtig ist, das am Ende der Paketerstellung keine Fehler gemeldet wurden.

Sollte die Paketerstellung fehlerfrei ablaufen, dann kann das Paket nun noch installiert werden mit:

```
cd ..
sudo dpkg -i knxd_*.deb knxd-tools_*.deb
```

### knxd konfigurieren

Als nächstes muß die Konfiguration des knxd für die zu verwendende Schnittstelle angepasst werden.
Dazu muß bei Systemen mit systemd die Datei **/etc/knxd.conf** bearbeitet werden:

```
sudo nano /etc/knxd.conf
```

Die Originalzeile **KNXD_OPTS="-e 0.0.1 -E 0.0.2:8 -u /tmp/eib -b ip:"** am besten auskommentieren und in der Zeile
darunter dann die gewählten Parameter eintragen.

Details zu Schnittstellen finden sich auf der [Github-Seite vom knxd](https://github.com/knxd/knxd).
Das **-c** ist für den knxd eigenen Cache. Danach folgen die Optionen für die Verwendung der Schnittstelle:

* IP Schnittstelle: **KNXD_OPTS="-e 0.0.1 -E 0.0.2:8 -c -b ipt:_IP der knx Schnittstelle_"**
* IP Router: **KNXD_OPTS="-e 0.0.1 -E 0.0.2:8 -c -b ip:_IP des knx Routers_"**
* USB-Interface: Bitte [Wiki zum knxd](https://github.com/knxd/knxd/tree/v0.14) konsultieren.

Es kann sein, das bei KNXD_OPTS hinter dem **-c** bei einigen Interfaces noch ein **--send-delay=30**
eingefügt werden muß um Telegrammverlust bei hohen Lasten zu minimieren. 
Die 30 bedeutet dabei eine zusätzliche Wartezeit von 30msec.
Es wird damit zwischen den Paketen eine kleine Pause eingelegt um ein überfahren der Schnittstelle zu vermeiden.
Der Parameter **--no-tunnel-client-queuing** ist obsolet und sollte nicht mehr eingesetzt werden.

### knxd und systemd

Um die Änderungen wirksam werden zu lassen, muß der knxd die neue Konfiguration noch berücksichtigen dazu muß er ggf. beendet und neu gestartet werden. Der knxd hat dazu zwei Einträge, zum einen ```knxd.socket``` der die normalerweise die Kommunikation über der Port 6720 übernimmt und der ```knxd.service``` der die restlichen Aufgaben übernimmt.

Zunächst beenden des knxd:

```
sudo systemctl stop knxd.socket
sudo systemctl stop knxd.service
```
Die Reihenfolge ist wichtig: beenden wir erst den knxd, kann ein Prozess genau dann einen Socket öffnen und der systemd startet ihn sofort wieder.

Um sicher zu gehen, das der knxd mit dem Systemstart auch gestartet wird muß dem systemd mitgeteilt werden das diese beiden Einträge auch eingeschaltet also ```enabled``` sind.

```
sudo systemctl enable knxd.service
sudo systemctl enable knxd.socket
```

Jetzt können wir den knxd starten mit 

```
sudo systemctl start knxd.socket
sudo systemctl start knxd.service
```
Auch hier ist die Reihenfolge wichtig: Starten wir erst den Service, werden dem knxd die Sockets nicht vom systemd übergeben.

Mit den folgenden Kommandos kann geprüft werden, ob die beiden Einträge ordnungsgemäßt funktionieren:

```
sudo systemctl status knxd.socket
sudo systemctl status knxd.service
```

Wenn alles ok ist, dann sieht das etwa so aus:

```
$ sudo systemctl status knxd.service
● knxd.service - KNX Daemon
   Loaded: loaded (/lib/systemd/system/knxd.service; enabled)
   Active: active (running) since Sa 2016-08-13 10:03:27 CEST; 5 days ago
 Main PID: 30769 (knxd)
   CGroup: /system.slice/knxd.service
           └─30769 /usr/bin/knxd -c -b ipt:192.168.10.38

$ sudo systemctl status knxd.socket
● knxd.socket - KNX Daemon (socket)
   Loaded: loaded (/lib/systemd/system/knxd.socket; enabled)
   Active: active (running) since Sa 2016-08-13 10:03:23 CEST; 5 days ago
   Listen: /var/run/knx (Stream)
           [::]:6720 (Stream)
```

Die Funktion des knxd läßt sich z.B. testen mit einer Gruppenadresse (hier: 1/0/170) für einen Schaltaktor mit 1 oder 0.

```
knxtool groupswrite ip:localhost 1/0/170 1
```

Sollte sich jetzt nichts tun, dann gibt es irgendwo einen Fehler und alles muß noch einmal geprüft werden. Vielleicht ist der Neustart des knxd vergessen oder ein Build-Fehler übersehen worden.

<!--- Für Systeme ohne systemd würde gelten:
Damit knxd beim Start ausgeführt wird, ist noch eine Anpassung notwendig:

    sudo nano /etc/default/knxd

dann folgende Einträge anpassen:

    START_KNXD=YES 
-->


## SmartHomeNG installieren

### zusätzliche Pakete installieren

Zunächst müssen einige zusätzlichen Pakete erfüllt werden:
<!---
apt-get update nicht notwendig
openssh-server apache2  git-core wget bereits installiert
--->

<!---
```
sudo apt-get -y install dialog openntpd python3 python3-dev python3-setuptools unzip build-essential
sudo easy_install3 pip
```
--->

```
sudo apt-get -y install dialog python3 python3-dev python3-setuptools unzip build-essential
sudo apt-get install python3-pip
```

Dann noch Pythons Paketmanager PIP auf den neuesten Stand bringen:

```
sudo python3 -m pip install --upgrade pip
```
<!--
Alternativ sollte auch ein

```
sudo easy_install3 -U pip
```

zum Ergebnis führen.
--> 

### Quellcode laden
SmartHomeNG Dateien vom github holen:

```
cd /usr/local
sudo git clone --recursive git://github.com/smarthomeNG/smarthome.git
sudo chown -R smarthome:smarthome /usr/local/smarthome
cd /usr/local/smarthome/etc
touch logic.yaml
```

### Erstmalige Konfiguration erstellen

#### smarthome.yaml

In der **smarthome.yaml** stehen die Koordinaten des Standortes der Installation. Die Koordinaten werden benötigt um unter anderem Sonnenaufgang / -untergang zu berechnen. 
Die Koordinaten für einen Standort kann man z.B. [hier](http://www.mapcoordinates.net/de) ermitteln.

Alternativ kann die mitgelieferte **smarthome.yaml.default** kopiert werden in **smarthome.yaml** mit ``cp smarthome.yaml.default smarthome.yaml`` 
oder das folgende Code snippet kann von der **cat** Zeile an bis zur Zeile unter **EOL** ausgewählt und ins ssh kopiert werden.

```
cat >smarthome.yaml <<EOL
## smarthome.yaml
lat: '52.52'
lon: '13.40'
elev: 36
tz: Europe/Berlin
EOL
```

In beiden Fällen sollte der Inhalt von **smarthome.yaml** nun mit einem Editor (z.B. **nano**) angepasst werden.


#### plugin.yaml 

Auch hier wird eine **plugin.yaml.default** mitgeliefert mit den meisten Voreinstellungen die per ``cp plugin.yaml.default plugin.yaml`` 
kopiert werden kann, allerdings sind in dieser Datei alle Einstellungen zunächst auskommentiert **#**.
Alternativ dazu kann analog zur obigen **smarthome.yaml** das folgende Code snippet von der **cat** Zeile an bis zur Zeile unter **EOL** ausgewählt und ins ssh kopiert werden:

```
cat >plugin.yaml <<EOL
# plugin.yaml

# Der BackendServer stellt eine Übersicht zur Laufzeit dar und liefert Informationen ähnlich wie das CLI Plugin
# Der Zugriff erfolgt über http://<IP oder Name des SmartHomeNG Servers bzw. ip>:<port>
# port wird als Attribut weiter unten definiert
# das Passwort ist zunächst im Klartext anzugeben. In neueren Versionen wird es eine Funktion im Backend geben,
# die aus einem gegebenen Passwort einen Hash erzeugt. Wenn user oder password fehlen gibt es keine Abfrage
BackendServer:
    class_name: BackendServer
    class_path: plugins.backend
    # ip: xxx.xxx.xxx.xxx
    port: 8383
    updates_allowed: 'True'
    threads: 8
    user: admin
    password: xxxx
    language: de

# KNX Verbindung via knxd
knx:
    class_name: KNX
    class_path: plugins.knx
    host: 127.0.0.1
    port: 6720
    # send_time: 600 # update date/time every 600 seconds, default none
    # time_ga: 1/1/1 # default none
    # date_ga: 1/1/2 # default none

# Bereitstellung eines Websockets zur Kommunikation zwischen SmartVISU und SmartHomeNG
visu:
    class_name: WebSocket
    class_path: plugins.visu_websocket
    # ip: 0.0.0.0
    # port: 2424
    # tls: no
    wsproto: 4
    acl: rw

# Autogenerierung von Webseiten für SmartVISU
smartvisu:
    class_name: SmartVisu
    class_path: plugins.visu_smartvisu
    # '"neue" Linux Versionen (z.B. Debian > 8.x, Ubuntu > 14.x)'
    smartvisu_dir: /var/www/html/smartVISU

    # nur \"alte\" Linux-Variationen
    # smartvisu_dir: /var/www/smartVISU
    # generate_pages: True
    # handle_widgets: True
    # overwrite_templates: Yes
    # visu_style: blk

# Command Line Interface
# wichtig für Funktionsprüfungen solange keine Visu zur Verfügung steht
cli:
    class_name: CLI
    class_path: plugins.cli
    ip: 0.0.0.0
    update: 'True'

# alter SQL-Treiber
# [sql]
# class_name: SQL
# class_path: plugins.sqlite
# SQL-Treiber, unterstützt auch die SmartVISU 2.8/2.9
# dazu muß im websocket plugin zwingend die Protokollversion 4 eingetragen sein

sql:
    class_name: SQL
    class_path: plugins.sqlite_visu2_8

# Onewire Plugin
# [ow]
# class_name: OneWire
# class_path: plugins.onewire
EOL
```

### Zusätzliche Python Module

Wieder zurück nach **/usr/local/smarthome** mit ```cd ..``` oder ```cd /usr/local/smarthome```

Für den ersten Start müssen noch einige Module nachgeladen werden, dazu wird für den Core die mitgelieferte **requirements/base.txt** genutzt:

```
sudo pip3 install -r requirements/base.txt
```

Jedes Plugin kann weitere Abhängigkeiten mit sich bringen. Diese sind einzeln zu installieren mit

```
sudo pip3 install -r plugins/<plugin-name-hier-einsetzen>/requirements.txt
```

oder aber alternativ kann man auch sämtliche von allen Plugins benötigten Module nachladen über 

```
sudo pip3 install -r requirements/all.txt
```


### SmartHomeNG starten
Erstmalig bietet es sich an, SmartHomeNG im Debugmodus zu starten um zu sehen was passiert und ob Fehler auftauchen.
Dafür ausführen:

```
cd /usr/local/smarthome/bin
python3 ./smarthome.py -d
```

Jetzt sollten jede Menge Logging-Meldungen über den Bildschirm laufen, die sehen in etwa so aus:

```
2017-08-05  00:00:07 DEBUG    M:lib.scheduler  T:Scheduler    IT.SwitchB next time: 2017-01-05 00:02:07+01:00
2017-08-05  00:00:14 WARNING  M:plugins.dlms   T:DLMS         update is alrady running, maybe it really takes very long or you should use longer query interval time
2017-08-05  00:00:14 DEBUG    M:lib.scheduler  T:Scheduler    DLMS next time: 2017-01-05 00:01:44+01:00
```
Vorne steht Datum und Uhrzeit, dann der Loglevel (DEBUG, ERROR, WARNING, INFO), dann je nach Setup in der Datei logging.yaml noch Modul, Thread und ein Meldungstext der den Logeintrag beschreibt.

Wir schauen nach ERROR und WARNING und versuchen diese zu vermeiden.
ToDo: Erweitern.

### Backend Plugin nutzen
Wenn jetzt erstmal SmartHomeNG am Laufen ist, sollte auch das Backend funktionieren. Dazu prüfen wir im Browser unter der Adresse **http:\\<IP vom SmartHomeNG>:8383** den Zugriff.
Bei der Frage nach Benutzer und Passwort geben wir **admin** und **xxxx** ein. Jetzt ist erstmal die Spielwiese eröffnet. Der Backendserver ist unabhängig von der SmartVISU und funktioniert auch dann, wenn ihr kein visu Plugin geladen habt. Ein paar Bilder vom Backendserver:

![Backend Items](assets/Backend_Items.png)

![Backend Dienste](assets/Backend_Dienste.png)

![Backend Logiken](assets/Backend_Logiken.png)

## SmartVISU installieren

Die SmartVISU ist eine Sammlung von HTML-Dateien und PHP Scripten die es ermöglicht 
Items vom SmartHomeNG anzuzeigen. Im wesentlichen wird dazu ein Webserver benötigt,
hier der Apache2 und für die Variablen Daten des SmartHomeNG braucht die SmartVisu 
noch eine Websocket-Verbindung zum SmartHomeNG.

### zusätzliche Pakete installieren

Der Apache2 braucht noch ein paar Pakete wie PHP um die Webseiten der SmartVISU
liefern zu können:
Bis einschließlich Debian 8.x (Jessie) mit folgendem Befehl:
```
sudo apt-get install libawl-php php5-curl php5 php5-json php-xml
```
Oder ab Debian 9.x (Stretch) mit folgendem Befehl:
```
sudo apt-get install libawl-php php-curl php php-json php-xml
```

### SmartVISU Quellcode laden 
Stand 3. Oktober 2016 ist SmartVISU 2.8 die letzte verfügbare Master-Version.
Da das Projekt fortgeführt wird, 
sollte vor dem Installieren [auf der Projektseite](http://www.smartvisu.de/) nachschaut und der Pfad gegebenfalls angepasst werden.
Die Dateien der SmartVISU werden in einem Unterverzeichnis ab, das für den Apache2 zugänglich ist:

<!--
```
cd /var/www/html
sudo rm index.html
sudo wget http://smartvisu.de/download/smartVISU_2.8.zip
sudo unzip smartVISU_2.8.zip
sudo rm smartVISU_2.8.zip
```
-->


```
cd /var/www/html
sudo rm index.html
sudo git clone git://github.com/Martin-Gleiss/smartvisu.git
sudo mv smartvisu smartVISU
```

Nun müssen die Zugriffsrechte und der Standardbenutzer richtig gesetzt werden:
```
sudo chown -R www-data:www-data smartVISU
sudo chmod -R 775 smartVISU
```


Dann versuchen, mit einem Browser von einem anderen Rechner aus auf SmartVISU zuzugreifen.
<ip-des-servers> natürlich mit der IP oder dem Name deines SmartVISU Servers ersetzen: 
`http://<ip-des-servers>/smartVISU`
Bei "Checking your configuration" sollte alles mit einem grünen Häckchen versehen sein.
Jetzt auf den "Config" Knopf drücken. Damit müsstest du in das SmartVISU Interface gelangen, direkt auf die Config Seite.
Bei I/O Connection "Smarthome.py" auswählen. ACHTUNG: Bei Adresse (URL / IP) die Interface Adresse des Servers eingeben oder den DNS Namen.
Hier NICHT localhost oder 127.0.0.1 eingeben, denn diese Adresse wird vom Client Browser benutzt (Javascripts). Somit muss die Verbindung nicht nur vom SmartVISU Server funktionieren, sondern auch von all deinen Geräten, von denen aus du SmartVISU benutzen willst.
Wenn du mit dem Autogenerator arbeiten willst, dann stelle noch im Tab "Interfaces" die Auswahl "Pages" auf "Smarthome".
Dann ganz unten auf "Save" drücken.  

##  Onewire installieren

### zusätzliche Pakete installieren

Für den Zugriff von SmartHomeNG auf einen OneWire Bus kann das owserver Paket genutzt werden.
Die dazu benötigten Komponenten werden installier mit:
```
sudo apt-get -y install owhttpd owserver
```

## owfs konfigurieren
Die owfs Konfigurationsdatei noch auf den verwendeten Adapter angepasst werden:

```
sudo nano /etc/owfs.conf
```
Eine Beispieldatei für einen USB-Adapter wie den weit verbreiteten DS9490R kann z.B. so aussehen:
```
######################## SOURCES ########################
#
# With this setup, any client (but owserver) uses owserver on the
# local machine...
! server: server = 127.0.0.1:4304
#
# ...and owserver uses the real hardware, by default fake devices
# This part must be changed on real installation
#server: FAKE = DS18S20,DS2405
#
# USB device: DS9490
server: usb = all
#
# Serial port: DS9097
#server: device = /dev/ttyS1
#
# owserver tcp address
#server: server = 192.168.10.1:3131
#
# random simulated device
#server: FAKE = DS18S20,DS2405
#
######################### OWFS ##########################
#
mountpoint = /mnt/1wire
allow_other
#
####################### OWHTTPD #########################
http: port = 2121
####################### OWFTPD ##########################
ftp: port = 2120
####################### OWSERVER ########################
server: port = 127.0.0.1:4304
```
Wichtig dabei ist vor allem das in der Config nicht localhost steht sondern 127.0.0.1 explizit angegeben wird. 
Dadurch wird eine Bindung des Ports 4304 an eine normale IP erreicht und nicht an tcp6 wie es sonst der Fall wäre. 
Mit tcp6 wiederum könnte das Smarthome.py derzeit nichts anfangen.

Bei der Installation werden owserver und owhttp automatisch gestartet.
Nach der Konfigurationsänderung muß der owserver neu gestartet werden:

```
sudo systemctl restart owserver
```

Damit das Onewire-Plugin von smartHomeNG genutzt werden kann, muß in der **/etc/plugin.conf**
müssen beim **[ow]**-Teil und den direkt nachfolgenden Zeilen die führenden Kommentarzeichen **#**
entfernt werden.


## Samba installieren
Wer mit einem Windows-Rechner auf die Dateien von SmartHomeNG und SmartVISU zugreifen möchte,
_kann_ dazu **Samba** installieren:

```
sudo apt-get install samba
```

Dann die smb.conf sichern und editieren:
```
sudo mv /etc/samba/smb.conf /etc/samba/smb.conf.bak
sudo nano /etc/samba/smb.conf
```
In die Datei folgendes einfügen:
```
[global]
    workgroup = WORKGROUP
    server string = SmartHome
    domain master = no
    syslog only = no
    syslog = 10
    panic action = /usr/share/samba/panic-action %d
    encrypt passwords = true
    passdb backend = tdbsam
    obey pam restrictions = yes
    unix password sync = yes
    unix extensions = no
    passwd program = /usr/bin/passwd %u
    passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .
    pam password change = yes
    map to guest = bad user
    invalid users = root
    guest ok = no
    usershare allow guests = no
    # disable printing
    load printers = no
    printing = bsd
    printcap name = /dev/null
    disable spoolss = yes

[Logs]
    path = /var/log
    comment = Logfiles
    available = yes
    browseable = yes
    writable = yes
    force user = root
    force group = root
    create mask = 0755
    directory mask = 0775

[SmartHome.py]
    path = /usr/local/smarthome
    comment = SmartHome.py Directories
    available = yes
    browseable = yes
    writable = yes
    force user = smarthome
    force group = smarthome
    create mask = 0664
    directory mask = 0775

[smartVISU]
    path = /var/www/html/smartVISU
    comment = smartVISU Directories
    available = yes
    browseable = yes
    writable = yes
    force user = www-data
    force group = www-data
    create mask = 0775
    directory mask = 0775
```

Nun muß der User smarthome noch bekannt gemacht werden mit ```sudo smbpasswd -a smarthome```.

Im Windows Explorer sollten nun via **\\<IP des Rechners oder hostname>** zwei Freigaben angezeigt werden.

Da bei Samba immer wieder Sicherheitslöcher aufgedeckt werden, empfiehlt sich ein Ausschluß des SMB1 Protocols. Näheres dazu [hier](https://www.samba.org/samba/docs/man/manpages-3/smb.conf.5.html)

## Abschlussarbeiten

Jetzt müsste alles installiert sein und alles funktionieren. Wenn nicht, dann bitte prüfen,
ob wirklich alles so durchgeführt wurde wie beschrieben. 
Ansonsten siehe [Fehlersuche](https://github.com/smarthomeNG/smarthome/wiki/SolveProblems).

### Weitere Konfiguration

Wer noch keine Erfahrung mit dem Erstellen von Items und der Konfiguration hat, kann als weiteren Einstieg [[hier|Initiale_Item-Konfiguration]] weiterlesen.

### Mehr Komfort via SSH Zugriff

Manche Kommandos auf der Shell gehen einfacher von der Hand, wenn man Abkürzungen nutzen kann. 
Folgende Kommandos bieten sich an:

```
alias la='ls -A'
alias ll='ls -l'
alias ls='ls --color=auto'
alias ..='cd ..'
alias cli='rlwrap telnet $IP 2323'
alias e='grep "FATAL\|ERROR\|WARNING\|CRITICAL"'
alias sh.error='tail -f -n 500 /var/log/smarthome/smarthome.log | e | colorize yellow .*WARNING.* purple .*ERROR.* red .*CRITICAL.* red .*FATAL.* '
alias sh.log='tail -f -n 50 /var/log/smarthome/smarthome.log | colorize green .*INFO.* yellow .*WARNING.* purple .*ERROR.* gray .*DEBUG.* red .*CRITICAL.* red .*FATAL.* '
```
Ein guter Ort die einzufügen ist die ``.bashrc`` des Benutzers **smarthome**.

```
cd ~
nano .bashrc
```

Um das colorize-Skript einzusetzen, muss es zuerst heruntergeladen und korrekt verschoben werden:
```
cd ~
wget http://www.fam.tuwien.ac.at/~schamane/_/_media/bash:mycolorize-r.sh
mv mycolorize.sh /usr/local/bin/colorize
chmod u+x /usr/local/bin/colorize
```

rlwrap wird voraussichtlich noch zu installieren sein:
```
apt-get install rlwrap
```


### SmartHomeNG als Dienst einrichten
Um SmartHomeNG als Dienst zu betreiben muß dazu noch eine Startup-Datei für systemd erstellt werden. Dazu den Texteditor anwerfen mit
```
sudo nano /lib/systemd/system/smarthome.service
```

und folgenden Text hineinkopieren:

```
[Unit]
Description=SmartHomeNG daemon
After=network.target
After=knxd.service
After=knxd.socket

[Service]
Type=forking
ExecStart=/usr/bin/python3 /usr/local/smarthome/bin/smarthome.py
User=smarthome
PIDFile=/usr/local/smarthome/var/run/smarthome.pid
Restart=on-abort

[Install]
WantedBy=default.target
```

Der so vorbereitete Dienst kann über den systemctl Befehl gestartet werden.
```
sudo systemctl start smarthome.service
```
Im Log schauen, ob keine Fehlermeldung beim Starten geschrieben wurde.

```
tail /usr/local/smarthome/var/log/smarthome.log
```

Wenn alles ok ist, kann der Autostart aktiviert werden:
```
sudo systemctl enable smarthome.service
```
Bei Systemstart wird nun SmartHomeNG automatisch gestartet.

Um den Dienst wieder auszuschalten und den Neustart bei Systemstart zu verhindern nutzt man:
```
sudo systemctl disable smarthome.service
```

Um zu sehen, ob SmartHomeNG läuft, genügt ein

```
sudo systemctl status smarthome.service
```

Läuft es noch nicht und man möchte sozusagen manuell starten reicht ein:

```
sudo systemctl start smarthome.service
```

Ein Neustart von SmartHomeNG würde mit 
```
sudo systemctl restart smarthome.service
```
funktionieren, ein Stop von SmartHomeNG entsprechend
```
sudo systemctl stop smarthome.service
```
