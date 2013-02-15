# coding: utf-8
import StringIO
import csv
from django.core.urlresolvers import reverse
from django.test import TestCase
from signalbox.models import Study
from signalbox.views.data import *
from reversion.models import Version
from signalbox.allocation import allocate
from signalbox.tests import helpers
from django.conf import settings



class TestDataHandling(TestCase):
    """Test that we can save and export data.

    Test that data is exported to CSV/Stata correctly. Some cases we should handle:

    - Simplest - single row per membership
    - Longitudinal - multiple responses per user to different obs
    - Complex longitudinal - mutliple responses to different obs from different scripts
    - Conflicting - multiple replies to a single observation

    """

    def get_questionnaire_page(self):
        """Start a reply and get the first page of a questionnaire -> Str """
        membership = helpers.setup_membership()
        obs = membership.observation_set.all()
        url = [i.link() for i in obs if i.link()][0]
        page = self.client.get(url, follow=True)
        nexturl = page.request['PATH_INFO']

        return nexturl

    # These tests commented out, because at present the logic relating to making
    # replies from Twilio is a bit complex and hard to test properly... we should
    # probably be mocking a Reply and CallSid and then testing using that.

    # def get_twiml_for_twilio(self):
    #     membership = helpers.setup_membership()
    #     testob = membership.observations().filter(created_by_script__script_type__id=3)[0]
    #     url = reverse('initialise_call', args=(testob.token,))
    #     twiml = self.client.post(url, {'CallSid': "testsid"}, follow=True)
    #     return twiml

    # def test_twiml_response(self):
    #     twiml = self.get_twiml_for_twilio()
    #     print twiml
    #     assert "<Response>" in twiml.content


    def test_adding_data(self):
        study = Study.objects.get(slug='test-study')
        user = helpers.make_user({'username': "TEST2", 'email': "TEST@TEST.COM", 'password': "TEST"})

        membership = helpers.make_membership(study, user)
        allocate(membership)
        membership.add_observations()

        questionnaire = self.get_questionnaire_page()
        datatopost = {k:v for k,v in helpers.QUESTIONNAIRE_POST_DATA.items()}
        datatopost.update({'page_id':0})
        x = self.client.post(questionnaire, datatopost, follow=True)
        answers = get_answers(Observation.objects.all())
        csvstring = build_csv_data_as_string(answers, study)
        questions = Question.objects.filter(id__in=answers.values('question__id'))
        generate_syntax('admin/ask/stata_syntax.html', questions)

        f = StringIO.StringIO(csvstring)
        dicts = list(csv.DictReader(f))

        headings = dicts[0].keys()


        expected_cols = ['is_reference_study', 'observation__id', 'membership__id']
        for i in expected_cols + helpers.QUESTIONNAIRE_POST_DATA.keys():
            assert i in headings

        rowtocheck = dicts[0]
        for k, v in helpers.QUESTIONNAIRE_POST_DATA.items():
            assert rowtocheck[k] == v

        # check this fucntion returns a file while we're at it
        stringtowrite = "rosa is lovely"
        saveddatafile = write_to_file(stringtowrite)
        assert type(saveddatafile) == file
        assert saveddatafile.read() == stringtowrite

        # and this too...
        z = build_zipfile(Observation.objects.all(), study, "tmp/testzip.zip")
        files = [i.filename for i in z.filelist]
        assert len(files) == 2
        assert 'data.csv' in files
