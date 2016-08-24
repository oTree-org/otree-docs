.. _rounds:

Rounds
======

In oTree, "rounds" and "subsessions" are almost synonymous. The difference is
that "rounds" refers to a sequence of subsessions that are in the same app.
So, a session that consists of a prisoner's dilemma iterated 3 times, followed
by an exit questionnaire, has 4 subsessions, which consists of 3 rounds of the
prisoner's dilemma, and 1 round of the questionnaire.


Round numbers
-------------

You can specify how many rounds a game should be played in models.py, in
``Constants.num_rounds``.

Subsession objects have an attribute ``round_number``, which contains the
current round number, starting from 1.

.. _in_rounds:

Passing data between rounds or apps
-----------------------------------

Each round has separate ``Subsession``, ``Group``, and ``Player`` objects.
For example, let's say you set ``self.player.my_field = True`` in round 1.
In round 2, if you try to access ``self.player.my_field``, you will find its value is ``None``
(assuming that is the default value of the field). This is because the ``Player`` objects
in round 1 are separate from ``Player`` objects in round 2.

To access data from a previous round or app,
you can use one of the techniques described below.

in_rounds, in_previous_rounds, in_round, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Player, group, and subsession objects have the following methods, which work
similarly:

-   in_previous_rounds()
-   in_all_rounds()
-   in_rounds()
-   in_round()

``player.in_previous_rounds()`` and ``player.in_all_rounds()``
each return a list of players representing the same participant in
previous rounds of the same app. The difference is that ``in_all_rounds()``
includes the current round's player.

For example, if you wanted to calculate a participant's payoff for all previous
rounds of a game, plus the current one:

.. code-block:: python

    cumulative_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

``player.in_rounds(m, n)`` returns a list of players representing the same participant from rounds ``m`` to ``n``.
``player.in_round(m)`` returns just the player in round ``m``.

Similarly, subsession objects have methods ``in_previous_rounds()``,
``in_all_rounds()``, ``in_rounds(m,n)`` and ``in_round(m)`` that work the same way.

Group objects also have methods ``in_previous_rounds()``, ``in_all_rounds()``, ``in_rounds(m,n)`` and ``in_round(m)``,
but note that if you re-shuffle groups between rounds,
then these methods may not return anything meaningful (their behavior in this
situation is unspecified).

.. _vars:

participant.vars
----------------

``in_all_rounds()`` only is useful when you need to access data from a previous
round of the same app.
If you want to pass data between subsessions of different app types (e.g. the
participant is in the questionnaire and needs to see data from their ultimatum
game results),
you should store this data in the participant object, which persists across
subsessions. Each participant has a field called ``vars``, which is a
dictionary that can store any data about the player. For example, if you ask
the participant's name in one subsession and you need to access it later, you
would store it like this::

    self.participant.vars['first name'] = 'John'

Then in a future subsession, you would retrieve this value like this::

    self.participant.vars['first name'] # returns 'John'

As described :ref:`here <object_model>`, the ``participant`` object can be
accessed from a ``Page`` object or ``Player`` object.

This means you can access it from ``views.py``:

.. code-block:: python

    # in views.py
    class MyPage(Page):
        def before_next_page(self):
            self.participant.vars['foo'] = 1

Or in the ``Player`` class in ``models.py``:

.. code-block:: python

    class Player(BasePlayer):
        def some_method(self):
            self.participant.vars['foo'] = 1

You can also access it from ``Group`` or ``Subsession``, as long as you retrieve
a ``Player`` instance (e.g. using ``get_players()`` or ``get_player_by_role()``,
etc.).

.. code-block:: python

    class Group(BaseGroup):
        def some_method(self):
            for p in self.get_players():
                p.participant.vars['foo'] = 1


.. _session_vars:

Global variables
----------------

For session-wide globals, you can use ``self.session.vars``.

This is a dictionary just like ``participant.vars``.

As described :ref:`here <object_model>`, the ``session`` object can be
accessed from a ``Page`` object or any of the models (``Player``, ``Group``,
``Subsession``, etc.).


Variable number of rounds
-------------------------

If you want a variable number of rounds, consider setting ``num_rounds``
to some high number, and then in your app, conditionally hide the
``{% next_button %}`` element, so that the user cannot proceed to the next
page.
