SESSION_CONFIGS
---------------

To configure a session, you would go to ``settings.py`` and
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




Once you have defined a session config, you can run the server,
open your browser to the admin interface, and create a new session.
You would select "My Session Config" as the configuration to use,
and then enter "30" for the number of participants.

An instance of a session would be created, and you would get the start links to
distribute to your participants.

DEBUG
-----

You can turn off debug mode by setting the environment variable ``OTREE_PRODUCTION``,
or by directly modifying ``DEBUG`` in settings.py.

If you turn off ``DEBUG`` mode, you need to manually run ``otree collectstatic`` before starting your server.
Also, you should set up `Sentry <sentry>` to receive email notifications of errors.
