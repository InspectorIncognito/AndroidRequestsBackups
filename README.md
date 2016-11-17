# AndroidRequestsBackups

This app performs database backups from the (TranSapp) server and loads them to the (TranSappViz) server. So, this app is designed to be used on two servers, the Sender (TranSapp) and the Receiver (TranSappViz) of backups, both using the AndroidRequests models.

It provides two backup types, complete and partial, which are designed to be scheduled on a daily basis (long period of time) and diff backups run some minutes (short period of time), respectively.

The processing pipeline is as follows:

- (TranSapp): Dump database tables to one `.sql` file (complete) or multiple `.json` files (one for each table)
- (TranSapp): Copy the related media files
- (TranSapp): Compress all and send it through sftp.
- (TranSappViz): Check for new data, otherwise, finish.
- (TranSappViz): Decompress files.
- (TranSappViz): Load to database and media folders.
- (TranSappViz): Performs database postprocessing stuff. 

Complete and partial backups only differ on the amount of data that is sent. Complete backups performs a complete database dump, but partial only take into account the latest M minutes of data and only from AndroidRequests models which might have changed.


## Project Setup

For each server, you must add the following apps to the project `settings.py` file.

```python
INSTALLED_APPS = (
	# ...
	'django_crontab',
	'AndroidRequestsBackups',
)
```
In case that you don't have installed  django-crontab, use the next command

```pip install django-crontab```

## Scheduling

Backups needs to be scheduled on the `settings.py` file, using the cron app. 

On (TranSapp), the recommended setting is to schedule complete backups once a day and partial backups every 5 minutes.
```python
# ONLY ON (TranSapp)
CRONJOBS = [	
    # daily complete backup at 3:30am
    ('30  3 * * *', 'AndroidRequestsBackups.jobs.complete_dump', '> /tmp/vizbkpapp_complete_dump_log.txt')
    
    # partial backups every 5 minutes
    ('*/5 * * * *', 'AndroidRequestsBackups.jobs.partial_dump',  '> /tmp/vizbkpapp_partial_dump_log.txt')
]
```

On (TranSappViz), the recommended setting is to schedule a lot of update checkings, this way new updates are applied as soon as possible (it's super duper free to fail if there aren't updates, assuming you are not scheduling a check every second). It is very important to keep the partial backup time interval al least at a half of the `VIZ_BKP_APP_TIME` paameter, otherwise bkps can be lost.

```python
# ONLY ON (TranSappViz)
CRONJOBS = [	
    # check for complete updates every one hour
    ('0 */1 * * *', 'AndroidRequestsBackups.jobs.complete_loaddata', '> /tmp/vizbkpapp_complete_loaddata_log.txt')
    
    # check for partial updates every 2 minutes
    ('*/2 * * * *', 'AndroidRequestsBackups.jobs.partial_loaddata',  '> /tmp/vizbkpapp_partial_loaddata_log.txt')
]
```

You can see the process log on the `/tmp/vizbkpapp_*_log.txt` files.

Note that is highly recommended to set the parameter `CRONTAB_LOCK_JOBS = True` on `settings.py`. This is not mandatory, but unexpected stuff might happen otherwise!.

See also [this wiki](https://en.wikipedia.org/wiki/Cron#Format) on how to write a schedule using the cron format. 


## Settings TODO:

Next we list you the variables that you need to setup on `settings.py`. 

###On both cases
```
- VIZ_BKP_APP_IMGS_FLDR
This is the folder where are stored the images in the aplication

- VIZ_BKP_APP_REMOTE_BKP_FLDR
this is the folder where to put backups in transappviz server 

- VIZ_BKP_APP_TIME
the time lapse to send partial backups
```
###On transapp server
```
- VIZ_BKP_APP_HOST_DATABASE
database name on TranSapp server

- VIZ_BKP_APP_TMP_BKP_FLDR
where to store temporal bkp files on transapp server

- VIZ_BKP_APP_PRIVATE_KEY
the private key of transapp server that allow you to connect with transappviz server 

- VIZ_BKP_APP_REMOTE_HOST
the ip direction of the transapviz server

- VIZ_BKP_APP_REMOTE_USER
username to access to the transappviz server
```
###On transappviz server
```
- VIZ_BKP_APP_REMOTE_DATABASE
database name of the transappviz server

- VIZ_BKP_APP_BKPS_LIFETIME
amount of days to keep backup files in the transappviz server, after that days this files will be deleted
```

## Finally, setting up the jobs

This must be done with root privileges, because we want to access the databases, drop them and create new ones on (TranSappViz), and finally, because all files on (TranSapp) can be only modified by root.

So, we need remove outdated jobs, and add the new ones. Open a terminal and type:
```(bash)
cd <path to the server folder>

# remove and update this app jobs for root user
sudo -u root python manage.py crontab remove
sudo -u root python manage.py crontab add
```

You can check the all the jobs an user owns this way. Only make sure `root` owns our jobs. Open a terminal and type:
```(bash)
sudo -u <username> python manage.py crontab show

sudo -u root python manage.py crontab show```







