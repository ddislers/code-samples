#!/usr/bin/env python3.7

'''
Python >=3.7 script to generate a human-readable XLSX
dump on a specified Nutanix Prism Central instance
'''

import os
import os.path
import sys
import socket
import getpass
import argparse
from time import localtime, strftime
from string import Template

try:
    import urllib3
    import requests
    import xlsxwriter
    from requests.auth import HTTPBasicAuth
    
except ModuleNotFoundError as error:
    # Output expected ImportErrors.
    print(f'''
    {error.__class__.__name__} exception has been caught.
    This typically indicates a required module is not installed.
    Please ensure you are running this script within a
    virtual development environment and that you have run the
    setup script as per the readme. Detailed exception info follows:

    {error}
    ''')
    sys.exit()


class DetailsMissingException(Exception):
    '''
    basic custom exception for when things "don't work"
    this is something that has been added simply to make extending
    the script much easier later
    '''
    pass


class EnvironmentOptions():
    '''
    this class is provided as an easy way to package the settings
    the script will use
    this isn't strictly necessary but does clean things up and removes
    the need for a bunch of individual global variables
    '''

    def __init__(self):
        self.cluster_ip = ""
        self.username = ""
        self.password = ""
        self.debug = False
        self.read_timeout = 3
        self.entity_response_length = 20
        # these are the supported entities for this environment
        self.supported_entities = ['vm', 'subnet', 'cluster', 'project',
                                   'network_security_rule', 'image',
                                   'host', 'blueprint', 'app']

    def __repr__(self):
        '''
        decent __repr__ for debuggability
        this is something recommended by Raymond Hettinger
        '''
        return (f'{self.__class__.__name__}(cluster_ip={self.cluster_ip},'
                f'username={self.username},password=<hidden>,'
                f'entity_response_length={self.entity_response_length},'
                f'read_timeout={self.read_timeout},debug={self.debug})')

    def get_options(self):
        '''
        method to make sure our environment options class holds the
        settings provided by the user
        '''

        parser = argparse.ArgumentParser()
        '''
        pc_ip is the only mandatory command-line parameter for this script
        username and password have been left as optional so that we have
        the opportunity to prompt for them later - this is better for
        security and avoids the need to hard-code anything
        '''
        parser.add_argument(
            'pc_ip',
            help='Prism Central IP address'
        )
        parser.add_argument(
            '-u',
            '--username',
            help='Prism Central username'
        )
        parser.add_argument(
            '-p',
            '--password',
            help='Prism Central password'
        )
        parser.add_argument(
            '-d',
            '--debug',
            help='Enable/disable debug mode'
        )

        args = parser.parse_args()

        '''
        do some checking to see which parameters we still need to prompt for
        conditional statements make sense here because a) we're doing a few of
        them and b) they're more 'Pythonic'
        '''
        self.username = (args.username if args.username else
                         input('Please enter your Prism Central username: '))
        self.password = args.password if args.password else getpass.getpass()

        '''
        conditional statement isn't required for the Prism Central IP since
        it is a required parameter managed by argparse
        '''
        self.cluster_ip = args.pc_ip

        self.debug = bool(args.debug == 'enable')


class ApiClient():
    '''
    the most important class in our script
    here we carry out the actual API request and process the
    responses, as well as any errors that returned from the
    response
    '''
    def __init__(self, cluster_ip, request, body,
                 username, password, timeout=10):
        self.cluster_ip = cluster_ip
        self.username = username
        self.password = password
        self.base_url = f'https://{self.cluster_ip}:9440/api/nutanix/v3'
        self.entity_type = request
        self.request_url = f'{self.base_url}/{request}'
        self.timeout = timeout
        self.body = body

    def __repr__(self):
        '''
        decent __repr__ for debuggability
        this is something recommended by Raymond Hettinger
        '''
        return (f'{self.__class__.__name__}(cluster_ip={self.cluster_ip},'
                f'username={self.username},password=<hidden>,'
                f'base_url={self.base_url},entity_type={self.entity_type},'
                f'request_url={self.request_url},'
                f'body (payload)={self.body})')

    def send_request(self):
        '''
        send the API request based on the parameters we
        have already collected
        '''

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        try:
            api_request = requests.post(
                self.request_url,
                data=self.body,
                verify=False,
                headers=headers,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=self.timeout,
            )
        except requests.ConnectTimeout:
            print('Connection timed out while connecting to '
                  f'{self.cluster_ip}. Please check your connection, '
                  'then try again.')
            sys.exit()
        except requests.ConnectionError:
            print('An error occurred while connecting to '
                  f'{self.cluster_ip}. Please check your connection, '
                  'then try again.')
            sys.exit()
        except requests.HTTPError:
            print('An HTTP error occurred while connecting to '
                  f'{self.cluster_ip}. Please check your connection, '
                  'then try again.')
            sys.exit()
        except Exception as error:
            '''
            catching generic Exception will throw warnings if you
            are running the script through something like flake8
            or pylint
            that's fine for what we're doing here, though :)
            '''
            print(f'An unhandled exception has occurred: {error}')
            print(f'Exception: {error.__class__.__name__}')
            print('Exiting ...')
            sys.exit()

        if api_request.status_code >= 500:
            print('An HTTP server error has occurred ('
                  f'{api_request.status_code})')
        else:
            if api_request.status_code == 401:
                # authentication error
                print('An authentication error occurred while connecting to '
                      f'{self.cluster_ip}. Please check your credentials, '
                      'then try again.')
                sys.exit()
            if api_request.status_code >= 401:
                print('An HTTP client error has occurred ('
                      f'{api_request.status_code})')
                sys.exit()
            else:
                print("Connected and authenticated successfully.")

        return api_request.json()


HTML_ROWS = {}
ENTITY_TOTALS = {}


def generate_xlsx(json_results):
    '''
    generate the actual XLSX doc
    this is where xlsxwriter is used
    '''

    day = strftime('%d-%b-%Y', localtime())
    time = strftime('%H%M%S', localtime())
    now = f'{day}_{time}'
    xlsx_filename = f'{now}_prism_central.xlsx'
    workbook = xlsxwriter.Workbook(xlsx_filename)

    '''
    the next block parses some of the Prism Central info that
    currently exists as individual lists
    '''

    '''
    these are entity types the script currently supports
    if new features or entity types become available in future,
    it should be a relatively simple task to update this list
    to support those entities
    '''
 #   supported_entities = [
 #       'vm', 'subnet', 'cluster', 'project', 'network_security_rule',
 #       'image', 'host', 'blueprint', 'app']
    supported_entities = ['vm', 'host']

    for row_label in supported_entities:
        ENTITY_TOTALS[row_label] = 0

    '''
    Create some worksheets. Probably a better way to do this, 
    xlsxwriter doesnt like dictionaries though. 
    '''

    worksheetvm = workbook.add_worksheet("vm")
    worksheetvm.write(0, 0, "VM Name")
    worksheetvm.write(0, 1, "Cluster")
    worksheetvm.write(0, 2, "Description")
    worksheetvm.write(0, 3, "vCPU Sockets")
    worksheetvm.write(0, 4, "Cores per Socket")
    worksheetvm.write(0, 5, "Memory(MiB)")

    worksheethost = workbook.add_worksheet("host")
    worksheethost.write(0, 0, "Host Serial")
    worksheethost.write(0, 1, "Host Name")
    worksheethost.write(0, 2, "Host IP")
    worksheethost.write(0, 3, "CVM IP")
    worksheethost.write(0, 4, "Memory (MiB)")
    worksheethost.write(0, 5, "CPU Sockets")
    worksheethost.write(0, 6, "Cores Per Socket")
    worksheethost.write(0, 7, "Hypervisor Version")
    worksheethost.write(0, 8, "Num VMs")

    print('\n')

    for json_result in json_results:

        # collect info that is common to all entity types
        for entity in json_result:
            if entity in supported_entities:
                ENTITY_TOTALS[f'{entity}'] = (json_result[1]["metadata"]
                                                ["total_matches"])
                print(f'Count of entity type {entity}: '
                        f'{json_result[1]["metadata"]["total_matches"]}')

        '''
        note that the next long section seems a little repetitive, but the
        string formatting for each entity is different enough to do it this way
        if each entity's info 'block' was the same, we could setup an iterator
        or use common formatting, but then the generated PDF wouldn't be very
        useful
        '''

        ##########
        #   VM   #
        ##########
        if json_result[0] == 'vm':
            wkscell = 1
            try:
                for vm in json_result[1]['entities']:
                    vm_name = vm["spec"]["name"]
                    cluster_name = vm["spec"]["cluster_reference"]["name"]
                    description = (vm['spec']['description']
                                    if 'description' in vm['spec']
                                    else 'None provided')
                    vcpus = vm['spec']['resources']['num_sockets']
                    coresper = vm['spec']['resources']['num_vcpus_per_socket']
                    memory = vm['spec']['resources']['memory_size_mib']

                    worksheetvm.write(wkscell, 0, vm_name)
                    worksheetvm.write(wkscell, 1, cluster_name)
                    worksheetvm.write(wkscell, 2, description)
                    worksheetvm.write(wkscell, 3, vcpus)
                    worksheetvm.write(wkscell, 4, coresper)
                    worksheetvm.write(wkscell, 5, memory)

                    wkscell += 1

            except KeyError:
                worksheetvm.write(wkscell, 0, "Data missing or malformed")

        ########
        # HOST #
        ########
        elif json_result[0] == 'host':
            wkscell = 1
            try:
                for host in json_result[1]['entities']:
                    if 'name' in host['status']:
                        host_serial = (host["status"]["resources"]
                                       ["serial_number"])
                        host_name = (host["status"]["name"])
                        host_ip = (host["status"]["resources"]
                                   ["hypervisor"]["ip"])
                        hypervisor_ver = (host["status"]["resources"]
                                   ["hypervisor"]["hypervisor_full_name"])
                        cvm_ip = (host["status"]["resources"]
                                  ["controller_vm"]["ip"])
                        num_vms = (host["status"]["resources"]
                                   ["hypervisor"]["num_vms"])
                        memory = (host["status"]["resources"]
                                   ["memory_capacity_mib"])
                        cpusock = (host["status"]["resources"]
                                   ["num_cpu_sockets"])
                        corepersock = (host["status"]["resources"]
                                   ["num_cpu_cores"])
                        
                        worksheethost.write(wkscell, 0, host_serial)
                        worksheethost.write(wkscell, 1, host_name)
                        worksheethost.write(wkscell, 2, host_ip)
                        worksheethost.write(wkscell, 3, cvm_ip)
                        worksheethost.write(wkscell, 4, memory)
                        worksheethost.write(wkscell, 5, cpusock)
                        worksheethost.write(wkscell, 6, corepersock)
                        worksheethost.write(wkscell, 7, hypervisor_ver)
                        worksheethost.write(wkscell, 8, num_vms)

                        wkscell += 1
                        
                    else:
                        host_serial = (host["status"]
                                       ["resources"]["serial_number"])
                        cvm_ip = (host["status"]["resources"]
                                  ["controller_vm"]["ip"])
                        
                        worksheethost.write(wkscell, 0, host_serial)
                        worksheethost.write(wkscell, 2, cvm_ip)

                        wkscell += 1

            except KeyError:
                worksheethost.write(wkscell, 0, "Data missing or malformed")

    print('\n')
    workbook.close()

    

def show_intro():
    '''
    function to simply show an extended help intro when the script
    is run - definitely not required but useful for development
    scripts like this one
    '''
    print(
        f'''
{sys.argv[0]}:

Connect to a Nutanix Prism Central instance, grab some high-level details then
generate a PDF from it

Intended to generate a very high-level and *unofficial* as-built document for
an existing Prism Central instance.

This script is GPL and there is *NO WARRANTY* provided with this script ...
AT ALL.  You can use and modify this script as you wish, but please make
sure the changes are appropriate for the intended environment.

Formal documentation should always be generated using best-practice methods
that suit your environment.
'''
    )


def main():
    '''
    main entry point into the 'app'
    every function needs a Docstring in order to follow best
    practices
    '''

    show_intro()

    environment_options = EnvironmentOptions()
    environment_options.get_options()

    if environment_options.debug:
        print(f'{environment_options}\n')

    '''
    disable insecure connection warnings
    please be advised and aware of the implications of doing this
    in a production environment!
    '''
    if environment_options.debug:
        print('Disabling urllib3 insecure request warnings ...\n')
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # make sure all required info has been provided
    if not environment_options.cluster_ip:
        raise DetailsMissingException('Cluster IP is required.')
    elif not environment_options.username:
        raise DetailsMissingException('Username is required.')
    elif not environment_options.password:
        raise DetailsMissingException('Password is required.')
    else:
        if environment_options.debug:
            print('All parameters OK.\n')

        '''
        'length' in Nutanix v3 API requests dictates how many entities
        will be returned in each request
        '''
        length = environment_options.entity_response_length
        if environment_options.debug:
            print(f'{length} entities will be returned for each request.')

        json_results = []
        endpoints = []

    for entity in environment_options.supported_entities:
        entity_plural = f'{entity}s'
        endpoints.append({'name': f'{entity}',
                          'name_plural': f'{entity_plural}',
                          'length': length})

    if environment_options.debug:
        print('Iterating over all supported endpoints ...\n')

    for endpoint in endpoints:
        client = ApiClient(
            environment_options.cluster_ip,
            f'{endpoint["name_plural"]}/list',
            (f'{{ "kind": "{endpoint["""name"""]}",'
                f'"length": {endpoint["""length"""]}}}'),
            environment_options.username,
            environment_options.password,
            environment_options.read_timeout
        )
        if environment_options.debug:
            print(f'Client info: {client}\n')
            print(f'Requesting "{client.entity_type}" ...\n')
        results = client.send_request()
        json_results.append([endpoint['name'], results])

    if environment_options.debug:
        print('Generating XLSX ...\n')
    generate_xlsx(json_results)

if __name__ == '__main__':
    main()
