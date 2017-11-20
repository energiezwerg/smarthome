# Berechnung der Daten für das SmartVisu icon.zenith

Berechnungen für icon.zenith:

```python
#!/usr/bin/env python3
# testlogik1.py

now = datetime.datetime.utcnow().hour * 60 + datetime.datetime.utcnow().minute
sunrise = sh.sun.rise().hour * 60 + sh.sun.rise().minute
sunset = sh.sun.set().hour * 60 + sh.sun.set().minute
icon = int(round(255 * ((now - sunrise) / (sunset - sunrise)),0))
sh.weather.sun.icon(icon)
```

Einbindung in der SmartVISU:

```
 {% import "icon.html" as icon %}
 {{ icon.zenith('weather.sun.icon', '', 'weather.sun.icon') }}
```

