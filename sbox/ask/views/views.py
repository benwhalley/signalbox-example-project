from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from ask.models import Asker, Question, AskPage, QuestionInAskPage
from signalbox.models import Reply
from ask.forms import PageForm


def mock_page(questions):
    """Creates a temporary AskPage to use when previewing questions. -> AskPage"""
    page = AskPage(asker=Asker(id=99999999))
    page.save()
    [page.questioninaskpage_set.add(QuestionInAskPage(page=page, question=i, order=j))
        for i, j in zip(questions, range(len(questions)))]
    return page  # remember to delete it, along with questions later


def page_preview(askpage, request):
    """Return a form which can be used to preview questions -> PageForm"""
    form = PageForm(request.POST or None, request.FILES or None,
                    page=askpage, reply=None, request=request)
    askpage.questioninaskpage_set.all().delete()
    askpage.delete()
    return form


@login_required
def preview_questions(request, ids):
    """Preview arbitrary questions, determined by CSV `ids' parameter -> HttpResponse"""

    idlist = [i for i in ids.split(",") if i]
    questions = Question.objects.filter(pk__in=idlist)
    page = mock_page(questions)
    form = page_preview(page, request)
    form.is_valid()

    return render_to_response(
        'admin/ask/question_preview.html', {'form': form, },
        context_instance=RequestContext(request))


def show_page(request, reply_token):
    """Handles displaying and saving each page as a form -> HttpResponse or HttpResponseRedirect"""

    reply = get_object_or_404(Reply, token=reply_token)
    # todo replace this with Reply.objects.authorised()
    can_see_clinical = bool(request.user.groups.filter(
        name__in=['Researchers', 'Clinicians']).count())
    if reply.is_clinical_data and not can_see_clinical:
        return HttpResponseRedirect(reverse("admin:index"))

    page = reply.get_current_page()
    form = PageForm(request.POST or None, request.FILES or None, page=page,
                    reply=reply, request=request)

    if form.is_valid():
        form.save(reply=reply)
        return reply.move_to_next_page(request)

    return render_to_response('asker_page.html',
        {
            'form': form,
            'page': reply.current_page,
            'hidemenu': page.asker.hide_menu,
            'reply': reply
        }, context_instance=RequestContext(request))


def print_asker(request, asker_id):
    """Returns full list of PageForms for Asker for print-ready output."""

    asker = get_object_or_404(Asker, id=asker_id)
    listofforms = [PageForm(request.POST or None, request=request, page=p, reply=None)
                   for p in asker.pages()]

    return render_to_response('asker_print.html',
                              {'forms': [(i, i.conditional_questions)
                                         for i in listofforms], 'asker': asker, },
                              context_instance=RequestContext(request))
