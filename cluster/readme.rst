Nutanix Developer Portal Code Samples - Cluster Management
##########################################################

create_image.py
...............

Python 3.6 script to create a Nutanix Images services image using the Prism REST API v2.0

.. code:: bash

  usage: create_image.py [-h] json

  positional arguments:
    json        JSON file containing query parameters

  optional arguments:
    -h, --help  show this help message and exit

Requires the passing of a JSON-formatted file that contains our request parameters.  This file must exist in the 

**params.json** has been supplied as an example, as follows:

.. code:: json

  {"ip":"10.0.0.1","username":"admin","ctr_name":"container1","ctr_uuid":"00000000-0000-0000-0000-000000000000","iso_url":"http://mirror.intergrid.com.au/centos/7.6.1810/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso","image_name":"CentOS7_Minimal","image_annotation":"CentOS 7 Minimal image created with Prism REST API v2.0"}