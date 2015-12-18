from django.conf.urls import url, include
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
