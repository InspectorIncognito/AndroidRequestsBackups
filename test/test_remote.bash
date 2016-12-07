#!/bin/bash
#
# test/test_remote.bash
#
# it's a shortcut for calling the tests which interact with a remote machine
# it is important to call them in order: ssh -> sftp, as the ssh script will 
# create the required folder for sftp to work ok.

REMOTE_USER="$1"
REMOTE_HOST="$2"
PRIVATE_KEY="$3"
BACKUP_FOLDER="$4"

echo ""
echo ""
echo " # AndroidRequestBackups test: remote connection to (TranSappViz)"
echo " # #############################################################################"
echo " - date: $(date)"

if [ -z "$REMOTE_USER"   ]; then (>&2 echo " - (FAIL) Required parameter REMOTE_USER"  ) ; exit 1; fi
if [ -z "$REMOTE_HOST"   ]; then (>&2 echo " - (FAIL) Required parameter REMOTE_HOST"  ) ; exit 1; fi
if [ -z "$PRIVATE_KEY"   ]; then (>&2 echo " - (FAIL) Required parameter PRIVATE_KEY"  ) ; exit 1; fi
if [ -z "$BACKUP_FOLDER" ]; then (>&2 echo " - (FAIL) Required parameter BACKUP_FOLDER") ; exit 1; fi


echo " - using REMOTE_USER: $REMOTE_USER"
echo " - using REMOTE_HOST: $REMOTE_HOST"
echo " - using PRIVATE_KEY: $PRIVATE_KEY"
echo " - using BACKUP_FOLDER: $BACKUP_FOLDER"


THIS_SCRIPT=$(readlink -f "$0")
THIS_FOLDER=$(dirname "$THIS_SCRIPT")

# remote tests
cd "$THIS_FOLDER"
bash "test_ssh_to_remote.bash" "$REMOTE_USER" "$REMOTE_HOST" "$PRIVATE_KEY" "$BACKUP_FOLDER" 

cd "$THIS_FOLDER"
bash "test_sftp_to_remote.bash" "$REMOTE_USER" "$REMOTE_HOST" "$PRIVATE_KEY" "$BACKUP_FOLDER" 

echo ""
echo " - finished: $(date)"
exit 0