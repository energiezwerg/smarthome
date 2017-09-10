Metadata section `plugin:`
--------------------------

The global metadata section ``plugin:`` has the following keys:

.. code:: yaml

    # Metadata for the plugin
    plugin:
        # Global plugin attributes
        type: cloud                 # plugin type (gateway, interface, protocol, system, cloud, un-classified)
    #    subtype: weather           # plugin subtype (if applicable)
        keywords: weather           # keywords, where applicable
        classname: <plugin_class>
        version: 1.4.3
        sh_minversion: 1.3a
    #    sh_maxversion:          # maximum shNG version to use this plugin (leave empty if latest)
        multi_instance: true        # plugin supports multi instance (if not specified, False is assumed)
        description:
            de: 'Plugin für ...'
            en: 'Plugin for ...'
        documentation: https://github.com/smarthomeNG/...        # url of additional wiki page (in addition to README.md of plugin
    #    support: https://knx-user-forum.de/forum/supportforen/smarthome-py      # url of the support thread or forum
        maintainer: msinn           # Optional: Who maintains this plugin?
    #   tester:                     # Optional: Who tests this plugin?

Description of the keys in the section ``plugin:``

    - **classname:** Name of the Python class to initialize
    - **version:** Version number of the plugin. It is checked against the version number defined in the Python source code
    - **sh_minversion:** Minimum SmartHomeNG version this plugin is compatible with. If *sh_minversion* is left empty, SmartHomeNG assumes that the plugin is compatible with every version of SmartHomeNG [Test not yet implemented]
    - **sh_maxversion:** Maximum SmartHomeNG version this plugin is compatible with (or empty, if compatible with the actual version of SmartHomeNG) [Test not yet implemented]
    - **description:** Multilanguage Text describing what the plugin does. - The texts in the different languages are specified in sub-entries in the form <language>: <text>. Use the standard two letter codes for specifying the language (de, en, fr, pl, ..)
    - **classpath:** **Usually not specified.** Only needed, if the plugin resides outside the ``/plugins`` folder


