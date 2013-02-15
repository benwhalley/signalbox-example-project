from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from django.conf import settings

from signalbox.utils import *
from signalbox.models import *
from registration.views import register
from signalbox.forms import UserProfileForm


def study_registration(request, study_id):
    study = get_object_or_404(Study, id=study_id)
    request.session['trying_to_join'] = study.id

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('join_study'))
    else:
        return register(request,
                        backend='registration.backends.simple.SimpleBackend',
                        success_url=reverse('join_study'),
                        extra_context={'study': study},
                        )


def update_profile_for_studies(request):

    form = UserProfileForm(
        request.POST or None, instance=request.user.get_profile())

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('join_study'))

    return render_to_response('signalbox/additional_info.html',
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def join_study(request):
    study = get_object_or_none(
        Study, id=request.session.get('trying_to_join', None))

    if not request.user.get_profile().has_all_required_details():
        return HttpResponseRedirect(reverse('update_profile_for_studies'))

    if not study:
        return HttpResponseRedirect(reverse('user_homepage'))

    try:
        dyad, created = Membership.objects.get_or_create(
            user=request.user, study=study)
        if created:
            messages.success(request, study.welcome_text)
        else:
            messages.error(request,
                    "You were already registered for this study (%s)" % (study.name))

    except Membership.MultipleObjectsReturned:
        messages.error(request, "You were already registered for this study (%s)" % (study.name))

    request.session['trying_to_join'] = None
    return HttpResponseRedirect(reverse('user_homepage'))


@login_required
def user_homepage(request):
    """Just returns the request to the template.

    This makes the User available to the template as {{user}} which  is used to
    output relevant details for them."""

    if not request.user.get_profile().has_all_required_details():
        return HttpResponseRedirect(reverse('update_profile_for_studies'))

    return render_to_response('signalbox/user_home.html',
                              {'installation_manager_email':
                                  settings.MANAGERS[0][1]},
                              context_instance=RequestContext(request))


class MembershipDetail(DetailView):
    """Class based view of Memberships to be used on the frontend."""
    model = Membership

    def get_object(self):
        obj = super(MembershipDetail, self).get_object()
        if obj.user == self.request.user:
            return obj
        else:
            raise Http404
