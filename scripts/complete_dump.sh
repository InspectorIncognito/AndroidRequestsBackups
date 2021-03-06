#!/bin/bash

#### #### #### #### #### #### #### #### #### #### #### #### #### #### 
#### BACKUP CREATION
#### #### #### #### #### #### #### #### #### #### #### #### #### #### 

TMP_DB_DUMP=database.sql
TMP_DB_DUMP_FULL="$TMP_BKP_FLDR"/"$TMP_DB_DUMP"

#### create image backup
#### ----- ----- ----- ----- ----- ----- ----- ----- -----

## compress all images
echo "- creating reports images backup"
cd "$IMGS_FLDR"
tar -zcf "$TMP_BKP_IMGS_FULL" *.jpeg
if [ ! -e "$TMP_BKP_IMGS_FULL" ]; then
	echo " - image backup file not found, but it should exists!: $TMP_BKP_IMGS_FULL"
	exit 1
fi

#### create migrations backup
#### ----- ----- ----- ----- ----- ----- ----- ----- -----

## compress migrations files
echo "- creating migrations backup"
cd "$MIGRATION_FLDR"
tar -zcf "$TMP_BKP_MIGRATION_FULL" *.py
if [ ! -e "$TMP_BKP_MIGRATION_FULL" ]; then
	echo " - migration backup file not found, but it should exists!: $TMP_BKP_MIGRATION_FULL"
	exit 1
fi

#### create database backup
#### ----- ----- ----- ----- ----- ----- ----- ----- -----

## dump to sql
echo "- creating complete backup ..."
cd "$TMP_BKP_FLDR"
pg_dump -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U"$DATABASE_USER" "$DATABASE_NAME" --table='*ndroid*equests_*' > "$TMP_DB_DUMP_FULL"
if [ ! -e "$TMP_DB_DUMP_FULL" ]; then
	echo "UPS!.. The db dump file was not found. Maybe, the pg_dump command failed!."
	echo "Required file: $TMP_DB_DUMP_FULL"
	exit 1
fi

## compress sql to tar.gz
tar -zcf "$TMP_DB_BACKUP" "$TMP_DB_DUMP"
echo "- looking for db backup results ..."
if [ ! -e "$TMP_BKP_DB_FULL" ]; then
	echo "UPS!.. The db backup file was not found."
	echo "Required file: $TMP_BKP_DB_FULL"
	exit 1
fi

## clean
rm -f "$TMP_DB_DUMP_FULL"
