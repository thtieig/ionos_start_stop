#!/usr/bin/env python3

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
# > Create token (using ionoctl) < #
#
# :~ ionosctl login
# :~ ionosctl token create > token
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#


import requests
import time
import os

# loads all variables from *variables.py* file
from variables import *

with open('token', 'r') as file:
    token = file.read().rstrip()

authheader = {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(token)}


#######################################################################################################################################
def nics_on_lan():
    payloadurl = "https://api.ionos.com/cloudapi/v6/datacenters/{}/lans/{}/nics?depth=1".format(dcuuid, lanid)
    r = requests.get(payloadurl, headers=authheader).json()
    nics = r
    return nics

def get_server_details(serveruuid):
    payloadurl = "https://api.ionos.com/cloudapi/v6/datacenters/{}/servers/{}?depth=3".format(dcuuid, serveruuid)
    r = requests.get(payloadurl, headers=authheader).json()
    # vmstate -> OS on or off
    vmstate = r['properties']['vmState']
    # licenceType -> type of OS
    licenceType = r['properties']['bootVolume']['properties']['licenceType']
    # type -> CUBE or ENTERPRISE servers
    type = r['properties']['type']
    return vmstate, licenceType, type

def shutoff_check(serveruuid):
    while get_server_details(serveruuid)[0] != 'SHUTOFF':
        time.sleep(10)
        os = get_server_details(serveruuid)[1]
        print("{} Server {} is not off yet".format(os, serveruuid))
    print("{} Server {} is safely SHUTOFF".format(os, serveruuid))

def shutdown_linux(privateip):
    os.system("ssh -q -o LogLevel=error -o \"UserKnownHostsFile=/dev/null\" -o \"StrictHostKeyChecking=no\" -t {}@{} 'shutdown -h now'".format(linuxadmin, privateip))

def shutdown_windows(privateip):
    os.system("net rpc shutdown -f -t -0 -C 'testing shutdown' -U \"{}\"%\"{}\" -I {}".format(windowsadmin, windowspass, privateip))

def shutoff_server(serveruuid):
    payloadurl = "https://api.ionos.com/cloudapi/v6/datacenters/{}/servers/{}/stop".format(dcuuid, serveruuid)
    r = requests.post(payloadurl, headers=authheader)
    print("Shutting off server {} - stopping the billing! Happy days!\n".format(serveruuid))

#######################################################################################################################################

# Loop through all the NICs connected to the private lan
for nic in nics_on_lan()['items'] :
    # Get the full href of the nic to extract the serverID
    nic_href = nic['href']
    # String manipulation to extract serverID from the NIC's URL
    server_id = nic_href[nic_href.find('servers/')+len('servers/'):nic_href.rfind('/nics')]
    # Get the first IP of the NIC
    nic_ip = nic['properties']['ips'][0]
    print("Currently on {} {}" .format(server_id, nic_ip))
    # Check if it's a CUBE - if so, skip and continue (no stop/start for CUBES allowed)
    if get_server_details(server_id)[2] == 'CUBE' :
        print("This is a CUBE and it will not shutoff.")
        continue
    # In case is LINUX, ssh and shutdown the server, then API turn off the server
    elif 'LINUX' in get_server_details(server_id)[1] :
        shutdown_linux(nic_ip)
    # In case is WINDOWS, remote shutdown the server (linux samba tool), then API turn off the server
    elif 'WINDOWS' in get_server_details(server_id)[1] :
        shutdown_windows(nic_ip)
    else:
    # In case of the OS is unknown, just API turn off the server
        print("OS unknown - graceful shutdown not possible.")
    shutoff_check(server_id)
    shutoff_server(server_id)
