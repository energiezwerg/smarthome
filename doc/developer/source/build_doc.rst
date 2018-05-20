
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

After the script has finished, the user documentation is stored in /usr/local/smarthome/doc/build_doc/work/doc/user/build/html
and the develper documentation is stored in /usr/local/smarthome/doc/build_doc/work/doc/developer/build/html.

Each documentation can be viewed by opening the corresponding index.html file in a browser.
