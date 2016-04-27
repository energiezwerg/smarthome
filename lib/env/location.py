
# lib/env/location.py
import math

if sh.sun:
    sunrise = sh.sun.rise().astimezone(sh.tzinfo())
    sh.env.location.sunrise(sunrise)
    azimut_rise, elevation_rise = sh.sun.pos(dt=sunrise)
    sh.env.location.sunrise.azimut.degrees(round(math.degrees(azimut_rise), 2))
    sh.env.location.sunrise.elevation.degrees(round(math.degrees(elevation_rise), 2))
    sh.env.location.sunrise.azimut.radians(round(azimut_rise,2))
    sh.env.location.sunrise.elevation.radians(round(elevation_rise,2))

    sunset = sh.sun.set().astimezone(sh.tzinfo())
    sh.env.location.sunset(sunset)
    azimut_set, elevation_set = sh.sun.pos(dt=sunset)
    sh.env.location.sunset.azimut.degrees(round(math.degrees(azimut_set), 2))
    sh.env.location.sunset.elevation.degrees(round(math.degrees(elevation_set), 2))
    sh.env.location.sunset.azimut.radians(round(azimut_set,2))
    sh.env.location.sunset.elevation.radians(round(elevation_set,2))


    # setting altitude/azimut
    azimut, elevation = sh.sun.pos()
    sh.env.location.sun_position.azimut.degrees(round(math.degrees(azimut), 2))
    sh.env.location.sun_position.elevation.degrees(round(math.degrees(elevation), 2))
    sh.env.location.sun_position.azimut.radians(round(azimut,2))
    sh.env.location.sun_position.elevation.radians(round(elevation,2))

    sh.env.location.moonrise(sh.moon.rise().astimezone(sh.tzinfo()))
    sh.env.location.moonset(sh.moon.set().astimezone(sh.tzinfo()))
    sh.env.location.moonphase(sh.moon.phase())

    # setting day and night
    day = sh.sun.rise(-6).day != sh.sun.set(-6).day
    sh.env.location.day(day)
    sh.env.location.night(not day)
