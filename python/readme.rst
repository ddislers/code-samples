Nutanix Developer Portal Code Samples - Python
##############################################

To use the Python code samples, the following environment is recommended.

- Python >=3.7 (3.7 or later ...)
- Python **requests** (official documentation for requests_) and **urllib3** (official install for urllib3_) libraries.  This will need to be done **before** running the Python scripts.
- The accompanying JSON files from this repository (instructions and usage provided below).
- A suitable Python editor, e.g. Microsoft Visual Studio Code_ for GUI editing.
- Access to a Nutanix Cluster for API testing purposes.
- Nutanix Community Edition is supported but may not always provide the exact same APIs as a "full" Nutanix cluster.

.. note:: Please note that instructions provided in this repository will assume the use of Visual Studio Code for GUI editing purposes.  Otherwise ubiquitous editors such as **vi** can be used.

Python Script Usage
...................

The provided Python scripts are designed to be standalone and can be run without additional dependencies beyond those provided above.

The examples and screenshots below are from the **create_vm_v3_basic.py** sample.  This sample uses **create_vm_v3_basic.json** for the request parameters.

#. Open Visual Studio Code.
#. Create a new file, then copy and paste the code sample from this repository into the editor.
#. Save the file with **.py** extension, e.g. **create_vm_v3_basic.py**.
#. Visual Studio Code will ask if you would like to install the 'Python' and 'Pylint' extensions - these is highly recommended.
#. Create a new file, then copy and paste the contents of **create_vm_v3_basic.json** into the editor.
#. Save the file with **.json** extension, e.g. **create_vm_v3_basic.json**.
#. Edit the JSON values for **cluster_ip**, **username** and **vm_name** so that they match your environment & requirements.  The script will prompt for the password when run.
#. Within Visual Studio Code, click **View** > **Command Palette** and start typing **Terminal**.  Select **Python: Create Terminal** when the option is shown.

.. note:: Configuring Visual Studio Code for "real" debugging is beyond the scope of this readme.  However, an extensive guide can be found at https://code.visualstudio.com/docs/editor/debugging.

#. **Important note before continuing**: The Python 3.7 executable location will vary between Linux, OS X and Windows.  Please run the executable for your operating system in the steps below.

.. code-block: bash

   /usr/bin/python3.7 ./create_vm_v3_basic.py create_vm_v3_basic.json

#. The script will prompt for your account password, then submit the request based on the script spec.  An example based on **create_vm_v3_basic.py** is shown below, running on Ubuntu 19.04.

   .. figure:: script_output.png

.. _Community: https://visualstudio.microsoft.com/vs/community/
.. _Code: https://code.visualstudio.com/
.. _requests: https://2.python-requests.org/en/master/user/install/
.. _urllib3: https://pypi.org/project/urllib3/
