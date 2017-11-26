Item Methoden
-------------

Die grundsätzlichen Methoden, die jedes Item hat, sind unter **Items** beschrieben. Darüber
hinaus stehen folgende Methoden zum Handling von Items zur Verfügung:

sh.return_item(path)
^^^^^^^^^^^^^^^^^^^^

Liefert das Item Objekt für den angegebenen Pfad zurück. 

.. code:: python

   sh.return_item('erdgeschoss.flur')


sh.return_items()
^^^^^^^^^^^^^^^^^

Liefert alle Item Objekte zurück. 

.. code:: python

   for item in sh.return_items():     
       logger.info(item.id())


sh.match_items(regex)
^^^^^^^^^^^^^^^^^^^^^

Liefert alle Items zurück, die der Regular Expression, dem Pfad und dem optionalen Attribut entsprechen. 

.. code:: python

   for item in sh.match_items('*.licht'):
       # Selektiere alle Items, deren Pfad mit 'licht' endet
       logger.info(item.id())
       
   for item in sh.match_items('*.licht:special'):
       # Selektiere alle Items, deren Pfad mit 'licht' endet und die das Attribut 'special' haben     
       logger.info(item.id())


sh.find_items(configattribute)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Liefert alle Items zurück, die über das angegebene spezielle Attribut verfügen.

.. code:: python

   for item in sh.find_items('my_special_attribute'):
       logger.info(item.id())


find_children(parentitem, configattribute)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Liefert alle untergeordneten Items zurück, die über das angegebene Konfigurations-Attribut verfügen.


