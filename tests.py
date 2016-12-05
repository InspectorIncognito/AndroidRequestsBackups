from django.test import SimpleTestCase, override_settings
from AndroidRequestsBackups import jobs
from django.conf import settings
import subprocess
import os


class AndroidRequestsBackupsTest(SimpleTestCase):
    """
    HINT:
    These tests does not require the database to have a certain
    state, so you can run them as follows (to avoid the database
    setting up time):

     > sudo -u root python manage.py test -k AndroidRequestsBackups

    ... note the root impersonating code. It is required to be able to
    performs some stuff, like pg_dump and database loads with sql.
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
        self.assertTrue(isinstance(int(settings.ANDROID_REQUESTS_BACKUPS_TIME), int))
        self.assertTrue(os.path.isabs(settings.ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR))

        if hasattr(settings, 'ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR'):
            self.assertTrue(os.path.isabs(settings.ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR))

        if hasattr(settings, 'ANDROID_REQUESTS_BACKUPS_PRIVATE_KEY'):
            self.assertTrue(os.path.isabs(settings.ANDROID_REQUESTS_BACKUPS_PRIVATE_KEY))

        if hasattr(settings, 'ANDROID_REQUESTS_BACKUPS_BKPS_LIFETIME'):
            self.assertTrue(isinstance(int(settings.ANDROID_REQUESTS_BACKUPS_BKPS_LIFETIME), int))

        if hasattr(settings, 'ANDROID_REQUESTS_BACKUPS_THIS_USER_HOME_TEST'):
            self.assertTrue(os.path.isabs(settings.ANDROID_REQUESTS_BACKUPS_THIS_USER_HOME_TEST))

        # how to test this?
        # ANDROID_REQUESTS_BACKUPS_REMOTE_HOST = "104.236.183.105"

        # and this?
        # ANDROID_REQUESTS_BACKUPS_REMOTE_USER = "transapp"

        # and also this?
        # DATABASE_NAME = "@as1^^&!invalid>>dfghjkl"

        # how to test this?
        # ANDROID_REQUESTS_BACKUPS_THIS_USER_TEST = "server"

    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR + "/test")
    def test_3_remote(self):
        command = "bash " + self.app_path + "test/test_remote.bash"
        args  = " " + settings.ANDROID_REQUESTS_BACKUPS_REMOTE_USER
        args += " " + settings.ANDROID_REQUESTS_BACKUPS_REMOTE_HOST
        args += " " + settings.ANDROID_REQUESTS_BACKUPS_PRIVATE_KEY
        args += " " + settings.ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR

        ret_val = subprocess.call(command + args, shell=True)
        self.assertEqual(0, ret_val)
        # pass

    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_HOST='localhost')
    @override_settings(ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR + "_test")
    def test_4_complete_dump(self):
        self.assertTrue(hasattr(settings, 'ANDROID_REQUESTS_BACKUPS_THIS_USER_TEST'))
        self.assertTrue(hasattr(settings, 'ANDROID_REQUESTS_BACKUPS_THIS_USER_HOME_TEST'))

        with self.settings(ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_THIS_USER_HOME_TEST + "/bkps/test"):
            with self.settings(ANDROID_REQUESTS_BACKUPS_REMOTE_USER=settings.ANDROID_REQUESTS_BACKUPS_THIS_USER_TEST):
                ret_val = jobs.complete_dump()
                self.assertEqual(0, ret_val)
                # pass

    @override_settings(ANDROID_REQUESTS_BACKUPS_REMOTE_HOST='localhost')
    @override_settings(ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_TMP_BKP_FLDR + "_test")
    def test_5_partial_dump(self):
        self.assertTrue(hasattr(settings, 'ANDROID_REQUESTS_BACKUPS_THIS_USER_TEST'))
        self.assertTrue(hasattr(settings, 'ANDROID_REQUESTS_BACKUPS_THIS_USER_HOME_TEST'))

        with self.settings(ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR=settings.ANDROID_REQUESTS_BACKUPS_THIS_USER_HOME_TEST + "/bkps/test"):
            with self.settings(ANDROID_REQUESTS_BACKUPS_REMOTE_USER=settings.ANDROID_REQUESTS_BACKUPS_THIS_USER_TEST):
                ret_val = jobs.partial_dump()
                self.assertEqual(0, ret_val)
                # pass

    def test_6_complete_loaddata(self):
        #ret_val = jobs.complete_loaddata()
        #self.assertEqual(0, ret_val)
        pass

    def test_7_partial_loaddata(self):
        # ret_val = partial_loaddata()
        # self.assertEqual(0, ret_val)
        pass
