from signalbox.decorators import group_required
from django.conf.urls.defaults import patterns, url
from ask.views import print_asker, show_codebook, preview_questions, export_instrument, bulk_add_questions
from django.views.generic.detail import DetailView
from ask.models import Asker


urlpatterns = patterns('',
    url(r'^question/add/multiple/$', bulk_add_questions, name="bulk_add_questions"),

    url(r'^asker/(?P<asker_id>\d+)/codebook/$', show_codebook,
        name="show_codebook",),

    url(r'^asker/(?P<asker_id>\d+)/print/$', print_asker,
        name="print_asker",),

    url(r'^instrument/export/(?P<pk>\d+)/$', export_instrument,
        name="export_instrument",),

    url(r'^preview/questions/(?P<ids>[\w,]+)/$', preview_questions, name="preview_questions"),

    url(r'asker/(?P<pk>\d+)/export/$',
            group_required(['Researchers', 'Research Assistants',])(
                DetailView.as_view(
                    model=Asker, template_name="admin/ask/asker/asker_export.html"
                )
            ),
            name="export_asker"),

)
