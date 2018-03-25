.. _groups:

Groups
======

oTree's group system lets you divide players into groups
and have players interact with others in the same group.
This is often used in multiplayer games.
(If you just need groups in the sense of "treatment groups",
where players don't actually interact with each other,
then see :ref:`treatments`.)

To set the group size, go to your app's models.py and set
``Constants.players_per_group``. For example, for a 2-player game:

.. code-block:: python

    class Constants(BaseConstants):
        # ...
        players_per_group = 2

If all players should be in the same group,
or if it's a single-player game, set it to ``None``:

.. code-block:: python

    class Constants(BaseConstants):
        # ...
        players_per_group = None

In this case, ``self.group.get_players()`` will return everybody in the subsession.

Each player has an attribute ``id_in_group``,
which will tell you if it is player ``1``, player ``2``, etc.

Getting players
---------------

Group objects have the following methods:

get_players()
~~~~~~~~~~~~~

Returns a list of the players in the group (ordered by ``id_in_group``).

get_player_by_id(n)
~~~~~~~~~~~~~~~~~~~

Returns the player in the group with the given ``id_in_group``.

get_player_by_role(r)
~~~~~~~~~~~~~~~~~~~~~

Returns the player with the given role.
If you use this method, you must define the :ref:`role <role>` method.
For example:

.. code-block:: python

    class Group(BaseGroup):
        def set_payoff(self):
            buyer = self.get_player_by_role('buyer')
            print(buyer.decision)
            # etc ...


    class Player(BasePlayer):
        decision = models.BooleanField()

        def role(self):
            if self.id_in_group == 1:
                return 'buyer'
            else:
                return 'seller'


Getting other players
---------------------

Player objects have methods ``get_others_in_group()`` and
``get_others_in_subsession()`` that return a list of the other players
in the group and subsession. For example, with 2-player groups you can
get the partner of a player:

.. code-block:: python

    class Player(BasePlayer):

        def get_partner(self):
            return self.get_others_in_group()[0]


Chat between participants
-------------------------

See the `participant chat add-on <https://github.com/oTree-org/otreechat>`__.


.. _shuffling:

Group matching
--------------

.. _fixed_matching:

Fixed matching
~~~~~~~~~~~~~~

By default, in each round, players are split into groups of ``Constants.players_per_group``.
They are grouped sequentially -- for example, if there are 2 players per group,
then P1 and P2 would be grouped together, and so would P3 and P4, and so on.
``id_in_group`` is also assigned sequentially within each group.

This means that by default, the groups are the same in each round,
and even between apps that have the same ``players_per_group``.

If you want to rearrange groups, you can use the below techniques.

group_randomly()
~~~~~~~~~~~~~~~~

Subsessions have a method ``group_randomly()`` that shuffles players randomly,
so they can end up in any group, and any position within the group.

If you would like to shuffle players between groups but keep players in fixed roles,
use ``group_randomly(fixed_id_in_group=True)``.

For example, this will group players randomly each round:

.. code-block:: python

    class Subsession(BaseSubsession):
        def creating_session(self):
            self.group_randomly()

This will group players randomly each round, but keep ``id_in_group`` fixed:

.. code-block:: python

    class Subsession(BaseSubsession):
        def creating_session(self):
            self.group_randomly(fixed_id_in_group=True)

The below example uses the command line to create a public goods game with 12 players,
and then does interactive group shuffling in ``otree shell``.
Assume that ``players_per_group = 3``, so that a 12-player game would have 4 groups::

    C:\oTree> otree resetdb --noinput
    C:\oTree> otree create_session public_goods 12
    C:\oTree> otree shell
    Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]

    # this line is only necessary if using otree shell
    >>> from public_goods.models import Subsession

    # this line is only necessary if using otree shell
    >>> self=Subsession.objects.first()

    # by default, oTree groups players sequentially
    >>> self.get_group_matrix()

    [[<Player  1>, <Player  2>, <Player  3>],
     [<Player  4>, <Player  5>, <Player  6>],
     [<Player  7>, <Player  8>, <Player  9>],
     [<Player 10>, <Player 11>, <Player 12>]]

    >>> self.group_randomly(fixed_id_in_group=True)
    >>> self.get_group_matrix()

    [[<Player  1>, <Player  8>, <Player 12>],
     [<Player 10>, <Player  5>, <Player  3>],
     [<Player  4>, <Player  2>, <Player  6>],
     [<Player  7>, <Player 11>, <Player  9>]]

    >>> self.group_randomly()
    >>> self.get_group_matrix()

    [[<Player  8>, <Player 10>, <Player  3>],
     [<Player  4>, <Player 11>, <Player  2>],
     [<Player  9>, <Player  1>, <Player  6>],
     [<Player 12>, <Player  5>, <Player  7>]]

Note that in each round,
players are initially grouped sequentially as described in :ref:`fixed_matching`,
even if you did some shuffling in a previous round.
To counteract this, you can use :ref:`group_like_round`.

.. _group_like_round:

group_like_round()
~~~~~~~~~~~~~~~~~~

To copy the group structure from one round to another round,
use the ``group_like_round(n)`` method.
The argument to this method is the round number
whose group structure should be copied.

In the below example, the groups are shuffled in round 1,
and then subsequent rounds copy round 1's grouping structure.

.. code-block:: python

    class Subsession(BaseSubsession):

        def creating_session(self):
            if self.round_number == 1:
                # <some shuffling code here>
            else:
                self.group_like_round(1)


get_group_matrix()
~~~~~~~~~~~~~~~~~~

Subsessions have a method called ``get_group_matrix()`` that
return the structure of groups as a matrix, i.e. a list of lists,
with each sublist being the players in a group, ordered by ``id_in_group``.

The following lines are equivalent.

.. code-block:: python

    matrix = self.get_group_matrix()
    # === is equivalent to ===
    matrix = [group.get_players() for group in self.get_groups()]


.. _set_group_matrix:

set_group_matrix()
~~~~~~~~~~~~~~~~~~

``set_group_matrix()`` lets you modify the group structure in any way you want.
First, get the list of players with ``get_players()``, or the pre-existing
group matrix with ``get_group_matrix()``.
Construct your matrix using Python list operations like
``.extend()``, ``.append()``, ``.pop()``, ``.reverse()``,
and list indexing and slicing (e.g. ``[0]``, ``[2:4]``).
Then pass this modified matrix to ``set_group_matrix()``::

    >>> matrix = s.get_group_matrix()
    >>> matrix

    [[<Player  8>, <Player 10>, <Player  3>],
     [<Player  4>, <Player 11>, <Player  2>],
     [<Player  9>, <Player  1>, <Player  6>],
     [<Player 12>, <Player  5>, <Player  7>]]

    >>> for group in matrix:
       ....:     group.reverse()
       ....:
    >>> matrix

    [[<Player  3>, <Player 10>, <Player  8>],
     [<Player  2>, <Player 11>, <Player  4>],
     [<Player  6>, <Player  1>, <Player  9>],
     [<Player  7>, <Player  5>, <Player 12>]]

    >>> self.set_group_matrix(matrix)
    >>> self.get_group_matrix()

    [[<Player  3>, <Player 10>, <Player  8>],
     [<Player  2>, <Player 11>, <Player  4>],
     [<Player  6>, <Player  1>, <Player  9>],
     [<Player  7>, <Player  5>, <Player 12>]]

Here is how this would look in ``creating_session``:

.. code-block:: python

    class Subsession(BaseSubsession):
        def creating_session(self):
            matrix = self.get_group_matrix()
            for row in matrix:
                row.reverse()
            self.set_group_matrix(matrix)

You can also pass a matrix of integers.
It must contain all integers from 1 to the number of players
in the subsession. Each integer represents the player who has that ``id_in_subsession``.
For example::

    >>> new_structure = [[1,3,5], [7,9,11], [2,4,6], [8,10,12]]
    >>> self.set_group_matrix(new_structure)
    >>> self.get_group_matrix()

    [[<Player  1>, <Player  3>, <Player  5>],
     [<Player  7>, <Player  9>, <Player 11>],
     [<Player  2>, <Player  4>, <Player  6>],
     [<Player  8>, <Player 10>, <Player 12>]]

You can even use ``set_group_matrix`` to make groups of uneven sizes.

To check if your group shuffling worked correctly,
open your browser to the "Results" tab of your session,
and look at the ``group`` and ``id_in_group`` columns in each round.

group.set_players()
~~~~~~~~~~~~~~~~~~~

If you just want to rearrange players within a group, you can use
the method on ``group.set_players()`` that takes as an argument a list of
the players to assign to that group, in order.

For example, if you want players
to be reassigned to the same groups but to have roles randomly shuffled
around within their groups (e.g. so player 1 will either become player 2
or remain player 1), you would do this:

.. code-block:: python

    class Subsession(BaseSubsession):

        def creating_session(self):
            for group in self.get_groups():
                players = group.get_players()
                players.reverse()
                group.set_players(players)


Example: assigning players to roles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you want to assign players to roles based on some external criterion,
like their gender.

This example shows how to make groups of 3 players, where player 1 is male, and players 2 & 3 are female.
The example assumes that you already set ``participant.vars['gender']``
on each participant (e.g. in a previous app),
and that there are twice as many female players as male players.

.. code-block:: python


    class Subsession(BaseSubsession):
        def creating_session(self):

            if self.round_number == 1:
                players = self.get_players()

                M_players = [p for p in players if p.participant.vars['gender'] == 'M']
                F_players = [p for p in players if p.participant.vars['gender'] == 'F']

                group_matrix = []

                # pop elements from M_players until it's empty
                while M_players:
                    new_group = [
                        M_players.pop(),
                        F_players.pop(),
                        F_players.pop(),
                    ]
                    group_matrix.append(new_group)

                self.set_group_matrix(group_matrix)
            else:
                self.group_like_round(1)
                # uncomment this line if you want to shuffle groups, while keeping M/F roles fixed
                # self.group_randomly(fixed_id_in_group=True)

Shuffling during the session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``creating_session`` is usually a good place to shuffle groups,
but remember that ``creating_session`` is run when the session is created,
before players begin playing. So, if your shuffling logic needs to depend on
something that happens after the session starts, you should do the
shuffling in a wait page instead.

Let's say you have defined a method on the ``Subsession`` class
called ``do_my_shuffle()`` that uses ``set_group_matrix``, etc.

You need to make a ``WaitPage`` with ``wait_for_all_groups=True``
and put the shuffling code in ``after_all_players_arrive``:

.. code-block:: python

    class ShuffleWaitPage(WaitPage):
        wait_for_all_groups = True

        def after_all_players_arrive(self):
            self.subsession.do_my_shuffle()

After this wait page, the players will be reassigned to their new groups.

Let's say you have a game with multiple rounds,
and in a wait page at the beginning you want to shuffle the groups,
and apply this new group structure to all rounds.
You can use ``group_like_round()`` together with ``in_rounds()``.
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
            return self.round_number == 1

Group by arrival time
~~~~~~~~~~~~~~~~~~~~~

See :ref:`group_by_arrival_time`.

Example: configurable group size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you want to be able to configure the number of players per group
each time you create a session. (Setting ``Constants.players_per_group = None``
kind of does this, but only if all players are in the same group.)

As described in :ref:`edit_config`, create a key in your session config
(you can call it ``players_per_group``), then use this code to chunk the players
into groups of that size:

.. code-block:: python

    class Subsession(BaseSubsession):
        def creating_session(self):
            group_matrix = []
            players = self.get_players()
            ppg = self.session.config['players_per_group']
            for i in range(0, len(players), ppg):
                group_matrix.append(players[i:i+ppg])
            self.set_group_matrix(group_matrix)
