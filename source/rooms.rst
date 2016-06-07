.. _rooms:

Rooms
=====

.. note::

    This is an upcoming feature. It is not ready for official use yet.

oTree lets you configure "rooms", which provide:

-   Persistent links that you can assign to participants or workstations,
    which stay constant across sessions
-   A "waiting room" that lets you see how many people are waiting to start a session,
    so that you can create a session with the right number of people.
    Also, you can see a listing of who specifically is waiting, and who has not joined yet.
-   Short links that are easy for participants to type, good for quick live demos.

This feature replaces the "default session" from oTree 0.4.

oTree lets you define multiple rooms. For example, you can have several rooms for different classes you teach,
or multiple labs.

To create a room, add to your ``settings.py``
a setting ``ROOMS`` (and, optionally, ``ROOM_DEFAULTS``).

``ROOMS`` should be a list of dictionaries;
each dictionary defines the configuration of a room.

For example:

.. code-block:: python

    ROOM_DEFAULTS = {
        'use_secure_urls': False,
    }

    ROOMS = [
        {
            'name': 'econ101',
            'display_name': 'Econ 101 class',
            'participant_label_file': 'econ101.txt',
        },
        {
            'name': 'econ_lab',
            'display_name': 'Experimental Economics Lab',
            'participant_label_file': 'econ102.txt',
        },
    ]


Here are the available keys:

-   ``name``: (required) internal name
-   ``display_name``: (required) display name
-   ``participant_label_file``: a path to a text file with the "guest list"
    for this room.
    Path can be either absolute or relative to the project's root directory.
    Should have one participant label per line. For example::


        PC-1
        PC-2
        PC-3
        PC-4
        PC-5
        PC-6
        PC-7
        PC-8
        PC-9
        PC-10


-   ``use_secure_urls``: whether oTree should add unique secret keys to URLs,
    so that even if someone can guess another participant's ``participant_label``,
    they can't guess that person's start URL. If you use this option, then you must
    have a ``participant_label_file``, and you cannot use the room-wide link.

``ROOM_DEFAULTS`` is
a dict that defines settings to be inherited by all rooms unless
explicitly overridden (works in an analogous way to ``SESSION_CONFIG_DEFAULTS``).
