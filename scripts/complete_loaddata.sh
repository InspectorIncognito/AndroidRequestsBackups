#!/bin/bash

cd "$BACKUP_FOLDER"/tmp

# check migrations where sent
if [ ! -e "$TMP_MIGRATION_BACKUP" ]; then
        echo "Backup file for migrations was not found: $TMP_IMG_BACKUP" 
        exit_and_free
fi

echo " - extracting migrations: $BACKUP_FOLDER/tmp/migrations" 
mkdir -p migrations && cd migrations
tar -zxf ../"$TMP_MIGRATION_BACKUP"


# check dump
cd "$BACKUP_FOLDER"/tmp/db
echo " - checking for JSON dump"
if [ ! -e database.sql ]; then
	echo "database.sql not found." 
	exit_and_free
fi
if [ ! -r database.sql ]; then
	echo "database.sql file found, but is not readable." 
	exit_and_free
fi

# load queries
echo " - loading records"
sudo -u postgres psql "$DATABASE_NAME" < database.sql


# copy images
echo " - copying images from $BACKUP_FOLDER/tmp/imgs to $IMGS_FLDR" 
cd "$BACKUP_FOLDER"
cd tmp
if [ "$(ls -A imgs/)" ]; then
    cp -arn imgs/* "$IMGS_FLDR"
else
    echo " - no images found"
fi

# copy migrations
echo " - copying migrations from $BACKUP_FOLDER/tmp/migrations to $MIGRATION_FLDR" 
cd "$BACKUP_FOLDER"
cd tmp
if [ "$(ls -A migrations/)" ]; then
    cp -arn migrations/* "$MIGRATION_FLDR"
else
    echo " - no migrations found"
fi
