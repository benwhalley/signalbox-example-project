from django.contrib.auth.views import logout
from django.views.generic import DetailView, ListView
from django.conf.urls.defaults import patterns, url
from signalbox.views.front import study_registration
from signalbox.views.replies import *
from signalbox.models import Study
from signalbox.views.front import join_study, user_homepage, MembershipDetail, update_profile_for_studies
from django.http import HttpResponseForbidden


urlpatterns = patterns('',
    url(r'^enter/data/(?P<observation_token>[\w]{8}(-[\w]{4}){3}-[\w]{12})/?$',
        start_data_entry, {'entry_method': "participant"}, name="start_data_entry"),

    url(r'^double/enter/data/(?P<observation_token>[\w]{8}(-[\w]{4}){3}-[\w]{12})/?$',
        start_data_entry, {'entry_method': "double_entry"},
        name="start_double_entry"),

    url(r'^studies/$', ListView.as_view(model=Study,
        queryset=Study.objects.filter(visible=True, paused=False)),
        name='study_list'),

    url(r'^studies/(?P<pk>\d+)/$', DetailView.as_view(model=Study,), {}, name='study', ),
    url(r'^studies/(?P<study_id>\d+)/register/$', study_registration, name='study_registration'),
    url(r'^studies/join/$', join_study, name='join_study'),
    url(r'^studies/participant/details/$', update_profile_for_studies, name='update_profile_for_studies'),



    url(r'^accounts/profile/membership/(?P<pk>\d+)$',
        MembershipDetail.as_view(), {}, name='membership_home', ),

    url(r'^profile/?$', user_homepage, name='user_homepage'),
    (r'^profile/$', 'django.views.generic.simple.redirect_to',
        {'url': 'accounts/profile/'}),
    url(r'^accounts/profile/?$', user_homepage, name='user_homepage'),

    url(r'^logout/?$', logout, {'next_page': '/'}, name='logout'),

    url(r'^crossdomain.xml$', lambda x: HttpResponseForbidden("Forbidden")),

)
