SamsrtHomeNG Documentation
==========================

This directory contains the developer and the user documentation. The developer Documentation is
in English. The user documentation is in German and will be multilingual. It will be translated
into English.

The developer documantation (master language 'en') is stored in dec/developer
The user documantation (master language 'de') is going to be stored in dec/user


How to build the doc
====================

Currently only th generation of html is configured. There are sections in the Makefile which also offer 
other targets but they are not working right now. (Feel free to improve that!)

At first you need to satisfy the needed modules described in requirements.txt. 
You can install them at once with either::

sudo pip3 install requirements

or::

sudo pip3 install sphinx sphinx_rtd_theme recommonmark


If you are using virtualenv or pyenv you might first checkout your environment and choose a different way


Then you simply copy the file build_doc.sh from the doc directory to an empty directory on your system and start 
the shell script build_doc by typing './build_doc.sh

You will find your newly created files in doc/developer/build/html or doc/user/build/html. 
Your starting point is index.html

