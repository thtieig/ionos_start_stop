# README #

Python script to start/stop IONOS Cloud Enterprise Servers automatically.   
NOTE: Currently, if the OS is off but the server is still active, script goes into a loop.  
NEXT: Add max timeout in shutoff_check function

## Requirements

### Infrastructure requirements
- Have this script installed on a CUBE server (NOT an Enterprise server) - we will call this "CUBE Management Server" (this might change in the future)
- Have a PRIVATE Network with all the Enterprise Cloud Servers we want to automatically start and stop connected to. Our CUBE Management Server needs to be connected as well to this private lan.

### OS requirements
- Debian or Ubuntu OS
- Python version 3 or above
- `token` file (see below how to generate one)
- `variables.py` file populated accordingly (rename `variables.py.template`)
- Package `samba-common` installed on the CUBE Management Server, in order to turn off Windows Servers remotely
- User on the CUBE Management Server able to ssh into all the LINUX servers that you want to turn off passwordless (using ssh key authentication). This user must have the permissions to run `shutdown` command.
- For the Windows servers, unless you use *Administrator*, we do recommend to setup a specific user with GPU policies that is authorised to do remote shutdown, and use those credentials instead.

## How does this script work?
The script works in this way:
- it finds all the Cloud Enterprise Servers connected to the local lan (defined in `variables.py`) and skip all the CUBE servers (including the CUBE Management Server)
- tries to remotely turn off the OS within the server (Linux and Windows are supported)
- once the OS is off, it will API shutdown the server, stopping the billing.

## How to use this script
The repository contains different files.  
In specific, we have `start.py` and `stop.py`. 
You need `variables.py` and `token` files to run start and stop scripts.
Simply run:
```
./stop.py
```
to STOP your Enterprise Cloud Servers, and
```
./start.py
```
to START them up again.

### How to create token file using `ionoctl`
```
# :~ ionosctl login
# :~ ionosctl token create > token
```
You can find more info on **ionoscl** [here](https://docs.ionos.com/cli-ionosctl)  
To install `ionosctl` on a Debian server, you can simply go [here](https://github.com/ionos-cloud/ionosctl/releases/). download the latest version available, extract and move `ionosctl` bin file into `/usr/local/bin`.  


### How to install the CRON job
This has been tested on Debian/Ubuntu distro.  
To schedule automatic start/stop of your servers, you can use the `cron` job script part of this package.       

To install the cron, simply run `./install_cron.sh` from the path where this file sits and make sure not to move this folder.  
The installer script will get your username and the current path of this repository stored on the local CUBE Management Server, and populate the cron script accordingly.  
If you want to install the cron as a different user or move the python scripts, we do recommend to do so before installing the cron, and running the installer with the right user.    

You can see the outcome of the cron in `/var/log/syslog`, grepping for *IONOS-CRON*.  

#### NOTES
We are aware that the file `variables.py` contains Windows password in clear. This is a prove of concept and we might review this part in the future. However, we do recommend to run `chmod 600 variables.py` to allow only root or the owner of the file to access it.  
Same concept for the `token` file. We do recommend `chmod 600 token` too.  
