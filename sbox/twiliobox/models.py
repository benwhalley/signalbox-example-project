from django.contrib.admin.models import User
from django.conf import settings
from django.db import models

client = settings.TWILIOCLIENT

class AnswerPhoneMessage(models.Model):
    sid = models.CharField(blank=True, max_length=100)
    added = models.DateTimeField(blank=True, auto_now_add=True)
    category = models.ForeignKey('AnswerPhoneMessageCategory', blank=True, null=True)
    notes = models.TextField(blank=True)
    participant = models.ForeignKey(User, blank=True, null=True, verbose_name="""Call is from this user:""")
    audio_uri = models.URLField(blank=True)
    
    def recording_uri(self):
        """If audio_uri is not set, grab it from Twilio and set it."""
        if not self.audio_uri:
            try:
                u = client.recordings.list(call_sid=self.sid)[0].uri
                self.audio_uri = u
                self.save()
            except:
                return None
        return self.audio_uri
    
    def __unicode__(self):
        return "%s: %s" % (self.added, self.sid,)
        


class AnswerPhoneMessageCategory(models.Model):
    name = models.CharField(blank=True, max_length=100)
    
    def __unicode__(self):
        return self.name