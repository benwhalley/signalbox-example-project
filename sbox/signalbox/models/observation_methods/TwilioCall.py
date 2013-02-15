import itertools
from signalbox.utils import current_site_url
from django.core.urlresolvers import reverse
from django.conf import settings
from signalbox.phone_field import international_string

client = settings.TWILIOCLIENT


def do(self):
    """Place the Call and update Observation."""

    self.status = -1  # in progress
    self.save()

    to_number = international_string(self.user.get_profile().get_voice_number())
    from_number = self.dyad.study.get_outbound_telephone_number()

    try:
        call = client.calls.create(to=to_number,
                       from_=from_number,
                       url=self.link(),
                       method="POST")
        self.touch()
        self.increment_attempts()
        self.add_data(key="external_id", value=call.sid)
        self.save()
        return (1, "Call %s is %s. %s" % (call.sid, call.status, call.uri))

    except Exception as e:
        self.touch()
        self.increment_attempts()
        self.add_data(key="failure", value=str(e))
        self.save()
        return (-1, str(e))


def link(self):
    """Return the uri of the first Twiml page for Twilio to consume."""
    twiml = current_site_url() + reverse('initialise_call', args=(self.token,))
    return twiml


def questions(self):
    """Return a list of questions in the attached Asker."""

    pages = self.asker.pages()
    questions_by_page = [p.questions_to_show() for p in pages]
    questions = itertools.chain(*questions_by_page)
    return list(questions)


def reschedule(self, delay=None, next=None):
    """Handle logic relating to rescheduling calls.

    XXX todo THIS IS STILL TODO
    """

    raise Exception("Not implemented yet")


def update(self, success_status):
    """Handle updates relating to do()ing calls. See also reschedule()"""

    if success_status > -1:
        self.increment_attempts()
        self.touch()

    self.status = success_status  # call set in progress
    self.save()
