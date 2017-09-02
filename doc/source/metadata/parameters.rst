Metadata section `parameters:`
------------------------------

The ``parameters:`` section has a section for each parameter that is implemented. The name of that
section is the name of the parameter.

The definitions in the ``parameters:`` section are used for validity checking of the plugin/module configuration. 
In the future the definitions will be used for a configuration tool for SmartHomeNG.

.. code:: yaml

    parameters:
        param1:
            type: int
            default: 1234
            description:
                de: 'Deutsche Beschreibung'
                en: 'English description'
            valid_list:
              - 1234
              - 2222
              - 4321
        
        param2:
            type: ...
            
        
.. include:: /metadata/parameter_keys.rst

