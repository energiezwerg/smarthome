# Initiale Item-Konfiguration

## Beispiele für erstmaliges Setup

Das Rückgrat von smarthomeNG bilden die Items. Jedes Item kann (muss aber nicht) bestimmte Eigenschaften haben. 
Eigenschaften (Attribute) sind z.B. welcher Datentyp ein Item ist oder wie das Item gelesen oder geschrieben werden kann. Wie welches Item gelesen und geschrieben werden kann, hängt von den installierten Plugins ab.

Ein kleines Beispiel: Du möchtest eine Lampe über KNX ein- und ausschalten. Dazu brauchst du zwei Schritte:

Erstens, du installierst/aktivierst das **KNX Plugin**. Das geschieht in der datei **../etc/plugins.yaml**. Typischerweise sieht der entsprechende Eintrag dann so aus

```yaml
knx:
   class_name: KNX
   class_path: plugins.knx
   host: 127.0.0.1
```

Als nächsten Schritt legst Du ein Item an, um die Lampe zu schalten. Hierzu legst du eine Datei (mit beliebigem Namen) im Verzeichnis **../items** an, welche auf die Endung **.yaml** hört,
z.B. die Datei **../items/Lampen.yaml**. In dieser Datei legst du nun das Item an. Das geschieht einfach über den Doppelpunkt der dem Namen folgt. 
Der Inhalt der Datei wäre also:

```yaml
Lampe:
```

Das ist wenig spannend, denn die Lampe soll ja vielleicht an- und ausgeschalten werden. Der passende Datentyp wäre bool. 
Damit sieht die Item-Definition wie folgt aus:

```yaml
Lampe:
    type: bool
```

Nächster Schritt ist in dem Item anzugeben, dass es über das KNX Plugin verändert werden kann, bzw. Veränderungen am Item auf dem KNX gesendet werden sollen.

Das Item muss also entsprechend erweitert werden. Dazu muss der KNX DPT und Gruppenadressen zum Senden und Empfangen angegeben werden. Das sieht dann z.B. so aus:

```yaml
Lampe:
    type: bool
    knx_dpt: 1
    knx_listen: 1/1/133
    knx_send: 1/1/130
```

Allerdings kann es jetzt ja sein, dass die Lampe auch dimmbar ist. Dazu musst du ein weiteres Item anlegen.
Dazu brauchst du ein neues Item, welches dann so aussieht:

```yaml
LampeDimmen:
    type: num
    knx_dpt: 5
    knx_listen: 1/1/134
    knx_send: 1/1/132
```

Allerdings würde das schnell unübersichtlich werden. Daher kann man Items auch schachteln. Das geschieht duch einrücken der entsprechenden Blöcke in der yaml Datei.

Für das Beispiel mit der Lampe, welche über KNX gesteuert wird könnte man es also so gestalten:

```yaml
Lampe:
    schalten:
        type: bool
        knx_dpt: 1
        knx_listen: 1/1/133
        knx_send: 1/1/130
    dimmen:
        type: num
        knx_dpt: 5
        knx_listen: 1/1/134
        knx_send: 1/1/132      
```


Um den Überblick zu behalten, halte ich mich an folgendes Schema:

```yaml
Stockwerk:
    Raum:
        Gewerk:
            Ort:
                Eigenschaft:

```

Beispiel:

```yaml
EG:
    Bad:
        Licht:
            Decke:
                schalten:
                    type: bool
                    knx_dpt: 1
                    knx_listen: 1/1/133
                    knx_send: 1/1/130
                dimmen:
                    type: num
                    knx_dpt: 5
                    knx_listen: 1/1/134
                    knx_send: 1/1/132      
```

Ein solches Schema hat den Vorteil, dass man mit ``*.*.Licht.*.schalten`` auf alle Lampen im Haus zugreifen kann, beispielsweise um eine Logik auszulösen.

Bislang ist das ganze aber immer noch langweilig. Du möchtest nämlich z.B. mittels der smartVisu ein Item verändern.

Kein Problem, dazu muss das nur dem Item mitgeteilt werden. Dazu muss das Item das entsprechende Attribut bekommen. Im Beispiel mit der Lampe wäre das:

```yaml
Lampe:
    schalten:
        type: bool
        knx_dpt: 1
        knx_listen: 1/1/133
        knx_send: 1/1/130
        visu_acl: rw
```

Damit das funktioniert, muss das Websocket Plugin aktiviert sein. Hierzu in der **../etc/plugin.yaml** folgenen Eintrag anlegen:

```yaml
visu:
    class_name: WebSocket
    class_path: plugins.visu_websocket
```

Falls du jetzt auf die Idee kommst, die Lampe auch mittels Dash-Button zu schalten, muss das Item einfach noch um das Dash-Button Attribut erweitert werden:

```yaml
Lampe:
    schalten:
        type: bool
        knx_dpt: 1
        knx_listen: 1/1/133
        knx_send: 1/1/130
        visu_acl: rw
        dashbutton_mac:  AC:63:B0:02:CA:12
        dashbutton_mode: 'flip'      
```

D.h. man kann die Lampe nun via KNX, SmartVisu oder Dashbutton ein- und ausschalten. 

Aber auch hier gilt: Funktioniert nur, wenn das dashbutton plugin in der ``/etc/plugin.yaml`` aktiviert ist.

Wie man grundsätzlich die verschiedenen Plugins in der **../etc/plugin.yaml** konfiguriert, steht im Abschmitt **Konfiguration/Plugins** der Doku.
Auch wie die Attribute in den Items gesetzt werden müssen, ist für jedes Plugin in der Doku der **Plugins** zu finden.

