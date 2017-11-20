# Beaufort Berechnung aus Windgeschwindigkeit

Windangabe in m/s als num. Am Beispiel Wert der Wetterstation:

```python
#!/usr/bin/env python3
# beaufort1.py

 if sh.knx_global.weather.wind() < 0.3:  
     sh.knx_global.weather.wind.string("Windstille")
     sh.knx_global.weather.wind.beaufort(0)
 elif sh.knx_global.weather.wind() >= 0.3 and sh.knx_global.weather.wind() < 1.6:
     sh.knx_global.weather.wind.string("leiser Zug")
     sh.knx_global.weather.wind.beaufort(1)
 elif sh.knx_global.weather.wind() >= 1.6 and sh.knx_global.weather.wind() < 3.4:
     sh.knx_global.weather.wind.string("leichte Brise")
     sh.knx_global.weather.wind.beaufort(2)
 elif sh.knx_global.weather.wind() >= 3.4 and sh.knx_global.weather.wind() < 5.5:
     sh.knx_global.weather.wind.string("schwacher Wind")
     sh.knx_global.weather.wind.beaufort(3)
 elif sh.knx_global.weather.wind() >= 5.5 and sh.knx_global.weather.wind() < 8.0:
     sh.knx_global.weather.wind.string("mäßiger Wind")
     sh.knx_global.weather.wind.beaufort(4)
 elif sh.knx_global.weather.wind() >= 8.0 and sh.knx_global.weather.wind() < 10.8:
     sh.knx_global.weather.wind.string("frischer Wind ")
     sh.knx_global.weather.wind.beaufort(5)
 elif sh.knx_global.weather.wind() >= 10.8 and sh.knx_global.weather.wind() < 13.9:
     sh.knx_global.weather.wind.string("starker Wind")
     sh.knx_global.weather.wind.beaufort(6)
 elif sh.knx_global.weather.wind() >= 13.9 and sh.knx_global.weather.wind() < 17.2:
     sh.knx_global.weather.wind.string("steifer Wind")
     sh.knx_global.weather.wind.beaufort(7)
 elif sh.knx_global.weather.wind() >= 17.2 and sh.knx_global.weather.wind() < 20.8:
     sh.knx_global.weather.wind.string("stürmischer Wind")
     sh.knx_global.weather.wind.beaufort(8)	
 elif sh.knx_global.weather.wind() >= 20.8 and sh.knx_global.weather.wind() < 24.5:
     sh.knx_global.weather.wind.string("Sturm")
     sh.knx_global.weather.wind.beaufort(9)
 elif sh.knx_global.weather.wind() >= 24.5 and sh.knx_global.weather.wind() < 28.5:
     sh.knx_global.weather.wind.string("schwerer Sturm")
     sh.knx_global.weather.wind.beaufort(10)
 elif sh.knx_global.weather.wind() >= 28.5 and sh.knx_global.weather.wind() < 32.7:
     sh.knx_global.weather.wind.string("orkanartiger Sturm")
     sh.knx_global.weather.wind.beaufort(11)
 else:
     sh.knx_global.weather.wind.string("Orkan")
     sh.knx_global.weather.wind.beaufort(12)
```

Quelle der Zuordnung m/s zu Bft: [Wikipedia](https://de.wikipedia.org/wiki/Beaufortskala)

## Alternative Umsetzung mit Funktion

```python
#!/usr/bin/env python3
# beaufort2.py

def get_beaufort(speed):
    """
    returns a tuple of a string with the (german) description and an integer with beaufort speed
    """
    if speed < 0.3:  
        return("Windstille",0)
    elif speed >= 0.3 and speed < 1.6:
        return("leiser Zug",1)
    elif speed >= 1.6 and speed < 3.4:
        return("leichte Brise",2)
    elif speed >= 3.4 and speed < 5.5:
        return("schwacher Wind",3)
    elif speed >= 5.5 and speed < 8.0:
        return("mäßiger Wind",4)
    elif speed >= 8.0 and speed < 10.8:
        return("frischer Wind ",5)
    elif speed >= 10.8 and speed < 13.9:
        return("starker Wind",6)
    elif speed >= 13.9 and speed < 17.2:
        return("steifer Wind",7)
    elif speed >= 17.2 and speed < 20.8:
        return("stürmischer Wind",8)	
    elif speed >= 20.8 and speed < 24.5:
        return("Sturm",9)
    elif speed >= 24.5 and speed < 28.5:
        return("schwerer Sturm",10)
    elif speed >= 28.5 and speed < 32.7:
        return("orkanartiger Sturm",11)
    else:
        return("Orkan",12)
        
decription, bft = get_beaufort(sh.knx_global.weather.wind())
sh.knx_global.weather.wind.string(description)
sh.knx_global.weather.wind.beaufort(bft)
```

## Alternative Umsetzung als Funktion mit Lookup

```python
#!/usr/bin/env python3
# beaufort3.py

def get_beaufort(speed):
    """
    returns a tuple of a string and an integer with the (german) description and speed class
    """
    table = [ 
        (  0.3, "Windstille",0),
        (  1.6, "leiser Zug",1),
        (  3.4, "leichte Brise",2),
        (  5.5, "schwacher Wind",3),
        (  8.0, "mäßiger Wind",4),
        ( 10.8, "frischer Wind ",5),
        ( 13.9, "starker Wind",6),
        ( 17.2, "steifer Wind",7),
        ( 20.8, "stürmischer Wind",8),
        ( 24.5, "Sturm",9),
        ( 28.5, "schwerer Sturm",10),
        ( 32.7, "orkanartiger Sturm",11),
        ( 999,  "Orkan",12) ]
    
    try:
        description = min(filter(lambda x: x[0] >= speed, table))[1]
        bft = min(filter(lambda x: x[0] >= speed, table))[2]
        return description,bft
    except ValueError:
        return None

decription, bft = get_beaufort(sh.knx_global.weather.wind())
sh.knx_global.weather.wind.string(description)
sh.knx_global.weather.wind.beaufort(bft)
```
