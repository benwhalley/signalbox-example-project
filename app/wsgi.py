#!/usr/bin/env python
import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django
django.setup()

from django.core.wsgi import get_wsgi_application
import django.core.handlers.wsgi
from dj_static import Cling
# we have to load models or we end up in importerror hell when gunicorn
# tries to import urls... this is borrowed from what runserver does.
from django.db.models.loading import get_models
get_models()

# serve static media via gunicorn see dj-static
application = Cling(django.core.handlers.wsgi.WSGIHandler())

application = Cling(get_wsgi_application())
