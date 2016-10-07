from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import password_reset

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/studies/', permanent=False), name='index'),
    url(r'^', include('signalbox.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^reset/password/$', password_reset, {}),
    url(r'^robots\.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^complete/setup/', TemplateView.as_view(template_name='complete.html')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
