import urllib
import urlparse
from urllib import urlencode
from more_itertools import first
import json
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from twilio import twiml
from reversion import revision
from signalbox.utils import current_site_url
from django.conf import settings
from signalbox.models import Observation, Reply, Answer, TextMessageCallback
from twiliobox.models import AnswerPhoneMessage

client = settings.TWILIOCLIENT


@csrf_exempt
def initialise_call(request, observation_token):
    """Accept inbound POST from Twilio, make a new Reply and redirect to view showing Twiml."""

    observation = get_object_or_404(Observation, token=observation_token)
    observation.make_reply(request, entry_method="twilio", external_id=request.POST.get('CallSid', None))
    url = current_site_url() + reverse('play_twiml_firstq') + "?" + urllib.urlencode({'CallSid': request.POST.get('CallSid', None)})
    return HttpResponseRedirect(url)


def question_is_last(questions, number):
    return len(questions) - 1 == number


def get_question(questions, index):
    try:
        return questions[index]
    except IndexError:
        return None


@revision.create_on_success
def save_answer(reply, question, querydict):
    """Takes a Reply, a question and the POST dict and returns a (saved) answer."""

    user_answer = first(querydict.getlist('Digits'), "")
    extra_json = json.dumps(querydict, sort_keys=True, indent=4)
    answer, created = Answer.objects.get_or_create(reply=reply, question=question)
    answer.answer = user_answer
    answer.meta = extra_json,
    answer.choices = question.choices_as_json()
    answer.save()

    return answer


@csrf_exempt
def play_twiml(request, first):
    """Controller to present Twiml for each question and save responses."""

    external_id = request.POST.get('CallSid', None) or request.GET.get('CallSid', None)
    if not external_id:
        raise Http404
    reply = Reply.objects.filter(external_id=external_id)[0]

    all_questions = list(reply.observation.created_by_script.asker.questions())
    questioninaskpage = get_question(all_questions, reply.twilio_question_index)
    prev_question = get_question(all_questions, reply.twilio_question_index - 1)
    is_last = question_is_last(all_questions, reply.twilio_question_index)
    twimlresponse = twiml.Response()
    url = current_site_url() + reverse('play_twiml') + "?" + urlencode({'CallSid': external_id})

    if request.POST and prev_question:
        answer = save_answer(reply, prev_question.question, request.POST)

        # if the user responds with a * then repeat the question again by redirecting
        # to the same url without incrementing the question number
        if answer.answer == "*":
            return HttpResponseRedirect(url)

    field = questioninaskpage.question.field_class()(questioninaskpage=questioninaskpage, reply=reply, request=request)

    if is_last:
        twimlresponse = field.voice_function(twimlresponse, questioninaskpage, url=url, reply=reply)
        reply.observation.update(1)  # mark the reply as complete
        reply.finish(request)

    else:
        twimlresponse = field.voice_function(twimlresponse, questioninaskpage, url=url, reply=reply)
        reply.twilio_question_index += 1
        reply.save()

    return HttpResponse(str(twimlresponse), content_type="text/xml")


TWILIO_SMS_FIELDS = "sid Date_Created Date_Updated Date_Sent Account_Sid From_ To Body \
Status Direction Price Api_Version Uri".lower().split(" ")

TWILIO_CALL_FIELDS = "Sid Parent_Call_Sid Date_Created Date_Updated Account_Sid To From \
Phone_Number_Sid Status Start_Time End_Time Duration Price Direction Answered_By \
Forwarded_From Caller_Name Uri".lower().split(" ")

TWILIO_FIELDS = set(TWILIO_CALL_FIELDS).union(TWILIO_SMS_FIELDS)


@permission_required('signalbox.reply.view')
def twilio_object_info(request, external_id, ob_type='calls'):
    """View presenting information gathered from the Twilio API on call or SMS objects."""

    m = eval('client.%s.get' % ob_type, )
    thisob = m(external_id)
    thisobdict = dict([(i, getattr(thisob, i, None)) for i in TWILIO_FIELDS])
    return render_to_response('twilio_detail.html',
        {'object': thisobdict},
        context_instance=RequestContext(request))


def get_from_post_or_get(request, key):
    return request.POST.get(key, None) or request.GET.get(key, None)


@csrf_exempt
def sms_callback(request):
    """Accept SMS callbacks from Twilio.
    """

    sid = get_from_post_or_get(request, 'SmsSid')

    callbackrecord, created = TextMessageCallback.objects.get_or_create(sid=sid, post=json.dumps(request.POST))
    callbackrecord.save()
    return HttpResponse(str(callbackrecord))


@csrf_exempt
def answerphone(request):
    """Twiml application view which services incoming calls from Twilio.


    We test for an sid and save a new record if one exists, but display the Twiml anyway for
    testing purposes."""

    sid = request.POST.get('CallSid', None) or request.GET.get('CallSid', None)
    if sid:
        apm, _ = AnswerPhoneMessage.objects.get_or_create(sid=sid)
        apm.save()

    twimlresponse = twiml.Response()
    twimlresponse.say(settings.ANSWER_PHONE_MESSAGE)

    if getattr(settings, 'ENABLE_ANSWER_PHONE', False):
        twimlresponse.record(max_length=60 * 5, action=reverse('answerphone_thanks'))
    else:
        twimlresponse.hangup()

    return HttpResponse(str(twimlresponse), content_type="text/xml")


@csrf_exempt
def answerphone_thanks(request):
    """Create Twiml to play a final thankyou message for the answerphone."""

    twimlresponse = twiml.Response()
    twimlresponse.say(settings.ANSWER_PHONE_MESSAGE_THANKS)
    twimlresponse.hangup()
    return HttpResponse(str(twimlresponse), content_type="text/xml")
