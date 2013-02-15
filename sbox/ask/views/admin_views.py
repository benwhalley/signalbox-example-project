import re
import json
from django.utils import encoding as en
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django import forms

from ask.forms import BulkAddQuestionsForm
from ask.models import Asker, Question, Instrument, ChoiceSet, QuestionInInstrument
from ask.models import truncatelabel
import ask.validators as valid

from django.contrib.auth.decorators import login_required
from signalbox.decorators import group_required
from signalbox.models import Reply
from django.core import serializers


@group_required(['Researchers', 'Research Assistants', ])
def export_instrument(request, pk):
    ins = get_object_or_404(Instrument, id=pk)
    return HttpResponse(ins.dump_json(), mimetype="application/json")


class ImportInstrumentForm(forms.Form):

    jsonfile = forms.FileField(required=True)

    def clean(self):
        bitstoload = self.cleaned_data['jsonfile'].read()
        self.instrument = json.loads(bitstoload)[0]
        try:
            for obj in serializers.deserialize("json", bitstoload):
                obj.save()
            return self.cleaned_data
        except Exception as e:
            raise ValidationError(e)


@group_required(['Researchers', 'Research Assistants', ])
def show_codebook(request, asker_id=None):
    '''Displays a Stata-style codebook for all of a survey's variables'''

    askers = [get_object_or_404(Asker, id=int(asker_id))]
    return render_to_response('admin/ask/codebook.html',
        {'askers': askers}, context_instance=RequestContext(request))


@login_required
def preview_asker(request, asker_id=None, page_num=None):
    page_num = int(page_num) or 0
    a = get_object_or_404(Asker, id=asker_id)
    p = a.return_page_by_index(int(page_num))
    if not p:
        raise Http404
    reply = Reply(asker=a, entry_method="preview", user=request.user,
        current_page=a.return_page_by_index(page_num))
    reply.save()
    url = reverse('show_page', kwargs={'reply_token': reply.token})
    return HttpResponseRedirect(url)


def statify(name, prefix=""):
    """
    Returns a valid Stata variable name, unique within the current database.
    """

    # kill anything which isn't ascii

    name = ''.join([x for x in name if ord(x) < 128])
    killwords = "i for to I'm about what with do is your how of the at please".split()
    name = re.sub(r'^\d+?\.?:?', "", name)
    namewords = name.lower().split()
    name = " ".join([i for i in namewords if i not in killwords])
    name = slugify(prefix + name)
    name = name.replace("-", "_")
    name = name[:30]
    matches = Question.objects.filter(variable_name__startswith=name).count()
    if matches > 0:
        name = name + "_" + str(matches)

    return name


@group_required(['Researchers', 'Research Assistants'])
def bulk_add_questions(request):
    form = BulkAddQuestionsForm(request.POST or None)

    if request.POST and form.is_valid():
        d = form.cleaned_data
        question_text_list = d['questions'].split("\r\n")
        questions = [
            Question(
                text=q,
                variable_label=truncatelabel(q, 80),
                variable_name=n,
                choiceset = d['choiceset'],
                q_type = d['q_type']
            )
            for q, n in zip(question_text_list, d['variable_names'])]

        added = []
        notadded = []
        for q in questions:
            try:
                q.save()
                added.append(q)
            except:
                notadded.append(q)
                messages.add_message(request, messages.WARNING,
                    'ERROR: %s %s not saved (perhaps the question already existed, or the variable name was not unique)' % (q.variable_name, q.text))

        messages.add_message(request, messages.INFO, '%s questions saved (%s).' % (len(added), (", ").join([i.text for i in added])))

        if d['add_to_instrument']:
            questionininstruments = [QuestionInInstrument(instrument=d['add_to_instrument'], question=q)
                for q in added]
            [i.save() for i in questionininstruments]
            return HttpResponseRedirect(reverse('admin:ask_instrument_change', args=(str(d['add_to_instrument'].id), )))

        return HttpResponseRedirect(reverse('admin:ask_question_changelist') + "?q=%s" % d['variable_prefix'])

    return render_to_response('admin/ask/bulk_add_questions.html',
        {'form': form},
        context_instance=RequestContext(request))
