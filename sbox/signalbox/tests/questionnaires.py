# coding: utf-8
import django
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase

from django.contrib.auth.models import User
from signalbox.models import Study, Membership, Reminder, ReminderInstance, Answer, Observation
from ask.models import Question, QuestionInAskPage, Instrument
from signalbox.utils import execute_the_todo_list, send_reminders_due_now
from signalbox.tests import helpers




class TestQuestionnaires(TestCase):
    """

    """

    fixtures = ['minimal.json', 'minimal_ask.json', 'serverconfig.json']


    def get_questionnaire_page(self):
        """Start a reply and get the first page of a questionnaire -> Str """
        membership = helpers.setup_membership()
        first = membership.observations().filter(created_by_script__asker__reference="demonstration_questionnaire")[0]
        url = first.link()
        page = self.client.get(url, follow=True)
        nexturl = page.request['PATH_INFO']

        return nexturl


    def test_submitting_questionnaire_bad_data(self):
        """By design, nothing is saved until the form validates

        Whether this is a good design or not is an open question, however when
        using the django form machinery, this is the default way, and it there
        would be a fair amount of work in making sure fields were saved
        individually after validating."""

        nexturl = self.get_questionnaire_page()
        assert [i.answer for i in Answer.objects.all()] == [] # nothing saved yet
        incorrect_data = {'demo_list': "999", 'demo_date': "2001-19-19", 'demo_integer':"notanumber"}
        data_to_post =  dict(helpers.QUESTIONNAIRE_POST_DATA.items() + incorrect_data.items())
        formsubmission = self.client.post(nexturl, data_to_post, follow=True)
        assert "9 is not one of the available choices." in formsubmission.content
        assert "This question needs an answer in whole numbers." in formsubmission.content
        assert "Enter a valid date" in formsubmission.content
        assert Answer.objects.all().count() == 0 # still nothing saved



    def test_submitting_multiple_choice_checkbox_field(self):
        pass


    def test_submitting_none_for_required_question(self):
        """Check to see if we can submit no answer when a question is required -> None"""

        pass




