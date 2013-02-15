from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django_extensions.db.fields import UUIDField
from signalbox.models.scoresheet import ScoreSheet
from utilities.linkedinline import admin_edit_url
from answer import Answer

ENTRY_METHOD_LOOKUP = {
    'double_entry': "Double entry by an administrator",
    'preview': "Preview",
    'participant': "Participant via the web interface",
    'twilio': "Twilio",
    'ad_hoc': "Ad-hoc data entry via admin interface"
}


class ReplyManager(models.Manager):

    def authorised(self, user):
        """Provide per-user access for Replies."""

        qs = super(ReplyManager, self).select_related()

        if user.is_superuser:
            return qs

        qs = qs.exclude(
            observation__created_by_script__allow_display_of_results=False)

        if not user.groups.filter(name="Clinicians").count() > 0:
            qs = qs.exclude(
                observation__created_by_script__is_clinical_data=True)

        return qs


class Reply(models.Model):

    '''Organises a set of Answers and tracks Asker completion.'''

    objects = ReplyManager()

    is_canonical_reply = models.BooleanField(default=False,)

    # todo XXX can this be deleted now... always track it via a script
    is_clinical_data = models.BooleanField(default=False,
        help_text="""Used to identify clinical records added during the study.""")

    observation = models.ForeignKey(
        'signalbox.Observation', blank=True, null=True)

    user = models.ForeignKey(User, blank=True, null=True,
        related_name="reply_user",
        help_text="""IMPORTANT: this is not necessarily the user providing the data (i.e. a
        patient) but could be an assessor or admin person doing double entry from paper. It
        could also be null, where data is added by an AnonymousUser (e.g. Twilio or external
        API which doesn't authenticate.)""")

    asker = models.ForeignKey('ask.Asker', null=True, blank=True,)

    current_page = models.ForeignKey('ask.AskPage', null=True, blank=True,
         help_text="""Keeps track of replies to Questionnaires via the web or Phone""")

    redirect_to = models.CharField(max_length=1000, null=True, blank=True,)

    last_submit = models.DateTimeField(null=True, blank=True, auto_now=True)

    started = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    originally_collected_on = models.DateField(null=True, blank=True,
       help_text="""Set this if the date that data were entered into the system is not the date
        that the participant originally provided the responses (e.g. when retyping paper data)""")

    complete = models.BooleanField(default=False, db_index=True)

    token = UUIDField()

    external_id = models.CharField(null=True, blank=True, max_length=100,
                                   help_text="""Reference for external API, e.g. Twilio""")

    twilio_question_index = models.IntegerField(
        null=True, blank=True, default=0)

    entry_method = models.CharField(
        choices=[(k, v) for k, v in ENTRY_METHOD_LOOKUP.items()],
        max_length=100, null=True, blank=True,)

    notes = models.TextField(null=True, blank=True,)

    def relevant_scoresheets(self):
        if self.observation and self.observation.dyad:
            return self.observation.dyad.study.scoresheets.all()
        else:
            return ScoreSheet.objects.all()

    def answers_ordered_as_per_original_asker(self):
        """Used in place of self.answer_set, mimics ordering of Asker used."""
        if not self.asker:
            return self.answer_set.all()

        ordered_questions = [i.question for i in self.asker.questions()]
        unordered_anwers = self.answer_set.all()
        answers_dict = {i.variable_name(): i for i in unordered_anwers}

        # insert 'faked' answers to enable user to see questions which were
        # not attempted in this reply.
        ordered_answers = [answers_dict.get(
            i.variable_name,
            Answer(question=i)) for i in ordered_questions]

        # add any additional answers - should just be page_id really
        remaining_variables = set(unordered_anwers) - set(ordered_answers)
        map(
            lambda x: ordered_answers.append(
                answers_dict.get(x.variable_name(), x)),
            remaining_variables)

        return ordered_answers

    def computed_scores(self):
        scoresheets = self.relevant_scoresheets()
        answers = self.answer_set.all()
        if self.observation:
            return [i.compute(answers) for i in scoresheets]

    def is_preview(self):
        if self.entry_method == "preview":
            return True
        return False

    def is_preferred_reply(self):
        """Returns whether this was the Reply to use for an Observation."""

        replies = self.observation.reply_set.all()
        if replies.count() < 2:
            return True
        else:
            canon = replies.filter(is_canonical_reply=True)
            return bool(self in canon)

    def save(self, *args, **kwargs):
        """Set to page 1 of the asker on the first run."""
        if not self.current_page and self.asker:
            self.current_page = self.asker.first_page()
        super(Reply, self).save(*args, **kwargs)

    def redirect_url(self):
        if self.redirect_to:
            return self.redirect_to

        if self.created_by_script:
            return self.created_by_script.redirect_url
        return reverse('user_homepage')

    def get_current_page(self):
        return self.current_page or self.asker.first_page()

    def number_non_empty_answers(self):
        return len([i for i in self.answer_set.all() if i.answer])

    def finish(self, request):
        """Questionnaire is complete, so finish up."""
        if not self.observation:
            # e.g. if we are previewing
            messages.add_message(request, messages.SUCCESS, "End of preview")

            return HttpResponseRedirect(
                reverse('admin:ask_asker_change', args=(self.asker.id, )))

        self.complete = True
        self.observation.status = 1
        self.save()
        self.observation.save()

        try:
            mess = self.observation.created_by_script.success_message
        except AttributeError:
            mess = "Saved questionnaire data."
        messages.add_message(request, messages.SUCCESS, mess)

        if self.entry_method == "double_entry":
            messages.add_message(request,
                messages.SUCCESS,
                "%s answers saved" % self.number_non_empty_answers(), )

        return HttpResponseRedirect(self.redirect_url())

    def move_to_next_page(self, request):
        next = self.current_page.next_page()
        if next:
            self.current_page = next
            self.save()
            return HttpResponseRedirect(
                reverse('show_page', kwargs={'reply_token': self.token}))
        else:
            return self.finish(request)

    def get_absolute_url(self):
        return reverse('preview_reply', args=(self.id, ))

    class Meta():
        app_label = 'signalbox'
        permissions = (
            ("can_double_enter", "Can add Data for another person"),
            ("can_resolve_duplicate_replies", "Can resolve duplicate replies"))
        ordering = ['-started']

    def admin_edit_url(self):
        return admin_edit_url(self)

    def __unicode__(self):
        return "Reply: {0}...".format(self.token[:8])
