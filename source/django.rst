oTree & Django
--------------

``otree`` command
~~~~~~~~~~~~~~~~~

The ``otree`` command is a customized version of Django's ``manage.py``.

For example, ``otree runserver`` is basically equivalent to ``python manage.py runserver``.

In addition to the built-in `Django management commands <https://docs.djangoproject.com/en/1.9/ref/django-admin/>`__ like ``runserver`` and ``startapp``,
oTree defines a few extra ones like ``resetdb``, ``create_session``, and ``runprodserver``.

For the list of available commands, enter ``otree help``.
For information about a specific command, enter ``otree help [command]``, e.g. ``otree help test``.

Project folder
~~~~~~~~~~~~~~

The folder containing your games is a Django project, as explained
`here <https://docs.djangoproject.com/en/1.8/intro/tutorial01/#creating-a-project>`__.

It comes pre-configured with all the files,
settings and dependencies so that it works right away.
You should create your apps inside this folder.

Differences between oTree and Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Models
^^^^^^

-  Field labels should go in the template formfield, rather than the
   model field's ``verbose_name``.
-  ``null=True`` and ``default=None`` are not necessary in your model
   field declarations; in oTree fields are null by default.
-  ``initial`` is an alias for ``default`` in a model field's kwargs.
-  On ``CharField``\ s, ``max_length`` is not required.

Adding custom views & URLs
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create URLs and views that are independent of oTree,
using Django's `URL dispatcher <https://docs.djangoproject.com/en/1.9/topics/http/urls/>`__
and `views <https://docs.djangoproject.com/en/1.9/topics/http/views/>`__.

First, define the view function in one of your project modules.
It can be a function-based view or class-based view.

.. code-block:: python

    # my_module.py
    from django.http import HttpResponse

    def my_view(request):
        return HttpResponse('This is a custom view')


Create a file ``urls.py`` in your project root.
In this file, put:

.. code-block:: python

    # urls.py
    from django.conf.urls import url
    from otree.default_urls import urlpatterns

    urlpatterns.append(url(r'^my_view/$', 'my_module.my_view'))


In your settings.py, set ``ROOT_URLCONF`` to point to the ``urls.py`` that you just created:

.. code-block:: python

    # settings.py
    ROOT_URLCONF = 'urls'
