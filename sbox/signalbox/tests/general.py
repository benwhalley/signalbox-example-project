"""
XXX still to test

OBSERVATION
add_jitter()
canonical_reply
still_open()
open_for_data_entry()

make_reply()
variables_which_differ_between_multiple_replies()


Scoresheets

ELSEHWERE
add_participant()
randomise_membership()
do_todo()


awaiting_followup()

EMAIL.do()
TwilioCall
TelephoneCall - e.g. reschedule()



signalbox.middleware.cms_page_permissions_middleware

LOW PRIORITY
resolve_double_entry_conflicts()

"""


import re
from datetime import timedelta, datetime
import django
from django.core import mail
from django.conf import settings
from django.test import TestCase

from django.contrib.auth.models import User
from signalbox.models import Study, Membership, Reminder, ReminderInstance, UserProfile
from signalbox.utils import execute_the_todo_list, send_reminders_due_now
from signalbox.models.observation_timing_functions import observations_due_in_window

from signalbox.allocation import allocate

from signalbox.tests import helpers


class TestConfig(TestCase):
    """Test that we can access the DB and some key parameters are set."""

    fixtures = ['users.json',]

    def test_key_parameters_exist(self):
        """Without these, things would probably break."""

        assert len(settings.SECRET_KEY) > 0
        assert type(settings.SITE_ID) == int
        assert settings.CALLERID
        assert settings.SMS_CALLERID
        assert settings.DEFAULT_FROM_EMAIL


    def test_loading_fixtures(self):
        users = User.objects.all()
        assert users.count() > 1


    def test_database_writeable(self):
        s, new = Study.objects.get_or_create(consent_text = "testmenow")
        s.save()
        assert Study.objects.filter(consent_text='testmenow').count() == 1
        s.delete()



class TestUserProfiles(TestCase):
    """Check functionality related to UserProfile model."""


    def test_user_profile_created(self):
        """Check the signal to create a user profile has fired."""

        user = helpers.make_user({'username': "TEST", 'email':"TEST@TEST.COM", 'password': "TEST"})
        assert type(user.get_profile()) == UserProfile



class TestScheduling(TestCase):
    """Check that Observations are created correctly and can be sent."""

    def test_creating_membership(self):
        """ -> Membership """
        study = Study.objects.get(slug='test-study')
        user = helpers.make_user({'username': "TEST", 'email':"TEST@TEST.COM", 'password': "TEST"})
        membership = helpers.make_membership(study, user)
        assert type(membership)==Membership

        return membership


    def test_adding_observations(self):
        """ -> Membership """

        membership = self.test_creating_membership()
        assert membership.condition == None
        allocate(membership)
        assert membership.condition != None

        assert len(membership.observations())==0
        membership.add_observations()
        assert len(membership.observations())==6

        return membership


    def test_observation_timings(self):
        """Check that observation timings are as we expect -> None"""

        membership = self.test_adding_observations()
        first = membership.observations()[0]
        last = membership.observations()[5]
        assert first.due < last.due
        assert first.ready_to_send() == True
        assert last.ready_to_send() == False


    def test_observation_due_selection(self):
        """Test the function which selects Observations in the time window."""

        membership = self.test_adding_observations()
        assert len(observations_due_in_window()) == 1
        ob = observations_due_in_window()[0]
        ob.due = datetime.now()+timedelta(days=100)
        ob.save()
        assert len(observations_due_in_window()) == 0


    def test_reminders_get_added(self):
        """Check that ReminderInstances are added for each Observation -> (Observation, Reminder) """
        membership = self.test_adding_observations()
        assert ReminderInstance.objects.all().count() == 3 # added to email surveys
        first = membership.observations().filter(created_by_script__reference="test-email-survey")[0]
        first_reminder = first.reminderinstance_set.all()[0]
        assert first_reminder.due - first.due == timedelta(days=2) # 48 hours later

        return (first, first_reminder)


    def test_reminder_is_sent(self):
        first, reminder = self.test_reminders_get_added()
        send_reminders_due_now()
        assert len(mail.outbox) == 0 # nothing sent

        reminder.due = datetime.now() # fiddle the time
        reminder.save()
        send_reminders_due_now()
        assert len(mail.outbox) == 1 # has been sent now

        send_reminders_due_now()
        assert len(mail.outbox) == 1 # not resent now


    def test_sending_observation(self):
        """ -> Observation """

        membership = self.test_adding_observations()
        first_observation = membership.observations().filter(
            created_by_script__reference="test-email-survey")[0]

        # test the email gets sent
        assert len(mail.outbox) == 0
        success, message = first_observation.do()
        assert success == True
        assert len(mail.outbox) == 1

        return first_observation


    def test_pausing_study(self):
        """-> None """

        membership = self.test_adding_observations()
        first_observation = membership.observations()[0]

        assert first_observation.ready_to_send() == True
        first_observation.dyad.study.paused = True
        assert first_observation.ready_to_send() == False


    def test_deactivating_membership(self):
        """-> None """

        membership = self.test_adding_observations()
        first_observation = membership.observations()[0]

        assert first_observation.ready_to_send() == True
        first_observation.dyad.active = False
        assert first_observation.ready_to_send() == False


    # def test_not_resending_observation(self):
    #     """Once an Observation has been sent, it shouldn't be resent immediately."""
    #     observation = self.test_sending_observation()
    #     observation.do()
    #     assert observation.ready_to_send() == False

    #     # unless we fiddle the last_attempted datetime
    #     observation.last_attempted = observation.last_attempted + timedelta(days=-1)
    #     assert observation.ready_to_send() == True


    # def test_resending_when_redial_delay_at_zero(self):
    #     """Check that Observation can be resent immediately if study.redial_delay == 0"""

    #     observation = self.test_sending_observation()
    #     assert observation.ready_to_send() == False
    #     observation.dyad.study.redial_delay = 0
    #     assert observation.ready_to_send() == True


    def test_no_sending_after_multiple_attempts(self):
        membership = self.test_adding_observations()
        observation = membership.observations()[0]
        assert observation.ready_to_send() == True
        observation.attempt_count = 50
        assert observation.ready_to_send() == False


    def test_emailsurvey_email_contains_url(self):
        "Check that we can see an access a url in the first line of the email -> None "

        self.test_sending_observation()
        response = self.client.get(mail.outbox[-1].body, {}, follow=True)
        assert len(response.redirect_chain) == 1 # we get redirected
        assert response.status_code == 200 # we get a page



