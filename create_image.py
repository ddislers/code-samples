#!/usr/bin/python3.6

import requests
import argparse
from base64 import b64encode

# setup our command line parameters
# for this example we only require the passing of parameters that are truly environment-specific
# other parameters are optional, otherwise generic values are used
parser = argparse.ArgumentParser()
parser.add_argument('ip',help='Cluster or CVM IP address')
parser.add_argument('username',help='Cluster username')
parser.add_argument('password',help='Cluster password')
parser.add_argument('ctr_name',help='Storage container name')
parser.add_argument('ctr_uuid',help='Storage container UUID')
parser.add_argument('--iso_url',help='ISO image URL',default='http://mirror.intergrid.com.au/centos/7.6.1810/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso')
parser.add_argument('--image_name',help='Image name',default='CentOS7_Minimal')
parser.add_argument('--image_annotation',help='Image annotation/description',default='CentOS 7 Minimal image created with Prism REST API v2.0')
args = parser.parse_args()

# setup the HTTP Basic Authorization header based on the supplied username and password
# please be aware of the security risks of passing credentials on the command line
encoded_credentials = b64encode(bytes(f"{args.username}:{args.password}",encoding="ascii")).decode("ascii")
auth_header = f'Basic {encoded_credentials}'

# setup the URL that will be used for the API request
url = f"https://{args.ip}:9440/api/nutanix/v2.0/images"

# setup the JSON payload that will be used for this request
payload = f'{{"annotation":"{args.image_annotation}","image_import_spec":{{"storage_container_name":"{args.ctr_name}","storage_container_uuid":"{args.ctr_uuid}","url":"{args.iso_url}"}},"image_type":"ISO_IMAGE","name":"{args.image_name}"}}'

# setup our request headers
# note the 'Authorization' header in particular as you'll need to generate this for your environment before continuing
headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'Authorization': f"{auth_header}",
    'cache-control': "no-cache"
    }

# submit the request
response = requests.request("POST", url, data=payload, headers=headers, verify=False)

print(response.text)
