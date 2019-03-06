Models
++++++

``models.py`` is where you define your app's data models:

-  Subsession
-  Group
-  Player

A player is part of a group, which is part of a subsession.
See :ref:`conceptual_overview`.

The purpose of ``models.py`` is to define the columns of your
database tables. Let's say you want your experiment to generate data
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

Defining a column
=================

Field types
-----------

Here are the main field types:

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

Since your models inherit from oTree's base classes
(``BaseSubsession``, ``BaseGroup``, and ``BasePlayer``),
the tables already have certain pre-defined fields and methods.
For example, the ``Player`` table has columns called ``payoff``
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

Unlike most other built-in subsession methods,
this method is one you must define yourself.
Any code you put here is executed when you create the session.

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

Note that ``self`` here is a subsession object,
because we are inside the ``Subsession`` class.
So, you cannot do ``self.player``, because there is more than 1 player
in the subsession. Instead, use ``self.get_players()`` to get all of them.

If your app has multiple rounds, ``creating_session`` gets run multiple
times consecutively:

.. code-block:: python

    class Constants(BaseConstants):
        name_in_url = 'print_statements'
        players_per_group = None
        num_rounds = 5


    class Subsession(BaseSubsession):
        def creating_session(self):
            print('in creating_session', self.round_number)

Will output::

    in creating_session 1
    in creating_session 2
    in creating_session 3
    in creating_session 4
    in creating_session 5


.. _before_session_starts:

before_session_starts
~~~~~~~~~~~~~~~~~~~~~

``before_session_starts`` has been renamed to :ref:`creating_session`.
However, new versions of oTree still execute ``before_session_starts``,
for backwards compatibility.

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



Group
-----

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


get_others_in_group()
~~~~~~~~~~~~~~~~~~~~~

See :ref:`groups`.

get_others_in_subsession()
~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`groups`.

.. _role:

role()
~~~~~~

Unlike most other built-in player methods, this is one you define yourself.

This function should return a label with the player's role,
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

Session
-------

num_participants
~~~~~~~~~~~~~~~~

The number of participants in the session.

config
~~~~~~

See :ref:`edit_config`
and :ref:`session_config_treatments`.

vars
~~~~

See :ref:`session_vars`.

Participant
-----------

vars
~~~~

See :ref:`vars`.

label
~~~~~

See :ref:`participant_label`.

id_in_session
~~~~~~~~~~~~~

The participant's ID in the session. This is the same as the player's
``id_in_subsession``.

payoff
~~~~~~

See :ref:`payoff`.

payoff_plus_participation_fee()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`payoff`.

.. _constants:

Constants
---------

The ``Constants`` class is the recommended place to put your app's
parameters and constants that do not vary from player
to player.

Here are the required constants:

-   ``name_in_url``: the name used to identify your app in the
    participant's URL.

    For example, if you set it to ``public_goods``, a participant's URL might
    look like this:

    ``http://otree-demo.herokuapp.com/p/zuzepona/public_goods/Introduction/1/``

-  ``players_per_group`` (described in :ref:`groups`)

-  ``num_rounds`` (described in :ref:`rounds`)


Miscellaneous topics
====================

Defining your own methods
-------------------------

You can define your own methods on models.
This helps you keep your code organized as it gets more complex.
For example, you can define a function to set players' payoffs:

.. code-block:: python

    class Group(BaseGroup):
        def set_payoffs(self):
            print('in set_payoffs')
            # etc ...

Just remember to call this function from somewhere, such as your page:

.. code-block:: python

    class MyWaitPage(WaitPage):
        def after_all_players_arrive(self):
            self.group.set_payoffs()

Because it will not be executed automatically, unlike built-in functions
like ``creating_session()``, ``after_all_players_arrive()``, etc.


.. _many-fields:

How to make many fields
-----------------------

Let's say your app has many fields that are almost the same, such as:

.. code-block:: python

    class Player(BasePlayer):

        f1 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f2 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f3 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f4 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f5 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f6 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f7 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f8 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f9 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f10 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )

        # etc...

This is quite complex; you should look for a way to simplify.

Are the fields all displayed on separate pages? If so, consider converting
this to a 10-round game with just one field. See the
`real effort <https://github.com/oTree-org/oTree/tree/master/real_effort>`__
sample game for an example of how to just have 1 page that gets looped over many rounds,
varying the question that gets displayed with each round.

If that's not possible, then you can reduce the amount of repeated code
by defining a function that returns a field
(``make_field`` is just an example name; you can call it anything).

.. code-block:: python

    def make_field(label):
        return models.IntegerField(
            choices=[1,2,3,4,5],
            label=label,
            widget=widgets.RadioSelect,
        )

    class Player(BasePlayer):

        q1 = make_field('I am quick to understand things.')
        q2 = make_field('I use difficult words.')
        q3 = make_field('I am full of ideas.')
        q4 = make_field('I have excellent ideas.')


