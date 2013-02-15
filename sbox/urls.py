from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from tastypie.api import Api
import ask.api


v1_api = Api(api_name='v1')
v1_api.register(ask.api.ChoiceSetResource())
v1_api.register(ask.api.AskerResource())



from django.contrib.auth.views import password_reset



urlpatterns = patterns('',
        (r'^exports/', include('data_exports.urls', namespace='data_exports')),

        (r'^reset/password/$', password_reset, {}),

        (r'^robots\.txt', direct_to_template,
            {'template': 'robots.txt', 'mimetype': 'text/plain'}),

        (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
            {'url': '/static/favicon.ico'}),

        (r'^', include('signalbox.urls.frontend_urls')),

        (r'^ask/', include('ask.urls')),
        (r'^twilio/', include('twiliobox.urls')),
        (r'^accounts/', include('registration.backends.simple.urls')),
        (r'^selectable/', include('selectable.urls')),
        (r'^admin/signalbox/', include('signalbox.urls.admin_urls')),
        (r'^admin/ask/', include('ask.admin_urls')),
        (r'^admin/', include(admin.site.urls)),
        (r'^api/', include(v1_api.urls)),
        (r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
