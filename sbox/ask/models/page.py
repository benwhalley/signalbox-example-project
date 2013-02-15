from django.db import models
from django.core.urlresolvers import reverse
from utilities.linkedinline import admin_edit_url
from question import QuestionInAskPage
from instrument import InstrumentInAskPage


def head(iterable):
    """Return the first item in an iterable or None"""
    try:
        return iterable[0]
    except IndexError:
        return None

class AskPageManager(models.Manager):
    def get_by_natural_key(self, reference, order):
        return self.get(asker__reference=reference, order=order)


class AskPage(models.Model):
    """A grouping of Questions and Instruments, as part of a Questionnaire."""

    def natural_key(self):
        return (self.asker.reference, self.order)

    asker = models.ForeignKey('Asker')
    order = models.FloatField(default=0)
    internal_name = models.CharField(max_length=255, blank=True, null=True)
    questions = models.ManyToManyField('Question', through="QuestionInAskPage")
    instruments = models.ManyToManyField('Instrument', through="InstrumentInAskPage")


    def get_absolute_url(self):
        return reverse('preview_asker',
            kwargs={'asker_id':self.asker.id, 'page_num':self.page_number()})

    def pages(self):
        return AskPage.objects.filter(asker=self.asker).order_by('order')

    def page_number(self):
        pages = [p for p in self.pages()]
        return pages.index(self)

    def progress_pages(self):
        """Returns a tuple with current page and number of pages for use in progress bar.
        """
        return (self.page_number()+1, self.asker.page_count())

    def percent_complete(self):
        if self.asker.show_progress:
            return int((self.page_number()+1.0)/self.asker.page_count()*100)
        return None

    def next_page(self):
        next_pages = self.pages().filter(order__gt=self.order)
        return head(next_pages)

    def prev_page(self):
        prev_pages = self.pages().filter(order__lt=self.order).order_by('-order')
        return head(prev_pages) or self.asker.first_page()

    def get_questions(self, reply=None):
        '''Returns an ordered list of Questions for the page.

        To do this we query, calculate the order within the page for questions inserted via
        instruments, and determine whether questions are required or not based on the settings in
        the InstrumentInAskPage instance.

        It would be nicer if we could do all this without having to merge into lists etc, and also
        query the related fields (like choices etc) using prefetch_related but this needs django 1.4

        '''

        que = list(QuestionInAskPage.objects.filter(page=self))
        instrumentsinpage = InstrumentInAskPage.objects.filter(page=self)

        if reply:
            instrumentsinpage = [i for i in instrumentsinpage if i.showme(reply)]

        # create a suborder within the instrument to keep instruments together as a block
        # dividing by 1000 means we can't have more than 1000 questions within an
        # instrument (checked on the instrument model).

        # Additionally, if the InstrumentInAskPage is set to require responses for all questions
        # then we set the question to be required when we add it to the list here.

        for i in instrumentsinpage:
            for q in i.all_questions():
                q.allow_not_applicable = i.allow_not_applicable
                q.required = q.required or (q.question.field_class().required_possible and bool(i.require_all))
                q.order = i.order+(q.order/1000)
                que.append(q)

        # sort the combined list based on the newly created ordering
        que.sort(lambda x, y: cmp(x.order, y.order))

        return que

    def questions_to_show(self, reply=None):
        """Return Questions in the page, filtered depending on users past answers in this Reply."""

        qlist = self.get_questions(reply)
        if reply:
            qlist = [q for q in qlist if q.showme(reply)==True]
        return qlist

    def questions_which_require_answers(self):
        return [i.question.response_possible() for i in self.questions_to_show()]

    class Meta:
        verbose_name = "Page"
        ordering = ['order']
        unique_together = ['internal_name', 'asker']
        app_label = "ask"

    def admin_edit_url(self):
        return admin_edit_url(self)

    def __unicode__(self):
        return u"%s" % (self.internal_name)

