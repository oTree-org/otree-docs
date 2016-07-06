Models
======

This is where you store your data models.

Model hierarchy
---------------

Every oTree app needs the following 3 models:

-  Subsession
-  Group
-  Player

A player is part of a group, which is part of a subsession.


Models and database tables
--------------------------

For example, let's say you are programming an ultimatum game, where in
each two-person group, one player makes a monetary offer (say, 0-100
cents), and another player either rejects or accepts the offer. When you
analyze your data, you will want your "Group" table to look something
like this:

.. csv-table::
    :header-rows: 1

    Group ID,Amount offered,Offer accepted
    1,50,TRUE
    2,25,FALSE
    3,50,TRUE
    4,0,FALSE
    5,60,TRUE


You need to define a Python class that defines the structure of this
database table. You define what fields (columns) are in the table, what
their data types are, and so on. When you run your experiment, the SQL
tables will get automatically generated, and each time users visit, new
rows will get added to the tables.

Here is how to define the above table structure:

.. code-block:: python

    class Group(BaseGroup):
        ...
        amount_offered = models.CurrencyField()
        offer_accepted = models.BooleanField()

Every time you add, remove, or change a field in ``models.py``, you need
to run ``otree resetdb``, or, in the launcher, click "Reset DB".
(However, you don't need to run ``resetdb`` if you only make a change that
doesn't affect your database schema, like modifying ``views.py`` or an HTML template, etc.)

The full list of available fields is in the Django documentation
`here <https://docs.djangoproject.com/en/1.7/ref/models/fields/#field-types>`__.

Additionally, oTree has ``CurrencyField``; see :ref:`currency`.

min, max, choices
-----------------

For info on how to set a field's ``min``, ``max``, or ``choices``,
see :ref:`form-validation`.

.. _constants:

Constants
---------

The ``Constants`` class is the recommended place to put your app's
parameters and constants that do not vary from player
to player.

Here are the required constants:

-   ``name_in_url`` specifies the name used to identify your app in the
    participant's URL.

    For example, if you set it to ``public_goods``, a participant's URL might
    look like this:

    ``http://otree-demo.herokuapp.com/p/zuzepona/public_goods/Introduction/1/``

-  ``players_per_group`` (described in :ref:`groups`)

-  ``num_rounds`` (described in :ref:`rounds`)

You should only use ``Constants`` to store actual constants -- things that never change.
If you want a "global" variable, you should set a field on the subsession, or use :ref:`session_vars`.


Subsession
----------

Here is a list of attributes and methods for subsession objects.

session
~~~~~~~

The session this subsession belongs to.
See :ref:`object_model`.

round_number
~~~~~~~~~~~~
If this subsession is repeated (i.e. has multiple rounds), this
field stores the position (index) of this subsession, among subsessions
in the same app.

For example, if a session consists of the subsessions:

    [app1, app2, app1, app1, app3]

Then the round numbers of these subsessions would be:

    [1, 1, 2, 3, 1]

See :ref:`shuffling`.

group_randomly()
~~~~~~~~~~~~~~~~

See :ref:`shuffling`.

group_like_round()
~~~~~~~~~~~~~~~~~~

See :ref:`shuffling`.

get_group_matrix()
~~~~~~~~~~~~~~~~~~

See :ref:`shuffling`.

set_group_matrix()
~~~~~~~~~~~~~~~~~~

See :ref:`shuffling`.


get_groups()
~~~~~~~~~~~~

Returns a list of all the groups in the subsession.

get_players()
~~~~~~~~~~~~~

Returns a list of all the players in the subsession.

in_previous_rounds()
~~~~~~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

in_all_rounds()
~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

in_round(round_number)
~~~~~~~~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

in_rounds(self, first, last)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

.. _before_session_starts:

before_session_starts
~~~~~~~~~~~~~~~~~~~~~

You can define this method like this:

.. code-block:: python

    class Subsession(BaseSubsession):

        def before_session_starts(self):
            ...

This method is executed at the moment when the session is created, meaning it
finishes running before the session begins (Hence the name).
It is executed once per subsession (i.e. once per round).
For example, if your app has 10 rounds, this method will get called 10 times,
once for each ``Subsession`` instance.

It has many uses, such as initializing fields, assigning players to treatments,
or shuffling groups.


Group
-----

Here is a list of attributes and methods for group objects.

session/subsession
~~~~~~~~~~~~~~~~~~

The session/subsession this group belongs to.
See :ref:`object_model`.


get_players()
~~~~~~~~~~~~~

See :ref:`groups`.

get_player_by_role(role)
~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`groups`.

get_player_by_id(id_in_group)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`groups`.

set_players(players_list)
~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`shuffling`.

in_previous_rounds()
~~~~~~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

in_all_rounds()
~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

in_round(round_number)
~~~~~~~~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

in_rounds(self, first, last)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

Player
------

Here is a list of attributes and methods for player objects.

id_in_group
~~~~~~~~~~~
Index starting from 1. In multiplayer games,
indicates whether this is player 1, player 2, etc.

payoff
~~~~~~
The player's payoff in this round. See :ref:`payoff`.

session/subsession/group/participant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The session/subsession/group/participant this player belongs to.
See :ref:`object_model`.


get_others_in_group()
~~~~~~~~~~~~~~~~~~~~~

See :ref:`groups`.

get_others_in_subsession()
~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`groups`.

role()
~~~~~~
You can define this method to return a string label of the player's role,
usually depending on the player's ``id_in_group``.

For example::

    def role(self):
        if self.id_in_group == 1:
            return 'buyer'
        if self.id_in_group == 2:
            return 'seller'

Then you can use ``get_player_by_role('seller')`` to get player 2.
See :ref:`groups`.

Also, the player's role will be displayed in the oTree admin interface,
in the "results" tab.

in_previous_rounds()
~~~~~~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

in_all_rounds()
~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

in_round(round_number)
~~~~~~~~~~~~~~~~~~~~~~

See :ref:`in_rounds`.

in_rounds(self, first, last)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`in_rounds`.