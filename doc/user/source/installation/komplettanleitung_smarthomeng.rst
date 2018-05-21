
.. role:: bluesup

##########################################
SmartHomeNG installieren :bluesup:`update`
##########################################

- Schritte der Installation:
    - [zusätzliche Pakete installieren](#zusätzliche-pakete-installieren-1)
    - [Quellcode laden](#quellcode-laden)
    - [Erstmalige Konfiguration erstellen](#erstmalige-konfiguration-erstellen)
    - [Zusätzliche Python Module](#zusätzliche-python-module)
    - [SmartHomeNG starten](#smarthomeng-starten)
    - [Backend Plugin nutzen](#backend-plugin-nutzen)


zusätzliche Pakete installieren
-------------------------------

Zunächst müssen einige zusätzlichen Pakete erfüllt werden:
<!---
apt-get update nicht notwendig
openssh-server apache2  git-core wget bereits installiert
--->

<!---
```
sudo apt-get -y install dialog openntpd python3 python3-dev python3-setuptools unzip build-essential
sudo easy_install3 pip
```
--->

.. code-block:: bash

   sudo apt-get -y install dialog python3 python3-dev python3-setuptools unzip build-essential
   sudo apt-get install python3-pip


Dann noch Pythons Paketmanager PIP auf den neuesten Stand bringen:

.. code-block:: bash

   sudo python3 -m pip install --upgrade pip


