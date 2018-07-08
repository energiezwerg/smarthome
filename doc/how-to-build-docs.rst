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


Then you simply copy two files (**build_doc.sh** and **remove_built_files.sh**) from the doc directory to an empty directory on your system and start 
the shell script build_doc by typing './build_doc.sh'

To build the user dokumentation only, start the script with option -u (./build_doc.sh -u)
To build the developer documentation only, start the script with option -d (./build_doc.sh -d)

The build process will create a directory named **work**

You will find your newly created files in doc/developer/build/html or doc/user/build/html in the **work** dirctory. 
Your starting point is index.html

If you want to make updates to the documentation, make changes to the files in the **work** directory.
When you start build_doc.sh again, the script will use the files in the **work** directory.

Do get your changes to github do the following:

- start the script **./remove_built_files.sh** to remove the created built files that should not be checked in
- copy the directory **source** from work/doc/developer to your local github environment (replacing the existing **source** directory, not merging it)
- copy the directory **source** from work/doc/user to your local github environment (replacing the existing **source** directory, not merging it)
- commit your changes

Afterwards yo can delete the directory **work**

