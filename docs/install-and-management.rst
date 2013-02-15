

Installing and managing a Signalbox instance
============================================



Setting up the server
~~~~~~~~~~~~~~~~~~~~~~

See `deploy/server_config.txt` for details.



Fabric and `deploy'
~~~~~~~~~~~~~~~~~~~

The `fabfile.py` uses `Fabric <http://docs.fabfile.org/>`_ to automate pulling from the default repo, updating, installing dependencies and scheduled tasks, running database migrations and restarting the webserver. See the `fabfile.py` for details.



Requirements.txt
~~~~~~~~~~~~~~~~

All python dependencies must go in `deploy/requirements.txt`. These are loaded automatically by the fabric deploy command.

.. warning:: Always specify an exact version number of dependencies to avoid conflicts (e.g. with django_cms).



Management and scheduled tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use django-kronos to create management tasks which run at regular intervals; see `https://github.com/jgorset/django-kronos
<https://github.com/jgorset/django-kronos>`_.

At the shell, `app/manage.py runtask send` or `app/manage.py runtask remind` will send observations or reminders, and these tasks log to `log/cron.log`.

On installation, `app/manage.py installtasks` will add the relevant entries to schedule sending of observations and reminders to the crontab.

Make sure the logfile can be written to from both the owner of the crontab and www-data.










