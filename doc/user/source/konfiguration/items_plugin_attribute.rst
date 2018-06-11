
.. index:: Items; plugin-spezifische Attribute
.. index:: plugin-spezifische Attribute

.. role:: redsup

Plugin-spezifische Attribute :redsup:`neu`
==========================================


In SmartHomeNG werden außer den Standard Attributen weiter Attribute unterstützt, die von Plugins
implementiert werden. Wenn das Plugin, welches diese Attribute implementiert nicht geladen ist,
haben die konfigurierten Werte keine Auswirkung auf die Funktion von SmartHomeNG.

Um diese Attribute leichter den Plugins zuordnen zu können, beginnen die
Attributnamen normalerweise mit einem Kürzel, welches das Plugin kennzeichnet, gefolgt von einem
Unterstrich ('_').

Beispiele für Kürzel, die kennzeichnen zu welchem Plugin die jeweiligen Attribute gehören sind:

+-----------------+------------------+-----------------------------------------------------------+
| **Kürzel**      | **Plugin**       | **Attribut-Beispiele**                                    |
+-----------------+------------------+-----------------------------------------------------------+
| knx_            | knx              | knx_dpt, knx_cache, knx_listen, knx_send                  |
+-----------------+------------------+-----------------------------------------------------------+
| hm_             | homematic        | hm_address, hm_function                                   |
+-----------------+------------------+-----------------------------------------------------------+
| sv_             | visu_smartvisu   | sv_page, sv_img, sv_nav_aside, sv_nav_aside2, sv_widget   |
+-----------------+------------------+-----------------------------------------------------------+
| hue_            | hue              | hue_lamp_id, hue_lamp_type, hue_listen, hue_send          |
+-----------------+------------------+-----------------------------------------------------------+
| avm_            | avm              | avm_data_type, avm_identifier                             |
+-----------------+------------------+-----------------------------------------------------------+
| enigma2_        | enigma           | enigma2_data_type, enigma2_page                           |
+-----------------+------------------+-----------------------------------------------------------+

Vererbung von Attributen
------------------------

Bei einigen Plugins ist es notwendig, bei jedem Item einen Identifier anzugeben. Beispiele sind das
homematic Plugin und das hue Plugin. Hier ist es hilfreich, den Identifier (z.B. die **hm_address**
oder die **hue_lamp_id**) nur an einer Stelle konfigurieren zu müssen.

Das hue Plugin hat eine Vererbung der hue_lamp_id von übergeordneten Items im Plugin implementiert,
indem das Plugin immer prüft, ob das Attribut in übergeordneten Items definiert wurde.

Inzwischen gibt es einen Standardmechanismus, der es möglich macht selektiv den Wert aus einem
übergeordneten Item zu erben. Dieser Mechanismus funktioniert **nur** bei plugin-spezifischen
Attributen.

Um den Wert eines Attributes von dem übergeordnetem Item (Parent-Item) zu erben, muss in der
Konfiguration das Attribut mit dem Wert '..' konfiguriert werden:

.. code-block:: yaml

   fenstergriff_kueche:
       type: num
       hm_address: 12345678

       sabotage:
          type: bool
          hm_address: ..
          hm_function: SABOTAGE

       low_battery:
          type: bool
          hm_address: ..
          hm_function: LOW_BAT


In diesem Beispiel siht man, dass die HomeMatic Adresse des Devices nur einmal angegeben werden muss.
Der Vorteil wird besonders sichtbar, wenn man mehrere Fenstergriffe hat. Dann kann man diesen Block
einfach kopieren und muss nur dem Item einen neuen Namen geben (z.B. fenstergriff_bad) und die
**hm_adress** an einer Stelle abzuändern.

