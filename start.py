#!/usr/bin/env python3

####################################################
# >>> START Enterprise Cloud servers using API <<< #
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
        print("Currently on {}" .format(server_id))
        # Check if it's a CUBE - if so, skip and continue (no stop/start for CUBES allowed)
        if get_server_details(server_id)[2] == 'CUBE' :
            print("This is a CUBE and no actions can be taken on this type of server.\nSkipping...\n")
            continue
        # In is NOT a CUBE, start the server
        else:
            # Check if the server is already OFF (INACTIVE)
            if check_server_state(server_id) == "INACTIVE" :
                # In case of the OS is unknown, just API turn off the server
                startup_server(server_id)
            else:
                print ("No actions taken on server {}.\nProbably already ON?\nManual check required.\n".format(server_id))

if __name__ == "__main__":
    main()