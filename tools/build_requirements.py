#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2018-       Martin Sinn                         m.sinn@gmx.de
# Copyright 2016        Christian Strassburg          c.strassburg@gmx.de
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

"""
This script assembles a complete list of requirements for the SmartHomeNG core and all plugins.

The list is not tested for correctness nor checked for contrary 
requirements. 

The procedure is as following:
1) walks the plugins subdirectory and collect all files with requirements
2) read the requirements for the core 
3) read all files with requirements and add them with source of requirement to a dict
4) write it all to a file all.txt in requirements directory

"""

import os
import fnmatch
import re
import pprint


def seperate_operator_version(op_vers):
    op_vers = op_vers.strip()
    if op_vers.startswith('>='):
        op = '>='
        vers = op_vers[2:]
    elif op_vers.startswith('=='):
        op = '=='
        vers = op_vers[2:]
    elif op_vers.startswith('<='):
        op = '<='
        vers = op_vers[2:]
    else:
        op = ''
        vers = op_vers
    vers = vers.strip()

    return [op,vers]


files = []
requirements = {}
SEP='/'
workdir = SEP.join(os.path.realpath(__file__).split(SEP)[:-2])

if not os.path.exists(workdir + SEP+"plugins"):
    print ("plugins directory not found!")
    exit(1)
if not os.path.exists(workdir + SEP+"requirements"):
    print ("requirements directory not found!")
    exit(1)

# build list of all plugins
for root, dirnames, filenames in os.walk(workdir + SEP + 'plugins'):
    for filename in fnmatch.filter(filenames, 'requirements.txt'):
        files.append(os.path.join(root, filename))

# Read base requirements
with open(workdir + SEP + "requirements"+SEP+"base.txt") as infile:
    for line in infile:
        if len(line.rstrip()) != 0:
            requirements.setdefault(line.rstrip(), []).append("SmartHomeNG Core")

# Read requirements for plugins
for fname in files:
    module = ''.join((fname.split(SEP))[-2:-1])

    with open(fname) as infile:
        for line in infile:
            if len(line.rstrip()) != 0:
                requirements.setdefault(line.rstrip(), []).append(module)

# build list of package requirement dicts
packagel = []
for key in requirements:
    packaged = {}
    wrk = re.split('<|>|=', key)
    packaged['pkg'] = wrk[0].strip()
    if packaged['pkg'].startswith('#'):
        continue

    pkg = key[len(packaged['pkg']):]
    if pkg.find(';') == -1:
        # keine python_version angegeben
        packaged['py_vers'] = ''
        wrk = re.split(',', pkg)
        wrk2 = []
        for r in wrk:
            r2 = seperate_operator_version(r)
            wrk2.append(r2)
        packaged['req'] = wrk2
    else:
        # python_version angegeben
        wrk = re.split(';', pkg)
        if wrk[1].startswith('python_version'):
            wrk[1] = wrk[1][len('python_version'):]
        packaged['py_vers'] = wrk[1]
        wrk = re.split(',', wrk[0])
        wrk2 = []
        for r in wrk:
            r2 = seperate_operator_version(r)
            wrk2.append(r2)
        packaged['req'] = wrk2

    plglist = requirements[key]
    packaged['plugins'] = requirements[key]
    packaged['key'] = packaged['pkg'] + '+' + packaged['py_vers']
    packagel.append(packaged)

# reassemble pip reqirements entries
for p in packagel:
    wrk = p['pkg']
    wrk += p['req'][0][0] + p['req'][0][1]
    if len(p['req']) > 1:
        wrk += ','+p['req'][1][0] + p['req'][1][1]
    if p['py_vers'] != '':
        wrk += ';' + 'python_version' + p['py_vers']
    p['requests'] = wrk

packagels = sorted(packagel, key=lambda k: k['key'])
#for p in packagels:
#    print(p)
#print('-----------------------------')

packagelo = []
for p in packagels:
    for idx, po in enumerate(packagelo):
        if p['key'] == po['key']:
            if p['req'][0][0] == po['req'][0][0]:
                if p['req'][0][0] == '>=' and (p['req'][0][1]) >= po['req'][0][1]:
                    if po['plugins'] != p['plugins']:
#                        print(po['pkg']+': '+'höhere Version (' + str(idx) + ') ' + po['req'][0][1] + ' / ' + p['req'][0][1])
                        pl = po['plugins']
                        pl.extend(p['plugins'])
                        p['plugins'] = pl
                        packagelo[idx] = p
                    break
                else:
                    print('gleiche Version '+ po['req'][0][1] + ' / '+ p['req'][0][1])
                    break
            elif po['req'][0][0] == '==':
                if p['req'][0][0] == '>=' and (not (po['req'][0][1] >= p['req'][0][1])):
                    print('ERROR: Requirements cannot be reconciled')
                    print(po['pkg']+': '+po['req'][0][0]+po['req'][0][1]+' is incompatible to '+p['req'][0][0]+p['req'][0][1])
                    packagelo.append(p)

#                print('po Gleichheit ' + po['req'][0][1] + ' / ' + p['req'][0][1], ' ', (po['req'][0][1] >= p['req'][0][1]))

            elif p['req'][0][0] == '==':
                print('p Gleichheit ' + po['req'][0][1] + ' / ' + p['req'][0][1])
    else:
        packagelo.append(p)


for key in requirements:
    requirements[key] = sorted(requirements[key], key=lambda name: (len(name.split('.')), name))


#pprint.pprint(requirements)

with open(workdir + SEP + 'requirements' + SEP+'all.txt', 'w') as outfile:
#    outfile.write("# !!!           SmartHomeNG          !!!\n")
#    outfile.write("# !!!      DON'T EDIT THIS FILE      !!!\n")
#    outfile.write("# !!!     THIS FILE IS GENERATED     !!!\n")
#    outfile.write("# !!! BY tools/build_requirements.py !!!\n")

#    for pkg, requirement in sorted(requirements.items(), key=lambda item: item[0]):
#        for req in sorted(requirement,
#                          key=lambda name: (len(name.split('.')), name)):
#           outfile.write('\n# {}'.format(req))
#        outfile.write('\n{}\n'.format(pkg))

    outfile.write("# !!!           SmartHomeNG          !!!\n")
    outfile.write("# !!!      DON'T EDIT THIS FILE      !!!\n")
    outfile.write("# !!!     THIS FILE IS GENERATED     !!!\n")
    outfile.write("# !!! BY tools/build_requirements.py !!!\n")
    for pkg in packagelo:
        for req in pkg['plugins']:
            outfile.write('\n# {}'.format(req))
#        outfile.write('\n{}\n'.format(pkg))
        outfile.write('\n{}\n'.format(pkg['requests']))

print("File 'requirements"+SEP+"all.txt' created.")
