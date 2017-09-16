#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2017-       Martin Sinn                         m.sinn@gmx.de
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


type_unclassified = 'unclassified'
plugin_sections = [ ['gateway', 'Gateway'],
                    ['interface', 'Interface'],
                    ['protocol', 'Protocol'],
                    ['system', 'System'],
                    [type_unclassified, 'Non classified Plugins'],
                    ['web', 'Web / Cloud Plugins']
                  ]


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
    
    
def get_description(section_dict, maxlen=70, lang='en'):
    desc = ''
    if lang == 'en':
        lang2 = 'de'
    else:
        lang2 = 'en'
    try:
        desc = section_dict['description'].get(lang, '')
    except:
        pass
    if desc == '':
        try:
            desc = section_dict['description'].get(lang2, '')
        except:
            pass
            
    import textwrap
    lines = textwrap.wrap(desc, maxlen, break_long_words=False)
    if lines == []:
        lines.append('')
    return lines


def get_maintainer(section_dict, maxlen=20):
    maint = section_dict.get('maintainer', '')
            
    import textwrap
    lines = textwrap.wrap(maint, maxlen, break_long_words=False)
    if lines == []:
        lines.append('')
    return lines


def get_tester(section_dict, maxlen=20):
    maint = section_dict.get('tester', '')
            
    import textwrap
    lines = textwrap.wrap(maint, maxlen, break_long_words=False)
    if lines == []:
        lines.append('')
    return lines


def get_docurl(section_dict, maxlen=70):
    maint = section_dict.get('documentation', '')
            
    import textwrap
    lines = textwrap.wrap(maint, maxlen, break_long_words=True)
    if lines == []:
        lines.append('')
    return lines


def get_supurl(section_dict, maxlen=70):
    maint = section_dict.get('support', '')
            
    import textwrap
    lines = textwrap.wrap(maint, maxlen, break_long_words=True)
    if lines == []:
        lines.append('')
    return lines


def build_pluginlist( plugin_type='all' ):
    """
    Return a list of dicts with a dict for each plugin of the requested type
    The dict contains the plugin name, type and description
    """
    result = []
    plugin_type = plugin_type.lower()
    for metaplugin in plugins_git:
        metafile = metaplugin + '/plugin.yaml' 
        plg_dict = {}
        if metaplugin in plugins_git:    #pluginsyaml_git
            if os.path.isfile(metafile):
                plugin_yaml = shyaml.yaml_load(metafile)
            else:
                plugin_yaml = ''
            if plugin_yaml != '':
                section_dict = plugin_yaml.get('plugin')
                if section_dict != None:
                    if section_dict.get('type').lower() in plugin_types:
                        plgtype = section_dict.get('type').lower()
                        plg_dict['name'] = metaplugin.lower()
                        plg_dict['type'] = plgtype
                        plg_dict['desc'] = get_description(section_dict, 85)
                        plg_dict['maint'] = get_maintainer(section_dict, 15)
                        plg_dict['test'] = get_tester(section_dict, 15)
                        plg_dict['doc'] = section_dict.get('documentation', '')
                        plg_dict['sup'] = section_dict.get('support', '')
                    else:
                        plgtype = type_unclassified
                        if plugin_type == type_unclassified:
                            print("not found: plugin type '{}' defined in plugin '{}'".format(section_dict.get('type'),metaplugin))
                else:
                    plgtype = type_unclassified

                if (plgtype == type_unclassified) and (plugin_yaml != ''):
                    plg_dict['name'] = metaplugin.lower()
                    plg_dict['type'] = type_unclassified
                    plg_dict['desc'] = get_description(section_dict, 85)
                    plg_dict['maint'] = get_maintainer(section_dict, 15)
                    plg_dict['test'] = get_tester(section_dict, 15)
                    plg_dict['doc'] = section_dict.get('documentation', '')
                    plg_dict['sup'] = section_dict.get('support', '')
                    print("unclassified: metafile = {}, plg_dict = {}".format(metafile, str(plg_dict)))
                    
                plg_dict['desc'].append('')
            else:
                plgtype = type_unclassified
                plg_dict['name'] = metaplugin.lower()
                plg_dict['type'] = type_unclassified
                plg_dict['desc'] = ['No metadata (plugin.yaml) was provided for this plugin!']
                plg_dict['maint'] = ['']
                plg_dict['test'] = ['']
                plg_dict['doc'] = ''
                plg_dict['sup'] = ''
                
            
            # Adjust list lengths
            maxlen = max( len(plg_dict['desc']), len(plg_dict['maint']), len(plg_dict['test']) )
            while len(plg_dict['desc']) < maxlen:
                plg_dict['desc'].append('')
            while len(plg_dict['maint']) < maxlen:
                plg_dict['maint'].append('')
            while len(plg_dict['test']) < maxlen:
                plg_dict['test'].append('')
                

        if (plgtype == plugin_type) or (plugin_type == 'all'):
#            result.append(metaplugin)
            result.append(plg_dict)
    return result


def write_rstfile(plgtype='All', heading=''):
    """
    Create a .rst file for each plugin category
    """
    if heading == '':
        title = plgtype + ' Plugins'
    else:
        title = heading

    rst_filename = 'plugins_doc/plugins_'+plgtype.lower()+'.rst'
    print('Datei: '+rst_filename+ ' '*(26-len(rst_filename)) +'  -  '+title)
    
    plglist = build_pluginlist(plgtype)
    
    fh = open(plugin_rst_dir+'/'+rst_filename, "w")
#    fh.write(title+'\n')
#    fh.write('-'*len(title)+'\n')
    fh.write('.. include:: /plugins_doc/plugins_'+plgtype+'_header.rst\n')
    fh.write('\n')

    if (len(plglist) == 0):
        fh.write('At the moments there are no plugins that have not been classified.\n')
    else:
        # write toc
        fh.write('.. toctree::\n')
        fh.write('   :maxdepth: 2\n')
        fh.write('   :glob:\n')
        fh.write('   :titlesonly:\n')
        fh.write('   :hidden:\n')
        fh.write('\n')
        for plg in plglist:
            fh.write('   /plugins/'+plg['name']+'/README.md\n')
        fh.write('\n')
        
        # write table with details
#        fh.write('.. include:: /plugins_doc/plugins_'+plgtype+'_header.rst\n')
        fh.write('\n')
        fh.write('\n')
        fh.write('.. table:: \n')
        fh.write('   :widths: grid\n')
        fh.write('\n')
        fh.write('   +-------------------+----------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+\n')
        fh.write('   | Plugin            | Description                                                                                                                                  | Maintainer      | Tester          |\n')
        fh.write('   +===================+============================================================================================================================+=================+=================+=================+\n')
        for plg in plglist:
            fh.write('   | {plg:<17.17} | {desc:<140.140} | {maint:<15.15} | {test:<15.15} |\n'.format(plg=plg['name'], desc=plg['desc'][0], maint=plg['maint'][0], test=plg['test'][0]))
            for l in range(1, len(plg['desc'])):
                fh.write('   | {plg:<17.17} | {desc:<140.140} | {maint:<15.15} | {test:<15.15} |\n'.format(plg='', desc=plg['desc'][l], maint=plg['maint'][l], test=plg['test'][l]))
            if plg['doc'] != '':
                plg['doc'] = "`Additional info <"+plg['doc']+">`_"
                fh.write('   | {plg:<17.17} |     {desc:<136.136} | {maint:<15.15} | {test:<15.15} |\n'.format(plg='', desc=plg['doc'], maint='', test=''))
            if plg['sup'] != '':
                if plg['doc'] != '':
                    fh.write('   | {plg:<17.17} |     {desc:<136.136} | {maint:<15.15} | {test:<15.15} |\n'.format(plg='', desc='', maint='', test=''))
                plg['sup'] = "`Support <"+plg['sup']+">`_"
                fh.write('   | {plg:<17.17} |     {desc:<136.136} | {maint:<15.15} | {test:<15.15} |\n'.format(plg='', desc=plg['sup'], maint='', test=''))
            fh.write('   +-------------------+----------------------------------------------------------------------------------------------------------------------------------------------+-----------------+-----------------+\n')
        fh.write('\n')
        fh.write('\n')
        
        fh.write('.. include:: /plugins_doc/plugins_footer.rst\n')

    fh.close()
    

# ==================================================================================
#   Main Generator Routine
#

if __name__ == '__main__':
    program_dir = os.getcwd()

    # change the working diractory to the directory from which the converter is loaded (../tools)
    os.chdir(os.path.dirname(os.path.abspath(os.path.basename(__file__))))
    
    plugindirectory = '../plugins'
    pluginabsdirectory = os.path.abspath(plugindirectory)
            
    os.chdir(pluginabsdirectory)
    
    plugins_git = get_pluginlist_fromgit()
    if not 'xmpp' in plugins_git:
        plugins_git.append('xmpp')
        
    print('--- Liste der Plugins auf github ('+str(len(plugins_git))+'):')
    
    pluginsyaml_git = get_pluginyamllist_fromgit()
    if not 'xmpp' in plugins_git:
        plugins_git.append('xmpp')
        
    print('--- Liste der Plugins mit Metadaten auf github ('+str(len(pluginsyaml_git))+'):')
    print()
    
    


    plugin_rst_dir = program_dir+'/source'
    print('zu schreiben in: '+plugin_rst_dir)

    plugin_types = []
    for pl in plugin_sections:
       plugin_types.append(pl[0])
           
    for pl in plugin_sections:
#        write_rstfile(pl[0], pl[1])
        write_rstfile(pl[0])
    print()
    