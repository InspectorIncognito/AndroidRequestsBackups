import subprocess
import datetime
from django.conf import settings
from django.core.mail import mail_admins


def _print_param_exception():
    print("MISSING SOME PARAMETERS FROM settings.py. MAKE SURE ALL " +
          "REQUIRED ANDROID_REQUESTS_BACKUPS FIELDS EXISTS.")


def _run_script(filename, short_desc, args=[]):

    # build command
    app_path = settings.BASE_DIR + "/AndroidRequestsBackups/"
    command = "bash " + app_path + "scripts/" + filename
    for arg in args:
        command += " " + arg

    # call
    ret_val = subprocess.call(command, shell=True)
    if ret_val != 0:

        # something failed, sending email
        subject = "Warning!: An AndroidRequestsBackups job has failed: " + short_desc.upper()
        message = "Dear admins,\n"
        message += "\n"
        message += "With date %s, " % datetime.datetime.now().isoformat()
        message += "a scheduled AndroidRequestsBackups job has failed.\n"
        message += "\n"
        message += "FAILING JOB: " + short_desc.upper() + "\n"
        message += "\n"
        message += "\n"
        message += "Please, inspect the related log file, as the CRONJOBS "
        message += "variable defines on the settings.py file.\n"
        message += "\n"
        message += "e.g: Run the following on (TranSapp):\n"
        message += " $ cat /tmp/android_request_bkps_complete_dump_log.txt\n"
        message += " $ cat /tmp/android_request_bkps_partial_dump_log.txt\n"
        message += "\n"
        message += "e.g: Run the following on (TranSappViz):\n"
        message += " $ cat /tmp/android_request_bkps_complete_loaddata_log.txt\n"
        message += " $ cat /tmp/android_request_bkps_partial_loaddata_log.txt\n"
        message += "\n"
        message += "\n"
        message += "Description by job type:\n"
        message += "------------------------------------------------\n"
        message += " - dump: This job runs on the (TranSapp) server. It "
        message += "attempts to perform a database backup and send it to "
        message += "the (TranSappViz) server.\n"
        message += " - loaddata: This job runs on the (TranSappViz) server. "
        message += "It attempts to perform a database load from (TranSapp) "
        message += "backups and run the related transformations.\n"
        message += "\n"
        message += "\n"
        message += "Description by job version:\n"
        message += "---------------------------------------------------\n"
        message += " - complete: This jobs work with the whole database, "
        message += "performing a full dump and load. This jobs are tipically "
        message += "scheduled to run once a day.\n"
        message += " - partial: This jobs work with a small amount of "
        message += "records, tipically only new or modified ones and up to "
        message += "the last N minutes. It performs small dumps and loads. "
        message += "This jobs are tipically scheduled to run every 5 minutes.\n"
        message += "\n"
        message += "\n"
        message += "Bye.\n"
        message += "\n"
        mail_admins(subject, message, fail_silently=True)
        # print "---"
        # print "Emailed message"
        # print "subject: " + subject
        # print "message: "
        # print message
        # print "---"

    return ret_val

def _retrieve_dump_params():
    try:
        element = (
            "dump.sh",
            [
                settings.BASE_DIR,
                settings.ANDROID_REQUESTS_BACKUPS['REMOTE_USER'],
                settings.ANDROID_REQUESTS_BACKUPS['REMOTE_HOST'],
                settings.ANDROID_REQUESTS_BACKUPS['REMOTE_BKP_FLDR'],
                settings.ANDROID_REQUESTS_BACKUPS['PRIVATE_KEY'],
                settings.ANDROID_REQUESTS_BACKUPS['TMP_BKP_FLDR'],
                settings.MEDIA_IMAGE,
                settings.DATABASES['default']['NAME']
            ]
        )
        return element
    except Exception as e:
        _print_param_exception()
        raise e


def _retrieve_load_params():
    try:
        element = (
            "loaddata.sh",
            [
                settings.BASE_DIR,
                settings.ANDROID_REQUESTS_BACKUPS['REMOTE_BKP_FLDR'],
                settings.MEDIA_IMAGE,
                settings.DATABASES['default']['NAME']
            ]
        )
        return element
    except Exception as e:
        _print_param_exception()
        raise e


def complete_dump():
    filename, params = _retrieve_dump_params()
    params.append("complete")
    return _run_script(filename, "complete dump", params)


def partial_dump():
    try:
        filename, params = _retrieve_dump_params()
        params.append("partial")
        params.append(settings.ANDROID_REQUESTS_BACKUPS['TIME'])
        return _run_script(filename, "partial dump", params)

    except Exception as e:
        _print_param_exception()
        raise e


def complete_loaddata():
    try:
        filename, params = _retrieve_load_params()
        params.append(settings.ANDROID_REQUESTS_BACKUPS['BKPS_LIFETIME'])
        params.append("complete")
        return _run_script(filename, "complete loaddata", params)

    except Exception as e:
        _print_param_exception()
        raise e


def partial_loaddata():
    try:
        filename, params = _retrieve_load_params()
        params.append("1")       # keep backups at most one day
        params.append("partial")
        params.append(settings.ANDROID_REQUESTS_BACKUPS['TIME'])
        return _run_script(filename, "partial loaddata", params)

    except Exception as e:
        _print_param_exception()
        raise e


def ssh_sftp_checker():
    app_path = settings.BASE_DIR + "/AndroidRequestsBackups/"
    command = "bash " + app_path + "test/test_remote.bash"
    args = " " + settings.ANDROID_REQUESTS_BACKUPS['REMOTE_USER']
    args += " " + settings.ANDROID_REQUESTS_BACKUPS['REMOTE_HOST']
    args += " " + settings.ANDROID_REQUESTS_BACKUPS['PRIVATE_KEY']
    args += " " + settings.ANDROID_REQUESTS_BACKUPS['REMOTE_BKP_FLDR'] + "/test"

    ret_val = subprocess.call(command + args, shell=True)
    if ret_val == 0:
        # we are done
        return

    # something failed, sending email
    subject = "Warning!: AndroidRequestsBackups connectivity check has failed."
    message = "Dear admins,\n"
    message += "\n"
    message += "With date %s, " % datetime.datetime.now().isoformat()
    message += "the AndroidRequestsBackups test for ssh and sftp connectivity "
    message += "has failed. This test attempts to stablish a ssh connection "
    message += "from the (TranSapp) to the (TranSappViz) server, and run a "
    message += "script on the remote. Then it stablishes an sftp connection "
    message += "to send a dummy file to the remote.\n"
    message += "\n"
    message += "\n"
    message += "Please, inspect the related log file, defined on the "
    message += "settings.py file. See the CRONJOBS variable. E.G: Run the "
    message += "following on the server:\n"
    message += "$ cat /tmp/android_request_bkps_ssh_sftp_checker_log.txt\n"
    message += "\n"
    message += "Bye.\n"
    message += "\n"    
    mail_admins(subject, message, fail_silently=True)
    print "---"
    print "Emailed message"
    print "subject: " + subject
    print "message: "
    print message
    print "---"
