# Abschlussarbeiten

- Schritte der Installation:
    - [Weitere Konfiguration](#weitere-konfiguration)
    - [Mehr Komfort via SSH Zugriff](#mehr-komfort-via-ssh-zugriff)
    - [SmartHomeNG als Dienst einrichten](#smarthomeng-als-dienst-einrichten)


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


## SmartHomeNG als Dienst einrichten
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
