Conceptual overview
===================

Sessions and subsessions
------------------------

In oTree, the top-level concept is a "Session". This term refers to an
event where a group of people spend time taking part in oTree
experiments. An example of a session would be:

"On Tuesday at 3PM, 30 people will come to the lab for 1 hour, during
which time they will play a trust game, followed by 2 rounds of an
ultimatum game, followed by a questionnaire. Participants get paid EUR
10.00 for showing up, plus their payoffs they earn playing the games."

A session can be broken down into what oTree calls "subsessions". These
are interchangeable units or modules that come one after another. Each
subsession has a sequence of one or more pages the player must interact
with. The session in the above example had 4 subsessions:

-  Trust game
-  Ultimatum game 1
-  Ultimatum game 2
-  Questionnaire

Each subsession is defined in an oTree app. The above session would
require 3 distinct apps to be coded:

-  Trust game
-  Ultimatum game
-  Questionnaire

You can define your session's properties in ``SESSION_TYPES`` in
``settings.py``. Here are the parameters for the above example:

.. code:: python

    {
        'name':'my_session',
        'participation_fee':10.00,
        'app_sequence':['trust', 'ultimatum', 'questionnaire'],
    }

``app_sequence`` allows you to have a session that consists of multiple
apps. For example, the questionnaire is a separate standalone app,
rather than being part of the ``ultimatum`` app. The advantage of this
is that you can reuse the same questionnaire app in different session
types, simply by adding it to the end of ``app_sequence``.

Participants and players
------------------------

In oTree, the terms "player" and "participant" have distinct meanings.
The distinction between a participant and a player is the same as the
distinction between a session and a subsession.

A participant is a person who takes part in a session. The participant
data model contains properties such as the participant's name, how much
they made in the session, and what their progress is in the session.

A player is an instance of a participant in one particular subsession. A
participant can be player 1 in the first subsession, player 5 in the
next subsession, and so on.
