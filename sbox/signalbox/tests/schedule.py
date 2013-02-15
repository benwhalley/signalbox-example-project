import re
from datetime import timedelta, datetime
import django
from django.core import mail
from django.conf import settings
from django.test import TestCase
import itertools as it
from signalbox.models import Script, ScriptType
from dateutil.relativedelta import *

class TestSchedule(TestCase):
    """Test that we can access the DB and some key parameters are set."""


    def test_natural_date_specification(self):
        script = Script.objects.get(reference='test-email')
        times = script.datetimes()
        assert len(times) == 3

        # first is (just) before present moment (i.e., syntax is 'now')
        assert times[0] < datetime.now()

        # others are later than now
        [self.assertTrue(i > datetime.now()) for i in times[1:]]

        # each is later than the last
        [self.assertTrue(j < k) for j, k in it.combinations(times, 2)]

        # all gaps divisble by 10
        [self.assertTrue(abs(relativedelta(j,k).minutes) in [10, 20])
                for j, k in it.combinations(times, 2)]




    def test_calculate_start_datetime(self):

        script = Script.objects.get(reference='test-email-survey')
        script.delay_in_whole_days_only = False
        script.save()
        date = datetime(2012, 07, 01, 23, 59, 0)

        # Test calculate_start_datetime
        start = script.calculate_start_datetime(date)
        assert str(start) == "2012-07-01 23:58:00"

        # Test delay_by_minutes
        script.delay_by_minutes = 1
        start = script.calculate_start_datetime(date)
        assert str(start) == "2012-07-02 00:00:00"

        # Test delay_by_hours
        script.delay_by_hours = 1
        start = script.calculate_start_datetime(date)
        assert str(start) == "2012-07-02 01:00:00"

        # Test delay_by_days
        script.delay_by_days = 1
        start = script.calculate_start_datetime(date)
        assert str(start) == "2012-07-03 01:00:00"

        # Test delay_by_weeks
        script.delay_by_weeks = 1
        start = script.calculate_start_datetime(date)
        assert str(start) == "2012-07-10 01:00:00"

        # Test delay_in_whole_days_only (hh:mm:ss set to zero)
        script.delay_in_whole_days_only = True
        start = script.calculate_start_datetime(date)
        assert str(start) == "2012-07-10 00:00:00"


    def test_delay(self):

        script = Script.objects.get(reference='test-email-survey')

        script.delay_by_minutes = 9
        d = script.delay()
        assert str(d) == "0:09:00"

        script.delay_by_hours = 8
        d = script.delay()
        assert str(d) == "8:09:00"

        script.delay_by_days = 7
        d = script.delay()
        assert str(d) == "7 days, 8:09:00"

        script.delay_by_weeks = 6
        d = script.delay()
        assert str(d) == "49 days, 8:09:00"

        script.delay_by_weeks = 52
        d = script.delay()
        assert str(d) == "371 days, 8:09:00"


    # def test_datetimes(self):
    #     script = Script.objects.get(reference='test-email-survey')

    #     # Test with valid minutes value
    #     date = datetime(2012, 07, 01, 0, 0, 0)
    #     script.repeat_byminutes = "0"
    #     script.repeat_bydays = "MO"
    #     dt = script.datetimes(start_date=date)
    #     assert len(list(dt)) == script.max_number_observations
