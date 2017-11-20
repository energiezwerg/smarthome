# *on_update* und *on_change*

## Attribut *on_update*

Ermöglicht das setzen des Wertes anderer Items, wenn das aktuelle Item ein Update erhält (auch wenn sich der Wert des aktuellen Items dabei nicht ändert). **Ab SmartHomeNG v1.4**

Der Syntax ist folgender:
```
<item> = <expression>   # wobei <expression> den selben syntax nutzt, der bereits vom eval-Attribut bekannt ist
<single expression>     # eval-Attribut bekannt ist. Wenn die zweite Form (ohne <item> = ) genutzt wird,
                        # muss die Zuweisung innerhalb der expression erfolgen: Eine <single expression> der
                        # Form `sh.<item>(<expression>)` ist äquivalent zur ersten Syntax Form.
```

- Ausdrücke (Expressions) können en selben Syntax nutzen wie das **eval** Attribut.
- Ausdrücke können relative Item Adressierungen nutzen.
- Auch die Item Angabe in `<item> = <expresseion>` kann eine relative Angabe sein.
- Zu beachten ist, dass <item> eine reine Item Pfad Angabe ist, während in einem Ausdruck (wie auch bei eval), ein Item in der Form `sh.<item>()` adressiert werden muss.
- **on_update** kann zusammen mit **eval** im selben Item genutzt werden, wobei **eval** vor **on_update** ausgeführt wird. Dadurch enthält *value* in dem **on_update** Ausdruck den aktualisierten Wert des Items. Im Gegensatz dazu enthält *value* im **eval** Ausdruck den vorangegangenen Wert des Items. Wenn im **on_update** Ausdruck auf den vorangegangenen Wert des Items zugegriffen werden soll, geht das mit der Item-Methode `prev_value()`. Um das Item selbst zu adressieren kann am einfachsten die relative Adressierung eingesetzt werden. Den vorangegangenen Wert des Items erhält man mit `sh..prev_value()`.

Beispiel:
```yaml
itemA1:
    # eine einzelne Zuweisung
    on_update: itemB = 1                  # bei jedem Update von itemA1

itemA2:
    # eine Liste mehrerer Zuweisungen
    on_update:
    - itemC = False                       # nur wenn sich der Wert von itemA ändert
    - itemD = sh.itemB()                  # 
    - itemE = sh.itemB() if value else 0  # 
    ...

itemB:
    ...

itemC:
    ...
```

Im .conf Format (deprecated) sieht das Beispiel folgendermaßen aus:
```
[itemA1]
    # eine einzelne Zuweisung
    on_update = itemB = 1                  # bei jedem Update von itemA1

[itemA2]
    # eine Liste mehrerer Zuweisungen
    on_update = itemC = False | itemD = sh.itemB() | itemE = sh.itemB() if value else 0
    ...

[itemB]
    ...

[itemC]
    ...

```

## Attribut *on_change*

Ermöglicht das setzen des Wertes anderer Items, wenn der Wert des aktuellen Items verändert wird. **Ab SmartHomeNG v1.4**

Der Syntax ist äquivalent zum Attribut [on_update](#attribut-on_update)


