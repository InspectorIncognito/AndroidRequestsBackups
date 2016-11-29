#!/bin/bash
#
# test/test_sftp_to_remote.bash
#
# This script tests the ssh connection to the remote visualization server
# 
# To do this, the following procedure is executed:
# - checks the required ssh key is present
# - attempts to create an ssh connection to the remote server
# - attempts to run an script file through ssh, on the remote server
#

REMOTE_USER=
REMOTE_HOST=
SECRET_KEY=
BACKUP_FOLDER=

REMOTE_USER="mpavez"
REMOTE_HOST="localhost"
SECRET_KEY="/home/mpavez/.ssh/id_rsa"
BACKUP_FOLDER="/home/mpavez/bkps/test"


# settings
echo "################################################################################"
echo "# test ssh connection to remote visualization server"
echo "################################################################################"
echo "---------"
echo "using REMOTE_USER: $REMOTE_USER"
echo "using REMOTE_HOST: $REMOTE_HOST"
echo "using SECRET_KEY: $SECRET_KEY"
echo "using BACKUP_FOLDER: $BACKUP_FOLDER"
echo "---------"
REMOTE_USERHOST="$REMOTE_USER"@"$REMOTE_HOST"


# checks
if [ ! -e "$SECRET_KEY" ]; then
	(>&2 echo " - (FAIL) ssh private key file not found: $SECRET_KEY.")
	exit 1 
fi
echo " - (OK): found ssh private key file: $SECRET_KEY."


# ssh connection
ssh -i "$SECRET_KEY" "$REMOTE_USERHOST" -q exit
if [ $? -ne 0 ]; then
	(>&2 echo " - (FAIL) there was a problem while trying to stablish an ssh connection to the remote server $REMOTE_USERHOST.")
	exit 1
fi
echo " - (OK) ssh connection works."

# ssh script
TEST_SCRIPT="/tmp/test_android_requests_backups_ssh.bash"
rm -f "$TEST_SCRIPT"
echo "mkdir -p $BACKUP_FOLDER" >> "$TEST_SCRIPT"
echo "if [ ! -e \"$BACKUP_FOLDER\" ]; then exit 1; else exit 0; fi"
ssh -i "$PRIVATE_KEY" "$REMOTE_USERHOST" "bash -s" -- < "$TEST_SCRIPT"
if [ $? -ne 0 ]; then
	(>&2 echo " - (FAIL): SSH script exited  with non zero status. Maybe, the $REMOTE_USER do not have the proper permissions to create the folder: $BACKUP_FOLDER")
	exit 1
fi
echo " - (OK) ssh script worked ok. successfully connected and ran script on remote."

# end
echo " - (WIN) . The SFTP test to a remote host passed successfully."
exit 0
#############################################################################################################

