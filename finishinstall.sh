#!/bin/bash
python manage.py syncdb --noinput
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '$DJANGO_ADMIN_USER_EMAIL', '$DJANGO_ADMIN_USER_PASSWORD'); exit()" |  python manage.py shell_plus
