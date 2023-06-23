#!/usr/bin/env python3

####################################################
# >>> STOP Enterprise Cloud servers using API  <<< #
####################################################

# loads functions from *functions.py* file
from functions import *

def main():
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
            print("This is a CUBE and it will not shutoff.\nSkipping...\n")
            continue
        # Check if the server is in ACTIVE status (API ON)
        if check_server_state(server_id) == "AVAILABLE" :
            # In case is LINUX, ssh and shutdown the server, then API turn off the server
            if 'LINUX' in get_server_details(server_id)[1] :
                shutdown_linux(nic_ip)
            # In case is WINDOWS, remote shutdown the server (linux samba tool), then API turn off the server
            elif 'WINDOWS' in get_server_details(server_id)[1] :
                shutdown_windows(nic_ip)
            else:
            # In case of the OS is unknown, just API turn off the server
                print("OS unknown - graceful shutdown not possible.\n")
            print ("DEBUG enter shutoff_check")
            shutoff_check(server_id)
            print ("DEBUG enter shutoff_server")
            shutoff_server(server_id)
        else:
            print ("Unable to STOP Server {}.\nAlready off?\nManual check required.\n".format(server_id))

if __name__ == "__main__":
    main()