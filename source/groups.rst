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
do this: ``players_per_group=[2,3]``; then, if you create a
session with 15 players, the group sizes will be ``2,3,2,3,2,3``.

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
in the group and subsession. For example, with 2-player groups you can
get the partner of a player, with this method on the ``Player``:

.. code-block:: python

    def get_partner(self):
        return self.get_others_in_group()[0]


.. _shuffling:

Shuffling groups
----------------

By default, in each round, players are split into groups of ``Constants.players_per_group``.
They are grouped sequentially -- for example, if there are 2 players per group,
then P1 and P2 would be grouped together, and so would P3 and P4, and so on.
``id_in_group`` is also assigned sequentially within each group.

This means that by default, the groups are the same in each round,
and even between apps that have the same ``players_per_group``.

(Note: to randomize participants to groups or roles, see :ref:`randomization`.)

A group has a method ``set_players`` that takes as an argument a list of
the players to assign to that group, in order. Alternatively, a
subsession has a method ``set_groups`` that takes as an argument a list
of lists, with each sublist representing a group.

For example, if you want players
to be reassigned to the same groups but to have roles randomly shuffled
around within their groups (e.g. so player 1 will either become player 2
or remain player 1), you would do this:

.. code-block:: python

    class Subsession(BaseSubsession):

        def before_session_starts(self):
            for group in self.get_groups():
                players = group.get_players()
                players.reverse()
                group.set_players(players)


.. _group_like_round:

If you shuffle the groups in one round
and would like the new group structure to be applied to another round,
you can use the ``group_like_round(n)`` method.
The argument to this method is the round number
whose group structure should be copied.

.. note::

    ``group_like_round()`` was introduced in oTree-core 0.4.15.
    In older versions, the group structure was automatically carried forward to future rounds.
    This behavior will soon be removed;
    instead you should use ``group_like_round`` to apply the grouping explicitly.

In the below example, the group structure in rounds 1 and 2 will be the default.
Round 3 has a different group structure, which is copied to rounds 4 and above.

.. code-block:: python

    class Subsession(BaseSubsession):

        def before_session_starts(self):
            if self.round_number == 3:
                # <some shuffling code here>
            if self.round_number > 3:
                self.group_like_round(3)


To check if your group shuffling worked correctly,
open your browser to the "Results" tab of your session,
and look at the ``group`` and ``id_in_group`` columns in each round.


Shuffling during the session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your experimental design may involve re-matching players based on the results
of a previous subsession. For example, you may want the highest-ranked players
in round 1 to play against each other in round 2.

You cannot accomplish this using ``before_session_starts``, because this method is run when the session is created,
before players begin playing.

Instead, you should make a ``WaitPage`` with ``wait_for_all_groups=True``
and put the shuffling code in ``after_all_players_arrive``. For example:

.. code-block:: python

    class ShuffleWaitPage(WaitPage):
        wait_for_all_groups = True

        def after_all_players_arrive(self):
            group_matrix = [g.get_players() for g in self.subsession.get_groups()]
            # ... some code to permute this matrix
            self.subsession.set_groups(group_matrix)

After this wait page, the players will be reassigned to their new groups.

Let's say you have a game with multiple rounds,
and in a wait page at the beginning you want to shuffle the groups,
and apply this new group structure to all rounds.

You can use ``group_like_round()`` in conjunction with the method ``in_rounds()``.
You should also use ``is_displayed()`` so that this method only executes once.
For example:

.. code-block:: python

    class ShuffleWaitPage(WaitPage):
        wait_for_all_groups = True

        def after_all_players_arrive(self):
            [...shuffle groups for round 1]
            for subsession in self.subsession.in_rounds(2, Constants.num_rounds):
                subsession.group_like_round(1)

        def is_displayed(self):
            return self.subsession.round_number == 1

Example: random shuffling (stranger)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class Subsession(BaseSubsession):

        def before_session_starts(self):
            players = self.get_players()
            random.shuffle(players)

            group_matrix = []

            # chunk into groups of Constants.players_per_group
            ppg = Constants.players_per_group
            for i in range(0, len(players), ppg):
                group_matrix.append(players[i:i+ppg])
            self.set_groups(group_matrix)


Example: re-matching by rank
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For example, let's say that in each round of an app, players get a numeric score for some task.
In the first round, players are matched randomly, but in the subsequent rounds,
you want players to be matched with players who got a similar score in the previous round.

First of all, at the end of each round, you should assign each player's score to ``participant.vars`` so that it can be easily
accessed in other rounds, e.g. ``self.player.participant.vars['score'] = 10``.

Then, you would define the following page and put it at the beginning of ``page_sequence``:

.. code-block:: python

    class ShuffleWaitPage(WaitPage):
        wait_for_all_groups = True

        # we can't shuffle at the beginning of round 1,
        # because the score has not been determined yet
        def is_displayed(self):
            return self.subsession.round_number > 1

        def after_all_players_arrive(self):

            # sort players by 'score'
            # see python docs on sorted() function
            sorted_players = sorted(
                self.subsession.get_players(),
                key=lambda player: player.participant.vars['score']
            )

            # chunk players into groups
            group_matrix = []
            ppg = Constants.players_per_group
            for i in range(0, len(sorted_players), ppg):
                group_matrix.append(sorted_players[i:i+ppg])

            # set new groups
            self.subsession.set_groups(group_matrix)


.. _complex_grouping_logic:

More complex grouping logic
---------------------------

If you need something more flexible or complex than what is allowed by
``players_per_group``, you can specify the grouping logic yourself in
``before_session_starts``, using the ``get_players()`` and ``set_groups()``
methods described above.

**Fixed number of groups with a divisible number of players**

For example, let's say you always want 8 groups, regardless of the number of
players in the session.
So, if there are *16 players*, you will have *2 players per group*,
and if there are *32 players*, you will have *4 players per group*.

You can accomplish this as follows:

.. code-block:: python

    class Constants(BaseConstants):
        players_per_group = None
        num_groups = 8
        ... # etc

    class Subsession(BaseSubsession):

           def before_session_starts(self):
            if self.round_number == 1:

                # create the base for number of groups
                num_players = len(self.get_players())
                players_per_group = [int(num_players/Constants.num_groups)] * Constants.num_groups

                # verify if all players are assigned
                idxg = 0
                while sum(players_per_group) < num_players:
                    players_per_group[idxg] += 1
                    idxg += 1

                # reassignment of groups
                list_of_lists = []
                players = self.get_players()
                for g_idx, g_size in enumerate(players_per_group):
                    offset = 0 if g_idx == 0 else sum(players_per_group[:g_idx])
                    limit = offset + g_size
                    group_players = players[offset:limit]
                    list_of_lists.append(group_players)
                self.set_groups(list_of_lists)
            else:
                self.group_like_round(1)

**Fixed number of groups with a no divisible number of players**

Lets make a more complex example based on the previous one. Let's say we need
to divide 20 players into 8 groups randomly. The problem is that
``20/8 = 2.5``.

So the more easy solution is to make the first *4 groups* with *3 players*, and
the last *4 groups* with only *2 players*.

.. code-block:: python

    class Constants(BaseConstants):
        players_per_group = None
        num_groups = 8
        ... # etc

    class Subsession(BaseSubsession):

        def before_session_starts(self):

            # if you whant to change the
            if self.round_number == 1:

                # extract and mix the players
                players = self.get_players()
                random.shuffle(players)

                # create the base for number of groups
                num_players = len(players)

                # create a list of how many players must be in every group
                # the result of this will be [2, 2, 2, 2, 2, 2, 2, 2]
                # obviously 2 * 8 = 16
                players_per_group = [int(num_players/Constants.num_groups)] * Constants.num_groups

                # add one player in order per group until the sum of size of
                # every group is equal to total of players
                idxg = 0
                while sum(players_per_group) < num_players:
                    players_per_group[idxg] += 1
                    idxg += 1
                    if idxg >= len(players_per_group):
                        idxg = 0

                # reassignment of groups
                list_of_lists = []
                for g_idx, g_size in enumerate(players_per_group):
                    # it is the first group the offset is 0 otherwise we start
                    # after all the players already exausted
                    offset = 0 if g_idx == 0 else sum(players_per_group[:g_idx])

                    # the asignation of this group end when we asign the total
                    # size of the group
                    limit = offset + g_size

                    # we select the player to add
                    group_players = players[offset:limit]
                    list_of_lists.append(group_players)
                self.set_groups(list_of_lists)
            else:
                self.group_like_round(1)

