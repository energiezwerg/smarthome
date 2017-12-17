# Debian Linux installieren

- Schritte der Installation:
    - [Softwareauswahl](#softwareauswahl)
    - [Einloggen via SSH  oder an der Konsole](#einloggen-via-ssh--oder-an-der-konsole)
    - [Systemaktualisierung](#systemaktualisierung)
    - [Restarbeiten am System](#restarbeiten-am-system)

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

