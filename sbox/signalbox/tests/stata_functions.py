import re
from datetime import timedelta, datetime
import django
from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ask.models import QuestionInAskPage
from ask.models import custom_widgets, fields
from ask.models import stata_functions as stata
from signalbox.models import Study, Membership, Reminder, ReminderInstance, Answer, Observation
from signalbox.allocation import allocate
from signalbox.views.data import *
from signalbox.tests import helpers
from ask.models import Question, QuestionInAskPage, Instrument
import floppyforms


class TestStataFunctions(TestCase):
    """Test that Stata functions return expected format."""

    fixtures = ['minimal.json', 'ask_test_fields.json', 'serverconfig.json']

    def get_widget(self, name):
        membership = helpers.setup_membership()
        first = membership.observations()[0]
        url = first.link()
        page = self.client.get(url, follow=True)
        c = page.context
        f = c['form']
        widget = f.fields[name]
        return widget


    # def test_label_variable(self):
    #     q = QuestionInAskPage.objects.get(question__variable_name="test_integer", page__id=1)
    #     w = self.get_widget('test_integer')
    #     # Test stata.label_variable
    #     v = w.label_variable(q.question)
    #     expected = u"label variable test_integer \"what is your favourite number\" \n" \
    #                 "note test_integer: WHAT IS YOUR FAVOURITE NUMBER"
    #     assert v == expected


    # def test_label_choices(self):
    #
    #     q = QuestionInAskPage.objects.get(question__variable_name="demo_pulldown", page__internal_name="first")
    #     w = self.get_widget('demo_pulldown')
    #     # Test stata.label_choices
    #     choices = w.label_choices(q.question)
    #     expected = u"label define test_pulldown 0 `\"No\"'  1 `\"Yes\"'  "
    #     assert choices == expected

    # def test_label_choices_checkboxes(self):
    #     q = QuestionInAskPage.objects.get(question__variable_name="test_checkboxes", page__id=1)
    #     w = self.get_widget('test_checkboxes')
    #     # Test stata.label_choices_checkboxes
    #     choices = w.label_choices(q.question)
    #     expected = u"label define test_checkboxes 0 `\"No\"'  1 `\"Yes\"'  \n\n" \
    #                 "    tostring test_checkboxes, replace\n" \
    #                 "    split test_checkboxes, p(\",\") destring gen(test_checkboxes__ticked_)\n" \
    #                 "    foreach v of varlist `r(varlist)' {\n" \
    #                 "        label variable `v' `\"test_checkboxes\"'\n" \
    #                 "    }\n    "
    #     assert choices == expected


    # def test_set_format_date(self):
    #     q = QuestionInAskPage.objects.get(question__variable_name="test_date", page__id=1)
    #     w = self.get_widget('test_date')
    #     # Test stata.set_format_date
    #     f = w.set_format(q.question)
    #     expected = u"\ntostring test_date, replace\n" \
    #                 "gen __tmpdate = date(test_date,\"YMD#\")\n" \
    #                 "drop test_date\n" \
    #                 "rename __tmpdate test_date\n" \
    #                 "format test_date %td\n    "
    #     assert f == expected


    # def test_set_format_time(self):
    #     qinpage = QuestionInAskPage.objects.get(question__variable_name="test_time", page__id=1)
    #     field = qinpage.question.field_class()
    #     # Test stata.set_format_time
    #     f = field.set_format(qinpage.question)
    #     expected = u"\n    tostring test_time, replace\n" \
    #                   "    split test_time, p(\",\") destring gen(test_time_split)\n" \
    #                   "    label variable test_time_split1 \"what is the time as a string\"\n" \
    #                   "    label variable test_time_split2 \"what is the time as seconds since 00:00\"\n" \
    #                   "    destring test_time_split2, replace\n    "
    #     assert f == expected


    # def test_set_format_datetime(self):
    #     qinpage = QuestionInAskPage.objects.get(question__variable_name="test_datetime", page__id=1)
    #     field = qinpage.question.field_class()
    #     # Test stata.set_format_datetime
    #     f = field.set_format(qinpage.question)
    #     expected = u"\ngen double __test_datetime = clock(test_datetime,\"YMD hms#\")\n" \
    #                   "drop test_datetime\n" \
    #                   "rename __test_datetime test_datetime\n" \
    #                   "format test_datetime %tc\n    "
    #     assert f == expected




