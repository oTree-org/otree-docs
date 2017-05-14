Models
======

``models.py`` is where you define your app's data models:

-  Subsession
-  Group
-  Player

A player is part of a group, which is part of a subsession.
See :ref:`conceptual_overview`.

Model fields
------------

The main purpose of ``models.py`` is to define the columns of your
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
        ...
        name = models.CharField()
        age = models.PositiveIntegerField()
        is_student = models.BooleanField()

When you run ``otree resetdb``, it will scan your ``models.py``
and create your database tables accordingly.
(Therefore, you need to run ``resetdb`` if you have added,
removed, or changed a field in ``models.py``.)

The full list of available fields is in the Django documentation
`here <https://docs.djangoproject.com/en/1.8/ref/models/fields/#field-types>`__.
The most commonly used ones are ``CharField``/``TextField`` (for text),
``FloatField`` (for real numbers),
``BooleanField`` (for true/false values),
``IntegerField``, and ``PositiveIntegerField``.
Don't use ``DecimalField`` unless you understand how it is different
from ``FloatField`` and have a specific need for it.

Additionally, oTree has ``CurrencyField``; see :ref:`currency`.

Setting a field's initial/default value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any field you define will have the initial value of ``None``.
If you want to give it an initial value, you can use ``initial=``:

.. code-block:: python

    class Player(BasePlayer):
        some_number = models.IntegerField(initial=0)


min, max, choices
~~~~~~~~~~~~~~~~~

For info on how to set a field's ``min``, ``max``, or ``choices``,
see :ref:`form-validation`.

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

Don't modify values in ``Constants``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As the name suggests, ``Constants`` is for holding
values that never change.

For example, let's say your ``Constants`` has an attribute ``my_dict``:

.. code-block:: python

    class Constants(BaseConstants):
        my_dict = {}

And you try to modify ``my_dict``:

.. code-block:: python

    class Subsession(BaseSubsession):
        def before_session_starts(self):
            # wrong
            Constants.my_dict['a'] = 1

As explained in the section :ref:`how_otree_executes_code`,
``Constants`` is a global variable,
so when you modify it above,
you are actually modifying it for all participants in all sessions.
This can lead to all kinds of unexpected behavior.

Instead, if you want a variable that is the same for all players in your session,
you should set a field on the subsession, or use :ref:`session_vars`.


Subsession
----------

Here is a list of attributes and methods for subsession objects.


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


.. _before_session_starts:

before_session_starts
~~~~~~~~~~~~~~~~~~~~~

You can define this method like this:

.. code-block:: python

    class Subsession(BaseSubsession):

        def before_session_starts(self):
            # code goes here

This method is executed at the moment when the session is created, meaning it
finishes running before the session begins (Hence the name).
It is executed once per subsession (i.e. once per round).
For example, if your app has 10 rounds, this method will get called 10 times,
once for each ``Subsession`` instance.

It has many uses, such as initializing fields, assigning players to treatments,
or shuffling groups.

A typical use of ``before_session_starts`` is to loop over the players and
set the value of a field on each:

.. code-block:: python

    class Subsession(BaseSubsession):

        def before_session_starts(self):
            for p in self.get_players():
                p.some_field = some_value

More info on the section on :ref:`treatments <treatments>`.

``before_session_starts`` is also used to :ref:`assign players to groups <shuffling>`.


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
Integer starting from 1. In multiplayer games,
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

Extra models
------------

Some complex apps require extra models
(other than Player, Group, and Subsession).
You can define these models using Django's API,
although you will have to write the code to create/update/save
them yourself, rather than relying on oTree.
See Markus Konrad's excellent article
`Using Custom Data Models in oTree <https://datascience.blog.wzb.eu/2016/10/31/using-custom-data-models-in-otree/>`__.

.. _how_otree_executes_code:

How oTree executes your code
----------------------------

Any code that is not inside a method
is basically *global* and *will only be executed once* --
when the server starts.

Some people write code mistakenly thinking that it will be re-executed for each
new session. For example, someone who wants to generate a random probability that a coin flip will
come up "heads" might do this in models.py:

.. code-block:: python

    class Constants(BaseConstants):
        heads_probability = random.random() # wrong

When the server starts, it loads models.py,
and executes the ``random.random()`` only once.
It will evaluate to some random number, for example "0.257291".
This means you have basically written this:

.. code-block:: python

    class Constants(BaseConstants):
        heads_probability = 0.257291

Because ``Constants`` is a global variable, that value 0.257291 will now be shared
by all players in all sessions.

For the same reason, this will not work either:

.. code-block:: python

    class Player(BasePlayer):

        heads_probability = models.FloatField(
            # wrong
            initial=random.random()
        )

The solution is to generate the random variables inside a method,
such as :ref:`before_session_starts`.
