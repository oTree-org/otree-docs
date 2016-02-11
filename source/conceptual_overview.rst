Conceptual overview
===================

Sessions
--------

In oTree, a session is an event during which participants take part in oTree
experiments. An example of a session would be:

"A number of participants will come to the lab and will play an ultimatum game, followed by a
questionnaire. Participants get paid EUR 10.00 for showing up, plus their earnings from the
games."

Subsessions
-----------

A session is a series of subsessions;
subsessions are the "sections" or "modules" that constitute a session.
For example, if a session consists of a public goods game followed by a questionnaire,
the public goods game would be subsession 1, and the questionnaire would be subsession 2.
In turn, each subsession is a sequence of pages the user must navigate through.
For example, To illustrate, if you had a 4-page public goods game followed by a 2-page questionnaire:


.. figure:: _static/diagrams/session_subsession.png
    :align: center

In oTree, the terms "player" and "participant" have distinct meanings.
The relationship between participant and player is the same as the
relationship between session and subsession.

A player is an instance of a participant in one particular subsession.
A player is like a temporary "role" played by a participant.
A participant can be player 2 in the first subsession, player 1 in the
next subsession, and so on. Following on the above example,
the participant would be represented as 2 different players:

.. figure:: _static/diagrams/session_subsession.png
    :align: center

Groups
------

Each subsession can be further divided into groups of players;
for example, the trust game subsession would have 15 groups of 2 players each.
(Note: groups can be shuffled between subsessions.)

Object hierarchy
----------------

    Session
        Subsession
            Group
                Player
                    Page

A player is part of a group, which is part of a subsession, which is part of a session.



Session configs
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
        'app_sequence':['my_app_1', 'my_app_2'],
    },



This session config is composed of 3 apps:

-  Trust game
-  Ultimatum game
-  Questionnaire

Note that you can reuse apps (such as the ``questionnaire`` app) in multiple
session configs.

Once you have defined a session config, you can run the server,
open your browser to the admin interface, and create a new session.
You would select "My Session Config" as the configuration to use,
and then enter "30" for the number of participants.

An instance of a session would be created, and you would get the start links to
distribute to your participants.

In this example, the session would contain 4 "subsessions":

-  Trust game
-  Ultimatum game [Round 1]
-  Ultimatum game [Round 2]
-  Questionnaire



.. _participants_and_players:


*Self* and object model
=======================

In oTree code, you will see the variable ``self`` in many places.
In Python, ``self`` refers to the object whose class you are
currently in.

For example, in this example, ``self`` refers to a ``Player`` object:

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

oTree's different objects are all connected, as illustrated by this
diagram.


.. figure:: _static/diagrams/object_model_self.png
    :align: center


Player, group, subsession, and session are in a simple hierarchy,
'session' being at the top and 'player' being at the bottom. Then, the
'page' has an pointer to all 4 of these objects.

For example, if you are in a method on the ``Player`` class, you can
access the player's payoff with ``self.payoff`` (because ``self`` is the
player). But if you are inside a ``Page`` class in ``views.py``, the
equivalent expression is ``self.player.payoff``,
which traverses the pointer from 'page' to 'player'.

Here are some code examples to illustrate:

.. code-block:: python

    class Session(...) # this class is defined in oTree-core
        def example(self):

            # current session object
            self

            # parent objects
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

            # example of chaining lookups
            self.player.participant
            self.session.config

You can follow pointers in a transitive manner. For example, if you are
in the Page class, you can access the participant as
``self.player.participant``. If you are in the Player class, you can
access the session config as ``self.session.config``.


