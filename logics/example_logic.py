#!/usr/bin/env python3
# logics/example_logic.py

# Diese Logik zeigt, wie Logeinträge verschiedener Levels in die Logdateien eingetragen werden.
#
# Dazu:
# - Diese Logik aktivieren
# - Diese Logik triggern (anschließend kann die Logik wieder deaktiviert werden
# - die Einträge in ../var/log/smarthome-warnings.log und ../var/log/smarthome-details.log prüfen

logger.warning("Logik '{}' (filename '{}') wurde getriggert (WARNING)".format(logic.name, logic.filename))
logger.info("Logik '{}' (filename '{}') wurde getriggert (INFO)".format(logic.name, logic.filename))
logger.debug("Logik '{}' (filename '{}') wurde getriggert (DEBUG)".format(logic.name, logic.filename))

