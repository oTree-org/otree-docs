Models
++++++

An oTree app has 3 data models:

-  Subsession
-  Group
-  Player

A player is part of a group, which is part of a subsession.
See :ref:`conceptual_overview`.

Let's say you want your experiment to generate data
that looks like this:

.. csv-table::
    :header-rows: 1

    name,age,is_student
    John,30,False
    Alice,22,True
    Bob,35,False
    ...

Here is how to define the above table structure:

.. code-block:: python

    class Player(BasePlayer):
        name = models.StringField()
        age = models.IntegerField()
        is_student = models.BooleanField()

So, a **model** is essentially a database table.
And a **field** is a column in a table.

Fields
======

Field types
-----------

-   ``BooleanField`` (for true/false and yes/no values)
-   ``CurrencyField`` for currency amounts; see :ref:`currency`.
-   ``IntegerField``
-   ``FloatField`` (for real numbers)
-   ``StringField`` (for text strings)
-   ``LongStringField`` (for long text strings; its form widget is a multi-line textarea)


Initial/default value
---------------------

Your field's initial value will be ``None``, unless you set ``initial=``:

.. code-block:: python

    class Player(BasePlayer):
        some_number = models.IntegerField(initial=0)


min, max, choices
-----------------

For info on how to set a field's ``min``, ``max``, or ``choices``,
see :ref:`form-validation`.

Built-in fields and methods
===========================

Player, group, and subsession already have some predefined fields.
For example, ``Player`` has fields called ``payoff``
and ``id_in_group``, as well as methods like
``in_all_rounds()`` and ``get_others_in_group()``.

These built-in fields and methods are listed below.


Subsession
----------

session
~~~~~~~

The session this subsession belongs to.
See :ref:`object_model`.


round_number
~~~~~~~~~~~~

Gives the current round number.
Only relevant if the app has multiple rounds
(set in ``Constants.num_rounds``).
See :ref:`rounds`.

.. _creating_session:

creating_session()
~~~~~~~~~~~~~~~~~~

``creating_session`` allows you to set initial values on fields on
players, groups, participants, or the subsession.
For example:

.. code-block:: python

    class Subsession(BaseSubsession):

        def creating_session(self):
            for p in self.get_players():
                p.payoff = c(10)

More info on the section on :ref:`treatments <treatments>` and
:ref:`group shuffling <shuffling>`.

Unlike most other built-in subsession methods,
this method is one you must define yourself.

``creating_session`` is **not** run at the beginning of each round.
It is run when you click the "create session" button, i.e. before anybody starts playing.
If your app has multiple rounds, ``creating_session`` gets run multiple
times consecutively:

.. code-block:: python

    class Subsession(BaseSubsession):

        def creating_session(self):
            print('in creating_session', self.round_number)

Will output all at once::

    in creating_session 1
    in creating_session 2
    in creating_session 3


get_groups()
~~~~~~~~~~~~

Returns a list of all the groups in the subsession.

get_players()
~~~~~~~~~~~~~

Returns a list of all the players in the subsession.

Other subsession methods
~~~~~~~~~~~~~~~~~~~~~~~~

-   :ref:`group_randomly() <shuffling>`
-   :ref:`group_like_round() <shuffling>`
-   :ref:`get_group_matrix() <shuffling>`
-   :ref:`set_group_matrix() <shuffling>`
-   :ref:`in_all_rounds() <in_rounds>`
-   :ref:`in_previous_rounds() <in_rounds>`
-   :ref:`in_rounds(first, last) <in_rounds>`
-   :ref:`in_round(round_number) <in_rounds>`


Group
-----

session/subsession
~~~~~~~~~~~~~~~~~~

The session/subsession this group belongs to.
See :ref:`object_model`.


Other group methods
~~~~~~~~~~~~~~~~~~~

-   :ref:`in_all_rounds() <in_rounds>`
-   :ref:`in_previous_rounds() <in_rounds>`
-   :ref:`in_rounds(first, last) <in_rounds>`
-   :ref:`in_round(round_number) <in_rounds>`
-   :ref:`get_player_by_role(role) <groups>`
-   :ref:`get_player_by_id(id_in_group) <groups>`
-   :ref:`get_players() <groups>`


Player
------

id_in_group
~~~~~~~~~~~
Automatically assigned integer starting from 1. In multiplayer games,
indicates whether this is player 1, player 2, etc.

payoff
~~~~~~
The player's payoff in this round. See :ref:`payoff`.

session/subsession/group/participant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The session/subsession/group/participant this player belongs to.
See :ref:`object_model`.

.. _role:

role()
~~~~~~

Unlike most other built-in player methods, this is one you define yourself.

This method should return a label with the player's role,
usually depending on ``id_in_group``.

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

Other player methods
~~~~~~~~~~~~~~~~~~~~

-   :ref:`in_all_rounds() <in_rounds>`
-   :ref:`in_previous_rounds() <in_rounds>`
-   :ref:`in_rounds(first, last) <in_rounds>`
-   :ref:`in_round(round_number) <in_rounds>`
-   :ref:`get_others_in_subsession() <groups>`
-   :ref:`get_others_in_group() <groups>`

Session
-------

num_participants
~~~~~~~~~~~~~~~~

The number of participants in the session.

config
~~~~~~

See :ref:`session_config_treatments`.

vars
~~~~

See :ref:`session_vars`.

Participant
-----------

id_in_session
~~~~~~~~~~~~~

The participant's ID in the session. This is the same as the player's
``id_in_subsession``.

Other participant attributes and methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   :ref:`vars <vars>`
-   :ref:`label <participant_label>`
-   :ref:`payoff <payoff>`
-   :ref:`payoff_plus_participation_fee <payoff>`

.. _constants:

Constants
---------

``Constants`` is the recommended place to put your app's
parameters and constants that do not vary from player
to player.

Here are the built-in constants:

-  ``players_per_group`` (described in :ref:`groups`)
-  ``num_rounds`` (described in :ref:`rounds`)

if you don't want your app's real name
to be displayed in URLs,
define a string constant ``name_in_url`` with your desired name.

Constants can be numbers, strings, booleans, lists, etc.
But for more complex data types like dicts, lists of dicts, etc,
you should instead define it in a subsession method. For example,
instead of defining a Constant called ``my_dict``, do this:

.. code-block:: python

    class Subsession(BaseSubsession):
        def my_dict(self):
            return dict(a=[1,2], b=[3,4])

Miscellaneous topics
====================

Defining your own methods
-------------------------

In addition to the methods listed on this page,
you can define your own.
Just remember to *use* them somewhere!
Just defining them with ``def`` has no effect.

For example:

.. code-block:: python

    class Group(BaseGroup):
        def set_payoffs(self):
            print('in set_payoffs')
            # etc ...

Then call it:

.. code-block:: python

    class MyWaitPage(WaitPage):
        after_all_players_arrive = 'set_payoffs'

.. _how_otree_executes_code:

About using random()
--------------------

Never generate random values outside of a method.
For example, don't do this:

.. code-block:: python

    class Constants(BaseConstants):
        p = random.randint(1, 10) # wrong

If it changes randomly, it isn't a constant.

Or this:

.. code-block:: python

    class Player(BasePlayer):

        p = models.FloatField(
            # wrong
            initial=random.randint(1, 10)
        )

These won't work because they will change every time
the server launches a new process.
It may appear to work during testing but will eventually break.
Instead, you should generate the random variables inside a method,
such as :ref:`creating_session` (and preferably not ``vars_for_template``,
which gets re-executed if the user refreshes the page).

If you want to set your own random seed, don't use the ``random.seed()`` function.
Instead, generate an instance of ``random.Random`` as described `here <https://stackoverflow.com/a/37356024>`__
