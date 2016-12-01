from django.core.management import call_command
from django.test import SimpleTestCase
from django.utils.six import StringIO
from AndroidRequestsBackups.jobs import *
import subprocess

class AndroidRequestsBackupsTest(SimpleTestCase):

    def setUp(self):
        """ set variables in settings.py to test commands """
        self.app_path = settings.BASE_DIR + "/AndroidRequestsBackups/"
        settings.ANDROID_REQUESTS_BACKUPS_REMOTE_USER     = "mpavez"
        settings.ANDROID_REQUESTS_BACKUPS_REMOTE_HOST     = "localhost"
        settings.ANDROID_REQUESTS_BACKUPS_SECRET_KEY      = "/home/mpavez/.ssh/id_rsa"
        settings.ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR = "/home/mpavez/bkps/test"
        
        self.remote_user     = settings.ANDROID_REQUESTS_BACKUPS_REMOTE_USER
        self.remote_host     = settings.ANDROID_REQUESTS_BACKUPS_REMOTE_HOST
        self.secret_key      = settings.ANDROID_REQUESTS_BACKUPS_SECRET_KEY
        self.remote_bkp_fldr = settings.ANDROID_REQUESTS_BACKUPS_REMOTE_BKP_FLDR



    def test_0_dependencies(self):
        command = "bash " + self.app_path + "test/test_dependencies.bash"
        self.assertEqual(0, subprocess.call(command, shell=True))    


    def test_1_remote(self):
        
        command = "bash " + self.app_path + "test/test_remote.bash"
        args  = " " + self.remote_user
        args += " " + self.remote_host
        args += " " + self.secret_key
        args += " " + self.remote_bkp_fldr
        
        # call
        self.assertEqual(0, subprocess.call(command + args, shell=True))



    def test_command_output2(self):
        pass
        #out = StringIO()
        #call_command('visualization_backup_loaddata', stdout=out)
        #self.assertIn('Expected output', out.getvalue())
        #complete_loaddata()
        #partial_loaddata()
