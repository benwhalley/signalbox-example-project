import json
import re
from django.core import serializers
from functools import partial
import itertools
from django.db import models
from django.core.urlresolvers import reverse
from utilities.linkedinline import admin_edit_url
from page import AskPage
from ask.models import Choice, Instrument


def baseround(x, base=5):
    return int(base * round(float(x) / base))


class AskerManager(models.Manager):
    def get_by_natural_key(self, reference):
        return self.get(reference=reference)


class Asker(models.Model):

    objects = AskerManager()

    def natural_key(self):
        return (self.reference, )

    reference = models.SlugField(max_length=128, help_text="""Not displayed to the
        user - for internal reference only""", unique=True,
        verbose_name="""Asker reference code""")

    page_title = models.CharField(max_length=128, default="", null=True,
        blank=True, help_text="""Displayed to the user at the top of *every*
        page; can be left blank for no title (use inividual page titles instead?)""")

    show_progress = models.BooleanField(default=True, help_text="""Show a
        progress field in the header of each page.""")

    hide_menu = models.BooleanField(default=True)

    def used_in_study_conditions(self):
        """Return a queryset of the StudyConditions in which this Asker appears."""
        from signalbox.models import StudyCondition, Script
        scripts = Script.objects.filter(asker=self)
        conds = set(StudyCondition.objects.filter(scripts__in=scripts))
        return conds

    def approximate_time_to_complete(self):
        """Returns the approximate number of minutes the asker will take to complete.

        Rounded to the nearest 5 minutes (with a minumum of 5 minutes)."""

        n_questions = len(self.questions())
        mins = (n_questions * .5) * .9
        return max([5, baseround(mins, 5)])

    def questions(self):
        questionsbypage = [i.get_questions() for i in self.pages()]

        for i, pagelist in enumerate(questionsbypage):
            for q in pagelist:
                q.on_page = i

        questions = list(itertools.chain(*questionsbypage))
        return questions

    def pages(self):
        return AskPage.objects.filter(asker=self)

    def first_page(self):
        return self.pages()[0]

    def last_page(self):
        return self.pages().order_by('-order')[0]

    def page_count(self):
        return self.pages().count()

    def return_page_by_index(self, number):
        everything = self.pages()
        try:
            return everything[int(number)]
        except IndexError:
            return None

    def admin_edit_url(self):
            return admin_edit_url(self)


    def json_export(self):
        """Export Asker and related objects as json.

        Export everything needed to recreate this questionnaire on
        another signalbox instance (or 3rd party system) with the
        exception of question assets."""
        j = partial(serializers.serialize, 'json', use_natural_keys=True, indent=2)

        pages = self.pages()

        questionlists = [i.get_questions() for i in pages]
        for i, j in zip(questionlists, pages):
            i = [j] + i

        return list(itertools.chain(*questionlists))


        return j(itertools.chain(*questionlists))

        jsonout = json.dumps(
                {
                    'pages': questionlists,
                }
            )

        return jsonout

        questions_in_pages = self.questions()

        questions = [i.question for i in questions_in_pages]

        choicesets = set([i.choiceset for
                i in questions if i.choiceset])

        choices = Choice.objects.filter(choiceset__in=choicesets)

        jsonstring = j(itertools.chain(*
                [
                    [self],
                    set(pages),
                    set(choicesets),
                    set(choices),
                    list(questions),
                    set(questions_in_pages),
                ]
            )
        )

        # this is dirty, but we don't want the keys when we re-import
        # because it might overwrite existing data. This was we can
        # just do ./manage.py loaddata file.json and things new copies
        # of everything will be created (although variable names still
        # need to be unique and other constraints apply)
        jsonstring = re.sub(r'"pk": \d+,', r'"pk": null,', jsonstring)

        return jsonstring


    class Meta:
        permissions = (
            ("can_preview", "Can preview surveys"),
        )
        verbose_name = "Questionnaire"
        app_label = "ask"

    def __unicode__(self):
        return self.reference
