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

The `django-crontab` python package can be installed using: `pip install django-crontab`

To install the `AndroidRequestsBackups` app, simple clone this repository into each server root folder.


## Settings:

Next we list you the variables that you need to setup on `settings.py`. 

### On both cases
```
- VIZ_BKP_APP_IMGS_FLDR
This is the folder where are stored the images in the aplication

- VIZ_BKP_APP_REMOTE_BKP_FLDR
this is the folder where to put backups in transappviz server 

- VIZ_BKP_APP_TIME
the time lapse to send partial backups
```
### On transapp server
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
### On transappviz server
```
- VIZ_BKP_APP_REMOTE_DATABASE
database name of the transappviz server

- VIZ_BKP_APP_BKPS_LIFETIME
amount of days to keep complete backup files in the transappviz server, after that days this files will be deleted
this time is fixed to 2 days for partial backups
```



## Scheduling

Backups needs to be scheduled on each `settings.py` file. The configuration depends on the working mode of each server. 

### The sender (TranSapp)

The recommended setting is to schedule complete backups once a day and partial backups every 5 minutes.

```python
# ONLY ON (TranSapp)
CRONJOBS = [	
    # daily complete backup at 3:30am
    ('30  3 * * *', 'AndroidRequestsBackups.jobs.complete_dump', '> /tmp/vizbkpapp_complete_dump_log.txt')
    
    # partial backups every 5 minutes
    ('*/5 * * * *', 'AndroidRequestsBackups.jobs.partial_dump',  '> /tmp/vizbkpapp_partial_dump_log.txt')
]
```  

### The receiver (TranSappViz)

The recommended setting is to schedule a lot of update checkings, this way new updates are applied as soon as possible (it's super duper free to fail if there aren't updates, assuming you are not scheduling a check every second). 

It is very important to keep the partial backup time interval AT MOST at a half of the `VIZ_BKP_APP_TIME` parameter, otherwise bkps will be stacked, which will result on a fixed update delay of `VIZ_BKP_APP_BKPS_LIFETIME` days (for complete bkps) or 2 days (for partial bkps).

```python
# ONLY ON (TranSappViz)
CRONJOBS = [	
    # check for complete updates every one hour
    ('0 */1 * * *', 'AndroidRequestsBackups.jobs.complete_loaddata', '> /tmp/vizbkpapp_complete_loaddata_log.txt')
    
    # check for partial updates every 2 minutes
    ('*/2 * * * *', 'AndroidRequestsBackups.jobs.partial_loaddata',  '> /tmp/vizbkpapp_partial_loaddata_log.txt')
]
```

### On both

On each server, you can see the process logs on the `/tmp/vizbkpapp_*_log.txt` files.


This app also requires to set the following `django-crontab` related parameters:

```python
CRONTAB_LOCK_JOBS = True        # this way, partial jobs will stack.
CRONTAB_COMMAND_SUFFIX = '2>&1  # this way, we can see error on log files.
```

See also [this wiki](https://en.wikipedia.org/wiki/Cron#Format) on how to write a schedule using the cron format. 


### Considerations:

Disk Space is a limited resource on Web Servers, so make sure not to fill them with garbage (i.e, backups). This can only happen on (TranSappViz), specially for complete backups, when they are scheduled to be run too often (like hours, minutes.) and when the `VIZ_BKP_APP_BKPS_LIFETIME` variable is too large.

At the moment, (TranSappViz) has a 20GB disk, and each complete backup ... ...


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

sudo -u root python manage.py crontab show
```

## Future Work

- Decouple the postprocessing script call from the (TranSappViz) code (do not use a direct call to `transform.py`)
- Consider migrating to a queue based architecture. See also: "ETL Queues" on google.

