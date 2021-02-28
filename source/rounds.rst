Apps & rounds
^^^^^^^^^^^^^

Apps
====

An oTree app is a folder containing Python and HTML code.
A project contains multiple apps.
A session is basically a sequence of apps that are played one after the other.

Combining apps
--------------

You can combine apps by setting your session config's ``app_sequence``.

Passing data between apps
-------------------------

See :ref:`participant fields <vars>` and :ref:`session fields <session_vars>`.


.. _rounds:

Rounds
======

You can make a game run for multiple rounds by setting ``Constants.num_rounds``.
For example, if your session config's ``app_sequence`` is ``['app1', 'app2']``,
where ``app1`` has ``num_rounds = 3`` and ``app2`` has ``num_rounds = 1``,
then your sessions will contain 4 subsessions.


Round numbers
-------------

You can get the current round number with ``player.round_number``
(this attribute is present on subsession, group, and player objects).
Round numbers start from 1.

.. _in_rounds:

Passing data between rounds or apps
-----------------------------------

Each round has separate subsession, ``Group``, and ``Player`` objects.
For example, let's say you set ``player.my_field = True`` in round 1.
In round 2, if you try to access ``player.my_field``,
you will find its value is ``None``.
This is because the ``Player`` objects
in round 1 are separate from ``Player`` objects in round 2.

To access data from a previous round or app,
you can use one of the techniques described below.

in_rounds, in_previous_rounds, in_round, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Player, group, and subsession objects have the following methods:

-   in_previous_rounds()
-   in_all_rounds()
-   in_rounds()
-   in_round()

For example, if you are in the last round of a 10-round game,
``player.in_previous_rounds()`` will return a list with 9 player objects,
which represent the current participant in all previous rounds.

``player.in_all_rounds()`` is almost the same but the list will have 10 objects,
because it includes the current round's player.

``player.in_rounds(m, n)`` returns a list of players representing the same participant from rounds ``m`` to ``n``.

``player.in_round(m)`` returns just the player in round ``m``.
For example, to get the player's payoff in the previous round,
you would do:

.. code-block:: python

    prev_player = player.in_round(player.round_number - 1)
    print(prev_player.payoff)

These methods work the same way for subsessions (e.g. ``subsession.in_all_rounds()``).

They also work the same way for groups, but it does not make sense to use them if you re-shuffle groups between rounds.

.. _vars:
.. _PARTICIPANT_FIELDS:

Participant fields
~~~~~~~~~~~~~~~~~~

.. note::

    As of March 2021, this is a new syntax for ``participant.vars``.
    Instead of setting ``participant.vars['my_field'] = 1``,
    you can now set ``participant.my_field = 1`` directly.
    Just make sure to define ``PARTICIPANT_FIELDS`` first.
    See `here <https://groups.google.com/g/otree/c/lbJg_ND5QkY>`__ for more info.

If you want to access a participant's data from a previous app,
you should store this data on the participant object,
which persists across apps (see :ref:`participants_and_players`).
(``in_all_rounds()`` only is useful when you need to access data from a previous
round of the same app.)

Go to settings and define ``PARTICIPANT_FIELDS``,
which is a list of the names of fields you want to define on your participant.

Then in your code, you can get and set any type of data on these fields:

.. code-block:: python

    participant.mylist = [1, 2, 3]

Internally, all participant fields are stored in a dict called ``participant.vars``.
``participant.xyz`` is equivalent to ``participant.vars['xyz']``

Participant fields are not included in the Excel/CSV data export,
or in the "Data" tab in the session admin. If you want that, you should either
use :ref:`custom-export` or save ``str(participant.vars)`` into a ``LongStringField``.
(The same concept applies for session fields.)

.. _session_vars:

Session fields
~~~~~~~~~~~~~~

.. note::

    This is a new feature; see the note above about ``PARTICIPANT_FIELDS``.

For global variables that are the same for all participants in the session,
add them to the ``SESSION_FIELDS``, which works the same as ``PARTICIPANT_FIELDS``.
Internally, all session fields are stored in ``session.vars``.

Variable number of rounds
-------------------------

If you want a variable number of rounds, consider using :ref:`live`.

Alternatively, you can set ``num_rounds`` to some high number, and then in your app, conditionally hide the
``{% next_button %}`` element, so that the user cannot proceed to the next
page, or use :ref:`app_after_this_page`. But note that having many rounds (e.g. more than 100)
might cause performance problems, so test your app carefully.
