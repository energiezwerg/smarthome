eval Ausdrücke
##############

Eval Syntax
===========

Der Syntax eines **eval** Ausdrucks ist der Syntax einer `Python conditional expression <https://www.python.org/dev/peps/pep-0308/>`_

Dieser Syntax wird bei den Item Attributen **eval**, **on_change** und **on_update** verwendet.

Beispiel:

``eval=value if value>0 else 0``

Es ist zu beachten, dass in diesen Ausdrücken ein **if** nicht ohne **else** möglich ist. Wenn
man bei einem Ausdruck bei Nichtzutreffen des **if** Zweiges keine Aktion/Zuweisung durchführen
möchte, muss man **else None** an die **if** Anweisung hängen. Also:

- Falsch: ``eval=value if value>0``
- Richtig: ``eval=value if value>0 else None``



Eval Trigger
------------

Ein häufiger Fehler bei der Nutzung von **eval** im Zusammenspiel mit **eval_trigger** ist,
bei **eval_trigger** auch den vollen Python-Pfad zu einem SmartHomeNG Item zu verwenden, wie
im **eval** Ausdruck. 

Richtig ist es, bei **eval_trigger** nur der Item-Pfad zu nutzen (ohne führendes **sh.** und 
ohne folgende **()**).


**Correct**: 

- eval: **sh.** my.value **()**
- eval_trigger: my.value | my.other.value

**incorrect**:

- eval: sh.my.value
- eval_trigger: **sh.** my.value | **sh.** my.other.value

