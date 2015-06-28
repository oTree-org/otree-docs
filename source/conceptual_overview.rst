Conceptual overview
===================

Sessions
--------

In oTree, a session is an event during which participants take part in oTree
experiments. An example of a session would be:

"A number of participants will come to the lab and will play trust games
(in groups of 2), followed by 2 rounds of ultimatum games, followed by a
questionnaire.
Participants get paid EUR 10.00 for showing up, plus their earnings from the
games."

To configure a session like this, you would go to ``settings.py`` and
define a "session type", which is a reusable configuration.
This lets you create multiple sessions, all with the same properties.

 Add an entry to ``SESSION_TYPES`` like this:

.. code-block:: python

    {
        'name': 'my_session_type',
        'display_name': 'My Session Type',
        'participation_fee': 10.00,
        'app_sequence':['trust', 'ultimatum', 'questionnaire'],
    }

This session type is composed of 3 apps:

-  Trust game
-  Ultimatum game
-  Questionnaire

Note that you can reuse apps (such as the ``questionnaire`` app) in multiple
session types.

Once you have defined a session type, you can run the server,
open your browser to the admin interface, and create a new session.
You would select "My Session Type" as the type for the session,
and then enter "30" for the number of participants.

An instance of a session would be created, and you would get the start links to
distribute to your participants.

In this example, the session would contain 4 "subsessions":

-  Trust game
-  Ultimatum game [Round 1]
-  Ultimatum game [Round 2]
-  Questionnaire

Each subsession can be further divided into groups of players;
for example, the trust game subsession would have 15 groups of 2 players each.
(Note: groups can be shuffled between subsessions.)

Participants and players
------------------------

In oTree, the terms "player" and "participant" have distinct meanings.
The distinction between a participant and a player is the same as the
distinction between a session and a subsession.

A participant is a person who takes part in a session. The participant
object contains properties such as the participant's name, how much
they made in the session, and what their progress is in the session.

A player is an instance of a participant in one particular subsession. A
participant can be player 1 in the first subsession, player 5 in the
next subsession, and so on.
