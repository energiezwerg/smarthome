
# lib/env/location.py

if sh.sun:
    sunrise = sh.sun.rise().astimezone(sh.tzinfo())
    sh.env.location.sunrise(sunrise)
    azimut_rise, elevation_rise = sh.sun.pos(dt=sunrise)
    azimut_rise = round(azimut_rise,2)
    elevation_rise = round(elevation_rise,2)
    sh.env.location.sunrise.azimut(azimut_rise)
    sh.env.location.sunrise.elevation(elevation_rise)

    sunset = sh.sun.set().astimezone(sh.tzinfo())
    sh.env.location.sunset(sunset)
    azimut_set, elevation_set = sh.sun.pos(dt=sunset)
    azimut_set = round(azimut_set,2)
    elevation_set = round(elevation_set,2)
    sh.env.location.sunset.azimut(azimut_set)
    sh.env.location.sunset.elevation(elevation_set)

    # setting altitude/azimut
    azimut, elevation = sh.sun.pos(degree=True)
    azimut = round(azimut,2)
    elevation = round(elevation,2)
    sh.env.location.sun_position.azimut(azimut)
    sh.env.location.sun_position.elevation(elevation)
    

    sh.env.location.moonrise(sh.moon.rise().astimezone(sh.tzinfo()))
    sh.env.location.moonset(sh.moon.set().astimezone(sh.tzinfo()))
    sh.env.location.moonphase(sh.moon.phase())

    # setting day and night
    day = sh.sun.rise(-6).day != sh.sun.set(-6).day
    sh.env.location.day(day)
    sh.env.location.night(not day)
