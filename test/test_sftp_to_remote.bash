#!/bin/bash
#
# test/test_sftp_to_remote.bash
#
# This script tests the sftp connection to the remote visualization server
# 
# To do this, the following procedure is executed:
# - checks the required ssh key is present
# - attempts to send a empty file through sftp to the remote
#

REMOTE_USER=
REMOTE_HOST=
SECRET_KEY=

REMOTE_USER=mpavez
REMOTE_HOST=localhost
SECRET_KEY=/home/mpavez/.ssh/id_rsa


# settings
echo "################################################################################"
echo "# test sftp connection and upload to the remote visualization server"
echo "################################################################################"
echo "---------"
echo "using REMOTE_USER: $REMOTE_USER"
echo "using REMOTE_HOST: $REMOTE_HOST"
echo "using SECRET_KEY: $SECRET_KEY"
echo "---------"
REMOTE_USERHOST="$REMOTE_USER"@"$REMOTE_HOST"

# checks
if [ ! -e "$SECRET_KEY" ]; then
	(>&2 echo " - (FAIL) ssh private key file not found: $SECRET_KEY.")
	exit 1 
fi
echo " - (OK): found ssh private key file: $SECRET_KEY."

# file to send
TEST_SFTP_COMMANDS="/tmp/test_android_requests_backups_sftp"

# create dummy sftp commands
rm -f "$TEST_SFTP_COMMANDS"
if [ -e "$TEST_SFTP_COMMANDS" ]; then
	(>&2 echo " - (FAIL) Failed to delete previous tmp file: $TEST_SFTP_COMMANDS.")
	exit 1 
fi
echo "cd /home/$REMOTE_USER" > "$SFTP_COMMANDS"
echo "put $TEST_SFTP_COMMANDS" >> "$TEST_SFTP_COMMANDS"
echo " - (OK) sent file by sftp."

# send
sftp -p -i "$SECRET_KEY" -b "$TEST_SFTP_COMMANDS" "$REMOTE_USERHOST"
if [ $? -ne 0 ]; then
	(>&2 echo " - (FAIL) there was a problem while sending the sftp file $TEST_SFTP_COMMANDS.")
	exit 1
fi
echo " - (OK) sent file by sftp."

# end
echo " - (WIN) . The SFTP test to a remote host passed successfully."
exit 0
#############################################################################################################

