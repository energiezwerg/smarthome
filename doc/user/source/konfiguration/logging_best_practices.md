# Logging - Best Practices

Die im folgenden beschriebene Logging Konfiguration erzeugt zwei Logfiles:

* Ein Hauptlog (smarthome.log), welches alle WARNINGs, ERRORs und CRITICAL errors des Cores und aller Plugins empfängt
* Ein Zusatzlog (smarthome-additional.log), welches frei konfigurierbar Logeinträge verschiedener Module und Plugins empfängt.

Das hat den Vorteil, dass das Hauptlog übersichtlich bleibt weil dort nur Warnungen und Fehler eingetragen werden. Anderseits kann man für einen oder mehrere Teile von SmartHomeNG der einen besonders interessiert, den Loglevel auf INFO oder DEBUG hochsetzen, ohne den Loglevel des Root-Loggers anzuheben und sich im Hauptlog durch Mengen von Einträgen aller Plugins wühlen zu müssen, die einen nicht interessieren.

Diese Best Practices haben folgende Abschnitte:

  * [Grundkonfiguration des Loggings](#grundkonfiguration-des-loggings)
  * [Konfiguration zusätzlicher Logausgaben](#konfiguration-zusätzlicher-logausgaben)
  * [Identifizieren von Neustarts im Zusatzlog](#identifizieren-von-neustarts-im-zusatzlog)
  * [Ein besserer simple-Formatter](#ein-besserer-simple-formatter) für das Hauptlog (und das Zusatzlog)

  [Erweiterte Konfigurationen des Loggings](#erweiterte-konfigurationen-des-loggings)
  * [Erweitertes Logging für die Plugin Entwicklung](#erweitertes-logging-für-die-plugin-entwicklung)


## Grundkonfiguration des Loggings

Die grundsätzliche Konfiguration des Loggings sieht dann so aus:

```yaml
# etc/logging.yaml

version: 1
disable_existing_loggers: False
formatters:
    simple:
        format: '%(asctime)s %(levelname)-8s %(threadName)-12s %(message)s'
        datefmt: '%Y-%m-%d  %H:%M:%S'

handlers:
    console:
        class: logging.StreamHandler
        formatter: simple
        stream: ext://sys.stdout

    file:
        class: logging.handlers.TimedRotatingFileHandler
        formatter: simple
        level: WARNING
        when: midnight
        backupCount: 7
        filename: ./var/log/smarthome.log
        encoding: utf8

    file_additional:
        class: logging.handlers.TimedRotatingFileHandler
        formatter: simple
        level: DEBUG
        when: midnight
        backupCount: 7
        filename: ./var/log/smarthome-additional.log
        encoding: utf8

loggers:
    __main__:
        level: WARNING
        handlers: [file]

root:
    level: WARNING
    handlers: [file]
```

Sie loggt nur Warnungen und Fehler in das Hauptlog. Das Zusatzlog wird nicht beschrieben. Diese Grundkonfiguration definiert drei handler (Ziele für Logausgaben):

* Die Konsole
* Das Logfile **smarthome.log**, welches nur nur Warnungen und Fehler aufnimmt
*  Das Logfile **smarthome-additional.log**, welches prinzipiell alle Logmeldungen (von DEBUG bis CRITICAL) aufnimmt

Die beiden Handler die Logfiles schreiben, sind als rotierende Handler ausgelegt, die in eigenen Dateien die Logeinträge der letzten sieben Tage aufheben. 

> **Note**: Die Rotation der Logfiles erfolgt um Mitternacht GMT, also nicht unbedingt um Mitternacht lokaler Zeit.

> **Note**: Die Änderungen in der Konfiguration werden erst bei einem Neustart von SmartHomeNG wirksam.

## Konfiguration zusätzlicher Logausgaben

Um zusätzliche Logausgaben zu konfigurieren muss nur der Abschnitt **logger:** der Logging Konfiguration angepasst/erweitert werden.

Die meisten Plugins schreiben ihre Logausgaben in in einen eigenen Logger, falls dieser in **logging.yaml** definiert ist. Die Logausgaben werden dann in diesen eigenen Logger und in den root-Logger geschrieben. Die Konfiguration des root-Loggers verhindert, das INFO und DEBUG ausgaben ins Hauptlog kommen. 

Welche Ausgaben in das Zusatzlog kommen, wird durch die Konfiguration der einzelnen Logger festgelegt. Prinzipiell kann das Zusatzlog ja alle Loglevel aufnehmen.

Um zum Beispiel für das Plugin **mqtt** INFO Logausgaben zu schreiben, muss ein zusätzlicher Logger folgendermaßen konfiguriert werden:

```yaml
# Ausschnitt aus etc/logging.yaml

loggers:
    plugins.mqtt:
        handlers: [file_additional]
        level: INFO
```

Dieser Logger schreibt in das Zusatzlog und zwar bis zum Level INFO.

Wenn jetzt noch zusätzlich für das Plugin **enogw** DEBUG Logausgaben geschrieben werden sollen, muss ein weiterer Logger folgendermaßen konfiguriert werden:

```yaml
# Ausschnitt aus etc/logging.yaml

loggers:
    plugins.mqtt:
        handlers: [file_additional]
        level: INFO

    plugins.enogw:
        handlers: [file_additional]
        level: DEBUG
```

Nun werden INFO Logs des mqtt Plugins, sowie DEBUG und INFO Logs des enogw Plugins in das Zusatzlog geschrieben.

## Identifizieren von Neustarts im Zusatzlog

Im Hauptlog wird eine Zeile 

```
2017-08-18  10:44:37 WARNING  Main         --------------------   Init SmartHomeNG 1.3   --------------------
```
bei jedem Start von SmartHomeNG geschrieben, um die Neustarts im Log einfacher auffinden zu können. Diese Zeile gibt es im Zusatzlog standardmäßig nicht.

Wenn man diese Zeile auch im Zusatzlog haben möchte, muss man die WARNINGs des main-Loggers auch in das Zusatzlog lenken. Das geschieht indem man den logger **`__main__`** folgendermaßenkonfiguriert:

```yaml
# Ausschnitt aus etc/logging.yaml

loggers:
    __main__:
        handlers: [file_additional]
        level: WARNING

    plugins.mqtt:
        handlers: [file_additional]
        level: INFO

    plugins.enogw:
        handlers: [file_additional]
        level: DEBUG
```

## Ein besserer simple-Formatter

In der Standardkonfiguration von SmartHomeNG wird bisher nach Datum und Loglevel der Threadname vor der eigentlichen Logmessage ausgegeben:

```yaml
formatters:
  simple:
    format: '%(asctime)s %(levelname)-8s %(threadName)-12s %(message)s'
    datefmt: '%Y-%m-%d  %H:%M:%S'
```

Wenn man die Angabe `%(threadName)-12s`durch `%(name)-16s` ersetzt, wird stattdessen des Name des Loggers ausgegeben:

```yaml
formatters:
    simple:
        format: '%(asctime)s %(levelname)-8s %(name)-16s %(message)s'
        datefmt: '%Y-%m-%d  %H:%M:%S'
```

Das ist hilfreicher um zu identifizieren woher die Logmessage stammt.

## Erweiterte Konfigurationen des Loggings

Mit den obigen Hinweisen hat man eine übersichtliche Log Umgebung und Konfiguration, die den meisten Anforderungen genügt. Wenn man dennoch darüber hinausgehende Anforderungen hat, kann man dieses Logging Modell auch noch erweitern.


### Erweitertes Logging für die Plugin Entwicklung

Für die Entwicklung von Plugins kann es hilfreich sein, wenn man im Log sehen kann, aus welchem Teil des Plugins die Logmessage kommt. Dazu kann man einen Formatter schreiben, der die Funktion/Methode die das Log geschrieben hat mit anzeigt.

Dazu erzeugt man einen zusätzlichen Formatter als Kopie aus dem (verbesserten) simple Formatter und nennt ihn `funcname`.
Dann fügt man den Platzhalter `%(funcName)-16s ` in den Format-String ein, der den Funktionsnamen ausgibt.

```yaml
formatters:
    simple:
        format: '%(asctime)s %(levelname)-8s %(name)-16s %(message)s'
        datefmt: '%Y-%m-%d  %H:%M:%S'
    funcname:
        format: '%(asctime)s %(levelname)-8s %(name)-16s %(funcName)-16s %(message)s'
        datefmt: '%Y-%m-%d  %H:%M:%S'
```

Damit dieser neue Formatter auch genutzt wird, muss er noch im Handler `file_additional`an Stelle des `simple` Formatters eingetragen werden:

```yaml
handlers:
    file_additional:
        class: logging.handlers.TimedRotatingFileHandler
        formatter: funcname
        level: DEBUG
        when: midnight
        backupCount: 7
        filename: ./var/log/smarthome-additional.log
        encoding: utf8
```

Das bewirkt, dass im Zusatzlog die Funktionsnamen mit geloggt werden, während im Hauptlog das Logging unverändert das `simple` Format nutzt.

