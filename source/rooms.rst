.. _rooms:

Rooms
=====

.. note::

    This is an upcoming feature. It is not ready for official use yet.

To create a room, add to your ``settings.py``
a setting ``ROOMS`` (and, optionally, ``ROOM_DEFAULTS``).

``ROOMS`` should be a list of dictionaries;
each dictionary defines the configuration of a room.

For example:

.. code-block:: python

    ROOM_DEFAULTS = {
        'use_secure_urls': True,
    }

    ROOMS = [
        {
            'name': 'ec101',
            'display_name': 'Econ 101',
            'participant_label_file': 'econ101.txt',
        },
        {
            'name': 'ec102',
            'display_name': 'Econ 102',
            'participant_label_file': 'econ102.txt',
        },
    ]


Here are the available keys:

-   ``name``: (required) internal name</li>
-   ``display_name``: (required) display name</li>
-   ``participant_label_file``: a path to a text file with the "guest list"
    for this room. Should have one participant label per line.
-   ``use_secure_urls``: whether oTree should add unique secret keys to URLs,
    so that even if someone can guess another participant's ``participant_label``,
    they can't guess that person's start URL.

``ROOM_DEFAULTS`` is
a dict that defines settings to be inherited by all rooms unless
explicitly overridden (works in an analogous way to ``SESSION_CONFIG_DEFAULTS``).
