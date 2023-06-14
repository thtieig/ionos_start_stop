##################
# Functions file #
##################
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

def startup_server(serveruuid):
    payloadurl = "https://api.ionos.com/cloudapi/v6/datacenters/{}/servers/{}/start".format(dcuuid, serveruuid)
    r = requests.post(payloadurl, headers=authheader)
    print("Starting up server {} - billing resumed.\n".format(serveruuid))
#######################################################################################################################################
