#!/bin/bash
#
# this script
# > it creates the ftp incomming folder if not exists
#
BACKUP_FOLDER="$1"

echo " - [ON REMOTE VIZ]: -------- PRE LOAD INIT --------"

## CHECKS
# backup folder
if [   -z "$BACKUP_FOLDER" ]; then
	echo "Usage: $ bash script_pre.sh <BACKUP_FOLDER>"
	exit 1
fi


## WORK

# create backup folder
echo " - [ON REMOTE VIZ]: creating folder for ftp files: $BACKUP_FOLDER"
mkdir -p "$BACKUP_FOLDER"
if [ $? -ne 0 ] ; then
	echo " - [ON REMOTE VIZ]: Failed to create remote backup folder: $BACKUP_FOLDER."
	echo " - [ON REMOTE VIZ]: Maybe, this user does not have the required permissions to write there."
    exit 1
fi
if [ ! -w "$BACKUP_FOLDER" ]; then
	echo "BACKUP_FOLDER folder exists but is not writable: $BACKUP_FOLDER"
	exit 1
fi

echo " - [ON REMOTE VIZ]: -------- PRE LOAD INIT --------"
exit 0