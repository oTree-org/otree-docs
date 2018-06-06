.. _conceptual_overview:

Conceptual overview
===================

Sessions
--------

In oTree, a session is an event during which multiple participants take part in a series of tasks or games.
An example of a session would be:

"A number of participants will come to the lab and play a public goods game, followed by a
questionnaire. Participants get paid EUR 10.00 for showing up, plus their earnings from the
games."

Subsessions
-----------

A session is a series of subsessions;
subsessions are the "sections" or "modules" that constitute a session.
For example, if a session consists of a public goods game followed by a questionnaire,
the public goods game would be subsession 1, and the questionnaire would be subsession 2.
In turn, each subsession is a sequence of pages.
For example, if you had a 4-page public goods game followed by a 2-page questionnaire:

.. figure:: _static/diagrams/session_subsession.png
    :align: center

If a game is repeated for multiple rounds, each round is a subsession.

Groups
------

Each subsession can be further divided into groups of players;
for example, you could have a subsession with 30 players, divided into 15 groups of 2 players each.
(Note: groups can be shuffled between subsessions.)


Object hierarchy
----------------

oTree's entities can be arranged into the following hierarchy::

    Session
        Subsession
            Group
                Player
                    Page


- A session is a series of subsessions
- A subsession contains multiple groups
- A group contains multiple players
- Each player proceeds through multiple pages

.. _participants_and_players:

Participant
-----------

In oTree, the terms "player" and "participant" have distinct meanings.
The relationship between participant and player is the same as the
relationship between session and subsession:

.. figure:: _static/diagrams/participant_player.png
    :align: center

A player is an instance of a participant in one particular subsession.
A player is like a temporary "role" played by a participant.
A participant can be player 2 in the first subsession, player 1 in the
next subsession, etc.



.. _object_model:

What is "self"?
---------------

In Python, ``self`` is an instance of the class you're currently under.
If you are ever wondering what ``self`` means in a particular context,
scroll up until you see the name of the class.

For example, in this code, ``self`` is a player
(an instance of the ``Player`` class).

.. code-block:: python

    class Player(BasePlayer):

        def set_payoff(self):
            print('in set_payoff, self is:', self)
            self.payoff = 100

The name ``self`` is just shorter and more convenient than ``player``.

This is similar to how people don't use their own names when they talk about themselves; they just
use pronouns like "me", "myself", and "I". So, ``self`` is basically a pronoun.

Functions vs. attributes
------------------------

Classes have **attributes** and **functions**.

Here is an example of a page with an attribute:

.. code-block:: python

    class Results(Page):
        # this is an attribute
        timeout_seconds = 60

This means that this page has a time limit of 60 seconds.

But what if you want the time limit to be dynamic? Maybe it should depend
on the current round number, or on the player's performance so far.

To solve this, we need to make it a *function* of the current page,
like this:

.. code-block:: python

    class Results(Page):
        # this is a function
        def get_timeout_seconds(self):
            if self.round_number == 1:
                return 60
            else:
                return 30

First, let's look at the line ``def get_timeout_seconds(self):``.
The ``def`` means we are defining a function called ``get_timeout_seconds``.
It is a function, so it has input and output.
The input (i.e. the argument) is called ``self``, which is the current
*instance* of the page. What do we mean by "instance"?
Although the ``Results`` page will be viewed many times
by many players, ``self`` has specific properties about the current page view.
For example, ``self.round_number`` gives us the current round number,
``self.player`` gives us the player currently viewing the page,
and ``self.session`` gives us the session that is currently taking place.

In conclusion, if you define an *attribute*, then it will be same for all players.
If you want something to be different from player to player, you need to use
a *function* that takes a parameter ``self``.
Sometimes, oTree gives both options.
For example, oTree provides both the ``timeout_seconds`` attribute
(for simple pages with fixed time limits), and the ``get_timeout_seconds``
function (for complex pages with dynamic time limits).

Self: extended examples
-----------------------

What properties can you access through ``self``?

Here is a diagram of how you can refer to objects in the hierarchy within your code:

.. figure:: _static/diagrams/object_model_self.png
    :align: center

For example, if you are in a method on the ``Player`` class, you can
access the player's payoff with ``self.payoff`` (because ``self`` is the
player). But if you are inside a ``Page`` class in ``pages.py``, the
equivalent expression is ``self.player.payoff``,
which traverses the pointer from 'page' to 'player'.

Here are some code examples to illustrate:

in your ``models.py``

.. code-block:: python

    class Subsession(BaseSubsession):
        def example(self):

            # current subsession object
            self

            # parent objects
            self.session

            # child objects
            self.get_groups()
            self.get_players()

            # accessing previous Subsession objects
            self.in_previous_rounds()
            self.in_all_rounds()

    class Group(BaseGroup):
        def example(self):

            # current group object
            self

            # parent objects
            self.session
            self.subsession

            # child objects
            self.get_players()

    class Player(BasePlayer):

        def example(self):

            # current player object
            self

            # method you defined on the current object
            self.my_custom_method()

            # parent objects
            self.session
            self.subsession
            self.group
            self.participant

            self.session.config

            # accessing previous player objects
            self.in_previous_rounds()

            # equivalent to self.in_previous_rounds() + [self]
            self.in_all_rounds()

in your ``pages.py``

.. code-block:: python

    class MyPage(Page):
        def example(self):

            # current page object
            self

            # parent objects
            self.session
            self.subsession
            self.group
            self.player
            self.participant
            self.session.config


