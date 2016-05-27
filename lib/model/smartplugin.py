#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016 Christian Strassburg  c.strassburg@gmx.de
#########################################################################
# Personal and non-commercial use only, redistribution is prohibited.
#########################################################################
from lib.model.smartobject import SmartObject
from lib.utils import Utils

class SmartPlugin(SmartObject):
    __instance = '' 
    __sh = None
    def get_version(self):
        return self.PLUGIN_VERSION
    
    def set_instance_name(self, instance):
        self.__instance = instance
    
    def get_instance_name(self):
        return self.__instance
  
    def __get_iattr(self, attr):
        """
            returns item attribute for plugin instance
            :rtype: str
        """
        if self.__instance == '':
            return attr
        else:
           return attr+"@"+self.__instance
    def has_iattr(self, conf, attr):
        if self.__get_iattr(attr) in conf or attr+"@*" in conf:
            return True
        return False
    
    def __new__(cls, *args, **kargs):
        if not hasattr(cls,'PLUGIN_VERSION'):
            raise NotImplementedError("'Plugin' subclasses should have a 'PLUGIN_VERSION' attribute")
        return SmartObject.__new__(cls,*args,**kargs)

    def set_sh(self, smarthome):
        self.__sh = smarthome

    def get_info(self):
        """ 
           returns a small plugin info like class, version and instance name as string
           :rtype: str
        """
        return "Plugin: '{0}.{1}', Version: '{2}', Instance: '{3}'".format(self.__module__, self.__class__.__name__,  self.get_version(),self.get_instance_name())

