#!/bin/bash
# this because of issues with django 1.8 see
# https://stackoverflow.com/questions/30875977/django-1-8-migrate-relation-django-content-type-already-exists
python manage.py migrate sites --fake-initial
python manage.py migrate auth --fake-initial
python manage.py migrate  --fake-initial

# set the superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '$DJANGO_ADMIN_USER_EMAIL', '$DJANGO_ADMIN_USER_PASSWORD'); exit()" |  python manage.py shell
