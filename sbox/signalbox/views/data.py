import os
import csv
import itertools
import zipfile
import tempfile
from datetime import timedelta, date, datetime
from django.utils.encoding import smart_unicode
from django.conf import settings
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from django import forms
from ask.models import fields
from ask.models import Question, Instrument
from signalbox.models import Answer, Membership, Observation, Reply
from signalbox.decorators import group_required
from signalbox.forms import SelectExportDataForm, DateShiftForm
from reversion import revision

EXPORT_DATEFORMAT = "%Y/%m/%d %H:%M:%S"

# The internal accessors are listed first in each tuple, and the name we want
# to export listed second.
FIELD_MAP = [
    ('reply__observation__n_in_sequence', 'n_in_sequence'),
    ('reply__observation__due', 'due'),
    ('reply__observation__id', 'observation__id'),
    ('reply__observation__created_by_script__name', 'script'),
    ('reply__observation__created_by_script__reference', 'script_reference'),
    ('reply__is_canonical_reply', 'is_canonical_reply'),
    ('reply__started', 'started'),
    ('reply__last_submit', 'finished'),
    ('reply__originally_collected_on', 'originally_collected_on'),
    ('reply__id', 'reply__id'),

    ('reply__observation__dyad__user__username', 'participant__username'),
    ('reply__observation__dyad__user__id', 'participant__id'),
    ('reply__observation__dyad__relates_to__user__username',
     'relates_to_participant__username'),
    ('reply__observation__dyad__relates_to__user__id',
     'relates_to_participant__id'),

    ('reply__observation__dyad__id', 'membership__id'),
    ('reply__observation__dyad__condition__tag', 'condition'),
    ('reply__observation__dyad__study__slug', 'study'),

    ('reply__observation__dyad__date_randomised', 'date_randomised')
]


def _internal_fields(FIELD_MAP):
    """Function to split FIELD up because it can get updated by the form.
    """

    return zip(*FIELD_MAP)[0]


ANSWER_VALUES = ['question__q_type',
                 'question__variable_name',
                 'answer']


def fupdate(dic, new):
    """Updates a dict and returns dict + new vals; useful when building a new list of dicts."""
    dic.update(new)
    return dic


def renamekeys(dictionary, oldnew_namepairs):
    """Renames keys in a dictionary -> dict"""
    for old, new in oldnew_namepairs:
        if old != new:
            dictionary[new] = dictionary.get(old, None)
            del dictionary[old]

    return dictionary


def write_to_file(string):
    thefile = tempfile.TemporaryFile()
    thefile.write(string)
    thefile.seek(0)

    return thefile


def _format_dates_for_export_in_place(dictionary):
    for k, v in dictionary.items():
        if isinstance(v, datetime) or isinstance(v, date):
            dictionary[k] = v.isoformat()


def _encode_dict_to_unicode_in_place(d):
    """Take a dictionary where values are str or None and encode all strings as utf-8 in place."""
    for k, v in d.items():
        if isinstance(v, basestring):
            d[k] = v.encode('utf-8')


def write_dict_to_file(datadict, headings):
    """Export dict to a csv file"""

    thefile = tempfile.TemporaryFile()
    writer = csv.DictWriter(thefile, headings, extrasaction='ignore')
    writer.writerow(dict([(i, i) for i in headings]))

    _ = [_encode_dict_to_unicode_in_place(i) for i in datadict]
    _ = [_format_dates_for_export_in_place(i) for i in datadict]

    writer.writerows(datadict)
    thefile.seek(0)
    return thefile


def makefile_string():
    return "do syntax.do\n!/Applications/StatTransfer10/st data.dta data.sav\nexit"


def generate_syntax(template, questions, reference_study=None):
    """Return a string of stata syntax to format exported datafile for a given set of questions."""

    t = get_template(template)
    syntax = t.render(
        Context({'questions': questions, 'reference_study': reference_study})
    )
    return syntax


def _reshape_wide(answers, grouping, variable, value):
    """Take a list of dictionaries, group, and then reshape to wide."""

    group_key_fun = lambda a: a[grouping]
    grouped = [list(cs) for _, cs in itertools.groupby(answers, group_key_fun)]

    combined_rows = [fupdate(reply[0], dict([(i[variable], i[value])
                                             for i in reply])) for reply in grouped]

    return combined_rows


BOOLS_MAPPING = {False: 0, True: 1}


def _remap_bools(dic):
    """Make booleans 1/0 for export to SPSS/Stata"""

    for k, val in dic.iteritems():
        if type(val) == bool:
            dic[k] = BOOLS_MAPPING[val]


def get_answers(studies):
    replies = Reply.objects.filter(observation__dyad__study__in=studies)
    answers = Answer.objects.all(
    ).select_related('question', 'question__choiceset', 'question__scoresheet'
                     ).filter(reply__in=replies
                              ).exclude(question__variable_name__isnull=True
                                        ).order_by('reply')
    return answers


def build_csv_data_as_string(answers, reference_study):

    answerkeys = list(ANSWER_VALUES) + list(_internal_fields(FIELD_MAP))
    answer_values = answers.values(*answerkeys)

    # here we check whether the questiontype for each answer has an `export_processor' attached
    # to it, used to format values for export to txt. If it does, apply it in place to the answer
    # in the answer dictionary
    for i in answer_values:
        qtp = fields.class_name(i['question__q_type'])
        iden = lambda x: x
        proc = getattr(fields, qtp).export_processor or iden

        i['answer'] = proc(i['answer'])
        # we don't need this any more --- because the answers will be reshaped to wide format in a
        # minute. With no special handling would be meaningless in a row with all a reply's answers
        del i['question__q_type']

    reply_dictionaries = _reshape_wide(
        answer_values, 'reply__id', 'question__variable_name', 'answer')

    _ = [(i.pop('answer'), i.pop('question__variable_name'))
         for i in reply_dictionaries]
    _ = [renamekeys(i, FIELD_MAP) for i in reply_dictionaries]
    _ = [reply.update({'is_reference_study': bool(reply['study'] == reference_study.slug)})
         for reply in reply_dictionaries]
    _ = [_remap_bools(d) for d in reply_dictionaries]

    headings = set(itertools.chain(*[i.keys() for i in reply_dictionaries]))
    data = write_dict_to_file(reply_dictionaries, headings).read()

    return data


def build_zipfile(studies, reference_study, zip_path):
    """Writes data and syntax to temporary directory and returns the path to that directory."""

    answers = get_answers(studies)
    answers_with_files = answers.exclude(upload="")

    data = build_csv_data_as_string(answers, reference_study)
    syntax = generate_syntax('admin/ask/stata_syntax.html',
        Question.objects.filter(id__in=answers.values('question__id')),
        reference_study=reference_study)

    zipf = zipfile.ZipFile(zip_path, "w")

    syntax = smart_unicode(syntax).encode('utf-8')

    zipf.writestr('syntax.do', syntax)
    zipf.writestr('data.csv', data)
    zipf.writestr('make.do', makefile_string())
    [zipf.writestr("uploads" + i.upload.name, i.upload.read(
    ), ) for i in answers_with_files if i.upload.name]

    return zipf


@group_required(['Researchers', ])
def export_dataframe(request):
    """Export the data one row per reply, along with stata syntax to import/label it, as a zip."""

    form = SelectExportDataForm(request.POST or None)
    if not form.is_valid():
        return render_to_response('manage/export_data.html', {'form': form},
                                  context_instance=RequestContext(request))

    if len(form.cleaned_data['observations']) == 0:
        messages.add_message(
            request, messages.WARNING, """No observations recorded yet.""")
        return render_to_response('manage/export_data.html', {'form': form},
                                  context_instance=RequestContext(request))

    zip_path = "/tmp/export.zip"
    zipcontent = build_zipfile(
        form.cleaned_data['studies'],
        form.cleaned_data['reference_study'],
        zip_path
    )
    zipcontent.close()
    zipcontent = open(zip_path, 'r').read()
    os.remove(zip_path)

    # return httpresponse
    response = HttpResponse(
        zipcontent, content_type='application/x-zip-compressed')
    response['Content-disposition'] = "attachment; filename=exported_data.zip"
    return response


def _shifted(obj, datetimefield, delta):
    setattr(obj, datetimefield, getattr(obj, datetimefield) + delta)
    return obj


@group_required(['Researchers', ])
@revision.create_on_success
def dateshift_membership(request, pk=None):
    '''Allows Researchers to shift the time of all observations within a Membership.'''

    membership = get_object_or_404(Membership, id=pk)
    form = DateShiftForm(request.POST or None)
    if form.is_valid():

        # calclate difference from current randomisation date and shift randomisation date
        delta = form.delta(current=membership.date_randomised)
        membership.date_randomised = membership.date_randomised + delta
        membership.save()

        shiftable = [i for i in membership.observations(
        ) if i.timeshift_allowed()]
        shifted = [_shifted(i, 'due', delta) for i in shiftable]
        shifted = [_shifted(i, 'due_original', delta) for i in shiftable]

        _ = [i.add_data("timeshift", value=delta) for i in shifted]
        _ = [i.save() for i in shifted]
        revision.comment = "Timeshifted observations by %s" % (delta,)

        form = DateShiftForm(
        )  # wipe the form to make it harder to double-submit by accident
        messages.add_message(request, messages.WARNING,
            """%s observations shifted by %s (read this carefully and thoroughly, it can be confusing).""" % (len(shifted), delta))

    else:
        messages.add_message(request, messages.ERROR,
                             """Be careful with this form!!! Changes are saved as soon as you submit.""")

    return render_to_response('admin/signalbox/dateshift.html',
                              {'form': form, 'membership': membership}, context_instance=RequestContext(request))
