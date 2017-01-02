# ----------------------------------------------------------------------------
# VIZ_BACKUP_APP
# see also: AndroidRequestsBackups/REAME.md
ANDROID_REQUESTS_BACKUPS = {
	
	# Folder (full path) where to put backups on remote (TranSappViz) server.
	# Any file older than ANDROID_REQUESTS_BACKUPS['BKPS_LIFETIME'] days
	# will be deleted!
	# This value MUST match the one on the other server!, otherwise
	# really bad stuff might happen
	'REMOTE_BKP_FLDR' : '/home/transapp/bkps',


	# Amount of data measured on minutes to send to the remote (TranSappViz)
	# server, i.e, modified data since (now - ANDROID_REQUESTS_BACKUPS['TIME']).
	# This value MUST match the one on the other server!, otherwise
	# some data can be lost
	'TIME'            : 5,

	# Amount of days to keep "complete backup" files. Older files are deleted.
	# This value is only valid for complete backups. Partial backups are only
	# kept for 1 day
	'BKPS_LIFETIME'   : 4,

	## testing
	# user used to connect to localhost. Tipically this is yourself.
	# just call `$echo $USER` on a bash shell.
	'TEST_USER'       : 'username',
	
	# full path to where to place the testing junk. Files will be written onto
	# the ANDROID_REQUESTS_BACKUPS['TEST_USER_HOME']/bkps/test folder.
	'TEST_USER_HOME'  : '/home/username',
}
# ----------------------------------------------------------------------------

def android_requests_backups_update_jobs(cronjobs):

	# check for complete updates every one hour
	cronjobs.append(
		('0 */1 * * *', 'AndroidRequestsBackups.jobs.complete_loaddata',
		'> /tmp/android_request_bkps_complete_loaddata_log.txt')
	)

	# check for partial updates every minute
	cronjobs.append(
		('2-58/1 * * * *', 'AndroidRequestsBackups.jobs.partial_loaddata',
		'> /tmp/android_request_bkps_partial_loaddata_log.txt')
	)

	return cronjobs
