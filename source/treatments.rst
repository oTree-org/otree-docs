.. _treatments:

Treatments
==========

To assign participants to different treatment groups, you
can put the code in the subsession's ``creating_session`` method
(for more info see :ref:`creating_session`).
For example, if you want some participants to be in a "blue" treatment group
and others to be in a "red" treatment group, first define
a ``color`` field on the ``Player`` model:

.. code-block:: python

    class Player(BasePlayer):
        color = models.StringField()

Then you can assign to this field randomly:

.. code-block:: python

    class Subsession(BaseSubsession):

        def creating_session(self):
            # randomize to treatments
            for player in self.get_players():
                player.color = random.choice(['blue', 'red'])
                print('set player.color to', player.color)

You can also assign treatments at the group level (put the ``StringField``
in the ``Group`` class and change the above code to use
``get_groups()`` and ``group.color``).

Treatment groups & multiple rounds
----------------------------------

If your game has multiple rounds, the above code gets executed
for each round. So if you want to ensure that participants are assigned
to the same treatment group each round, you should set the property at
the participant level, which persists across subsessions, and only set
it in the first round:

.. code-block:: python

    class Subsession(BaseSubsession):

        def creating_session(self):
            if self.round_number == 1:
                for p in self.get_players():
                    p.participant.vars['color'] = random.choice(['blue', 'red'])

Then elsewhere in your code, you can access the participant's color with
``self.participant.vars['color']``.

There is no direct equivalent for ``participant.vars`` for groups,
because groups can be re-shuffled across rounds.
You should instead store the variable on one of the participants in the group:

.. code-block:: python

    def creating_session(self):
        if self.round_number == 1:
            for g in self.get_groups():
                p1 = g.get_player_by_id(1)
                p1.participant.vars['color'] = random.choice(['blue', 'red'])

Then, when you need to access a group's color, you would look it up like this:

.. code-block:: python

    p1 = self.group.get_player_by_id(1)
    color = p1.participant.vars['color']

For more on vars, see :ref:`vars`.

Balanced treatment groups
-------------------------

The above code makes a random drawing independently for each player,
so you may end up with an imbalance between "blue" and "red".
To solve this, you can use ``itertools.cycle``, which alternates:

.. code-block:: python

    import itertools

    class Subsession(BaseSubsession):

        def creating_session(self):
            colors = itertools.cycle(['blue', 'red'])
            for p in self.get_players():
                p.color = next(colors)


.. _session_config_treatments:

Choosing which treatment to play
--------------------------------

In the above example, players got randomized to treatments. This is
useful in a live experiment, but when you are testing your game, it is
often useful to choose explicitly which treatment to play. Let's say you
are developing the game from the above example and want to show your
colleagues both treatments (red and blue). You can create 2 session
configs that have the same keys in the session config dictionary,
except the ``treatment`` key:

.. code-block:: python

    SESSION_CONFIGS = [
        {
            'name':'my_game_blue',
            # other arguments...

            'treatment':'blue',

        },
        {
            'name':'my_game_red',
            # other arguments...
            'treatment':'red',
        },
    ]

Then in the ``creating_session`` method, you can check which of the
2 session configs it is:

.. code-block:: python

    def creating_session(self):
        for p in self.get_players():
            if 'treatment' in self.session.config:
                # demo mode
                p.color = self.session.config['treatment']
            else:
                # live experiment mode
                p.color = random.choice(['blue', 'red'])

Then, when someone visits your demo page, they will see the "red" and
"blue" treatment, and choose to play one or the other. If the demo
argument is not passed, the color is randomized.

Also see :ref:`edit_config`.

Use BooleanField instead of StringField, where possible
-------------------------------------------------------

Many ``StringFields`` should be broken down into ``BooleanFields``, especially
if they can only have less than 5 distinct values.

Suppose you have a field called ``treatment``:

.. code-block:: python

    treatment = models.StringField()

And let's say ``treatment`` it can only have 4 different values:

-   ``high_income_high_tax``
-   ``high_income_low_tax``
-   ``low_income_high_tax``
-   ``low_income_low_tax``

In your pages, you might use it like this:

.. code-block:: python

    class HighIncome(Page):
        def is_displayed(self):
            return self.player.treatment == 'high_income_high_tax' or self.player.treatment == 'high_income_low_tax'

    class HighTax(Page):
        def is_displayed(self):
            return self.player.treatment == 'high_income_high_tax' or self.player.treatment == 'low_income_high_tax'


It would be much better to break this to 2 separate BooleanFields::

    high_income = models.BooleanField()
    high_tax = models.BooleanField()

Then your pages could be simplified to:

.. code-block:: python

    class HighIncome(Page):
        def is_displayed(self):
            return self.player.high_income

    class HighTax(Page):
        def is_displayed(self):
            return self.player.high_tax