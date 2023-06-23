#!/bin/bash
SCRIPTPATH=$(pwd)
RUNUSER=$USER
CRONSCRIPT="/etc/cron.d/ionos-start-stop"

clear

echo -e "
This script installs the cron job on the current server, to automatically start and stop your IONOS Enterprise Cloud servers.

By default, the cron does the following:
- starts all the servers at 6:30AM, Monday to Friday
- turn off the same servers at 8:30PM on the same days.
- Saturday and Sunday the servers stay off.

Once the setup is complete, you can review and manually modify the schedule.
"

echo -e "\033[0;31mWe do recommend to have manually tested the script, before installing the cron job.\033[0m"

echo -e "
=====================================================================================
The script will run as: \033[0;44m${RUNUSER}\033[0m
The path where the start and stop scripts is: \033[0;42m${SCRIPTPATH}\033[0m
=====================================================================================
"

echo -e "If the above details are NOT correct, press \033[0;31mCTRL+C to abort\033[0m.

Alternatively, press any key to continue..."

read voidvar


cat <<EOF > ${CRONSCRIPT}
#########################################################
#     Cron script - Modify the schedule accordingly     #
#########################################################

# * * * * * command to be executed
# - - - - -
# | | | | |
# | | | | ----- Day of week (0 - 7) (Sunday=0 or 7)
# | | | ------- Month (1 - 12)
# | | --------- Day of month (1 - 31)
# | ----------- Hour (0 - 23)
# ------------- Minute (0 - 59)


# Start all servers at 6:30 AM every working day (Mon-Fri)
30 6 * * 1-5 ${RUNUSER} cd ${SCRIPTPATH} && ./start.py 2>&1 | /usr/bin/logger -t IONOS-CRON ; cd -

# Stop all servers at 8:30 PM every working day (Mon-Fri)
30 20 * * 1-5 ${RUNUSER} cd ${SCRIPTPATH} && ./stop.py 2>&1 | /usr/bin/logger -t IONOS-CRON ; cd -

#########################################################
EOF

echo "${CRONSCRIPT} has been installed.
Here the content of the cron script:
"

echo -e '\033[0;46m'
cat  ${CRONSCRIPT}
echo -e '\033[0m'

echo -e "\nIf you want to modify the schedule, feel free to edit ${CRONSCRIPT} manually.\n\n"