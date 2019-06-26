.. _django:

Django
------

Here are things for Django developers to know about oTree.

``otree`` command
~~~~~~~~~~~~~~~~~

The ``otree`` command is a customized version of Django's ``manage.py``.

In addition to the built-in
`Django management commands <https://docs.djangoproject.com/en/1.9/ref/django-admin/>`__ like ``startapp``,
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

You can create URLs and pages that are independent of oTree,
using Django's `URL dispatcher <https://docs.djangoproject.com/en/1.9/topics/http/urls/>`__
and `pages <https://docs.djangoproject.com/en/1.9/topics/http/pages/>`__.

First, define the view function in one of your project modules.
It can be a function-based view or class-based view.

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

    The information in this section is for advanced programmers
    who want to use oTree's unstable features.

    oTree is using channels v 0.17.3,
    which is incompatible with the current version of channels, 2.x.

    When oTree upgrades to channels 2.x, any existing oTree apps that depend on
    the old version of Channels will likely break and may need significant fixes
    (upgrading your code to the channels 2.x format is a non-trivial task).

    So, if you opt to use Channels, you should account for this in your long-term
    plans.


oTree uses `Django channels <https://channels.readthedocs.io/en/stable/>`__
for real-time (WebSocket) functionality.

If you are comfortable with more advanced programming, you can add your own
real-time interactions such as a continuous-time market.

Channels is pre-installed as part of oTree.
First, create a module ``consumers.py`` in one of your apps.
For each WebSocket,
you should create a ``connect`` consumer and ``disconnect`` consumer.

See `otree.channels.consumers <https://github.com/oTree-org/otree-core/blob/master/otree/channels/consumers.py>`__
for examples of more complex consumers. Also see :ref:`auto_save`.

Next, create a module ``routing.py`` in your project root
and append your routes to oTree's built-in routes:

.. code-block:: python

    from channels.routing import route
    from myapp.consumers import ws_add, ws_disconnect
    from otree.channels.routing import channel_routing

    channel_routing += [
        route("websocket.connect", ws_add, path=r"^/chat"),
        route("websocket.disconnect", ws_disconnect, path=r"^/chat"),
    ]

In settings.py, set ``CHANNEL_ROUTING = 'routing.channel_routing'``
(this is the dotted path to your ``channel_routing`` variable in ``routing.py``)
