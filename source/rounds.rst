Apps & rounds
^^^^^^^^^^^^^

Apps
====

An oTree app is a folder containing Python and HTML code.
A project contains multiple apps.
A session is basically a sequence of apps that are played one after the other.

Combining apps
--------------

You can combine apps by setting your session config's ``'app_sequence'``.

Passing data between apps
-------------------------

See :ref:`participant.vars <vars>` and :ref:`session.vars <session_vars>`.


.. _rounds:

Rounds
======

You can make a game run for multiple rounds by setting ``Constants.num_rounds``.
For example, if your session config's ``app_sequence`` is ``['app1', 'app2']``,
where ``app1`` has ``num_rounds = 3`` and ``app2`` has ``num_rounds = 1``,
then your sessions will contain 4 subsessions.


Round numbers
-------------

You can get the current round number with ``self.round_number``
(this attribute is present on subsession, group, player, and page objects).
Round numbers start from 1.

.. _in_rounds:

Passing data between rounds or apps
-----------------------------------

Each round has separate subsession, ``Group``, and ``Player`` objects.
For example, let's say you set ``self.player.my_field = True`` in round 1.
In round 2, if you try to access ``self.player.my_field``,
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
you would do ``self.player.in_round(self.round_number - 1).payoff``.

These methods work the same way for subsessions (e.g. ``self.subsession.in_all_rounds()``).

They also work the same way for groups, but it does not make sense to use them if you re-shuffle groups between rounds.

.. _vars:

participant.vars
----------------

If you want to access a participant's data from a previous app,
you should store this data on the participant object,
which persists across apps (see :ref:`participants_and_players`).
(``in_all_rounds()`` only is useful when you need to access data from a previous
round of the same app.)
Put it in ``participant.vars``, which is a dictionary that can store any data.
For example, you can set an attribute like this::

    self.participant.vars['blah'] = [1, 2, 3]

Later in the session (e.g. in a separate app),
you can retrieve it like this::

    # the below line gives [1, 2, 3]
    self.participant.vars['blah']
    # or try printing:
    print('vars is', self.participant.vars)

As described :ref:`here <object_model>`, the current participant can be
accessed from a ``Page`` or ``Player``:

.. code-block:: python

    class MyPage(Page):
        def before_next_page(self):
            self.participant.vars['foo'] = 1

.. code-block:: python

    class Player(BasePlayer):
        def some_method(self):
            self.participant.vars['foo'] = 1

You can also access it from ``Group`` or subsession, as long as you retrieve
a ``Player`` instance (e.g. using ``get_players()`` or ``get_player_by_id()``,
etc.).

.. code-block:: python

    class Subsession(BaseSubsession):
        def creating_session(self):
            for p in self.get_players():
                p.participant.vars['foo'] = 1

You can test if ``'my_var'`` exists with ``if 'my_var' in self.participant.vars:``.

``participant.vars`` is not included in the Excel/CSV data export,
or in the "Data" tab in the session admin. If you want that, you should either
use :ref:`custom-export` or save ``str(self.participant.vars)`` into a ``LongStringField``.
(The same concept applies for ``session.vars``.)

.. _session_vars:

session.vars
~~~~~~~~~~~~

For global variables that are the same for all participants in the session,
you can use ``self.session.vars``.
This is a dictionary just like ``participant.vars``. The difference is that
if you set a variable in ``self.session.vars``, it will apply
to all participants in the session, not just one.

As described :ref:`here <object_model>`, the ``session`` object can be
accessed from a ``Page`` object or any of the models (``Player``, ``Group``,
``Subsession``, etc.).



Variable number of rounds
-------------------------

If you want a variable number of rounds, consider using :ref:`live`.

Alternatively, you can set ``num_rounds`` to some high number, and then in your app, conditionally hide the
``{% next_button %}`` element, so that the user cannot proceed to the next
page, or use :ref:`app_after_this_page`. But note that having many rounds (e.g. more than 100)
might cause performance problems, so test your app carefully.
