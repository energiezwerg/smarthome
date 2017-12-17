#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016 Christian Strassburg  c.strassburg@gmx.de
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


for root, dirnames, filenames in os.walk(workdir + SEP + 'plugins'):
    for filename in fnmatch.filter(filenames, 'requirements.txt'):
        files.append(os.path.join(root, filename))

with open(workdir + SEP + "requirements"+SEP+"base.txt") as infile:
    for line in infile:
        if len(line.rstrip()) != 0:
            requirements.setdefault(line.rstrip(), []).append("SmartHomeNG Core")
for fname in files:
    module = ''.join((fname.split(SEP))[-2:-1])

    with open(fname) as infile:
        for line in infile:
            if len(line.rstrip()) != 0:
                requirements.setdefault(line.rstrip(), []).append(module)

for key in requirements:
    requirements[key] = sorted(requirements[key], key=lambda name: (len(name.split('.')), name))
with open(workdir + SEP + 'requirements' + SEP+'all.txt', 'w') as outfile:
    outfile.write("# !!!           SmartHomeNG          !!!\n")
    outfile.write("# !!!      DON'T EDIT THIS FILE      !!!\n")
    outfile.write("# !!!     THIS FILE IS GENERATED     !!!\n")
    outfile.write("# !!! BY tools/build_requirements.py !!!\n")

    for pkg, requirement in sorted(requirements.items(), key=lambda item: item[0]):
        for req in sorted(requirement,
                          key=lambda name: (len(name.split('.')), name)):
           outfile.write('\n# {}'.format(req))
        outfile.write('\n{}\n'.format(pkg))
        
print("File 'requirements"+SEP+"all.txt' created.")
