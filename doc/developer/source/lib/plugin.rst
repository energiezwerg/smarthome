Plugins-API
===========

There are two ways to access the API
        
1. Directly

   Use it the following way to access the api, if you have no access to the sh object in your method or function:

   .. code-block:: python

       # to get access to the object instance:
       from lib.plugin import Plugins
       plugins = plugins.get_instance()

       # to access a method (eg. return_plugins()):
       plugins.return_plugins()


2. Through the main SmartHome object 
        
   If you have access to the sh object in your method or function, you can use the following way:
           
   .. code-block:: python

       # to access a method (eg. return_plugins()):
       sh.plugins.return_plugins()


The API is implemented through the following library:


lib.plugin
----------

.. automodule:: lib.plugin
    :members:
    :undoc-members:
    :show-inheritance:
    :member-order: bysource
