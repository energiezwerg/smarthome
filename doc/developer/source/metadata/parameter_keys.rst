
Description of the keys in the section of a parameter/attribute:

- **type:** specifies the datatype of the parameter/attribute. Valid datatypes are:

    - *bool* - a boolean value
    - *int* - an integer vaue
    - *float* - a float value
    - *num* - an equivalent to float
    - *scene* - a positive integer in the range between 0 and 255
    - *str* - a string
    - *list* - a list 
    - *list(subtype)* - a list with each entry of a specified type (e.g: *list(int)* or 'list(ipv4)*)
    - *dict* - a dictionary
    - *ip* - a string, representing a hostname or an ipv4-address
    - *ipv4* - a string, representing strictly an ipv4-address
    - *mac* - a string, representing a mac-address
    - *foo* - the universal datatype

- **default:** Optional: Specifies the default value to be used, if no value is given in in the configuration file `/etc/plugin.yaml` or `/etc/module.yaml`

- **description:** is a multilanguage text. - The texts in the different languages are specified in sub-entries in the form <language>: <text>. Use the standard two letter codes for specifying the language (de, en, fr, pl, ..)

- **valid_list:** Optional: List of allowed values for the parameter

- **valid_min:** Optional: For datatypes *int*, *pint*, *float*, *pfloat*, *num* and *scene*: minimum allowed value for the parameter

- **valid_max:** Optional: For datatypes *int*, *pint*, *float*, *pfloat*, *num* and *scene*: maximum allowed value for the parameter

- **mandatory:** Optional: If set to True, a value must be configured for the plugin/module to get loaded an initialized

