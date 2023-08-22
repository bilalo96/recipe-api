""" Test djnago management commands"""

from unittest.mock import patch #we going to mock behavior of the database because we need to be able to simulate when the database is returning or not
# from psycobg2 import OperationaError as Psycobg2Error #one of the possibility error we might get when try to connect to database
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command   # call the command we are testing
from django.db.utils import OperationalError # one of the possibility error depinding on what stage of the start up process it is
from django.test import SimpleTestCase# use SimpleTestCase because we testing the behavior of the database

@patch('core.management.commands.wait_for_db.Command.check')# we put patch decoretor here because we are test all different test methods,'core.management.commands.wait_for_db.Command.check' the command we are moucking
class CommandTests(SimpleTestCase):
    """Test commands"""
    def test_wait_for_db_ready(self,patched_check):# patched_check:to customize the behavior
        """Test waitng for database if ready"""
        patched_check.return_value=True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):# mocking work when exciptions
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])






