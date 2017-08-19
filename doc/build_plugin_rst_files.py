#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016-       Martin Sinn                         m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG
#  https://github.com/smarthomeNG/smarthome
#  http://knx-user-forum.de/
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
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import os

print('')
print(os.path.basename(__file__) + ' - Builds the .rst files for the documentation')
print('')

import sys
# find lib directory and import lib/item_conversion
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#sys.path.insert(0, '../lib')
#import item_conversion

# um im Test-build_doc Umfeld zu laufen:
sys.path.insert(0, '..')
sys.path.insert(0, '../lib')
import shyaml

import subprocess


def get_pluginlist_fromgit():
    plglist = []
    plg_git = subprocess.check_output(['git', 'ls-files', '*/__init__.py'], stderr=subprocess.STDOUT).decode().strip('\n')
    for plg in plg_git.split('\n'):
        if plg.split('/')[1] == '__init__.py':
#            print(plg.split('/')[0], '   -   ', plg)
            plglist.append(plg.split('/')[0])
    return plglist
    
    
def get_local_pluginlist():
    plglist = os.listdir('.')
    
    for entry in plglist:
        if entry[0] in ['.','_'] or entry == 'deprecated_plugins':
            plglist.remove(entry)
    for entry in plglist:
        if entry[0] in ['.','_']:
            plglist.remove(entry)
    for entry in plglist:
        if entry[0] in ['.','_']:
            plglist.remove(entry)
    return plglist
    
    
def get_pluginyamllist_fromgit():
    plglist = []
    plg_git = subprocess.check_output(['git', 'ls-files', '*/plugin.yaml'], stderr=subprocess.STDOUT).decode().strip('\n')
    for plg in plg_git.split('\n'):
        if plg.split('/')[1] == 'plugin.yaml':
#            print(plg,'   -   ', plg.split('/')[0], )
            plglist.append(plg.split('/')[0])
    return plglist
    
    
def build_pluginlist( plugin_type='all' ):
    """
    return a list with all pluginnames of the requested type
    """
    result = []
    plugin_type = plugin_type.lower()
    for metaplugin in plugins_git:
#        metafile = plugindirectory + '/' + metaplugin + '/plugin.yaml' 
        metafile = metaplugin + '/plugin.yaml' 
#        print("Plugin '{}', Metafile '{}'".format(metaplugin, metafile) )
        if metaplugin in pluginsyaml_git:
            plugin_yaml = shyaml.yaml_load(metafile)
#        print(plugin_yaml['plugin']['type'])
            section_dict = plugin_yaml.get('plugin')
            if section_dict != None:
                plgtype = section_dict.get('type').lower()
            else:
                plgtype = 'un-classified'
        else:
            plgtype = 'un-classified'
        if (plgtype == plugin_type) or (plugin_type == 'all'):
            result.append(metaplugin)
#            print("Plugin '{}', type = '{}'".format(metaplugin, plgtype) )
    return result


def write_rstfile(plgtype='All'):

    plglist = build_pluginlist(plgtype)
#    print()
#    print(plgtype+':')
#    print( plglist )
    print()

    print('zu schreiben in: '+program_dir)
    rst_filename = 'plugins_'+plgtype.lower()+'.rst'
    print('Dateiname: '+rst_filename)
    
    title = plgtype + ' Plugins'

    fh = open(program_dir+'/'+rst_filename, "w")
    fh.write(title+'\n')
    fh.write('-'*len(title)+'\n')
    fh.write('\n')
    fh.write('.. toctree::\n')
    fh.write('   :maxdepth: 2\n')
    fh.write('   :glob:\n')
    fh.write('   :titlesonly:\n')
    fh.write('\n')
    for plg in plglist:
        fh.write('   plugins/'+plg+'/README.md\n')
    fh.write('\n')
    fh.close()
    

# ==================================================================================
#   Main Generator Routine
#

if __name__ == '__main__':
    program_dir = os.getcwd()

    # change the working diractory to the directory from which the converter is loaded (../tools)
    os.chdir(os.path.dirname(os.path.abspath(os.path.basename(__file__))))
    
#    plugindirectory = os.path.abspath('../plugins')
    plugindirectory = '../plugins'
    pluginabsdirectory = os.path.abspath(plugindirectory)
    
#    if item_conversion.is_ruamelyaml_installed() == False:
#        exit(1)
        
    os.chdir(pluginabsdirectory)
    
#    plg_git = subprocess.check_output(['git', 'ls-files', '*/__init__.py'], stderr=subprocess.STDOUT).decode().strip('\n')
#    plugins_git = []
#    for plg in plg_git.split('\n'):
#        if plg.split('/')[1] == '__init__.py':
##            print(plg.split('/')[0], '   -   ', plg)
#            plugins_git.append(plg.split('/')[0])

    plugins_git = get_pluginlist_fromgit()
    if not 'xmpp' in plugins_git:
        plugins_git.append('xmpp')
        
    print('--- Liste der Plugins auf github ('+str(len(plugins_git))+'):')
    print(plugins_git)
    print()
    
    pluginsyaml_git = get_pluginyamllist_fromgit()
    if not 'xmpp' in plugins_git:
        plugins_git.append('xmpp')
        
    print('--- Liste der Plugins mit Metadaten auf github ('+str(len(pluginsyaml_git))+'):')
    print(pluginsyaml_git)
    print()
    print('----------------------------------------------')
    print()
    
    

    plgtype = 'Gateway'
    plgtype = 'System'

    write_rstfile('Gateway')
    write_rstfile('Interface')
    write_rstfile('Protocol')
    write_rstfile('System')
    write_rstfile('un-Classified')
    write_rstfile('Web')

    print()
    abs_path = os.path.abspath('.')
    print("os.listdir('.'):")
    print(" -> "+abs_path)
    plugins_local = get_local_pluginlist()
        
    print()
    for plg in plugins_local:
        if not(plg in plugins_git):
            print(plg, ord(plg[0]))
    print()
    