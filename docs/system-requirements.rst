System requirements
===================


Server
~~~~~~~~


The core dependencies are a unix-based server with:

* Python 2.7
* Django 1.3 (at least if using django_cms, and not tested with 1.4)


SignalBox depends on a number of third party apps and libraries to function including:

- django-reversion (for audit trails)
- django-selectable (user interface components)
- python-dateutil
- Markdown


Some other dependencies could be removed fairly easily, depending on the needs of the study. See deploy/requirements.txt file for a full list.


See :ref:`Installation guide <install-and-management>`


Browser
~~~~~~~~

The front-end (participant facing) should work in most browsers, including IE7.

The admin interface will largely function in IE7, although the menus are slightly broken.

Everything will work in IE8 onwards.


.. note:: It's recommended to use Chrome-Frame if IE7 is the only available browser. See: `<https://developers.google.com/chrome/chrome-frame/>`_

.. warning:: Check everything works in your target browsers early in the trial setup. The NHS has some weird and wonderful stuff deployed.

