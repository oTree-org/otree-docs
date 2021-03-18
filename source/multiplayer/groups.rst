.. _groups:

Groups
======

You can divide players into groups for multiplayer games.
(If you just need groups in the sense of "treatment groups",
where players don't actually interact with each other,
then see :ref:`treatments`.)

To set the group size, go to your app's Constants and set
``players_per_group``. For example, for a 2-player game,
set ``players_per_group = 2``.

If all players should be in the same group,
or if it's a single-player game, set it to ``None``:

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


Getting other players
---------------------

Player objects have methods ``get_others_in_group()`` and
``get_others_in_subsession()`` that return a list of the *other* players
in the group and subsession.

.. _roles:

Roles
-----

.. note::

    New as of January 2021

If each group has multiple roles, such as buyer/seller, principal/agent, etc.,
you can define them in Constants. Make their names end with ``_role``:

.. code-block:: python

    class Constants(BaseConstants):
        ...

        principal_role = 'Principal'
        agent_role = 'Agent

oTree will then automatically assign each ``role`` to a different player
(sequentially according to ``id_in_group``).
You can use this to show each role different content, e.g.:

.. code-block:: python

    class AgentPage(Page):

        @staticmethod
        def is_displayed(player):
            return player.role == Constants.agent_role

In a template:

.. code-block:: html

    You are the {{ player.role }}.

You can also use ``group.get_player_by_role()``, which is similar to ``get_player_by_id()``:

.. code-block:: python

    def set_payoffs(group):
        principal = group.get_player_by_role(Constants.principal_role)
        agent = group.get_player_by_role(Constants.agent_role)
        # ...

If you want to switch players' roles,
you should rearrange the groups, using ``group.set_players()``, ``subsession.group_randomly()``,
etc.


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

    def creating_session(subsession):
        subsession.group_randomly()

This will group players randomly each round, but keep ``id_in_group`` fixed:

.. code-block:: python

    def creating_session(subsession):
        subsession.group_randomly(fixed_id_in_group=True)

For the following example, assume that ``players_per_group = 3``, and that there are 12 participants in the session:

.. code-block:: python

    def creating_session(subsession):
        print(subsession.get_group_matrix()) # outputs the following:
        # [[<Player  1>, <Player  2>, <Player  3>],
        #  [<Player  4>, <Player  5>, <Player  6>],
        #  [<Player  7>, <Player  8>, <Player  9>],
        #  [<Player 10>, <Player 11>, <Player 12>]]

        subsession.group_randomly(fixed_id_in_group=True)
        print(subsession.get_group_matrix()) # outputs the following:
        # [[<Player  1>, <Player  8>, <Player 12>],
        #  [<Player 10>, <Player  5>, <Player  3>],
        #  [<Player  4>, <Player  2>, <Player  6>],
        #  [<Player  7>, <Player 11>, <Player  9>]]

        subsession.group_randomly()
        print(subsession.get_group_matrix()) # outputs the following:
        # [[<Player  8>, <Player 10>, <Player  3>],
        #  [<Player  4>, <Player 11>, <Player  2>],
        #  [<Player  9>, <Player  1>, <Player  6>],
        #  [<Player 12>, <Player  5>, <Player  7>]]

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

    def creating_session(subsession):
        if subsession.round_number == 1:
            # <some shuffling code here>
        else:
            subsession.group_like_round(1)


get_group_matrix()
~~~~~~~~~~~~~~~~~~

Subsessions have a method called ``get_group_matrix()`` that
return the structure of groups as a matrix, for example:

.. code-block:: python

    [[1, 3, 5],
     [7, 9, 11],
     [2, 4, 6],
     [8, 10, 12]]



.. _set_group_matrix:

set_group_matrix()
~~~~~~~~~~~~~~~~~~

``set_group_matrix()`` lets you modify the group structure in any way you want.
First, get the list of players with ``get_players()``, or the pre-existing
group matrix with ``get_group_matrix()``.
Make your matrix then pass it to ``set_group_matrix()``:

.. code-block:: python

    def creating_session(subsession):
        matrix = subsession.get_group_matrix()

        for row in matrix:
            row.reverse()

        # now the 'matrix' variable looks like this,
        # but it hasn't been saved yet!
        # [[<Player  3>, <Player  2>, <Player  1>],
        #  [<Player  6>, <Player  5>, <Player  4>],
        #  [<Player  9>, <Player  8>, <Player  7>],
        #  [<Player 12>, <Player 11>, <Player 10>]]

        # save it
        subsession.set_group_matrix(matrix)

You can also pass a matrix of integers.
It must contain all integers from 1 to the number of players
in the subsession. Each integer represents the player who has that ``id_in_subsession``.
For example:

.. code-block:: python

    def creating_session(subsession):

        new_structure = [[1,3,5], [7,9,11], [2,4,6], [8,10,12]]
        subsession.set_group_matrix(new_structure)

        print(subsession.get_group_matrix()) # will output this:

        # [[<Player  1>, <Player  3>, <Player  5>],
        #  [<Player  7>, <Player  9>, <Player 11>],
        #  [<Player  2>, <Player  4>, <Player  6>],
        #  [<Player  8>, <Player 10>, <Player 12>]]

To check if your group shuffling worked correctly,
open your browser to the "Results" tab of your session,
and look at the ``group`` and ``id_in_group`` columns in each round.

group.set_players()
~~~~~~~~~~~~~~~~~~~

This is similar to ``set_group_matrix``, but it only shuffles players within a group,
e.g. so that you can give them different roles.

Shuffling during the session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``creating_session`` is usually a good place to shuffle groups,
but remember that ``creating_session`` is run when the session is created,
before players begin playing. So, if your shuffling logic needs to depend on
something that happens after the session starts, you should do the
shuffling in a wait page instead.

You need to make a ``WaitPage`` with ``wait_for_all_groups=True``
and put the shuffling code in ``after_all_players_arrive``:

.. code-block:: python

    class ShuffleWaitPage(WaitPage):

        wait_for_all_groups = True

        @staticmethod
        def after_all_players_arrive(subsession):
            subsession.group_randomly()
            # etc...


Group by arrival time
~~~~~~~~~~~~~~~~~~~~~

See :ref:`group_by_arrival_time`.
