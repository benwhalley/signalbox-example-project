from django.conf.urls.defaults import patterns, url
from ask.views import preview_asker, show_page


urlpatterns = patterns('',
    url(r'^preview/(?P<asker_id>\d+)?/(?P<page_num>\d+)?/$', preview_asker,
        name="preview_asker"),
    url(r'^(?P<reply_token>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', show_page, name="show_page"),

)
