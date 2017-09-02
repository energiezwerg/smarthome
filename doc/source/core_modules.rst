Core modules
============

Theare are loadable modules (SmartHomeNG modules) that can be used when developping plugins.
They implement additional functionality that is not implemented in the core itself.

Modules are configured in ``etc/modules.yaml``. The parameters are described in the README.md
files of the modules.

At the moment, the following modules exist:


.. toctree::
   :maxdepth: 3
   :titlesonly:
   
   /modules_doc/modules_readmes


A module is made up of two files:

- The program code: __init__.py
- The metadata: module.yaml

Both files reside in a folder within the ``/modules`` folder. The name of the folder reflects
the name of the module.

The metadata file cas two main sections:

- ``module:`` - Global metadata of the module
- ``parameters:`` - Definition of the parameters that can bei used in ``/etc/module.yaml`` to configure the module

The global metadata section has the following keys:

.. code:: yaml

    # Metadata for the plugin
    module:
        # Global plugin attributes
        classname: Http
        version: 1.4.3
        sh_minversion: 1.3a
    #   sh_maxversion:          # maximum shNG version to use this plugin (leave empty if latest)
        description:
            de: 'Modul zur Implementierung von Backend-Webinterfaces für Plugins'
            en: 'Module for implementing a backend-webinterface for plugins'

Description of the keys in the section ``module:``

    - **classname:** Name of the Python class to initialize
    - **version:** Version number of the module. It is checked against the version number defined in the Python source code
    - **sh_minversion:** Minimum SmartHomeNG version this module is compatible with [Test not yet implemented]
    - **sh_maxversion:** Maximum SmartHomeNG version this module is compatible with (or empty) [Test not yet implemented]
    - **description:** Multilanguage Text describing what the module does. - The texts in the different languages are specified in sub-entries in the form <language>: <text>. Use the standard two letter codes for specifying the language (de, en, fr, pl, ..)
    - **classpath:** **Usually not specified.** Only needed, if the module resides outside the ``/modules`` folder

The ``parameters:`` section has a section for each parameter that is impelemented. The name of that
section is the name of the parameter.


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
            
        
Description of the keys in the section of a parameter:

- **type:** specifies the datatype of the parameter. Valid datatypes are:

    - *bool* - a boolean value
    - *int* - an integer vaue
    - *pint* - a positive integer value
    - *float* - a float value
    - *pfloat* - a positive float value
    - *str* - a string
    - *list* - a list
    - *dict* - a dictionary
    - *ip* - a string, representing an ip-address
    - *mac* - a string, representing a mac-address
    - *foo* - the universal datatype

- **default:** specifies the default value to be used, if no value is given in `/etc/module.yaml`

- **description:** is a multilanguage text. - The texts in the different languages are specified in sub-entries in the form <language>: <text>. Use the standard two letter codes for specifying the language (de, en, fr, pl, ..)

- **valid_list** List of allowed values for the parameter

- **min** for datatypes *int* and *float*: minimum allowed value for the parameter [Test not yet implemented]

- **max** for datatypes *int* and *float*: maximum allowed value for the parameter [Test not yet implemented]

