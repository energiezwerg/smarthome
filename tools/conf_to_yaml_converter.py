#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016-       Martin Sinn                         m.sinn@gmx.de
# -Parts (from the parser) Copyright 2013 Marcus Pop       marcus@popp.mx
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
print(os.path.basename(__file__) + ' - tool to convert shng .conf files to yaml')
print('')

try:
    import ruamel.yaml as yaml
    print('using python module ruamel.yaml version: ' + yaml.__version__)
    print('')
except:
    print('ERROR: module ruamel.yaml not found')
    print('')
    print('Please install ruamel.yaml using the command:')
    print('sudo pip3 install ruamel.yaml')
    print('')
    exit(1)

import collections
from collections import OrderedDict


yaml_version = '1.1'
indent_spaces = 4
store_raw_output = True			# Only for testing, otherwise False



# ==================================================================================
#   config loader from config.py modified for parsing to yaml
#


def strip_quotes(string):
    string = string.strip()
    if string[0] in ['"', "'"]:  # check if string starts with ' or "
        if string[0] == string[-1]:  # and end with it
            if string.count(string[0]) == 2:  # if they are the only one
                string = string[1:-1]  # remove them
    return string


def handle_multiline_string(string):
    if len(string) > 0 and string.find('\n') > -1 and string[0] != '|':
        string = '|\n' + string
    return string


def parse_for_convert(filename, config=None):
    valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@*'
    valid_set = set(valid_chars)
    if config is None:
        config = collections.OrderedDict()
    item = config
    lastline_was_comment = False
    last_comment_nr = 0
    print("- parsing '{}'".format(os.path.basename(filename)), end="")
    with open(filename, 'r', encoding='UTF-8') as f:
        linenu = 0
        parent = collections.OrderedDict()
        lines = iter(f.readlines())
        for raw in lines:
            linenu += 1
            line = raw.lstrip('\ufeff')  # remove BOM
            
            multiline = []
            if line.rstrip().endswith('\\'):
                i = 0
                while line.rstrip().endswith('\\'):
                    multiline.append( line.rstrip().rstrip('\\').strip() )
                    i += 1
                    linenu += 1
                    line = next(lines, '').lstrip()
                line = '\n'.join(multiline) + '\n'+line.strip()
                lastline_was_comment = False

            if (len(multiline) == 0) or (line[0] == '#'):
                if len(multiline) == 0:
                    comment_in_line = line.find('#')
                    comment = line.partition('#')[2].strip()
                    if comment_in_line > -1 and comment == '':
                        comment = '>**<'
                    line = line.partition('#')[0].strip()
                    # inline comment
                    if (line != '') and (comment != '') and line.find('[') == -1:
                        attr, __, value = line.partition('=')
                        comment = attr.strip() + ': ' + comment
                        line = line + '    ## ' + comment
                        comment = ''
                else:
                    comment = line
                    line = ''
                if comment != '':
                    while (comment != '') and (comment[0] == '#'):
                        comment = comment[1:].strip()
                if comment != '':
                    comment = comment.replace('\t', ' ')
                    if 'comment' in item.keys():
                        if lastline_was_comment:
                            if last_comment_nr > 0:
                                item['comment'+str(last_comment_nr)] = handle_multiline_string(item['comment'+str(last_comment_nr)] + '\n' + strip_quotes(comment))
                            else:
                                item['comment'] = handle_multiline_string(item['comment'] + '\n' + strip_quotes(comment))
                        else:
                            i = 1
                            while 'comment'+str(i) in item.keys():
                                i += 1
                            item['comment'+str(i)] = handle_multiline_string(strip_quotes(comment))
                            last_comment_nr = i
                    else:
#                        logger.info("comment: '{}'".format(comment))
                        item['comment'] = handle_multiline_string(strip_quotes(comment))
                        last_comment_nr = 0
                    lastline_was_comment = True
                
            if line is '':
                continue
            if line[0] == '[':  # item
                lastline_was_comment = False
                #
                comment_in_line = line.find('#')
                comment = line.partition('#')[2].strip()
                if comment_in_line > -1 and comment == '':
                    comment = '>**<'
                line = line.partition('#')[0].strip()
                #
                brackets = 0
                level = 0
                closing = False
                for index in range(len(line)):
                    if line[index] == '[' and not closing:
                        brackets += 1
                        level += 1
                    elif line[index] == ']':
                        closing = True
                        brackets -= 1
                    else:
                        closing = True
                        if line[index] not in valid_chars + "'":
                            print()
                            print("ERROR: Problem (1) parsing '{}' invalid character in \nline {}: {}. \nValid chars: {}".format(os.path.basename(filename), linenu, line, valid_chars))
                            return config
                if brackets != 0:
                    print()
                    print("ERROR: Problem parsing '{}' unbalanced brackets in line {}: {}".format(filename, linenu, line))
                    return config
                #
                if comment_in_line > -1:
                    print()
                    print("ERROR: Problem parsing '{}' \nunhandled comment {} in \nline {}: {}. \nValid chars: {}".format(os.path.basename(filename), comment, linenu, line, valid_chars))
                #
                name = line.strip("[]")
                name = strip_quotes(name)
                if level == 1:
                    if name not in config:
                        config[name] = collections.OrderedDict()
                    item = config[name]
                    parents = collections.OrderedDict()
                    parents[level] = item
                else:
                    if level - 1 not in parents:
                        print()
                        print("ERROR: Problem parsing '{}' no parent item defined for item in line {}: {}".format(filename, linenu, line))
                        return config
                    parent = parents[level - 1]
                    if name not in parent:
                        parent[name] = collections.OrderedDict()
                    item = parent[name]
                    parents[level] = item

            else:  # attribute
                lastline_was_comment = False
                attr, __, value = line.partition('=')
                if not value:
                    continue
                attr = attr.strip()
                if not set(attr).issubset(valid_set):
                    print()
                    print("line: '{}'".format(line))
                    print("ERROR: Problem (2) parsing '{}' invalid character in line {}: {}. Valid characters are: {}".format(filename, linenu, attr, valid_chars))
                    continue
                if '|' in value:
                    item[attr] = [strip_quotes(x) for x in value.split('|')]
                else:
                    svalue = handle_multiline_string(strip_quotes(value))
                    try:
                        ivalue = int(svalue)
                        item[attr] = ivalue
                    except:
                        item[attr] = svalue.replace('\t', ' ')

        return config


# ##################################################################################
#   YAML handling routines
#

def yaml_save_roundtrip(filename, data):
    """
    Dump yaml using the RoundtripDumper and correct linespacing in output file
    """

    sdata = yaml.dump(data, Dumper=yaml.RoundTripDumper, version=yaml_version, indent=indent_spaces, block_seq_indent=2, width=12288, allow_unicode=True)

    ldata = sdata.split('\n')
    rdata = []
    for index, line in enumerate(ldata):
        # Fix for ruamel.yaml handling: Reinsert empty line before comment of next section
        if len(line.lstrip()) > 0 and line.lstrip()[0] == '#':
            indentcomment = len(line) - len(line.lstrip(' '))
            indentprevline = len(ldata[index-1]) - len(ldata[index-1].lstrip(' '))
            if indentprevline - indentcomment >= 2*indent_spaces:
                rdata.append('')
            rdata.append(line)
        # Fix for ruamel.yaml handling: Remove empty line with spaces that have been inserted
        elif line.strip() == '' and line != '':
            if ldata[index-1] != '':
                rdata.append(line)
        else:
            rdata.append(line)

    sdata = '\n'.join(rdata)
    if sdata[0] == '\n':
        sdata =sdata[1:]
    
    with open(filename+'.yaml', 'w') as outfile:
        outfile.write( sdata )



def yaml_save(filename, data):
    """
    ***Converter Special ***
    
    Save contents of an OrderedDict structure to a yaml file

    :param filename: name of the yaml file to save to
    :param data: OrderedDict to save
    """

    ordered = (type(data).__name__ == 'OrderedDict')
    dict_type = 'dict'
    if ordered:
        dict_type = 'OrderedDict'
    print(", saving to '{}'".format(os.path.basename(filename)+'.yaml'))
    if ordered:
        sdata = _ordered_dump(data, Dumper=yaml.SafeDumper, indent=indent_spaces, width=12288, allow_unicode=True, default_flow_style=False)
    else:
        sdata = yaml.dump(data, Dumper=yaml.SafeDumper, indent=indent_spaces, width=12288, allow_unicode=True, default_flow_style=False)
    sdata = _format_yaml_dump( sdata )

    if store_raw_output == True:
        with open(filename+'_raw.yaml', 'w') as outfile:
            outfile.write( sdata )

    # Test if roundtrip gives the same result
    data = yaml.load(sdata, yaml.RoundTripLoader)
    yaml_save_roundtrip(filename, data)

    # Test if second roundtrip gives the same result
#    Do not output the roundtrip-test file
#    with open(filename+'.yaml', 'r') as stream:
#        sdata = stream.read()        
#    data = yaml.load(sdata, yaml.RoundTripLoader)
#    yaml_save_roundtrip(filename+'2', data)


def _format_yaml_dump(data):
    """
    ***Converter Special ***
    
    Format yaml-dump to make file more readable
    (yaml structure must be dumped to a stream before using this function)
    | Currently does the following:
    | - Add an empty line before a new item

    :param data: string to format
    
    :return: formatted string
    """

    data = data.replace('\n\n', '\n')
    ldata = data.split('\n')
    rdata = []
    
    for index, line in enumerate(ldata):
        if len(line) > 0: 
            # Handle inline-comments from converter
            if line.find('##') > -1 and line.find(": '") > -1 and line[-1:] == "'":
                line = line.replace('##', '#')
                line = line.replace(": '", ": ")
                line = line[:-1]
            
            # Handle comments from converter
            if line.find('comment') > -1 and line.find(':') > line.find('comment'):
#                print('comment-line>', line, '<')
                indent = len(line) - len(line.lstrip(' '))
                if ldata[index+1][-1:] == ':':
                    indent = len(ldata[index+1]) - len(ldata[index+1].lstrip(' '))
                if line.find(': "|') > -1:
                    line = line[:-1]
                    line = line.replace(': "|', ': |')
                else:
                    line = line.replace(': ', ': |\\n', 1)
#                print('# ' + line[line.find("|\\n")+3:])
                line = " "*indent + '# ' + line[line.find("|\\n")+3:]
                line = line.replace('>**<', '')
                line = line.replace('\\n', '\n'+" "*indent + '# ')
                
            # Handle newlines for multiline string-attributes ruamel.yaml
            if line.find(': "|') > -1 and line[-1:] == '"' and line.find('\\n') > -1:
                indent = len(line) - len(line.lstrip(' ')) + indent_spaces
                line = line[:-1]
                line = line.replace(': "|', ': |')
                line = line.replace('\\n', '\n'+" "*indent)
                
        rdata.append(line)

    
    ldata = rdata
    rdata = []
    for index, line in enumerate(ldata):
        if len(line.lstrip()) > 0 and  line.lstrip()[0] == '#' and ldata[index+1][-1:] == ':':
            rdata.append('')
            rdata.append(line)
        
        # Insert empty line before section (key w/o a value)
        elif line[-1:] == ':':
            if not (len(ldata[index-1].lstrip()) > 0 and ldata[index-1].lstrip()[0] == '#'):
                # no empty line before list attributes
                if ldata[index+1].strip()[0] != '-':
                    rdata.append('')
                rdata.append(line)
            else:
                rdata.append(line)
        else:
            rdata.append(line)

    fdata = '\n'.join(rdata)
    if fdata[0] == '\n':
        fdata = fdata[1:]
    return fdata
        

def _ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    """
    Ordered yaml dumper
    Use this instead ot yaml.Dumper/yaml.SaveDumper to get an Ordereddict

    :param stream: stream to write to
    :param Dumper: yaml-dumper to use
    :**kwds: Additional keywords
    
    :return: OrderedDict structure
    """

    # usage example: ordered_dump(data, Dumper=yaml.SafeDumper)
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


# ==================================================================================
#   Convert all .conf files in a directory
#

def convert_directory(dir):

    for item_file in sorted(os.listdir(dir)):
        if item_file.endswith('.conf'):
            # Remove path and extension
            item_file = os.path.basename(item_file)
            item_file = os.path.splitext(item_file)[0]
            configurationfile = dir+'/'+item_file

            try:
                ydata = parse_for_convert(configurationfile+'.conf')
                if ydata != None:
                    yaml_save(configurationfile, ydata)
            except Exception as e:
                print()
                print("ERROR: Problem reading {0}: {1}".format(dir+'/'+configurationfile, e))


# ==================================================================================
#   Main Converter Routine
#

if __name__ == '__main__':

    # change the working diractory to the directory from which the converter is loaded (../tools)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    directory = os.path.abspath('../items')
    etc_dir = os.path.abspath('../etc')
    
    print('converting .conf-files from the following directories:')
    print('- item-directory  : ' + directory)
    print('- config-directory: ' + etc_dir)
    print('')

    ans_item = input('Convert item files (y/n)?: ').upper()
    ans_etc  = input('Convert config files (y/n)?: ').upper()
    print()
    
    if ans_item == 'Y':
        print('Converting item files:')
        convert_directory(directory)
        print('')

    if ans_etc == 'Y':
        print('Convering configuration files:')
        convert_directory(etc_dir)
        print('')

    if ans_item == 'Y' or ans_etc == 'Y':
        print('Conversion finished!')
        print()
        
    if ans_item == 'Y':
        print('You MUST move the old item.conf files out of the directory,')
        print('since SmartHomeNG tries to read all .yaml AND all .conf files')
        print('stored in the item directory.')
        print()

    if ans_etc == 'Y':
        print('You should move the old .conf files out of the etc directory to avoid')
        print('confusion. If both files (.conf and .yaml) exist, SmartHomeNG only reads')
        print('the .yaml file.')
        print()
