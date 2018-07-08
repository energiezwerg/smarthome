
===================
Build Documentation
===================

This developer documentation and the german user documentation are part of the github repository.
An actual version of this documentation can be built from the develop branch by following the instructions below.


-----------------------------------
Checkout and Build of Documentation
-----------------------------------

Create a directory for the build process to work in:

.. code-block:: bash

   cd /usr/local
   sudo mkdir shng_doc
   sudo chown -R smarthome:smarthome /usr/local/shng_doc


Copy the build script from your SmartHomeNG installation to that directory and make it executable:

.. code-block:: bash

   cd shng_doc
   cp /usr/local/smarthome/doc/build_doc.sh .
   chmod 755 build_doc.sh


Install the Python packages needed for the build process:

.. code-block:: bash

   sudo pip3 install sphinx sphinx_rtd_theme recommonmark


Build the documentation:

.. code-block:: bash

   ./build_doc.sh


This script creates a subdirectory **work** in which the build process takes place and the results are stored.

After the script has finished, the user documentation is stored in

  /usr/local/smarthome/doc/build_doc/work/doc/user/build/html

and the develper documentation is stored in

  /usr/local/smarthome/doc/build_doc/work/doc/developer/build/html

Each documentation can be viewed by opening the corresponding index.html file in a browser.


---------------------------
Options of the build script
---------------------------

The script build_doc.sh has some options that are helpfull if the documentation is built repeatedly.

If you start the build script a second time, it will build the documentation from the files, that have been checked out
from git on the first run. If the files should be copied from git again, build_doc.sh has to be started with the option **-f**
(f = force checkout).

If only one of the documentations (user or developer) should be build, the options **-u** or **-d** can be used.

If the documentation should be built from the master branch, the option **-m** can be used. It should be combined with **-f** to
ensure that the right files are checked out.

