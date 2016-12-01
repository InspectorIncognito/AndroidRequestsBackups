#!/bin/bash
#
# test/test_sftp_to_remote.bash
#
# This script tests the sftp connection to the remote visualization server
# 
# To do this, the following procedure is executed:
# - checks the required ssh key is present
# - attempts to send a file through sftp to the remote
#

REMOTE_USER="$1"
REMOTE_HOST="$2"
SECRET_KEY="$3"
BACKUP_FOLDER="$4"
# REMOTE_USER="mpavez"
# REMOTE_HOST="localhost"
# SECRET_KEY="/home/mpavez/.ssh/id_rsa"
# BACKUP_FOLDER="/home/mpavez/bkps/test"

# settings
echo ""
echo " AndroidRequestBackups test: sftp upload to the remote visualization server"
echo " -----------------------------------------------------------------------------"
if [ -z "$REMOTE_USER"   ]; then (>&2 echo " >>> (FAIL) Required parameter REMOTE_USER"  ) ; exit 1; fi
if [ -z "$REMOTE_HOST"   ]; then (>&2 echo " >>> (FAIL) Required parameter REMOTE_HOST"  ) ; exit 1; fi
if [ -z "$SECRET_KEY"    ]; then (>&2 echo " >>> (FAIL) Required parameter SECRET_KEY"   ) ; exit 1; fi
if [ -z "$BACKUP_FOLDER" ]; then (>&2 echo " >>> (FAIL) Required parameter BACKUP_FOLDER") ; exit 1; fi
# echo "---------"
# echo "using REMOTE_USER: $REMOTE_USER"
# echo "using REMOTE_HOST: $REMOTE_HOST"
# echo "using SECRET_KEY: $SECRET_KEY"
# echo "using BACKUP_FOLDER: $BACKUP_FOLDER"
# echo "---------"
REMOTE_USERHOST="$REMOTE_USER"@"$REMOTE_HOST"

# checks
if [ ! -r "$SECRET_KEY" ]; then
	(>&2 echo " >>> (FAIL) ssh private key file not found or not readable: '$SECRET_KEY'.")
	exit 1 
fi
echo " - (OK) found ssh private key file: '$SECRET_KEY'."

# file to send
TEST_SFTP_COMMANDS="/tmp/test_android_requests_backups_sftp"

# create dummy sftp commands
rm -f "$TEST_SFTP_COMMANDS"
if [ -e "$TEST_SFTP_COMMANDS" ]; then
	(>&2 echo " >>> (FAIL) Failed to delete previous tmp file: '$TEST_SFTP_COMMANDS'.")
	exit 1 
fi
echo "cd $BACKUP_FOLDER" > "$TEST_SFTP_COMMANDS"
echo "put $TEST_SFTP_COMMANDS" >> "$TEST_SFTP_COMMANDS"
echo " - (OK) generated sftp batch file on '$TEST_SFTP_COMMANDS'."

# send
sftp -p -i "$SECRET_KEY" -b "$TEST_SFTP_COMMANDS" "$REMOTE_USERHOST"
if [ $? -ne 0 ]; then
	(>&2 echo " >>> (FAIL) there was a problem while sending the sftp file '$TEST_SFTP_COMMANDS'.")
	exit 1
fi
echo " - (OK) sent file by sftp."

# end
echo " >>> (SUCCESS) The SFTP test to a remote host passed successfully."
exit 0
