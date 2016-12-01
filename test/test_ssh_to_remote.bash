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
#   the script will attempt to create a test folder and a test file
#

REMOTE_USER="$1"
REMOTE_HOST="$2"
SECRET_KEY="$3"
BACKUP_FOLDER="$4"

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
if [ ! -r "$SECRET_KEY" ]; then
	(>&2 echo " - (FAIL) ssh private key file not found or not readable: '$SECRET_KEY'.")
	exit 1 
fi
echo " - (OK) found ssh private key file: '$SECRET_KEY'."


# ssh connection
ssh -i "$SECRET_KEY" "$REMOTE_USERHOST" -q exit
if [ $? -ne 0 ]; then
	(>&2 echo " - (FAIL) there was a problem while trying to stablish an ssh connection to the remote server '$REMOTE_USERHOST'.")
	exit 1
fi
echo " - (OK) ssh connection works."


# ssh script
TEST_SCRIPT="/tmp/test_android_requests_backups_ssh.bash"
rm -f "$TEST_SCRIPT"
echo "mkdir -p \"$BACKUP_FOLDER\""                             >> "$TEST_SCRIPT"
echo "if [ ! -d \"$BACKUP_FOLDER\" ]; then exit 1; fi"         >> "$TEST_SCRIPT"
echo "rm -f \"$BACKUP_FOLDER\"/test_ssh_file"                  >> "$TEST_SCRIPT"
echo "if [ -e \"$BACKUP_FOLDER\"/test_ssh_file ]; then echo \"Failed to remove the file $BACKUP_FOLDER/test_ssh_file\"; exit 1; fi" >> "$TEST_SCRIPT"
echo "touch \"$BACKUP_FOLDER/test_ssh_file\""                  >> "$TEST_SCRIPT"
echo "if [ ! -w \"$BACKUP_FOLDER\" ]; then exit 1; exit 0; fi" >> "$TEST_SCRIPT"
echo "exit 0"                                                  >> "$TEST_SCRIPT"
ssh -i "$SECRET_KEY" "$REMOTE_USERHOST" "bash -s" -- < "$TEST_SCRIPT"
if [ $? -ne 0 ]; then
	(>&2 echo " - (FAIL): SSH script exited  with non zero status. Maybe, the '$REMOTE_USER' user does not has the proper permissions to create the folder: '$BACKUP_FOLDER'.")
	exit 1
fi
echo " - (OK) ssh script worked ok. successfully connected and ran script on remote."

# end
echo " - (WIN) The SSH test to a remote host passed successfully."
echo "################################################################################"
echo ""
exit 0
#############################################################################################################

