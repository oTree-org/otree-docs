.. _groups:

Groups and multiplayer games
============================

To create a multiplayer game, go to your app's models.py and set
``Constants.players_per_group``. For example, in a 2-player game like an
ultimatum game or prisoner's dilemma, you would set this to 2. If your
app does not involve dividing the players into multiple groups, then set
it to ``None``. e.g. it is a single-player game or a game where
everybody in the subsession interacts together as 1 group. In this case,
``self.group.get_players()`` will return everybody in the subsession. If
you need your groups to have uneven sizes (for example, 2 vs 3), you can
do this: ``players_per_group=[2,3]``; in this case, if you have a
session with 15 players, the group sizes would be ``[2,3,2,3,2,3]``.

Each player has an attribute ``id_in_group``, which is an integer,
which will tell you if it is player 1, player 2, etc.

Group objects have the following methods:

-  ``get_players()``: returns a list of the players in the group.
-  ``get_player_by_id(n)``: Retrieves the player in the group with a
   specific ``id_in_group``.
-  ``get_player_by_role(r)``. The argument to this method is a string
   that looks up the player by their role value. (If you use this
   method, you must define the ``role`` method on the player model,
   which should return a string that depends on ``id_in_group``.)

Player objects have methods ``get_others_in_group()`` and
``get_others_in_subsession()`` that return a list of the other players
in the group and subsession, respectively.

Wait pages
----------

Wait pages are necessary when one or more players need to wait for
another player to take some action before they can proceed. For example,
in an ultimatum game, player 2 cannot accept or reject before they have
seen player 1's offer.

Wait pages are defined in views.py. If you have a wait page in your
sequence of pages, then oTree waits until all players in the group have
arrived at that point in the sequence, and then all players are allowed
to proceed.

If your subsession has multiple groups playing simultaneously, and you
would like a wait page that waits for all groups (i.e. all players in
the subsession), you can set the attribute
``wait_for_all_groups = True`` on the wait page.

Wait pages can define the following methods:

-  ``def after_all_players_arrive(self)``

This code will be executed once all players have arrived at the wait
page. For example, this method can determine the winner of an auction
and set each player's payoff.

-  ``def title_text(self)``

The text in the title of the wait page.

-  ``def body_text(self)``

The text in the body of the wait page

Group re-matching between rounds
--------------------------------

For the first round, the players are split into groups of
``Constants.players_per_group``. This matching is random, unless you
have set ``group_by_arrival_time`` set in your session type in
settings.py, in which case players are grouped in the order they start
the first round.

In subsequent rounds, by default, the groups chosen are kept the same.
If you would like to change this, you can define the grouping logic in
``Subsession.before_session_starts``. For example, if you want players
to be reassigned to the same groups but to have roles randomly shuffled
around within their groups (e.g. so player 1 will either become player 2
or remain player 1), you would do this:

.. code:: python

    def before_session_starts(self):
        for group in self.get_groups():
            players = group.get_players()
            players.reverse()
            group.set_players(players)

A group has a method ``set_players`` that takes as an argument a list of
the players to assign to that group, in order. Alternatively, a
subsession has a method ``set_groups`` that takes as an argument a list
of lists, with each sublist representing a group. You can use this to
rearrange groups between rounds, but note that the
``before_session_starts`` method is run when the session is created,
before players begin playing. Therefore you cannot use this method to
shuffle players depending on the results of previous rounds (there is a
separate technique for doing this which will be added to the
documentation in the future).
