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

Accessing data from previous rounds
-----------------------------------

Each round has separate ``Subsession``, ``Group``, and ``Player`` objects.
For example, let's say you set ``self.player.my_field = True`` in round 1.
In round 2, if you try to access ``self.player.my_field``, you will find its value is ``None``
(assuming that is the default value of the field). This is because the ``Player`` objects
in round 1 are separate from ``Player`` objects in round 2.

To access data from a previous round, you can use the methods ``in_previous_rounds()`` and ``in_all_rounds()``
on player, group, and subsession objects.

``player.in_previous_rounds()`` and ``player.in_all_rounds()``
each return a list of players representing the same participant in
previous rounds of the same app. The difference is that ``in_all_rounds()``
includes the current round's player.

For example, if you wanted to calculate a participant's payoff for all previous
rounds of a game, plus the current one:

.. code-block:: python

    cumulative_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

Similarly, subsession objects have methods ``in_previous_rounds()`` and
``in_all_rounds()`` that work the same way.

Group objects also have ``in_previous_rounds()`` and ``in_all_rounds()``
methods, but note that if you re-shuffle groups between rounds,
then these methods may not return anything meaningful (their behavior in this
situation is unspecified).

.. note::

    ``Group.in_all_rounds()`` and ``Group.in_previous_rounds()`` were added in otree-core 0.3.8

.. _vars:

Accessing data from previous subsessions in different apps
----------------------------------------------------------

``in_all_rounds()`` only is useful when you need to access data from a previous
round of the same app.
If you want to pass data between subsessions of different app types (e.g. the
participant is in the questionnaire and needs to see data from their ultimatum
game results),
you should store this data in the participant object, which persists across
subsessions. Each participant has a field called ``vars``, which is a
dictionary that can store any data about the player. For example, if you ask
the participant's name in one subsession and you need to access it later, you
would store it like this:

``self.player.participant.vars['first name'] = 'John'``

Then in a future subsession, you would retrieve this value like this:

``self.player.participant.vars['first name']`` # returns 'John'

Global variables
----------------

For session-wide globals, you can use ``self.session.vars``.

This is a dictionary just like ``participant.vars``.

Variable number of rounds
-------------------------

If you want a variable number of rounds, consider setting ``num_rounds``
to some high number, and then in your app, conditionally hide the
``{% next_button %}`` element, so that the user cannot proceed to the next
page.
