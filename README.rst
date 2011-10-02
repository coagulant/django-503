Django 503
==========

An app to show 503 error page, while your django site is on maintenance.

Installation
------------

Recommended way to install is pip::

  pip install django-503


Usage
-----

* Add ``django_503`` to ``INSTALLED_APPS`` in settings.py::

    INSTALLED_APPS = (...
                      'django_503',
                      ...
                     )

* Add ``'django_503.middleware.MaintenanceMiddleware'`` to your ``MIDDLEWARE_CLASSES``
after session and auth middlewares like this::

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
        'django_503.middleware.MaintenanceMiddleware',
    )

Now you can turn on maintenance mode by changing app config via django admin interface.
Make sure, you use admin.autodiscover() for that ot work.