from django.conf.urls.defaults import patterns, url
import views

urlpatterns = patterns('',

    url(r'^initialise/(?P<observation_token>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$',
        views.initialise_call, {}, "initialise_call"),

    url(r'^twiml/first/$',
        views.play_twiml, {'first': True}, "play_twiml_firstq"),

    url(r'^twiml/$', views.play_twiml, {'first': False}, "play_twiml"),

    url(r'^sms/info/(?P<external_id>\w+)/$',
        views.twilio_object_info, {'ob_type': 'sms.messages'}, "twilio_object_info"),

    url(r'^call/info/(?P<external_id>\w+)/$',
        views.twilio_object_info, {'ob_type': 'calls'}, "twilio_object_info"),

    url(r'^answerphone/?$', views.answerphone, {}, "answerphone"),

    url(r'^answerphone/thanks/$',
        views.answerphone_thanks, {}, "answerphone_thanks"),

    url(r'^sms/callback/$', views.sms_callback, {}, "sms_callback"),

)
