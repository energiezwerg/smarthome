.. index:: Backup und Restore Tool
.. index:: Tools; Backup und Restore Tool

backup_restore.py
=================

Dieses Skript kann ein Backup der Konfiguration erzeugen, indem es die Konfigurationsdateien 
aus den Verzeichnissen **../etc**, **../items** und **../scenes** in eine tar.gz Datei 
zusammenführt.

Alternativ kann das Skript die Konfigurationsdateien aus einem früheren Backup wiederherstellen.


.. attention::

   Das Skript sichert in der jetzigen Form keine **Logiken** und und es erzeugt auch kein Backup 
   einer verwendeten **Datenbank**.


.. code::

   smarthome@<yourcomputer>:/usr/local/smarthome$ python3 tools/backup_restore.py -h

   usage: backup_restore.py [-h] (-b | -r dir) [--backupfile file]
                            [--include dir [dir ...]] [--exclude dir [dir ...]]
                            [-v] [--overwrite]

   optional arguments:
     -h, --help            show this help message and exit
     -b, --backup          create a config backup
     -r dir, --restore dir
                           restore a backup
     --backupfile file     name for outputfile (default: backup.tar.gz)
     --include dir [dir ...]
                           include directory to backup
     --exclude dir [dir ...]
                           exclude directory from backup (only for
                           etc,items,scenes)
     -v, --verbose         generate more output
     --overwrite           allways overwrite existing files

