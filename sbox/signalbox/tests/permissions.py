import re
from datetime import timedelta, datetime
import django 
from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from signalbox.models import Study, Membership, Reminder, ReminderInstance, UserProfile
from signalbox.utils import execute_the_todo_list, send_reminders_due_now

from signalbox.allocation import allocate

from signalbox.tests import helpers


class TestDecorators(TestCase):
    """Test that we can access the DB and some key parameters are set."""
    
    fixtures = ['users.json', 'minimal_ask.json', 'serverconfig.json']
    
    def test_protected_view(self):
        """"""
        
        pass
        ### TODO