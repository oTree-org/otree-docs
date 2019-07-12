.. _django:

Django
------

Here are things for Django developers to know about oTree.

``otree`` command
~~~~~~~~~~~~~~~~~

The ``otree`` command is a customized version of Django's ``manage.py``.

In addition to the built-in Django management commands like ``startapp``,
oTree defines a few extra ones like ``resetdb``, ``create_session``, and ``runprodserver``.

Migrations and "resetdb"
~~~~~~~~~~~~~~~~~~~~~~~~

If you are using oTree, you generally shouldn't use ``makemigrations`` and ``migrate``.
Instead, run ``otree resetdb``, which will reset and sync the database.
If you need to preserve the database between updates, you can try the strategy
mentioned in :ref:`migrations`.

Project folder
~~~~~~~~~~~~~~

The folder containing your games is a Django project, as explained
`here <https://docs.djangoproject.com/en/1.11/intro/tutorial01/#creating-a-project>`__.

It comes pre-configured with all the files,
settings and dependencies so that it works right away.
You should create your apps inside this folder.

Server
~~~~~~

oTree doesn't work with Gunicorn, mod_wsgi, or any other typical WSGI server.
Because it uses `Django Channels <http://channels.readthedocs.io/en/latest/>`__
for WebSocket support, it should be run with ``otree runprodserver``,
which internally starts the Daphne server, several channels workers, and a task queue.
More info :ref:`here <server-ubuntu>`.

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
using Django's `URL dispatcher <https://docs.djangoproject.com/en/1.9/topics/http/urls/>`__
and `views <https://docs.djangoproject.com/en/1.11/topics/http/views/>`__.

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
    from django.conf.urls import url
    from otree.urls import urlpatterns

    urlpatterns.append(url(r'^my_view/$', 'my_app.pages.my_view'))


In your settings.py, set ``ROOT_URLCONF`` to point to the ``urls.py`` that you just created:

.. code-block:: python

    # settings.py
    ROOT_URLCONF = 'urls'

If you need to access oTree's models, you will have to handle querying and saving
objects yourself.

.. _channels:

Real-time and WebSockets
~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

    This section is for advanced programmers who want to use oTree's unstable/unsupported features.

    The information below has changed as of July 2019.

oTree uses `Django channels <https://channels.readthedocs.io/en/stable/>`__
for real-time (WebSocket) functionality.
You can add your own real-time interactions such as a continuous-time market.

As of July 2019, we have released a beta version with support for
Django Channels 2.x.
(Until now, oTree has used Django Channels 0.17.3.)
You can install the beta with::

    pip install -U otree --pre

Django Channels 2.x has many API changes.
Any existing oTree apps that depend on
the old version of Channels will **break** when you upgrade.

`This <https://channels.readthedocs.io/en/latest/one-to-two.html>`__ article lists the differences
in the new version of channels.
In particular:

-   ``channels.Group`` no longer exists.
    Instead, you use ``group_add`` and ``group_send``.
-   You need to wrap ``group_add`` and ``group_send`` in ``async_to_sync``.
-   If you want to send to a group from ``models.py`` or ``pages.py``,
    you use ``get_channel_layer()``, then do ``group_send``.
    Rather than sending JSON to the websocket directly, you invoke a method on your consumer class,
    by adding ``"type": "your_method_name"`` to the event.
    See `here <https://channels.readthedocs.io/en/latest/topics/channel_layers.html#using-outside-of-consumers>`__
    (don't be confused by dots in type names, they just get converted to underscores).

The "ChatConsumer" example
`here <https://channels.readthedocs.io/en/latest/tutorial/part_2.html#enable-a-channel-layer>
is a good simple example showing the new API.

You also need to define websocket routes (which are like URL patterns that decide which consumer to run).
You can put them in a module called ``your_app/otree_extensions/routing.py``.
You should make a list of routes called ``websocket_routes`` (not ``channel_routing`` like before).
Then in ``settings.py``, set ``EXTENSION_APPS = ['your_app']``.

Once you have installed the beta, see ``otree.channels.consumers``
to see how oTree queries and saves models inside consumers.