# smartVISU installieren

- Schritte der Installation:
    - [zusätzliche Pakete installieren](#zusätzliche-pakete-installieren-2)
    - [SmartVISU Quellcode laden](#smartvisu-quellcode-laden)


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

> **Achtung**: Wenn PHP 7 installiert ist/wird muss darauf geachtet werden, dass im Gegensatz zu älteren Versionen das Paket **mbstring** nicht mit installiert wird. Es muss mit den folgenden Kommandos nachinstalliert werden:
>
```
sudo apt-get install php7.0-mbstring
sudo service apache2 restart
```

### SmartVISU Quellcode laden 
Stand 18. Februar 2018 wird die letzte verfügbare Master-Version 2.8 der SmartVISU geladen.
Seit Dezember 2017 steht die Version 2.9 in den Startlöchern.
Diese Dokumentation ist nicht tagesaktuell, daher bitte vor dem Installieren
[auf der Projektseite](http://www.smartvisu.de/) prüfen, welches der aktuelle Master ist.
Eine alternative Installation der SmartVISU 2.9 ist möglich, es sollten aber
idealerweise **git** Kenntnisse vorhanden sein.
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

#### Variante 1

Alle Dateien erhalten als Besitzer und Gruppe www-data. Das versetzt den Webserver Apache2 in die Lage auf die 
Dateien zuzugreifen.

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

#### Variante 2

Es scheint mit der obigen Variante Probleme zu geben, wenn mit ``git pull`` Aktualisierungen geholt werden. Da man nicht als **www-data** angemeldet ist gibt es Zugriffprobleme mit git. 
Als Alternative hier die im Forum diskutierte Variante:

```
cd /var/www/html
sudo rm index.html
sudo mkdir smartVISU
sudo chown smarthome:www-data smartVISU
# guid setzen
chmod g+rws smartVISU/
cd smartVISU
git clone git://github.com/Martin-Gleiss/smartvisu.git .
# Apache2 Zugriff erlauben
sudo find . -type d -exec chmod g+rwsx {} +
sudo find . -type f -exec chmod g+r {} +
```

#### Alternativ: SmartVISU 2.9 develop

Optional umschalten auf die SmartVISU 2.9 develop Version geht über eine Shell
im Verzeichnis der smartVISU mit

```
git checkout develop
```

ein zurückwechseln auf den masterbranch entsprechend mit

```
git checkout master
```

### Zugriff auf die SmartVISU testen

Mit einem Browser kann nun erstmals auf die SmartVISU zugegriffen werden:
Hierbei ist ``<ip-des-servers>`` natürlich mit der IP oder dem Hostnamen deines SmartVISU Servers ersetzen: 
``http://<ip-des-servers>/smartVISU``
Bei **Checking your configuration** sollte alles mit einem grünen Häckchen versehen sein.
Über den Knopf **Config** kommt man ins SmartVISU Interface direkt auf die Config Seite.

Bei I/O Connection **Smarthome.py** auswählen. [Ab SmartVISU 2.9 **SmartHomeNG** auswählen].
Bei Adresse (URL / IP) die IP Adresse des Servers oder den DNS Namen eingeben auf dem SmartHomeNG installiert ist.
Bei Port ist standardmäßig ``2424`` einzugeben.

**ACHTUNG**: 
Hier **NICHT** ***localhost*** oder ***127.0.0.1*** eingeben, 
denn diese Adresse wird vom Client Browser benutzt (Javascripts) 
um aktuelle Daten über einen Websocket direkt von SmartHomeNG abzufragen. 

Im Tab **Interfaces** muß noch die anzuzeigende Visuseite eingestellt werden.
Dort kann unter anderem gewählt werden zwischen verschiedenen Demoseiten.

Um die Einstellungen zu sichern bitte Save auswählen.
[In älteren Visuversionen mußte zweimal auf Save gedrückt werden,
das sollte mit SV 2.9 behoben sein.]

#### Eigene Visuseiten anlegen

Um mit der SmartVISU eine eigene Visu anzulegen, muß innerhalb des Ordners
``pages`` der SmartVISU ein neues Verzeichnis angelegt werden,
in dem dann die eigenen Seiten z.B. für Räume oder Funktionsbereich abgelegt werden.
Es existiert im Ordner ``pages`` bereits ein Unterordner ``_template``.
Dieser wird als Basis der neuen Visu einfach kopiert ``cp _template <meineneuevisu>``.
Für <meineneuevisu> sollte ***nicht smarthome*** gewählt werden wenn später
die Visu vom SmartHomeNG Plugin **visu_smartvisu** erstellt werden soll.
Die manuell erstellten Seiten könnten sonst einfach von SmartHomeNG überschrieben werden.
Die Dateien für die SmartVISU sind einfache HTML Dateien. Die einzelnen Schalter, Buttons, Anzeigen (sogenannte Widgets) sind Makros die mit der Makrosprache TWIG definiert sind.
Die HTML können auf eigene Bedürfnisse beliebig angepasst werden.
Im einzelnen ist das [auf der Projektseite](http://www.smartvisu.de/) nachzulesen.

### SmartHomeNG Plugin __visu_smartvisu__

Mit dem Plugin ***visu_smartvisu*** können aus der Definition der Items in
SmartHomeNG automatisch Visuseiten erstellt werden. Diese Visuseiten werden
im Verzeichnis ``smarthome`` erstellt.
Dazu bitte beim entsprechenden Plugin die Doku lesen.
