Settings
========

Your settings can be found in ``settings.py``.
Here are explanations of a few oTree-specific settings.
Full info on all Django's settings can be found `here <https://docs.djangoproject.com/en/1.8/ref/settings/>`__.

.. _SESSION_CONFIGS:

SESSION_CONFIGS
---------------

To create a session, you first need to
define a "session config".

In ``settings.py``, add an entry to ``SESSION_CONFIGS`` like this
(assuming you have created apps named ``my_app_1`` and ``my_app_2``):

.. code-block:: python

    {
        'name': 'my_session_config',
        'display_name': 'My Session Config',
        'num_demo_participants': 2,
        'app_sequence': ['my_app_1', 'my_app_2'],
    },


Once you have defined a session config, you can run ``otree resetdb``,
then ``otree runserver``,
open your browser to the admin interface, and create a new session.
You would select "My Session Config" as the configuration to use.

For more info on how to use ``SESSION_CONFIGS``, see :ref:`edit_config`
and :ref:`session_config_treatments`.

SESSION_CONFIG_DEFAULTS
-----------------------

If you set a property in ``SESSION_CONFIG_DEFAULTS``, it will be inherited by all configs
in ``SESSION_CONFIGS``, except those that explicitly override it.
the session config can be accessed from methods in your apps as ``self.session.config``,
e.g. ``self.session.config['participation_fee']``


DEBUG
-----

You can turn off debug mode by setting the environment variable ``OTREE_PRODUCTION`` to ``1``,
or by directly modifying ``DEBUG`` in settings.py.

If you turn off ``DEBUG`` mode, you need to manually run ``otree collectstatic`` before starting your server,
or else CSS/JS and other static files will fail to load and your site will look broken.
Also, you should set up :ref:`Sentry <sentry>` to receive email notifications of errors.


REAL_WORLD_CURRENCY_CODE
------------------------

See :ref:`currency`.

USE_POINTS
----------

See :ref:`points`.

SENTRY_DSN
----------

See :ref:`Sentry <sentry>`.


AUTH_LEVEL
----------

See ``AUTH_LEVEL``.

It's somewhat preferable to set the environment variable ``OTREE_AUTH_LEVEL``
on your server, rather than setting ``AUTH_LEVEL`` directly in settings.py.
This will allow you to develop locally without having to enter a password
each time you launch the server, but still get password protection on your
actual server.

ROOMS
-----

See :ref:`rooms`.

ROOM_DEFAULTS
-------------

See :ref:`rooms`.


ADMIN_USERNAME, ADMIN_PASSWORD
------------------------------

For security reasons, it's recommended to put your admin password in an environment variable,
then read it in ``settings.py`` like this::

    ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

To set ``OTREE_ADMIN_PASSWORD`` on Heroku, enter this command, substituting your
own password of course::

    $ heroku config:set OTREE_ADMIN_PASSWORD=blahblah

If you change ``ADMIN_USERNAME`` or ``ADMIN_PASSWORD``,
you need to reset the database.