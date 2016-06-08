Settings
========

Your settings can be found in ``settings.py``.
Here are explanations of a few oTree-specific settings.
Full info on all Django's settings can be found `here <https://docs.djangoproject.com/en/1.8/ref/settings/>`__.

SESSION_CONFIGS
---------------

To configure a session, you need to
define a "session config", which is a reusable configuration.
This lets you create multiple sessions, all with the same properties.

Add an entry to ``SESSION_CONFIGS`` like this (assuming you have created apps named ``my_app_1``
and ``my_app_2``):

.. code-block:: python

    {
        'name': 'my_session_config',
        'display_name': 'My Session Config',
        'participation_fee': 10.00,
        'app_sequence': ['my_app_1', 'my_app_2'],
    },


Once you have defined a session config, you can run ``otree resetdb``, then ``otree runserver``,
open your browser to the admin interface, and create a new session.
You would select "My Session Config" as the configuration to use.

An instance of a session would be created, and you would get the start links to
distribute to your participants.

SESSION_CONFIG_DEFAULTS
-----------------------

If you set a property in ``SESSION_CONFIG_DEFAULTS``, it will be inherited by all configs
in ``SESSION_CONFIGS``, except those that explicitly override it.
the session config can be accessed from methods in your apps as ``self.session.config``,
e.g. ``self.session.config['participation_fee']``


DEBUG
-----

You can turn off debug mode by setting the environment variable ``OTREE_PRODUCTION``,
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
If you are launching a study and want visitors to only be able to
play your app if you provided them with a start link, set the
environment variable ``OTREE_AUTH_LEVEL`` to ``STUDY``,
which will in turn set the setting ``AUTH_LEVEL``.
If you would like to put your site online in public demo mode where
anybody can play a demo version of your game, set ``OTREE_AUTH_LEVEL``
to ``DEMO``. This will allow people to play in demo mode, but not access
the full admin interface.

ROOMS
-----

See :ref:`rooms`.

ROOM_DEFAULTS
-------------

See :ref:`rooms`.