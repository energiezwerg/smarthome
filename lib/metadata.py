#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2017-       Martin Sinn                         m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG  If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import logging
import os
import collections

from lib.utils import Utils
import lib.shyaml as shyaml
from lib.constants import (YAML_FILE, FOO, META_DATA_TYPES, META_DATA_DEFAULTS)

META_MODULE_PARAMETER_SECTION = 'parameters'
META_PLUGIN_PARAMETER_SECTION = 'parameters'
#META_DATA_TYPES=['bool', 'int', 'float', 'str', 'list', 'dict', 'ip', 'ipv4', 'mac', 'foo']
#META_DATA_DEFAULTS={'bool': False, 'int': 0, 'float': 0.0, 'str': '', 'list': [], 'dict': {}, 'OrderedDict': {}, 'num': 0, 'scene': 0, 'ip': '0.0.0.0', 'ipv4': '0.0.0.0', 'mac': '00:00:00:00:00:00', 'foo': None}


logger = logging.getLogger(__name__)

class Metadata():

    _version = '?'
    
    
    def __init__(self, sh, addon_name, addon_type, classpath=''):
        self._sh = sh
        self._addon_name = addon_name.lower()
        self._addon_type = addon_type
        self._paramlist = []

        self._log_premsg = "{} '{}': ".format(addon_type, self._addon_name)

#        logger.warning(self._log_premsg+"classpath = '{}'".format( classpath ) )
        if classpath == '':
            if addon_type == 'plugin':
                addon_type_dir = 'plugins'
            elif addon_type == 'module':
                addon_type_dir = 'modules'
            else:
                return
            self.relative_filename = os.path.join( addon_type_dir, self._addon_name, addon_type+YAML_FILE )
        else:
            self.relative_filename = os.path.join( classpath.replace('.', os.sep), addon_type+YAML_FILE )
#        logger.warning(self._log_premsg+"relative_filename = '{}'".format( self.relative_filename ) )
        
        self.parameters = None
        filename = os.path.join( self._sh.get_basedir(), self.relative_filename )
        self.meta = shyaml.yaml_load(filename, ordered=True)
        if self.meta != None:
            if self._addon_type == 'module':
                self.parameters = self.meta.get(META_MODULE_PARAMETER_SECTION)
            else:
                self.parameters = self.meta.get(META_PLUGIN_PARAMETER_SECTION)
            if self.parameters != None:
                self._paramlist = list(self.parameters.keys())
                logger.info(self._log_premsg+"Metadata paramlist = '{}'".format( str(self._paramlist) ) )
            
        # Test parameter definitions for validity
        for param in self._paramlist:
            logger.debug(self._log_premsg+"param = '{}'".format( str(param) ) )
            if self.parameters[param] != None:
                typ = str(self.parameters[param].get('type', FOO)).lower()
                # to be implemented: timeframe
                self.parameters[param]['listtype'] = ''
                if not (typ in META_DATA_TYPES):
                    # test for list with specified datatype
                    if typ.startswith('list(') and typ.endswith(')'):
                        self.parameters[param]['type'] = 'list'
                        subtyp = typ[5:]
                        subtyp = subtyp[:-1].strip()
                        if subtyp in META_DATA_TYPES:
                            self.parameters[param]['listtype'] = subtyp
                        else:
                            self.parameters[param]['listtype'] = FOO
                    else:
                        logger.error(self._log_premsg+"Invalid definition in metadata file '{}': type '{}' for parameter '{}' -> using type '{}' instead".format( self.relative_filename, typ, param, FOO ) )
                        self.parameters[param]['type'] = FOO
            else:
#                self.parameters[param]['type'] = FOO
                pass
            
        # Read global metadata for addon
        
        if self.meta != None:
            self.addon_metadata = self.meta.get(addon_type)
        else:
            self.addon_metadata = None
        
    
    def _strip_quotes(self, string):
        if type(string) is str:
            string = string.strip()
            if len(string) >= 2:
                if string[0] in ['"', "'"]:  # check if string starts with ' or "
                    if string[0] == string[-1]:  # and end with it
                        if string.count(string[0]) == 2:  # if they are the only one
                            string = string[1:-1]  # remove them
        return string


    # ------------------------------------------------------------------------
    # Methods for global values
    #

    def get_string(self, key):
        """
        Return the value for a global key as a string
        
        :param key: global key to look up (in section 'plugin' or 'module')
        :type key: str
        
        :return: value for the key
        :rtype: str
        """
        if self.addon_metadata == None:
            return ''

        return self.addon_metadata.get(key, '')
        

    def get_mlstring(self, mlkey):
        """
        Return the value for a global multilanguage-key as a string
        
        It trys to lookup th value for the default language. 
        If the value for the default language is empty, it trys to look up the value for English.
        If there is no value for the default language and for English, it trys to lookup the value for German.
        
        :param key: global multilabguage-key to look up (in section 'plugin' or 'module')
        :type key: str
        
        :return: value for the key
        :rtype: str
        """
        if self.addon_metadata == None:
            return ''

        key_dict = self.addon_metadata.get(mlkey)
        if key_dict == None:
            return ''
        try:
            result = key_dict.get(self._sh.get_defaultlanguage(), '')
        except:
            return ''
        if result == '':
            result = key_dict.get('en','')
            if result == '':
                result = key_dict.get('de','')
        return result
        
    
    def get_bool(self, key):
        """
        Return the value for a global key as a bool
        
        :param key: global key to look up (in section 'plugin' or 'module')
        :type key: str
        
        :return: value for the key
        :rtype: bool
        """
        if self.addon_metadata == None:
            return False

        return Utils.to_bool(self.addon_metadata.get(key, ''))
        

    def test_shngcompatibility(self):
        """
        Test if the actual running version of SmartHomeNG is in the range of supported versions for this addon (module/plugin)
        
        :return: True if the SmartHomeNG version is in the supported range
        :rtype: bool
        """
        l = str(self._sh.version).split('.')
        shng_version = l[0]+'.'+l[1]
        l = str(self.get_string('sh_minversion')).split('.')
        min_shngversion = l[0]
        if len(l) > 1:
            min_shngversion += '.'+l[1]
        l = str(self.get_string('sh_maxversion')).split('.')
        max_shngversion = l[0]
        if len(l) > 1:
            max_shngversion += '.'+l[1]
        mod_version = self.get_string('version')

        if min_shngversion != '':
            if min_shngversion > shng_version:
                logger.error("{0} '{1}': The version of SmartHomeNG is too old for this {0}. It requires at least version v{2}. The {0} was not loaded.".format(self._addon_type, self._addon_name, min_shngversion))
                return False
        if max_shngversion != '':
            if max_shngversion < shng_version:
                logger.error("{0} '{1}': The version of SmartHomeNG is too new for this {0}. It requires a version up to v{2}. The {0} was not loaded.".format(self._addon_type, self._addon_name, max_shngversion))
                return False
        return True
        
        
    def get_version(self):
        """
        Returns the version of the addon
        
        If test_version has been called before, the code_version is taken into account,
        otherwise the version of the metadata-file is returned
        
        :return: version
        :rtype: str
        """
        if self._version == '?':
            self._version = self.get_string('version')
        return self._version
        
            
    def test_version(self, code_version):
        """
        Tests if the loaded Python code has a version set and compares it to the metadata version.
        
        :param code_version: version of the python code
        :type code_version: str
        
        :return: True: version numbers match, or Python code has no version
        :rtype: bool
        """
        self._version = self.get_string('version')
        if code_version == None:
            logger.info("{} '{}' version not defined in Python code, metadata version is {}".format(self._addon_type, self._addon_name, self._version))
            return True
        else:
            if self._version == '':
                logger.info("{} '{}' metadata contains no version number".format(self._addon_type, self._addon_name))
                self._version = code_version
            else:
                if str(code_version) != self._version:
                    logger.error("{} '{}' version differs between Python code ({}) and metadata ({})".format(self._addon_type, self._addon_name, str(code_version), self._version))
                    return False
        return True
        
        
    # ------------------------------------------------------------------------
    # Methods for parameter checking
    #

    def _test_valuetype(self, typ, subtype, value):
        """
        Returns True, if the value can be converted to the specified type
        """
        if typ == 'bool':
            return (Utils.to_bool(value, default='?') != '?')
        elif typ == 'int':
            return Utils.is_int(value)
        elif typ in ['float','num']:
            return Utils.is_float(value)
        elif typ == 'scene':
            if Utils.is_int(value):
                return (int(value) >= 0) and (int(value) < 256)
            else:
                return False
        elif typ == 'str':
            return True     # Everything can be converted to a string
        elif typ == 'list':
            if subtype != '' and subtype != FOO:
                result = True
                if isinstance(value, list):
                    for val in value:
                        if not self._test_valuetype(subtype, '', val):
                            result = False
#                            logger.warning("_test_valuetype: val = {}, result = False".format(val))
#                    logger.warning("_test_valuetype: value = {}, type(value) = {}, typ = {}, subtype = {}".format(value, type(value), typ, subtype))
                return result
            return (type(value) is list)
        elif typ == 'dict':
            return (type(value) is dict)
        elif typ == 'ip':
            if Utils.is_ip(value):
                return True
            return Utils.is_hostname(value)
        elif typ == 'ipv4':
            return Utils.is_ip(value)
        elif typ == 'mac':
            return Utils.is_mac(value)
        elif typ == FOO:
            return True

    
    def _test_value(self, param, value):
        """
        Returns True, if the value can be converted to specified type
        """
        if param in self._paramlist:
            typ = self.get_parameter_type(param)
            subtype = self.get_parameter_subtype(param)
            return self._test_valuetype(typ, subtype, value)
        return False
    

    def _expand_listvalues(self, param, value):
        """
        If a parameter is defined as a list, but the value is of a bsic datatype,
        value is expanded to a list. In all other cases, the value is returned nuchanged
        """
        result = value
        if param in self._paramlist:
            typ = self.get_parameter_type(param)
            if (typ == 'list') and (not isinstance(value, list)):
                result = Utils.string_to_list(value)
#            if (typ == 'list'):
#                logger.warning("_expand_listvalues: value = >{}<, type(value) = >{}<, result = >{}<, type(result) = >{}<".format(value, type(value), result, type(result)))
        return result


    def _convert_valuetotype(self, typ, value):
        """
        Returns the value converted to the parameters type
        """
        if typ == 'bool':
            result = Utils.to_bool(value)
        elif typ in ['int','scene']:
            result = int(value)
        elif typ in ['float','num']:
            result = float(value)
        elif typ == 'str':
            result = str(value)
        elif typ == 'list':
            if isinstance(value, list):
                result = value
            else:
                result = [value]
        elif typ == 'dict':
            result = dict(value)
        elif typ in ['ip', 'ipv4', 'mac']:
            result = str(value)
        elif typ == FOO:
            result = value
        else:
            logger.error(self._log_premsg+"unhandled type {}".format(typ))
        return result
        
            
    def _convert_value(self, param, value, is_default=False):
        """
        Returns the value converted to the parameters type
        """
        result = False
        if param in self._paramlist:
            typ = self.get_parameter_type(param)
            result = self._convert_valuetotype(typ, value)

            orig = result
            result = self._test_validity(param, result, is_default)
            if result != orig:
                # Für non-default Prüfung nur Warning
                if is_default:
                    logger.error(self._log_premsg+"Invalid default '{}' in metadata file '{}' for parameter '{}' -> using '{}' instead".format( orig, self.relative_filename, param, result ) )
                else:
                    logger.warning(self._log_premsg+"Invalid value '{}' in plugin configuration file for parameter '{}' -> using '{}' instead".format( orig, param, result ) )
        return result
    
#  plugin 'hue': Invalid default '2' in metadata file 'plugins/hue/plugin.yaml' for parameter 'cycle_lamps' -> using '10' instead



    def _test_validity(self, param, value, is_default=False):
        """
        Checks the value against a list of valid values.
        If valid, it returns the value. 
        Otherwise it returns the first entry of the list of valid values.
        """
        result = value
        if self.parameters[param] != None:
            if self.parameters[param].get('type') in ['int', 'float', 'num', 'scene']:
                valid_min = self.parameters[param].get('valid_min')
                if valid_min != None:
                    if self._test_value(param, valid_min):
                        if result < self._convert_valuetotype(self.get_parameter_type(param), valid_min):
                            if is_default == False:
#                                result = self.get_parameter_defaultvalue(param)   # instead of valid_min
                                result = valid_min
                            else:
                                result = valid_min
                valid_max = self.parameters[param].get('valid_max')
                if valid_max != None:
                    if self._test_value(param, valid_max):
                        if result > self._convert_valuetotype(self.get_parameter_type(param), valid_max):
                            if is_default == False:
#                                result = self.get_parameter_defaultvalue(param)   # instead of valid_max
                                result = valid_max
                            else:
                                result = valid_max
        
        if self.parameters[param] == None:
            logger.warning(self._log_premsg+"_test_validity: param {}".format(param))
        else:
            valid_list = self.parameters[param].get('valid_list')
            if (valid_list == None) or (len(valid_list) == 0):
                pass
            else:
                if result in valid_list:
                    pass
                else:
                    result = valid_list[0]
        return result

    def _get_default_if_none(self, typ):
        """
        Returns the default value for  datatype.
        It is used, if no default value is defined for a parameter.
        """
        return META_DATA_DEFAULTS.get(typ, None)
        
    
    def get_parameterlist(self):
        """
        Returns the list of parameter names
        
        :return: List of strings with parameter names
        :rtype: list of str
        """
        result = []
        for param in self._paramlist:
            result.append(param)
        return result
        
        
    def get_parameter_type(self, param):
        """
        Returns the datatype of a parameter
        
        If the defined datatype is 'foo', None is returned

        :param param: Name of the parameter
        :type param: str
        
        :return: datatype of the parameter
        :rtype: str or None
        """
        if self.parameters == None:
            return FOO
        if self.parameters[param] == None:
            return FOO
        return str(self.parameters[param].get('type', FOO)).lower()
        
        
    def get_parameter_subtype(self, param):
        """
        Returns the subtype of a parameter
        
        If the defined datatype is 'foo', None is returned
        If no subtype is defined (or definable), an empty string is returned

        :param param: Name of the parameter
        :type param: str
        
        :return: subtype of the parameter
        :rtype: str or None
        """
        if self.parameters == None:
            return FOO
        if self.parameters[param] == None:
            return FOO
        result = str(self.parameters[param].get('type', FOO)).lower()
        sub = ''
        if result == 'list':
            sub =  self.parameters[param].get('listtype', '?')
        return sub
        
        
    def get_parameter_type_with_subtype(self, param):
        """
        Returns the datatype of a parameter with subtype (if subtype exists)
        
        If the defined datatype is 'foo', None is returned
        
        Subtypes are returnd for parameter type 'list'

        :param param: Name of the parameter
        :type param: str
        
        :return: datatype with subtype of the parameter
        :rtype: str or None
        """
        if self.parameters == None:
            return FOO
        if self.parameters[param] == None:
            return FOO
        result = str(self.parameters[param].get('type', FOO)).lower()
        sub = self.get_parameter_subtype(param)
        if sub != '':
            result = result+'(' + sub + ')'
        return result
        
    def get_parameter_defaultvalue(self, param):
        """
        Returns the default value for the parameter
        
        If no default value is specified for the parameter, the default value for the datatype
        of the parameter is returned.
        
        If the parameter is not defined, None is returned
        
        :param param: Name of the parameter
        :type param: str
        
        :return: Default value
        :rtype: str or None
        """
        value = None
        if param in self._paramlist:
            if self.parameters[param] != None:
                if self.get_parameter_type(param) == 'dict':
                    if self.parameters[param].get('default') != None:
                        value = dict(self.parameters[param].get('default'))
                else:
                    value = self.parameters[param].get('default')
                typ = self.get_parameter_type(param)
                if value == None:
                    value = self._get_default_if_none(typ)
                    
                value = self._expand_listvalues(param, value)
                if not self._test_value(param, value):
                    # Für non-default Prüfung nur Warning
                    logger.error(self._log_premsg+"Invalid data for type '{}' in metadata file '{}': default '{}' for parameter '{}' -> using '{}' instead".format( self.parameters[param].get('type'), self.relative_filename, value, param, self._get_default_if_none(typ) ) )
                    value = None
                if value == None:
                    value = self._get_default_if_none(typ)

                value = self._convert_value(param, value, is_default=True)

                orig_value = value
                value = self._test_validity(param, value, is_default=True)
                if value != orig_value:
                    # Für non-default Prüfung nur Warning
                    logger.error(self._log_premsg+"Invalid default '{}' in metadata file '{}' for parameter '{}' -> using '{}' instead".format( orig_value, self.relative_filename, param, value ) )

        return value


    def get_parameterdefinition(self, parameter, key):
        """
        Returns the value for a key of a parameter as a string
        
        :param parameter: parameter to get the definition info from
        :param key: key of the definition info
        :type parameter: str
        :type key: str

        :return: List of strings with parameter names (None if parameter is not found)
        :rtype: str
        """
        try:
            result = self.parameters[parameter].get('key')
        except:
            result = None
        return result
            
        
    def check_parameters(self, args):
        """
        Checks the values of a dict of configured parameters. 
        
        Returns a dict with all defined parameters with values and a bool indicating if all parameters are ok (True)
        or if a mandatory parameter is not configured (False). It returns default values
        for parameters that have not been configured. The resulting dict contains the
        values in the the datatype of the parameter definition  

        :param args: Configuraed parameters with the values
        :type args: dict of parameter-values (values as string)
        
        :return: All defined parameters with values, Flag if all parameters are ok (no mandatory is missing)
        :rtype: dict, bool
        """
        addon_params = collections.OrderedDict()
        if self.meta == None:
            logger.info(self._log_premsg+"No metadata found" )
            return (addon_params, True)
        if self.parameters == None:
            logger.info(self._log_premsg+"No parameter definitions found in metadata" )
            return (addon_params, True)
            
        allparams_ok = True
        for param in self._paramlist:
            value = Utils.strip_quotes(args.get(param))
            if value == None:
                if (self.parameters[param] is not None) and self.parameters[param].get('mandatory'):
                    logger.error(self._log_premsg+"'{}' is mandatory, but was not found in /etc/{}".format(param, self._addon_type+YAML_FILE))
                    allparams_ok = False
                else:
                    addon_params[param] = self.get_parameter_defaultvalue(param)
                    logger.info(self._log_premsg+"value not found in plugin configuration file for parameter '{}' -> using default value '{}' instead".format(param, addon_params[param] ) )
#                    logger.warning(self._log_premsg+"'{}' not found in /etc/{}, using default value '{}'".format(param, self._addon_type+YAML_FILE, addon_params[param]))
            else:
                value = self._expand_listvalues(param, value)
                if self._test_value(param, value):
                    addon_params[param] = self._convert_value(param, value)
                    logger.debug(self._log_premsg+"Found '{}' with value '{}' in /etc/{}".format(param, value, self._addon_type+YAML_FILE))
                else:
                    if self.parameters[param].get('mandatory') == True:
                        logger.error(self._log_premsg+"'{}' is mandatory, but no valid value was found in /etc/{}".format(param, self._addon_type+YAML_FILE))
                        allparams_ok = False
                    else:
                        addon_params[param] = self.get_parameter_defaultvalue(param)
                        logger.error(self._log_premsg+"Found invalid value '{}' for parameter '{}' in /etc/{}, using default value '{}' instead".format(value, param, self._addon_type+YAML_FILE, str(addon_params[param])))

        return (addon_params, allparams_ok)
        
    
