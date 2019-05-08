.. _rooms:

Rooms
=====

oTree lets you configure "rooms", which provide:

-   Persistent links that you can assign to participants or workstations,
    which stay constant across sessions
-   A "waiting room" that lets you see how many people are waiting to start a session,
    so that you can create a session with the right number of people.
    Also, you can see a listing of who specifically is waiting, and who has not joined yet.
-   Short links that are easy for participants to type, good for quick live demos.

Here is a screenshot:

.. figure:: _static/admin/room-combined.png
    :align: center

Creating rooms
--------------

You can create multiple rooms -- say, for for different classes you teach,
or different labs you manage.

To create a room, add to your ``settings.py``
a setting ``ROOMS`` (and, optionally, ``ROOM_DEFAULTS``).

``ROOMS`` should be a list of dictionaries;
each dictionary defines the configuration of a room.

For example:

.. code-block:: python

    ROOM_DEFAULTS = {}

    ROOMS = [
        {
            'name': 'econ101',
            'display_name': 'Econ 101 class',
            'participant_label_file': '_rooms/econ101.txt',
        },
        {
            'name': 'econ_lab',
            'display_name': 'Experimental Economics Lab',
        },
    ]

``ROOM_DEFAULTS`` is
a dict that defines settings to be inherited by all rooms unless
explicitly overridden (works in an analogous way to ``SESSION_CONFIG_DEFAULTS``).

Here are the available properties:

name and display_name (required)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The internal name and display name, respectively.

participant_label_file (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A path to a text file with the "guest list"
for this room.
Path can be either absolute or relative to the project's root folder.
The file should contain one participant label per line. For example::

        PC_1
        PC_2
        PC_3
        PC_4
        PC_5
        PC_6
        PC_7
        PC_8
        PC_9
        PC_10

If you omit ``participant_label_file``, then anyone can join
as long as they know the room-wide URL.
See :ref:`no-participant-labels`.

use_secure_urls (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~

This setting provides an extra layer of security on top of the ``participant_label_file``.
For example, if you are not using secure URLs, your start URLs would look something
like this::

    http://localhost:8000/room/econ101/?participant_label=Student1
    http://localhost:8000/room/econ101/?participant_label=Student2

The issue is that if Student1 is mischievous,
he might change his URL's participant_label from "Student1" to "Student2",
so that he can impersonate playing as Student2.
However, if you set ``'use_secure_urls': True,``
oTree will add a unique secret key to each participant's URLs,
like this::

    http://localhost:8000/room/econ101/?participant_label=Student1&hash=29cd655f
    http://localhost:8000/room/econ101/?participant_label=Student2&hash=46d9f31d

So, even if someone can guess another participant's ``participant_label``,
they won't be able to open that person's start URL without the secret hash code.


Using rooms
-----------

In the admin interface, click "Rooms" in the header bar,
and click the room you created.
Scroll down to the section with the participant URLs.

If you have a participant_label_file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Have each participant open the URLs.
Then, in the room's admin page, check how many people are present,
and create a session for that number of people.

You can either use the
room-wide URL, or the participant-specific URLs.

The participant-specific URLs already contain the participant label, so as soon as
they are clicked, the participant will go straight to the waiting page.
For example, one participant can open URL ``http://localhost:8000/room/econ101/?participant_label=Student1``,
and another participant can open URL ``http://localhost:8000/room/econ101/?participant_label=Student2``.

Or, you can give both students the room-wide URL, which does not contain ``participant_label``:

    http://localhost:8000/room/econ101/

When a user clicks the room-wide URL,
they are prompted to enter their participant label:

.. figure:: _static/admin/room-combined.png
    :align: center

For example, if a participant enters their label as ``Student1``,
oTree simply appends the participant label to the room-wide URL, e.g.,
``http://localhost:8000/room/econ101/?participant_label=Student1``,
checks if the label is contained in the participant label file,
and if so, redirects the participant to the wait page.


.. note::
otr
    Some language translations are currently missing, in which case it will
    be shown in English. You can fix that by contributing a translation
    `here <https://github.com/oTree-org/otree-internationalization>`__.

.. _no-participant-labels:

If you don't have a participant_label_file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting is simple; just have each participant open the room-wide URL.
Have each participant open the URLs.
Then, in the room's admin page, check how many people are present,
and create a session for that number of people.

Although this option is simple, it is less reliable than using participant labels,
because someone could play twice by opening the URL in 2 different browsers.


Reusing for multiple sessions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Room URLs are designed to be reused across sessions.
In a lab, you can set the room URL (either room-wide or participant-specific)
as the browser's home page.

In classroom experiments, you can give each student the room-wide URL they can use
repeatedly during the semester.

What if not all participants show up?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're doing a lab experiment and the number of participants is unpredictable,
you can consider using the room-wide URL, and asking participants to manually enter their
participant label when they sit down at their computer.

That way, computers will only be counted as "active" if a participant is actually present.
Computers with no participants will remain on the "Enter participant label" page,
and will not be counted as present.

Alternatively, you can open each computer's browser to a participant-specific URLs,
but before creating the session, be sure to close the browsers on unattended computers,
so they are not included in the session.
