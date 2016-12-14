from django.test import SimpleTestCase
from AndroidRequestsBackups import jobs
from django.conf import settings
import subprocess
import os
import unittest

@unittest.skipIf(os.geteuid() != 0, "SKIP: This tests requires to the run as root")
class AndroidRequestsBackupsTest(SimpleTestCase):
    
    def setUp(self):
        self.app_path = settings.BASE_DIR + "/AndroidRequestsBackups/"

    def tearDown(self):
        pass

    def test_1_dependencies(self):
        command = "bash " + self.app_path + "test/test_dependencies.bash"
        self.assertEqual(0, subprocess.call(command, shell=True))

    def test_2_settings(self):
        # dependencies settings
        self.assertTrue(hasattr(settings, 'CRONTAB_LOCK_JOBS'))
        self.assertTrue(hasattr(settings, 'CRONTAB_COMMAND_SUFFIX'))
        self.assertTrue(settings.CRONTAB_LOCK_JOBS)
        self.assertEqual(settings.CRONTAB_COMMAND_SUFFIX, "2>&1")

        # this app settings
        self.assertTrue(isinstance(int(settings.ANDROID_REQUESTS_BACKUPS['TIME']), int))
        self.assertTrue(os.path.isabs(settings.ANDROID_REQUESTS_BACKUPS['REMOTE_BKP_FLDR']))

        if hasattr(settings, 'ANDROID_REQUESTS_BACKUPS') and 'TMP_BKP_FLDR' in settings.ANDROID_REQUESTS_BACKUPS:
            self.assertTrue(os.path.isabs(settings.ANDROID_REQUESTS_BACKUPS['TMP_BKP_FLDR']))

        if hasattr(settings, 'ANDROID_REQUESTS_BACKUPS') and 'PRIVATE_KEY' in settings.ANDROID_REQUESTS_BACKUPS:
            self.assertTrue(os.path.isabs(settings.ANDROID_REQUESTS_BACKUPS['PRIVATE_KEY']))

        if hasattr(settings, 'ANDROID_REQUESTS_BACKUPS') and 'BKPS_LIFETIME' in settings.ANDROID_REQUESTS_BACKUPS:
            self.assertTrue(isinstance(int(settings.ANDROID_REQUESTS_BACKUPS['BKPS_LIFETIME']), int))

        if hasattr(settings, 'ANDROID_REQUESTS_BACKUPS') and 'TEST_USER_HOME' in settings.ANDROID_REQUESTS_BACKUPS:
            self.assertTrue(os.path.isabs(settings.ANDROID_REQUESTS_BACKUPS['TEST_USER_HOME']))

        # how to test this?
        # ANDROID_REQUESTS_BACKUPS['REMOTE_HOST'] = "104.236.183.105"

        # and this?
        # ANDROID_REQUESTS_BACKUPS['REMOTE_USER'] = "transapp"

        # and also this?
        # DATABASE_NAME = "@as1^^&!invalid>>dfghjkl"

        # how to test this?
        # ANDROID_REQUESTS_BACKUPS['TEST_USER'] = "server"

    def test_4_complete_dump(self):
        # assert params
        test_settings = settings.ANDROID_REQUESTS_BACKUPS
        if (
            'REMOTE_USER' not in test_settings or
            'REMOTE_HOST' not in test_settings or
            'REMOTE_BKP_FLDR' not in test_settings or
            'PRIVATE_KEY' not in test_settings or
            'TMP_BKP_FLDR' not in test_settings or
            'TIME' not in test_settings
        ):
            # return if missing parameters
            return

        self.assertTrue('TEST_USER' in settings.ANDROID_REQUESTS_BACKUPS)
        self.assertTrue('TEST_USER_HOME' in settings.ANDROID_REQUESTS_BACKUPS)

        # real test
        test_settings['REMOTE_HOST'] = 'localhost'
        test_settings['TMP_BKP_FLDR'] = settings.ANDROID_REQUESTS_BACKUPS['TMP_BKP_FLDR'] + "_test"
        test_settings['REMOTE_BKP_FLDR'] = settings.ANDROID_REQUESTS_BACKUPS['TEST_USER_HOME'] + "/bkps/test"
        test_settings['REMOTE_USER'] = settings.ANDROID_REQUESTS_BACKUPS['TEST_USER']
        with self.settings(ANDROID_REQUESTS_BACKUPS=test_settings):
            ret_val = jobs.complete_dump()
            self.assertEqual(0, ret_val)

    def test_5_partial_dump(self):
        # assert params
        test_settings = settings.ANDROID_REQUESTS_BACKUPS
        if (
            'REMOTE_USER' not in test_settings or
            'REMOTE_HOST' not in test_settings or
            'REMOTE_BKP_FLDR' not in test_settings or
            'PRIVATE_KEY' not in test_settings or
            'TMP_BKP_FLDR' not in test_settings or
            'TIME' not in test_settings
        ):
            # return if missing parameters
            return
        self.assertTrue('TEST_USER' in settings.ANDROID_REQUESTS_BACKUPS)
        self.assertTrue('TEST_USER_HOME' in settings.ANDROID_REQUESTS_BACKUPS)

        # real test
        test_settings['REMOTE_HOST'] = 'localhost'
        test_settings['TMP_BKP_FLDR'] = settings.ANDROID_REQUESTS_BACKUPS['TMP_BKP_FLDR'] + "_test"
        test_settings['REMOTE_BKP_FLDR'] = settings.ANDROID_REQUESTS_BACKUPS['TEST_USER_HOME'] + "/bkps/test"
        test_settings['REMOTE_USER'] = settings.ANDROID_REQUESTS_BACKUPS['TEST_USER']
        with self.settings(ANDROID_REQUESTS_BACKUPS=test_settings):
            ret_val = jobs.partial_dump()
            self.assertEqual(0, ret_val)

    def test_6_complete_loaddata(self):
        # assert params
        test_settings = settings.ANDROID_REQUESTS_BACKUPS
        if (
            'REMOTE_BKP_FLDR' not in test_settings or
            'BKPS_LIFETIME' not in test_settings or
            'TIME' not in test_settings
        ):
            # return if missing parameters
            return
        self.assertTrue('TEST_USER_HOME' in settings.ANDROID_REQUESTS_BACKUPS)

        # real test
        test_settings['REMOTE_BKP_FLDR'] = settings.ANDROID_REQUESTS_BACKUPS['TEST_USER_HOME'] + "/bkps/test"
        with self.settings(ANDROID_REQUESTS_BACKUPS=test_settings):
            ret_val = jobs.complete_loaddata()
            self.assertEqual(0, ret_val)

    def test_7_partial_loaddata(self):
        test_settings = settings.ANDROID_REQUESTS_BACKUPS
        if (
            'REMOTE_BKP_FLDR' not in test_settings or
            'BKPS_LIFETIME' not in test_settings or
            'TIME' not in test_settings
        ):
            # return if missing parameters
            return
        self.assertTrue('TEST_USER_HOME' in settings.ANDROID_REQUESTS_BACKUPS)

        # real test
        test_settings['REMOTE_BKP_FLDR'] = settings.ANDROID_REQUESTS_BACKUPS['TEST_USER_HOME'] + "/bkps/test"
        with self.settings(ANDROID_REQUESTS_BACKUPS=test_settings):
            ret_val = jobs.partial_loaddata()
            self.assertEqual(0, ret_val)
