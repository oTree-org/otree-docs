.. _django:

Django
------

Here are things for Django developers to know about oTree.

``otree`` command
~~~~~~~~~~~~~~~~~

The ``otree`` command is a customized version of Django's ``manage.py``.

For example, ``otree runserver`` is basically equivalent to ``python manage.py runserver``.

In addition to the built-in `Django management commands <https://docs.djangoproject.com/en/1.9/ref/django-admin/>`__ like ``runserver`` and ``startapp``,
oTree defines a few extra ones like ``resetdb``, ``create_session``, and ``runprodserver``.

For the list of available commands, enter ``otree help``.
For information about a specific command, enter ``otree help [command]``, e.g. ``otree help test``.

Migrations and "resetdb"
~~~~~~~~~~~~~~~~~~~~~~~~

If you are using oTree, you generally shouldn't use ``makemigrations`` and ``migrate``.
We are not fully compatible with migrations yet.
Instead, run ``otree resetdb``, which will reset and sync the database.


Project folder
~~~~~~~~~~~~~~

The folder containing your games is a Django project, as explained
`here <https://docs.djangoproject.com/en/1.8/intro/tutorial01/#creating-a-project>`__.

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

-  If you are using oTree in a typical way (with models.py and views.py),
   You don't need to explicitly call ``.save()`` on your models;
   oTree will do it automatically.
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
    from otree.urls import urlpatterns

    urlpatterns.append(url(r'^my_view/$', 'my_module.my_view'))


In your settings.py, set ``ROOT_URLCONF`` to point to the ``urls.py`` that you just created:

.. code-block:: python

    # settings.py
    ROOT_URLCONF = 'urls'

If you need to access oTree's models, you will have to handle querying and saving
objects yourself.

Real-time and WebSockets
~~~~~~~~~~~~~~~~~~~~~~~~

oTree uses `Django channels <https://channels.readthedocs.io/en/stable/>`__
for real-time (WebSocket) functionality.

If you are comfortable with more advanced programming, you can add your own
real-time interactions such as chat between players.

First, create a module ``consumers.py`` in one of your apps.
For each WebSocket,
you should create a ``connect`` consumer and ``disconnect`` consumer.
Here we will use a trivial example, taken from the Channels "getting started"
documentation:

.. code-block:: python

    # In consumers.py
    from channels import Group

    # Connected to websocket.connect
    def ws_add(message):
        message.reply_channel.send({"accept": True})
        Group("chat").add(message.reply_channel)

    # Connected to websocket.disconnect
    def ws_disconnect(message):
        Group("chat").discard(message.reply_channel)

See `otree.channels.consumers <https://github.com/oTree-org/otree-core/blob/master/otree/channels/consumers.py>`__
for examples of more complex consumers. If you need to access oTree's models in your consumers,
you will have to handle querying and saving objects yourself.

Next, create a module ``routing.py`` (either in your project root or in an app)
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

Chat box
^^^^^^^^

oTree doesn't have an out-of-the box chat funcito
A number of people have expressed interest in implementing a chat box for oTree.
Here are some ideas, based on how I would implement it myself.

I would implement a template tag that would be used like this::

    {% chatbox %}

It could take some optional parameters like::

    {% chatbox room=my_group_id nickname=player.role %}

``room`` is an ID for the room.
A chat room is typically scoped to a group,
which can be uniquely identified by the group's primary key
in combination with the app name (or ``Constants.name_in_url``).
If someone wants a different scope (e.g. it should be scoped to the current page
or to just a few members of the group), they can override the ``room`` arg.

So, your template tag could look like the below
(see the `Django docs on custom template tags <https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/>`__):

.. code-block:: python

    @register.inclusion_tag('mychatapp/chat.html', takes_context=True)
    def chatbox(context, *args, **kwargs):
        player = context['player']
        group = context['group']
        Constants = context['Constants']

        context.update(kwargs)

        # in case room and nickname are omitted from kwargs
        context.setdefault({
            'room': '{}-{}'.format(Constants.name_in_url, group.id),
            'nickname': 'Player {}'.format(player.id_in_group),
        })

        return context

``chat.html`` would contain the HTML/CSS/JS of the chat widget.
Consider implementing the widget with React or Web Components/Polymer.
There are many examples of chat rooms built with Django channels,
for example `this <https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/consumers.py>`__.

Each time a message is sent to the server, you should include
data like ``participant.code``. That way, inside the channels consumer,
you can create a model instance for the chat message.
The model schema could look like this:

.. code-block:: python

    from django.db import models
    from otree.models import Participant, Session

    class ChatMessage(models.Model):
        session = models.ForeignKey(Session)
        participant = models.ForeignKey(Participant)
        timestamp = models.DateTimeField(auto_created=True)
        room = models.CharField(max_length=100)
        message = models.TextField()
        nickname = models.CharField(max_length=100)

