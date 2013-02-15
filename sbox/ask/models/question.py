"""Questions and related models to place them in questionnaire pages and instruments."""
from storages.backends.s3boto import S3BotoStorage
from django.template.loader import get_template
import json
from django.db import models
from django.template import Context, Template
from jsonfield import JSONField
from django.core.exceptions import ValidationError
from ask.models import fields
import ask.validators as valid
from fields import FIELD_NAMES
from utilities.linkedinline import admin_edit_url


truncatelabel = lambda x, y: (x[:int(y) / 2] + '...' + x[- int(y) / 2:]) if len(x) > y else x


def get_custom_attr(name, default, module_list):
    """Like getattr, but searches a list of modules retuning the first one found, or implicit None."""

    name = name or default
    for i in module_list:
        try:
            return getattr(i, name)
        except AttributeError:
            pass


ASSET_TEMPLATE_CHOICES = (
    ('image.html', 'image'),
    ('movie.html', 'movie'),
    ('audio.html', 'audio'),
)

class QuestionAsset(models.Model):
    question = models.ForeignKey('ask.Question')
    slug = models.SlugField(help_text="""A name to refer to this asset
        with in the question_text field. To display an image or media
        player within the question, include the text {{SLUG}} in the
        question_text field of the question.""")
    asset = models.FileField(upload_to="questionassets", blank=True, null=True,
        help_text="""Can be an image (.jpg, .png, or .gif), audio file (.m4a, .mp4, or .mp3) or movie (.mp4 only) for display
        as part of the question text.""")
    template = models.CharField(max_length=255,
        choices=ASSET_TEMPLATE_CHOICES, )

    def render(self):
        templ = get_template("questionasset/" + self.template)
        context = {'object': self }
        return templ.render(Context(context))


    def __unicode__(self):
        return self.render()

    class Meta:
        app_label = 'ask'


class QuestionManager(models.Manager):
    def get_by_natural_key(self, variable_name):
        return self.get(variable_name=variable_name)


class Question(models.Model):
    """Question objects; e.g. mutliple choice, text, etc."""

    objects = QuestionManager()

    def natural_key(self):
        return (self.variable_name, )
    natural_key.dependencies = ['ask.choiceset']

    last_modified = models.DateTimeField(auto_now=True)

    text = models.TextField(blank=True, null=True,
        help_text="""For ShowScore questions, include {{score}} within the text here to
        indicate where the computed score should be placed.""")

    variable_name = models.SlugField(default="", max_length=32, unique=True,
        validators=[valid.first_char_is_alpha, valid.illegal_characters,
            valid.is_lower], help_text="""Variable names can use characters a-Z,
            0-9 and underscore (_), and must be unique within the system.""")

    variable_label = models.CharField(max_length=80, blank=True, null=True,
        help_text="""A label for the variable created in exported datasets.
        This is what you will see in SPSS or Stata when analysing the data, so
        it should be as descriptive as possible, but short to fit within plots
        and other output as needed.""")

    choiceset = models.ForeignKey('ChoiceSet', null=True, blank=True)

    scoresheet = models.ForeignKey('signalbox.ScoreSheet', null=True, blank=True,
        related_name="scoresheettoshow", help_text="""For ShowScore questions only - the summary
        score to be calculated and shown""", )

    help_text = models.TextField(blank=True, null=True)

    always_required = models.BooleanField(default=False)

    # we use S3 because otherwise there's a real lag on the call from twilio
    audio = models.FileField(storage=S3BotoStorage(), upload_to="audio", blank=True, null=True,
        help_text="""Audio file for use in automated telephone calls.""")

    def display_text(self, reply=None, page=None, request=None):

        templ = Template(self.text)
        context = {'reply': reply, 'user': reply.observation.dyad.user, 'page': page}
        if self.scoresheet and reply:
            context['score'] = "{:g}".format(self.scoresheet.compute(reply.answer_set.all())['score'])
        for i in self.questionasset_set.all():
            context[i.slug] = unicode(i)

        return templ.render(Context(context))

    q_type = models.CharField(choices=[(i, i.upper()) for i in FIELD_NAMES],
        blank=False, max_length=100)

    def field_class(self):
        """Return the relevant form field class. """
        return getattr(fields, fields.class_name(self.q_type))

    def label_variable(self):
        return self.field_class().label_variable(self)

    def set_format(self):
        return self.field_class().set_format(self)

    def label_choices(self):
        return self.field_class().label_choices(self)

    widget_kwargs = JSONField(blank=True, help_text="""A JSON representation of a python dictionary of
        attributes which, when deserialised, is passed to the form widget when the questionnaire is
        rendered. See django-floppyforms docs for options.""")

    field_kwargs = JSONField(blank=True, help_text="""A JSON representation of a python dictionary of
        attributes which, when deserialised, is passed to the field when the questionnaire is
        rendered. See django-floppyforms docs for options.""")

    def voice_function(self):
        """Returns the function to render instructions for external telephony API."""

        return self.field_class().voice_function

    def choices_as_json(self):
        """-> str"""
        if self.choiceset:
            return self.choiceset.values_as_json()
        return None

    def tts_function_string(self):
        """Returns a string to call the OS X `say` function to render audio.

        Replaces line breaks with spaces to avoid problems with pasting into the
        command line window.

        """

        return """say "%s" -o %s.aiff""" % (" ".join(self.text.splitlines()), self.variable_name)

    def choices(self):
        """Returns a list of typles (name, val) in format for Django ChoiceField or None.
        """
        cset = self.choiceset
        if cset:
            choices = cset.get_choices()
            choicelist = [(i.score, i.label) for i in choices]
            return choicelist
        return None

    def response_possible(self):
        return self.field_class().response_possible

    def previous_answer(self, reply):
        """Check for previous answer during this reply and return the previous answer value.
        """
        if reply and self.response_possible():
            try:
                return reply.answer_set.filter(question=self)[0].answer
            except IndexError:
                return ""

    def used_in_askers(self):
        return QuestionInAskPage.objects.filter(question=self)

    def used_in_instruments(self):
        qininstruments = QuestionInInstrument.objects.filter(question=self)
        return qininstruments

    def __unicode__(self):
        return truncatelabel(self.variable_name, 26)

    def clean_fields(self, *args, **kwargs):
        """Do some extra validation related to form fields used for the question."""

        super(Question, self).clean_fields(*args, **kwargs)

        if not self.q_type:
            return False

        fieldclass = self.field_class()

        errors = {}

        if (fieldclass.response_possible and not self.variable_label):
            errors['variable_label'] = ["You need a label for this sort of question."]

        if (not fieldclass.has_choices) and self.choiceset:
            errors['choiceset'] = ["You don't need a choiceset for this type of question."]

        if fieldclass.has_choices and (not self.choiceset):
            errors['choiceset'] = ["You need a choiceset for this type of question."]

        if self.always_required and (not fieldclass.response_possible):
            errors['always_required'] = ["This type of question (%s) doesn't allow a response." % (self.q_type,)]

        if errors:
            raise ValidationError(errors)

    def admin_edit_url(self):
        return admin_edit_url(self)

    class Meta:
        app_label = 'ask'
        ordering = ['variable_name']


class ChoiceManager(models.Manager):
    def get_by_natural_key(self, choiceset, label, score):
        return self.get(choiceset=choiceset, label=label, score=score)


class Choice(models.Model):
    """A possible option to choose in response to a Question."""

    objects = ChoiceManager()

    def natural_key(self):
        return (self.choiceset, self.label, self.score)
    natural_key.dependencies = ['ask.choiceset']

    choiceset = models.ForeignKey('ChoiceSet', blank=True, null=True)

    is_default_value = models.BooleanField(default=False, db_index=True,
        help_text="""Indicates whether the value will be checked by default.""")

    order = models.IntegerField(db_index=True, help_text="""Order in which the choices are displayed.""")

    label = models.CharField(u"Label", max_length=200, blank=True, null=True)

    score = models.IntegerField(help_text="This is the value saved in the DB")

    def __unicode__(self):
        return u'%s [%s]' % (self.label, self.score)

    class Meta:
        app_label = 'ask'
        ordering = ['order']
        unique_together = (('choiceset', 'score'),)


class ChoiceSetManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class ChoiceSet(models.Model):
    """The set of options attached to Questions."""

    objects = ChoiceSetManager()

    def natural_key(self):
        return (self.name, )

    name = models.SlugField(max_length=64, unique=True)

    prompt_wording = models.TextField(help_text="""Only used for telephone surveys (i.e. for
        vxml, not for html surveys). This text is what the user would hear (via computer
        text to speech) to describe the options after the question text has been. If left
        blank, system will try and render a sensible audio version using labels and scores
        of choices attached.""", blank=True, null=True)

    def spoken(self):
        """Return string to create a spoken version of the options, for Twilio."""

        return self.prompt_wording or "; ".join(["Press %s for %s" % (i.score, i.label)
            for i in self.get_choices()])

    def default_value(self):
        """Return the default value (the score itself) for this ChoiceSet"""
        # TODO... should really be checking that there aren't 2 default values
        # rather than just picking the first.
        choices = self.choice_set.filter(is_default_value=True)
        if choices:
            return getattr(choices[0], 'score', None)

    def values_as_json(self):
        choices = dict([(unicode(i.score), unicode(i.label)) for i in self.get_choices()])
        return json.dumps(choices, indent=4, sort_keys=True)

    def get_choices(self):
        cset = Choice.objects.filter(choiceset=self)
        return cset

    def choices_as_string(self):
        return "; ".join(["%s [%s]" % (i.label, i.score) for i in self.get_choices()])

    def __unicode__(self):
        return u'%s' % (self.name, )

    class Meta:
        app_label = 'ask'
        ordering = ["name"]


class QuestionInAskPageManager(models.Manager):
    def get_by_natural_key(self, question, page):
        return self.get(question=question, page=page)


class QuestionInAskPage(models.Model):
    """Link model identifying which questions appear in which AskPages"""

    objects = QuestionInAskPageManager()

    def natural_key(self):
        return (self.question, self.page)
    natural_key.dependencies = ['ask.question']

    question = models.ForeignKey('ask.Question', verbose_name="""Question""")

    order = models.FloatField(default=0, verbose_name="Page order", help_text="""The order in which
        items will apear in the page (the sequence includes instruments, below).""")

    page = models.ForeignKey('ask.AskPage')

    allow_not_applicable = models.BooleanField(default=False)

    required = models.BooleanField(default=False)

    showif = models.ForeignKey('ask.ShowIf', null=True, blank=True,
        help_text="""Conditionally hide or show this Question based on these rules""",
        verbose_name="""Show the question if""")

    def showme(self, reply):
        """Return a boolean indicating whether the question should be hidden."""
        if self.showif:
            return self.showif.evaluate(reply)
        return True

    def admin_edit_url(self):
        return admin_edit_url(self, indirect_pk_field='question')

    def __unicode__(self):
        return str(self.question)

    class Meta():
        app_label = 'ask'
        ordering = ('order',)
        verbose_name_plural = "Questions in the page"



class QuestionInInstrumentManager(models.Manager):
    def get_by_natural_key(self, question, page):
        return self.get(question=question, instrument=instrument)


class QuestionInInstrument(models.Model):
    """Link model identifying which Questions appear in particular Instruments"""

    objects = QuestionInInstrumentManager()

    def natural_key(self):
        return (self.question, self.instrument)
    natural_key.dependencies = ['ask.question']

    question = models.ForeignKey(Question)
    order = models.FloatField(default=0)
    instrument = models.ForeignKey('ask.Instrument')
    required = models.BooleanField(default=False)
    showif = models.ForeignKey('ask.ShowIf', null=True, blank=True,
        help_text="""Conditionally hide or show this Question based on these rules""",
        verbose_name="""Show the question if""")

    def showme(self, reply):
        """Return a boolean indicating whether the question should be hidden."""
        if not self.showif:
            return True
        return self.showif.evaluate(reply)

    class Meta():
        ordering = ('order',)
        app_label = 'ask'

    def __unicode__(self):
        return str(self.question)

    def admin_edit_url(self):
        return admin_edit_url(self, indirect_pk_field='question')


class ShowIf(models.Model):
    """Condition to determine whether user sees an object."""

    class Meta:
        app_label = 'ask'

    previous_question = models.ForeignKey(Question, blank=True, null=True,
        related_name="previous_question",
        help_text='''For previous values, enter the name of the question which
        will already have been answered in this survey (technically, within this Reply)''')

    summary_score = models.ForeignKey('signalbox.ScoreSheet', blank=True, null=True,
        help_text="""A summary score to be calculated based on answer already entered in the current
        Reply.""")

    values = models.CharField(max_length=255, blank=True, null=True,
        help_text='''CASE INSENSITIVE values to match, comma separated. The question is shown if
        any value matches''')

    less_than = models.IntegerField(blank=True, null=True, help_text="""Previous question response
        or summary score must be less than this value.""")

    more_than = models.IntegerField(blank=True, null=True, help_text="""Previous question response
        or summary score must be more than this value.""")

    def evaluate(self, reply):
        """Check whether a suitable previous answer exists and return Boolean."""

        if self.summary_score:
            vals_to_be_tested = set([self.summary_score.compute(reply.answer_set.all())['score']])

        if self.previous_question:
            vals_to_be_tested = set([a.answer for a in
                reply.answer_set.filter(question=self.previous_question)])

        if self.values:
            valid_value_set = set(self.valid_values())
            return bool(not valid_value_set.isdisjoint(vals_to_be_tested))

        if self.more_than or self.less_than:
            return False not in [self.lowest() < int(i) < self.highest() for i in vals_to_be_tested]

    def lowest(self):
        """Return a number that the user's previous response should be higher than"""
        return self.more_than or float("-inf")

    def highest(self):
        """Return a number that the user's previous response should be lower than"""
        return self.less_than or float("inf")

    def valid_values(self):
        """Return a Set of valid lowercased values to match against."""
        vals = self.values.split(",")
        return set([v.strip().lower() for v in vals])

    def clean(self):
        super(ShowIf, self).clean()
        if self.previous_question and self.summary_score:
            raise ValidationError("""You can hide/show this item based on a previous question value
            or a summary score, but not both.""")

        if self.values and (self.less_than or self.more_than):
            raise ValidationError("""You can either specify a range using the more_than and
            less_than fields, or exact values, but not both.""")

    def condition_to_pass(self):
        if self.values:
            return str("is in [%s]" % self.values, )
        if self.summary_score:
            return "is between %s and %s" % (self.lowest(), self.highest())

    def __unicode__(self):
        if self.previous_question:
            test = truncatelabel(self.previous_question.variable_name, 26)
        else:
            test = self.summary_score
        return "%s %s" % (test, self.condition_to_pass())
