# knxd installieren

- Schritte der Installation:
    - [zusätzliche Pakete installieren](#zusätzliche-pakete-installieren)
    - [Quellcode laden, compilieren und ein Paket schnüren](#quellcode-laden-compilieren-und-ein-paket-schnüren)
    - [knxd konfigurieren](#knxd-konfigurieren)
    - [knxd und systemd](#knxd-und-systemd)



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


<!--- Die Installation auf einem frischen Jessie zeigt 
folgende nicht erfüllte Bauabhängigkeiten:
debhelper (>= 7.0.0)
autotools-dev
autoconf
automake
libtool
libusb-1.0-0-dev (>= 1.0.9) pkg-config
libsystemd-dev (>= 228) | libsystemd-daemon-dev (>= 200) | base-files (<< 8)
dh-systemd | base-files (<< 8) libev-dev
--->

<!---
Diese Abhängigkeiten werden mit den nachfolgenden Paketinstallationen aufgelöst.
Wenn sich **dpkg-buildpackage** über weitere fehlende Pakete beschweren sollte,
("Unmet build dependencies"): dann sollten sie nachinstalliert
(``sudo apt-get install …``) und ein neuer Versuch gestartet werden.<br>
Wenn **x | y** gefordert wird, erstmal nur **x** installieren.
Wenn das nicht funktioniert, kann auch **y** installiert werden<br>
Bei Beschwerden über inkompatible Pakete können diese ggf. entfernt werden.
Bitte in obigem Fall die Komplettanleitung anpassen !!!
--->

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


