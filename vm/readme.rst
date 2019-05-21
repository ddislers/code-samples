Nutanix Developer Portal Code Samples - VM Management
#####################################################

create_vm_v3_basic
..................

Bash script to create a Nutanix cluster VM with only the absolute bare minimum of required information i.e. VM name.  Uses **Prism REST API v3** and will work on both Prism Central and Prism Element.

Requires **create_vm_v3_basic.json** to exist in the same directory as the script and formatted as follows:

.. code:: json

  {"cluster_ip":"10.0.0.1","username":"admin","vm_name":"BasicVMViaAPIv3"}

.. code:: bash

  usage: create_basic_vm_v3

create_vm_v3_basic.py
.....................

Python 3.6 script to create a Nutanix cluster VM with only the absolute bare minimum of required information i.e. VM name.  Uses **Prism REST API v3** and will work on both Prism Central and Prism Element.

.. code:: bash

  usage: create_vm_v3_basic.py [-h] json

  positional arguments:
    json        JSON file containing query parameters

  optional arguments:
    -h, --help  show this help message and exit

Requires the passing of a JSON-formatted file that contains our request parameters.  This file must exist in the same directory as the script.

**create_vm_v3_basic.json** has been supplied in this repo as an example, as follows:

.. code:: json

  {"cluster_ip":"10.0.0.1","username":"admin","vm_name":"BasicVM"}

create_vm_v3_basic.ps1
......................

PowerShell script to create a Nutanix cluster VM with only the absolute bare minimum of required information i.e. VM name.  Uses **Prism REST API v3** and will work on both Prism Central and Prism Element.

.. code:: bash

  usage: PS C:\Users\NutanixDev\Samples> .\create_vm_v3_basic.ps1

- Set your cluster/CVM IP address by editing **$parameters.cluster_ip**
- Set the name for the new VM by editing **$parameters.vm_name**

create_vm_v3_detailed.py
........................

Python 3.6 script to create a Nutanix cluster VM with an extensive and detailed VM configuration.  Uses Prism REST API v3 and will work on both Prism Central and Prism Element.

.. code:: bash

  usage: create_vm_v3_detailed.py [-h] json

  positional arguments:
    json        JSON file containing query parameters

  optional arguments:
    -h, --help  show this help message and exit

Requires the passing of a JSON-formatted file that contains our request parameters.  This file must exist in the same directory as the script.

**create_vm_v3_detailed.json** has been supplied in this repo as an example, as follows:

.. code:: json

  {"cluster_ip":"10.0.0.1","username":"admin","vm_name":"DetailedVMViaAPIv3","vcpus_per_socket":1,"num_sockets":1,"memory_size_mib":1024,"first_disk_size_mib":1024,"first_nic_subnet_name":"vlan.0","first_nic_subnet_uuid":"00000000-0000-0000-0000-000000000000","cluster_name":"Cluster01","cluster_uuid":"00000000-0000-0000-0000-000000000000"}
