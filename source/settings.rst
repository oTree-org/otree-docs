Settings
========

Here are explanations of a few oTree-specific settings.
Full info on all Django's settings can be found `here <https://docs.djangoproject.com/en/1.11/ref/settings/>`__.

.. _SESSION_CONFIGS:

SESSION_CONFIGS
---------------

To create a session, you first need to
define a "session config".

If you are using oTree Studio, click "Session Configs" in the sidebar.
If you are using PyCharm, go to ``settings.py`` and add an entry to ``SESSION_CONFIGS`` like this
(assuming you have created apps named ``my_app_1`` and ``my_app_2``):

.. code-block:: python

    dict(
        name='my_session_config',
        display_name='My Session Config',
        num_demo_participants=2,
        app_sequence=['my_app_1', 'my_app_2']
    ),

For more info on how to use ``SESSION_CONFIGS``, see :ref:`edit_config`
and :ref:`session_config_treatments`.

SESSION_CONFIG_DEFAULTS
-----------------------

If you set a property in ``SESSION_CONFIG_DEFAULTS``, it will be inherited by all configs
in ``SESSION_CONFIGS``, except those that explicitly override it.
the session config can be accessed from methods in your apps as ``self.session.config``,
e.g. ``self.session.config['participation_fee']``


REAL_WORLD_CURRENCY_CODE
------------------------

See :ref:`currency`.

USE_POINTS
----------

See :ref:`points`.


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

To set ``OTREE_ADMIN_PASSWORD`` on Heroku, log into your Heroku dashboard's
settings, and set the config var ``OTREE_ADMIN_PASSWORD`` to your password.

If you change ``ADMIN_USERNAME`` or ``ADMIN_PASSWORD``,
you need to reset the database.

.. _DEMO_PAGE_TITLE:

DEMO_PAGE_TITLE
---------------

The title of the demo page.

DEMO_PAGE_INTRO_HTML
--------------------

The HTML in the sidebar of the demo page.