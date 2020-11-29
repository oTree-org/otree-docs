.. _django:

Django
------

Here are things for Django developers to know about oTree.

Migrations and "resetdb"
~~~~~~~~~~~~~~~~~~~~~~~~

You generally shouldn't use ``makemigrations`` and ``migrate``.
Instead, run ``otree resetdb``, which will reset and sync the database.
If you need to preserve the database between updates, you can try the strategy
mentioned in :ref:`migrations`.

Server
~~~~~~

oTree is based on ASGI, so it doesn't work with WSGI servers like Gunicorn.

Models
~~~~~~

.. _auto_save:

Auto-save of models
'''''''''''''''''''

In oTree, you don't need to explicitly call ``.save()`` on your models;
oTree will do it automatically (it uses an idmap cache).
However, this auto-save feature does not apply to custom models or pages that don't inherit from oTree's,
or custom WebSocket/AJAX code. In that case, you have to remember to save your database
models yourself as you would in a regular Django project.

You will also need to figure out how to query your models using Django's ORM
and the model's pk/code, etc.

Misc notes on models
''''''''''''''''''''

-  ``null=True`` and ``default=None`` are not necessary in your model
   field declarations; in oTree fields are null by default.
-  ``initial`` is an alias for ``default`` in a model field's kwargs.
-  ``label`` is an alias for ``verbose_name`` in a model field's kwargs.

Adding custom pages & URLs
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create URLs and views that are independent of oTree,
using Django's `URL dispatcher <https://docs.djangoproject.com/en/2.2/topics/http/urls/>`__
and `views <https://docs.djangoproject.com/en/2.2/topics/http/views/>`__.

First, define the view function in one of your project modules.

.. code-block:: python

    # In my_app.pages
    from django.http import HttpResponse

    def my_view(request):
        return HttpResponse('This is a custom view')


Create a file ``urls.py`` in your project root.
In this file, put:

.. code-block:: python

    # urls.py
    from django.urls import path
    from otree.urls import urlpatterns
    import my_app.pages

    urlpatterns.append(path('my_view/', my_app.pages.my_view))

In your settings.py, set ``ROOT_URLCONF`` to point to the ``urls.py`` that you just created:

.. code-block:: python

    # settings.py
    ROOT_URLCONF = 'urls'


.. _channels:

Real-time and WebSockets
~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    oTree 3.0 has a feature called :ref:`live pages <live>`,
    which are an easier way of adding real-time functionality to your app.
    Before using Django Channels, see if you can accomplish it using live pages.

.. warning::

    This section is for advanced programmers who want to use oTree's internal and unsupported features.

oTree uses `Django channels <https://channels.readthedocs.io/en/stable/>`__
for real-time (WebSocket) functionality.
You can add your own real-time interactions such as a continuous-time market.

You also need to define websocket routes (which are like URL patterns that decide which consumer to run).
You can put them in a module called ``your_app/otree_extensions/routing.py``.
You should make a list of routes called ``websocket_routes``.
Then in ``settings.py``, set ``EXTENSION_APPS = ['your_app']``.

See ``otree.channels.consumers``
to see how oTree queries and saves models inside consumers.

If you are building your app for long-term stability,
beware of importing anything from ``otree.channels`` into your code.
Since it is not part of ``otree.api``, it may be removed abruptly.
