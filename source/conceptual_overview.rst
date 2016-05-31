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
In turn, each subsession is a sequence of pages the user must navigate through.
For example, if you had a 4-page public goods game followed by a 2-page questionnaire:

.. figure:: _static/diagrams/session_subsession.png
    :align: center

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
next subsession, and so on. Following on the above example,
the participant would be represented as 2 different players:

.. _object_model:

What is "self"?
---------------

In Python, ``self`` refers to the object whose class you are
currently in. If you are ever wondering what ``self`` means in a particular context,
scroll up until you see the name of the class.

In the below example, ``self`` refers to a ``Player`` object:

.. code-block:: python

    class Player(object):

        def my_method(self):
            return self.my_field

In the next example, however, ``self`` refers to a ``Group`` object:

.. code-block:: python

    class Group(object):

        def my_method(self):
            return self.my_field


``self`` is conceptually similar to the word "me". You refer to yourself
as "me", but others refer to you by your name. And when your friend says
the word "me", it has a different meaning from when you say the word
"me".

Here is a diagram of how you can refer to objects in the hierarchy within your code:

.. figure:: _static/diagrams/object_model_self.png
    :align: center


For example, if you are in a method on the ``Player`` class, you can
access the player's payoff with ``self.payoff`` (because ``self`` is the
player). But if you are inside a ``Page`` class in ``views.py``, the
equivalent expression is ``self.player.payoff``,
which traverses the pointer from 'page' to 'player'.

Self: extended examples
-----------------------

Here are some code examples to illustrate:

.. code-block:: python

    class Session(...) # this class is defined in oTree-core
        def example(self):

            # current session object
            self

            self.config

            # child objects
            self.get_subsessions()
            self.get_participants()

    class Participant(...) # this class is defined in oTree-core
        def example(self):

            # current participant object
            self

            # parent objects
            self.session

            # child objects
            self.get_players()

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

in your ``views.py``

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



