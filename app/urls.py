from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import password_reset

urlpatterns = i18n_patterns('',
        url(r'^$', RedirectView.as_view(url='/studies/', permanent=False), name='index'),
        (r'^', include('signalbox.urls')),

        (r'^admin/', include(admin.site.urls)),
        (r'^accounts/', include('registration.backends.simple.urls')),
        # (r'^', include('cms.urls')),
        (r'^reset/password/$', password_reset, {}),
        (r'^robots\.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
)
