# import re
# from datetime import timedelta, datetime
# import django
# from django.core import mail
# from django.conf import settings
# from django.test import TestCase
# from django.core.urlresolvers import reverse
# from django.contrib.auth.models import User
# from ask.models import custom_widgets, fields
# from ask.models import stata_functions as stata
# from signalbox.models import Study, Membership, Reminder, ReminderInstance, Answer, Observation
# from signalbox.allocation import allocate
# from signalbox.views.data import *
# from signalbox.tests import helpers
# from ask.models import Question, QuestionInAskPage, Instrument
# import floppyforms


# class TestFields(TestCase):
#     """Test custom SignalboxField widgets"""

#     def get_widget(self, name):
#         membership = helpers.setup_membership()
#         first = membership.observations()[0]
#         url = first.link()
#         page = self.client.get(url, follow=True)
#         c = page.context
#         f = c['form']
#         widget = f.fields[name]
#         return widget


#     def test_date_widget(self):
#         w = self.get_widget('test_date')
#         assert w.widget.attrs.get('class') == 'datepicker'
#         # N.B. set_format tested in TestStataFunctions


#     def test_datetime_field(self):
#         w = self.get_widget('test_datetime')
#         assert w.widget.attrs.get('class') == 'datetimepicker'
#         # N.B. set_format tested in TestStataFunctions


#     def test_checkbox_widget_export_processor(self):
#         field = self.get_widget('test_checkboxes')
#         # Test valid values
#         val = field.export_processor("[]")
#         assert val == ""
#         val = field.export_processor("[u'0']")
#         assert val == u'0'
#         val = field.export_processor("[u'0', u'1']")
#         assert val == u'0,1'
#         val = field.export_processor("[u'0', u'1', u'2', u'3']")
#         assert val == u'0,1,2,3'
#         # Test export_processor exception
#         val = field.export_processor("0,1,2,3")
#         assert val == '0,1,2,3'


#     def test_checkbox_widget_redisplay_processor(self):
#         q = QuestionInAskPage.objects.get(question__variable_name="test_checkboxes", page__id=1)
#         field = q.question.field_class()
#         val = field.redisplay_processor("[u'0', u'1', u'2', u'3']")
#         assert val == [u'0', u'1', u'2', u'3']


#     def test_required_checkbox(self):
#         w = self.get_widget('test_required_checkbox')
#         assert w.required == True


#     def test_pulldown_field(self):
#         w = self.get_widget('test_pulldown')
#         assert w.prepend_null_choice == True
#         assert w.choices == [['', '---'], (0, u'No'), (1, u'Yes')]


#     def test_pulldown_field_na(self):
#         w = self.get_widget('test_pulldown_na')
#         assert w.choices == [['', '---'], ['NA', 'NA'], (0, u'No'), (1, u'Yes')]
#         q = QuestionInAskPage.objects.get(question__variable_name="test_pulldown_na", page__id=1)
#         assert q.allow_not_applicable == True


#     def test_time_field(self):
#         w = self.get_widget('test_time')
#         assert w.widget.attrs.get('class') == 'timepicker'
#         # Check export_processor (appends offset from 00:00:00 in seconds)
#         assert w.export_processor("12") == "12,43200.0"
#         assert w.export_processor("12:34") == "12:34,45240.0"
#         assert w.export_processor("12:34:56") == "12:34:56,45296.0"
#         # N.B. set_format tested in TestStataFunctions



