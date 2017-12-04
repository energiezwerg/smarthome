*on_update* und *on_change*
###########################

Attribut *on_update*
====================

Ermöglicht das setzen des Wertes anderer Items, wenn das aktuelle Item ein Update erhält (auch 
wenn sich der Wert des aktuellen Items dabei nicht ändert). **Ab SmartHomeNG v1.4**

Der Syntax ist folgender:

+-------------------------+----------------------------------------------------------------------+
|  <item> = <expression>  | wobei <expression> den selben syntax nutzt, der bereits vom          |
|                         | eval-Attribut bekannt ist                                            |
+-------------------------+----------------------------------------------------------------------+
|  <single expression>    | eval-Attribut bekannt ist. Wenn die zweite Form (ohne <item> = )     |
|                         | genutzt wird, muss die Zuweisung innerhalb der expression erfolgen:  |
|                         | Eine <single expression> der Form `sh.<item>(<expression>)` ist      |
|                         | weitestgehend äquivalent zur ersten Syntax Form.                     |
+-------------------------+----------------------------------------------------------------------+


- Expressions (eval Ausdrücker) können en selben Syntax nutzen wie das **eval** Attribut.
- Expressions können relative Item Adressierungen nutzen.
- Auch die Item Angabe in **<item> = <expresseion>** kann eine relative Angabe sein.
- Zu beachten ist, dass <item> eine reine Item Pfad Angabe ist, während in einem Ausdruck 
  (wie auch bei eval), ein Item in der Form **sh.<item>()** adressiert werden muss.
- **on_update** kann zusammen mit **eval** im selben Item genutzt werden, wobei **eval** vor 
  **on_update** ausgeführt wird. Dadurch enthält **value** in dem **on_update** eval-Ausdruck den 
  aktualisierten Wert des Items. Im Gegensatz dazu enthält **value** im eval-Ausdruck des **eval**
  Attributs den vorangegangenen Wert des Items. Wenn im **on_update** Ausdruck auf den vorangegangenen 
  Wert des Items zugegriffen werden soll, geht das mit der Item-Methode **prev_value()**. Um das 
  Item selbst zu adressieren kann am einfachsten die relative Adressierung eingesetzt werden. 
  Den vorangegangenen Wert des Items erhält man mit **sh..prev_value()**.

.. attention::

   Es ist zu beachten, dass die beiden Versionen des **on_update** Syntax nicht vollständig
   identisch sind. Der Unterschied tritt zutage, wenn die <expression> als Ergebnis **None**
   liefert. 
   
   Die erste Version (<item> = <expression>) verhält sich analog zum **eval** Attribut:
   Wenn das Ergebnis der <expression> **None** ist, wird <item> nicht verändert. **None** kann
   hierbei bewusst eingesetzt werden, um einen Wert unverändert zu lassen und damit verhindern,
   dass <item> ungewollt weitere Trigger auslöst.
   
   In der zweiten Version (<single expression>) würde ein Ergebnis **None** dazu führen, dass
   das Ziel Item (sh.<item>) den Wert None zugewiesen bekommt.


Beispiel:

.. code-block:: yaml
   :caption: ../items/<filename>.yaml (Ausschnitt)

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


Im .conf Format (deprecated) sieht das Beispiel folgendermaßen aus:

.. code-block:: none
   :caption: ../items/<filename>.conf (Ausschnitt) (deprecated)

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


Attribut *on_change*
====================

Ermöglicht das setzen des Wertes anderer Items, wenn der Wert des aktuellen Items verändert 
wird. **Ab SmartHomeNG v1.4**

Der Syntax ist äquivalent zum Attribut **on_update**.

