#  Onewire installieren


- Schritte der Installation:
    - [zusätzliche Pakete installieren](#zusätzliche-pakete-installieren-3)
    - [owfs konfigurieren](#owfs-konfigurieren)


### zusätzliche Pakete installieren

Für den Zugriff von SmartHomeNG auf einen OneWire Bus kann das owserver Paket genutzt werden.
Die dazu benötigten Komponenten werden installiert mit:

```
sudo apt-get -y install owhttpd owserver
```

### owfs konfigurieren
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

Wichtig dabei ist vor allem das in der Config nicht ***localhost*** steht sondern ***127.0.0.1*** explizit angegeben wird. 
Dadurch wird eine Bindung des Ports **4304** an eine normale IP erreicht und nicht an IPv6 wie es sonst der Fall wäre. 
Mit tcp6 wiederum könnte das Smarthome.py derzeit nichts anfangen.

Bei der Installation werden owserver und owhttp automatisch gestartet.
Nach der Konfigurationsänderung muß der owserver neu gestartet werden:

```
sudo systemctl restart owserver
```

Damit das Onewire-Plugin von SmartHomeNG genutzt werden kann, muß in der **../etc/plugin.yaml** bzw. **../etc/plugin.conf** müssen beim **ow:**-Abschnitt bzw. **[ow]**-Abschnitt und den direkt nachfolgenden Zeilen die führenden Kommentarzeichen **#**
entfernt werden.

