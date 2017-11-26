
.. index:: Items; Standardattribute
.. index:: Standardattribute

Standard Attribute
==================


In SmartHomeNG werden eine Reihe von Standard Attributen unterstützt. Diese sind in der folgenden 
Liste aufgeführt. Die Bedeutung und Verwendung der Attribute wird auf den folgenden Seiten beschrieben.

Zusätzlich können Plugins Attribute definieren. Die Bedeutung und Verwendung dieser zusätzlichen 
Attribute ist in der Dokumentation des jeweiligen Plugins nachzulesen.

+-----------------+------------------------------------------------------------------------------+
| **Attribut**    | **Beschreibung**                                                             |
+-----------------+------------------------------------------------------------------------------+
| type            | Um Werte zu speichern, muss ein Typ vorgegeben werden. Unterstützte Typen    |
|                 | sind bool, num, str, list, dict, foo, scene (siehe Tabelle unten)            |
+-----------------+------------------------------------------------------------------------------+
| name            | ein optionaler Name für das Item                                             |
+-----------------+------------------------------------------------------------------------------+
| remark          | ein optionaler Kommentar für das Item. Es ist sinnvoll Kommentare zu einem   |
|                 | Item als **remark** Attribut zu erfassen und nicht als Kommentar ( **#** )   |
|                 | in die Konfigurationsdatei zu schreiben. Dadurch können Kommentare bei einer |
|                 | kommenden Umstellung des Formates der Konfigurationsdateien automatisch      |
|                 | konvertiert werden.                                                          |
+-----------------+------------------------------------------------------------------------------+
| initial_value,  | Ein optionaler Startwert für dieses Item                                     |
| value           |                                                                              |
+-----------------+------------------------------------------------------------------------------+
| cache           | Wenn 'Yes', dann wird der Wert des Items zwischengespeichert und beim        |
|                 | erneuten Start von SmartHomeNG wird der alte Wert aus dem Zwischenspeicher   |
|                 | geladen (vergleichbar mit dem Permanentspeicher vom HS)                      |
+-----------------+------------------------------------------------------------------------------+
| enforce_updates | Wenn das Attribut auf 'Yes' gesetzt wird, führt jede Wertzuweisung ans Item  |
|                 | dazu, das abhängige Logiken und item Evaluationen getriggert werden, auch    |
|                 | wenn sich der Wert des Items bei der Zuweisung nicht ändert.                 |
+-----------------+------------------------------------------------------------------------------+
| threshold       | legt einen Schwellwert oder einen Schwellwertbereich fest., z.B. 21.4|25.0   |
|                 | der eine Logik triggert, wenn der Wert höher als 25.0 or niedriger als 21.4  |
|                 | ist. Es kann auch ein einzelner Wert notiert werden                          |
+-----------------+------------------------------------------------------------------------------+
| eval            | eval legt einen Ausdruck fest, nach dem der Wert des Items berechnet wird.   |
|                 | Mit eval_trigger wird festgelegt, wann eine (Neu)berechnung erfolgt (siehe   |
|                 | Beschreibung unten)                                                          |
+-----------------+------------------------------------------------------------------------------+
| eval_trigger    | Liste von Items, bei deren Veränderung eine Neuberechnung der in eval        |
|                 | definierten Formel erfolgen soll (siehe Beschreibung unten)                  |
+-----------------+------------------------------------------------------------------------------+
| crontab         | Die Evaluierung des Items findet zu angegebenen Zeitpunkten statt (siehe     |
|                 | Beschreibung unten)                                                          |
+-----------------+------------------------------------------------------------------------------+
| cycle           | Definiert ein regelmäßiges Aufrufen des Items (und damit der verknüpften     |
|                 | Logik oder Eval-Funktion). **Ab SmartHomeNG v1.3** werden die                |
|                 | Konfigurationsmöglichkeiten erweitert (siehe Beschreibung unten).            |
+-----------------+------------------------------------------------------------------------------+
| autotimer       | setzt den Wert des Items nach einer Zeitspanne auf einen bestimmten Wert.    |
|                 | **Ab SmartHomeNG v1.3** werden die Konfigurationsmöglichkeiten erweitert     |
|                 | (siehe [Beschreibung unten](#attribut-autotimer)).                           |
+-----------------+------------------------------------------------------------------------------+
| on_update       | Ermöglicht das setzen des Wertes anderer Items, wenn das aktuelle Item ein   |
|                 | Update erhält (auch wenn sich der Wert des aktuellen Items dabei nicht       |
|                 | ändert). **Ab SmartHomeNG v1.4**                                             |
+-----------------+------------------------------------------------------------------------------+
| on_change       | Ermöglicht das setzen des Wertes anderer Items, wenn der Wert des aktuellen  |
|                 | Items verändert wird. **Ab SmartHomeNG v1.4**                                |
+-----------------+------------------------------------------------------------------------------+


.. toctree::
   :maxdepth: 5
   :hidden:

   items_standard_attribute_type.rst
   items_standard_attribute_eval.md
   items_standard_attribute_crontab.md
   items_standard_attribute_cycle.md
   items_standard_attribute_autotimer.md
   items_standard_attribute_on_update.md

