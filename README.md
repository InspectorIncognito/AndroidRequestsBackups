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

On failure, all backup jobs are configured to send an email to the server admins, as defined on the `ADMINS` variable, so this requires the `ADMIN` and `EMAIL_*` configurations on the `settings.py` file.

### Table of contents

  * [About migrations](#about-migrations)
  * [Project Setup](#project-setup)
  * [Settings](#settings)
  	* [Common Settings](#on-both-servers)
  	* [(TranSapp) only](#on-transapp-server)
  	* [(TranSappViz) only](#on-transappviz-server)
  * [Scheduling](#scheduling)
  	* [(TranSapp) only](#the-sender-transapp)
  	* [(TranSappViz) only](#the-receiver-transappviz)
  	* [Common Settings](#on-both)
  	* [Considerations](#considerations)
  * [Jobs Usage](#finally-setting-up-the-jobs)
  * [Testing](#testing)
  * [Future Work](#future-work)



## About migrations

This aplication assumes both servers use the `AndroidRequests` app, this means both databases must have the same tables (`AndroidRequests_*`) and must be consistent to each other. This can be managed by running `AndroidRequests` migrations on both servers.

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

### Installing `AndroidRequestsBackups`

To install the `AndroidRequestsBackups` app, the recommended procedure is to install it as a submodule:
```bash
$ cd <server_repo>
$ git submodule add https://github.com/InspectorIncognito/AndroidRequestsBackups.git
$ git submodule init
$ git submodule update
```

#### Mantaining the submodule up to date:

Whenever you have modified the submodule files, you can push them as usual. But then, you will have to update your repo reference:
```bash
# add new/updated files
$ cd <submodule>
$ git add ...
$ git commit -m "blah ..."
$ git push ...

# update reference
$ cd <server_repo>
$ git add AndroidRequestsBackups
$ git commit -m "just updated my hash of AndroidRequestsBackups"
$ git push ...
```

Whenever you want to update your repository submodules, simply update all stuff:
```bash
$ cd <server_repo>

# download your repo changes
$ git fetch
$ git merge origin/master

# update submodule
$ git submodule update
```

For more information on git submodule usage, see [the official book](https://git-scm.com/book/en/v2/Git-Tools-Submodules).



## Settings:

Also, each server requires the `ANDROID_REQUESTS_BACKUPS` dictionary to be set on the `settings.py` file. The contents of this variable depends on whether the server is (TranSapp) or (TranSappViz).

To ease this process, we provide you a template file with the required configurations for each server. You can find them on `transapp_settings.template.py` (for TranSapp) and `transappviz_settings.template.py` (for TranSappViz). If you want to secure this values, you can copy the file to your `keys/` folder and call them like this:

```python
## load AndroidRequestsBackups settings
from server.keys.android_requests_backups import ANDROID_REQUESTS_BACKUPS
```

### On both servers

```python
# Folder (full path) where to put backups on remote (TranSappViz) server.
# Any file older than ANDROID_REQUESTS_BACKUPS['BKPS_LIFETIME'] days
# will be deleted!
# This value MUST match the one on the other server!, otherwise
# really bad stuff might happen
ANDROID_REQUESTS_BACKUPS['REMOTE_BKP_FLDR'] = "/home/username/bkps"

# Amount of data measured on minutes to send to the remote (TranSappViz)
# server, i.e, modified data since (now - ANDROID_REQUESTS_BACKUPS['TIME']).
# This value MUST match the one on the other server!, otherwise
# some data can be lost
ANDROID_REQUESTS_BACKUPS['TIME']            = 5
```

- The database name used to fetch and load data is taken from the `settings.DATABASES['default']['NAME']` variable.
- Images to send are retrieved from the `settings.MEDIA_IMAGE` folder. Only files with `.jpeg` extension are considered.

### On (TranSapp) server

```python
# Folder to use for tmp processing on (TranSapp) (full path).
# At some point, this folder can be completely deleted, so ensure
# this is not something important!, like '/home' or '/'."
ANDROID_REQUESTS_BACKUPS['TMP_BKP_FLDR']    = "/tmp/backup_viz"

# Remote (TranSappViz) server credentials.
# - private key: used to access the remote
# - remote host: remote host IP or hostname 
# - remote user: username on the remote
ANDROID_REQUESTS_BACKUPS['PRIVATE_KEY']     = "/root/.ssh/id_rsa"
ANDROID_REQUESTS_BACKUPS['REMOTE_HOST']     = "0.0.0.0"
ANDROID_REQUESTS_BACKUPS['REMOTE_USER']     = "username"
```

- Additionally, you need to create `.pgpass` file to save database password and then using with pg_dump command. This have to do in root home folder because is that user exects pg_dump

```bash
#hostname:port:database:username:password
```

### On (TranSappViz) server

```python
# Amount of days to keep "complete backup" files. Older files are deleted.
# This value is only valid for complete backups. Partial backups are only
# kept for 1 day
ANDROID_REQUESTS_BACKUPS['BKPS_LIFETIME']   = 4
```

## Scheduling

Backups needs to be scheduled on each `settings.py` file. The configuration depends on the working mode of each server.

As before, you can use the same template files to update the cronjobs configuration, this way you can manage all AndroidRequestsBackups configuration in one place:

```python
## load AndroidRequestsBackups jobs and update the current ones
from server.keys.android_requests_backups import android_requests_backups_update_jobs
CRONJOBS = android_requests_backups_update_jobs(CRONJOBS)
```


### The sender (TranSapp)

The recommended setting is to schedule complete backups once a day and partial backups every 5 minutes.

```python
# ONLY ON (TranSapp)
CRONJOBS = [	
    # daily complete backup at 3:30am
    ('30  3 * * *', 'AndroidRequestsBackups.jobs.complete_dump', '> /tmp/android_request_bkps_complete_dump_log.txt')
    
    # partial backups every 5 minutes
    ('*/5 * * * *', 'AndroidRequestsBackups.jobs.partial_dump',  '> /tmp/android_request_bkps_partial_dump_log.txt')
]
```  

### The receiver (TranSappViz)

The recommended setting is to schedule a lot of update checkings, this way new updates are applied as soon as possible (it's super duper free to fail if there aren't updates, assuming you are not scheduling a check every second). 

It is very important to keep the partial backup time interval AT MOST at a half of the `ANDROID_REQUESTS_BACKUPS['TIME']` parameter, otherwise bkps will be stacked, which will result on a fixed update delay of `ANDROID_REQUESTS_BACKUPS['BKPS_LIFETIME']` days (for complete bkps) or 2 days (for partial bkps).

```python
# ONLY ON (TranSappViz)
CRONJOBS = [	
    # check for complete updates every one hour
    ('0 */1 * * *', 'AndroidRequestsBackups.jobs.complete_loaddata', '> /tmp/android_request_bkps_complete_loaddata_log.txt')
    
    # check for partial updates every minute
    ('*/1 * * * *', 'AndroidRequestsBackups.jobs.partial_loaddata',  '> /tmp/android_request_bkps_partial_loaddata_log.txt')
]
```

### On both

On each server, you can see the process logs on the `/tmp/android_request_bkps_*_log.txt` files.

This app also requires to set the following `django-crontab` related parameters:

```python
CRONTAB_LOCK_JOBS = True        # this way, partial jobs will stack.
CRONTAB_COMMAND_SUFFIX = '2>&1' # this way, we can see error on log files.
```

See also [this wiki](https://en.wikipedia.org/wiki/Cron#Format) on how to write a schedule using the cron format. 


### Considerations:

Disk Space is a limited resource on Web Servers, so make sure not to fill them with garbage (i.e, backups). This can only happen on (TranSappViz), specially for complete backups, when they are scheduled to be run too often (like hours, minutes.) or when the `ANDROID_REQUESTS_BACKUPS['BKPS_LIFETIME']` variable is too large.

At the moment, (TranSappViz) has a 20GB disk, and each complete backup is ~50MB size .. so using a 10 days lifetime will give you a 500MB disk space usage. 

If somehow you managed to fill the disk, then everything will die... And you will have problems even when trying to connect by ssh to the server. YOU DO NOT WANT THIS TO HAPPEN!.. So please, be carefull.


## Finally, setting up the jobs

This must be done with root privileges on both servers. On both (TranSapp) and (TranSappViz), we need to access the database as the postgres user to perform dumps and loads. Also, some (TranSapp) server files can only be modified or read by root.

So, we need to remove outdated jobs, and add the new ones. Open a terminal and type:
```(bash)
cd <path to the server folder>

# remove and update this app jobs for root user
sudo -u root python manage.py crontab remove
sudo -u root python manage.py crontab add
```

You can check the all the jobs an user owns this way. Just make sure only the `root` user owns the `AndroidRequestsBackups` jobs. Open a terminal and type:
```(bash)
sudo -u <username> python manage.py crontab show

sudo -u root python manage.py crontab show
```


## Testing

### Overview

The AndroidRequestsBackups also implements some testing routines, following the django unit testing scheme.

It is recommended to put this tests on a continuous integration server, so you can notice early when the backup process brokens. However, this can only be made if you have complete access to the CI machine, because you will need to set up the root user keys.

Tests are managed via the `tests.py` file. The underlying implementation of some of them is in bash scripts, under the `tests` folder. At the moment, the following tests are provided:
- check if bash dependencies are installed
- check if `settings.py` defines the required parameters.
- perform a complete dump and send it to localhost
- perform a partial dump and send it to localhost
- perform a complete loaddata from localhost dummy backup files
- perform a partial loaddata from localhost dummy backup files

Also there is a test implemented as a cronjob, which will attempt to connect to the (TranSappViz) server from (TranSapp), and run a simple script through ssh and sftp.


### Prerequisites

#### settings.py

Some tests require you have properly set the following variables on settings.py file:

```bash
# user used to connect to localhost. Tipically this is yourself.
# just call `$echo $USER` on a bash shell. Try not to use the root user,
# as on any bug, you can mess your server!.
ANDROID_REQUESTS_BACKUPS['TEST_USER']      = "username"

# full path to where to place the testing junk. Files will be written onto
# the ANDROID_REQUESTS_BACKUPS['TEST_USER_HOME']/bkps/test folder.
ANDROID_REQUESTS_BACKUPS['TEST_USER_HOME'] = "/home/username"
```

#### KEYS

Tests require to perform a ssh connection from `root@localhost` to `<username>@localhost`. 

Thus, you will need to generate a public and private keys for root:
```bash
## connected as root
# rsa encription, no passphrase, filename
$ ssh-keygen -t rsa -N "" -f "/root/.ssh/id_rsa"
```

Then add the generated public key to the server user authorized keys registry:
```bash
## connected as root
$ cat /root/.ssh/id_rsa.pub >> /home/username/.ssh/authorized_keys
$ cat /home/username/.ssh/authorized_keys  # obs: make sure the key was be pasted on a new
                                           # line!, so you has not break the registry.
```

Also, this key must be used at least once!, to prevent raising a shell prompt asking whether you want to add your own fingerprint. 
```bash
## connected as root
# Just try a ssh localhost connection and accept when prompted:
$ ssh username@localhost -i /root/.ssh/id_rsa
```


#### Permissions

Also, make sure you have permissions to write to the `ANDROID_REQUESTS_BACKUPS['TEST_USER_HOME']/bkps/test` folder, otherwise, almost every test will fail.
```bash
$ ls -la                             # check permissions
$ sudo mkdir -p <folder>             # create it 
$ sudo chown -R <your_user> <folder> # change the owner to your user 
```


### AND Testing

#### Manual

Implemented tests will only run if called with root permissions. So just calling `python manage.py test` will not suffice. Root permissions are required to be able to perform some stuff, like `pg_dump` and database loads with `psql`. You can run them like this:
```bash
$ sudo -u root python manage.py test
```

If you only want to run the AndroidRequestsBackups tests, you can take advantage that tests does not require the database to have a certain state, so you can run them as follows (to avoid the database setting up time):
```bash
$ sudo -u root python manage.py test -k AndroidRequestsBackups
```

#### Automated Job

We also provide you a cronjob, so you can continuously check the connection state between both servers. The job will attempt to connect to the (TranSappViz) server from (TranSapp), run a simple script through ssh and send a file through sftp.

This test was designed as a job to be able to have a quick feedback when the connectivity is lost, which means your visualization server is outdated!. On failure, it will send an email to the admins, the same as the other jobs.

This job should only run on the (TranSapp) server. Just add it to the CRONJOBS variable:

```python
CRONJOBS = [
    ...
    # remote connection checker. every 1 hour
    ('0 */1 * * *', 'AndroidRequestsBackups.jobs.ssh_sftp_checker', '> /tmp/android_request_bkps_ssh_sftp_checker_log.txt'),
    ...
]
```

And remember to update your jobs:
```(bash)
sudo -u root python manage.py crontab remove
sudo -u root python manage.py crontab add
```


## Future Work

- Automatically check whether `AndroidRequests` migrations are applied to (TranSappViz): add this to a test and send an email or add it to the load script. Also, the current (TranSapp) migrations registry can be sent and checked on (TranSappViz).
- Decouple the postprocessing script call from the (TranSappViz) code (do not use a direct call to `transform.py`)
- Consider migrating to a queue based architecture. See also: "ETL Queues" on google.
