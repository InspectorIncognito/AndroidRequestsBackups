from django.core.management import call_command
from django.test import SimpleTestCase, override_settings
from django.utils.six import StringIO
from AndroidRequestsBackups import jobs
from django.conf import settings
import subprocess
import os

class AndroidRequestsBackupsTest(SimpleTestCase):
    """
    HINT: these tests does not require the database, so you can
    run them as follow (to avoid the database setting up time):
     > python manage.py test -k AndroidRequestsBackups
    """

    def setUp(self):
        """ set variables in settings.py to test commands """
        self.app_path = settings.BASE_DIR + "/AndroidRequestsBackups/"


    def tearDown(self):
        pass


    def test_0_dependencies(self):
        self.assertTrue(settings.CRONTAB_LOCK_JOBS)
        self.assertEqual(settings.CRONTAB_COMMAND_SUFFIX, "2>&1")


    def test_1_dependencies(self):
        command = "bash " + self.app_path + "test/test_dependencies.bash"
        self.assertEqual(0, subprocess.call(command, shell=True))

    def test_2_settings(self):
        # # (TranSapp)
        # ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR    = "/tmp/backup_viz"
        # ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR = "/home/transapp/bkps"
        # ANDROID_REQUESTS_BACKUPS_TIME            = "5"
        # ANDROID_REQUESTS_BACKUPS_PRIVATE_KEY     = "/home/server/.ssh/id_rsa"
        # ANDROID_REQUESTS_BACKUPS_REMOTE_HOST     = "104.236.183.105"
        # ANDROID_REQUESTS_BACKUPS_REMOTE_USER     = "transapp"

        # # (TranSappViz)
        # ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR = "/home/transapp/bkps"
        # ANDROID_REQUESTS_BACKUPS_TIME            = "5"
        # ANDROID_REQUESTS_BACKUPS_BKPS_LIFETIME   = "4"
        pass
 

    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR + "/test")
    def test_3_remote(self):
        command = "bash " + self.app_path + "test/test_remote.bash"
        args  = " " + settings.ANDROID_REQUESTS_BACKUPS_REMOTE_USER
        args += " " + settings.ANDROID_REQUESTS_BACKUPS_REMOTE_HOST
        args += " " + settings.ANDROID_REQUESTS_BACKUPS_PRIVATE_KEY
        args += " " + settings.ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR
        
        ret_val = subprocess.call(command + args, shell=True)
        self.assertEqual(0, ret_val)


    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_USER=settings.ANDROID_REQUESTS_BACKUPS_THIS_USER_TEST)
    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_HOST='localhost')
    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_THIS_USER_HOME_TEST + "/bkps/test")
    @override_settings(ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR + "_test")
    def test_4_complete_dump(self):
        ret_val = jobs.complete_dump()
        self.assertEqual(0, ret_val)


    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_USER=settings.ANDROID_REQUESTS_BACKUPS_THIS_USER_TEST)
    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_HOST='localhost')
    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_THIS_USER_HOME_TEST + "/bkps/test")
    @override_settings(ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR + "_test")
    def test_5_partial_dump(self):
        ret_val = jobs.partial_dump()
        self.assertEqual(0, ret_val)


    # def test_6_complete_loaddata(self):
    #     ret_val = complete_loaddata()
    #     self.assertEqual(0, ret_val)


    # def test_7_partial_loaddata(self):
    #     ret_val = partial_loaddata()
    #     self.assertEqual(0, ret_val)

