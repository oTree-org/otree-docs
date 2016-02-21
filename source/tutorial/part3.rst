Part 3: Matching pennies
========================

We will now create a "Matching pennies" game with the following
features:

-  4 rounds
-  The roles of the players will be reversed halfway through
-  In each round, a "history box" will display the results of previous
   rounds
-  A random round will be chosen for payment

The completed app is
`here <https://github.com/oTree-org/oTree/tree/master/matching_pennies_tutorial>`__.


Create the app
--------------

.. code-block:: bash

    $ otree startapp my_matching_pennies


Define models.py
----------------

We define our constants as we have previously. Matching pennies is a
2-person game and the payoff for winning a paying round is 100 points.
In this case, the game has 4 rounds, so we set ``num_rounds`` (see :ref:`rounds`).

.. code-block:: python

    class Constants(BaseConstants):
        name_in_url = 'my_matching_pennies'
        players_per_group = 2
        num_rounds = 4
        stakes = c(100)

Now let's define our ``Player`` class:

-  In each round, each player decides "Heads" or "Tails", so we define a
   field ``penny_side``, which will be displayed as a radio button.
-  We also have a boolean field ``is_winner`` that records if this
   player won this round.
-  We define the ``role`` method (see :ref:`groups`) to define which player is the "Matcher"
   and which is the "Mismatcher".

So we have:

.. code-block:: python

    class Player(BasePlayer):

        penny_side = models.CharField(
            choices=['Heads', 'Tails'],
            widget=widgets.RadioSelect()
        )

        is_winner = models.BooleanField()

        def role(self):
            if self.id_in_group == 1:
                return 'Mismatcher'
            if self.id_in_group == 2:
                return 'Matcher'

Now let's define the code to randomly choose a round for payment. Let's
define the code in ``Subsession.before_session_starts``, which is the
place to put global code that initializes the state of the game, before
gameplay starts. (See :ref:`before_session_starts`.)

The value of the chosen round is "global" rather than different for each
participant, so the logical place to store it is as a "global" variable
in ``self.session.vars`` (see :ref:`session_vars`).

So, we start by writing something like this, which chooses a random
integer between 1 and 4, and then assigns it into ``session.vars``:

.. code-block:: python

    class Subsession(BaseSubsession):

        def before_session_starts(self):
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round

There is a slight mistake, however. Because there are 4 rounds (i.e.
subsessions), this code will get executed 4 times, each time overwriting
the previous value of ``session.vars['paying_round']``, which is
superfluous. We can fix this with an ``if`` statement that makes it only
run once (if ``round_number`` is 1; see :ref:`rounds`):

.. code-block:: python

    class Subsession(BaseSubsession):

        def before_session_starts(self):
            if self.round_number == 1:
                paying_round = random.randint(1, Constants.num_rounds)
                self.session.vars['paying_round'] = paying_round

Now, let's also define the code to swap roles halfway through. This kind
of group-shuffling code should also go in ``before_session_starts``. We
put it after our existing code.

So, in round 3, we should do the shuffle,
and then in round 4, use ``group_like_round(3)`` to copy the group structure from round 3.
(See :ref:`group_like_round <group_like_round>`)

We use ``group.get_players()`` to get the ordered list of players in
each group, and then reverse it (e.g. the list ``[P1, P2]`` becomes
``[P2, P1]``). Then we use ``group.set_players()`` to set this as the
new group order:

.. code-block:: python

    class Subsession(BaseSubsession):

        def before_session_starts(self):
            if self.round_number == 1:
                ...
            if self.round_number == 3:
                # reverse the roles
                for group in self.get_groups():
                    players = group.get_players()
                    players.reverse()
                    group.set_players(players)
            if self.round_number > 3:
                self.group_like_round(3)

(You can learn more about group shuffling in :ref:`shuffling`.)

Now we define our ``Group`` class. We define the payoff method. We use
``get_player_by_role`` to fetch each of the 2 players in the group. We
could also use ``get_player_by_id``, but I find it easier to identify
the players by their roles as matcher/mismatcher. Then, depending on
whether the penny sides match, we either make P1 or P2 the winner.

So, we start with this:

.. code-block:: python

    class Group(BaseGroup):

        def set_payoffs(self):
            matcher = self.get_player_by_role('Matcher')
            mismatcher = self.get_player_by_role('Mismatcher')

            if matcher.penny_side == mismatcher.penny_side:
                matcher.is_winner = True
                mismatcher.is_winner = False
            else:
                matcher.is_winner = False
                mismatcher.is_winner = True

We should expand this code by setting the actual ``payoff`` field.
However, the player should only receive a payoff if the current round is
the randomly chosen paying round. Otherwise, the payoff should be 0
points. So, we check the current round number and compare it against the
value we previously stored in ``session.vars``. We loop through both
players (``[P1,P2]``, or ``[mismatcher, matcher]``) and do the same
check for both of them.

.. code-block:: python

    class Group(BaseGroup):

        def set_payoffs(self):
            matcher = self.get_player_by_role('Matcher')
            mismatcher = self.get_player_by_role('Mismatcher')

            if matcher.penny_side == mismatcher.penny_side:
                matcher.is_winner = True
                mismatcher.is_winner = False
            else:
                matcher.is_winner = False
                mismatcher.is_winner = True
            for player in [mismatcher, matcher]:
                if (self.subsession.round_number ==
                    self.session.vars['paying_round'] and player.is_winner):
                        player.payoff = Constants.stakes
                else:
                    player.payoff = c(0)

Define the templates and views
------------------------------

This game has 2 main pages:

-  A ``Choice`` page that gets repeated for each round. The user is asked to choose heads/tails, and they are
   also shown a "history box" showing the results of previous rounds.
-  A ``ResultsSummary`` page that only gets displayed once at the end, and
   tells the user their final payoff.

Choice
~~~~~~

In ``views.py``, we define the ``Choice`` page. This page should contain
a form field that sets ``player.penny_side``, so we set ``form_model``
and ``form_fields``.

Also, on this page we would like to display a "history box" table that
shows the result of all previous rounds. So, we can use
``player.in_previous_rounds()``, which returns a list referring to the
same participant in rounds 1, 2, 3, etc. (For more on the distinction
between "player" and "participant", see :ref:`participants_and_players`.)

.. code-block:: python

    class Choice(Page):

        form_model = models.Player
        form_fields = ['penny_side']

        def vars_for_template(self):
            return {
                'player_in_previous_rounds': self.player.in_previous_rounds(),
            }

We then create a template ``Choice.html`` below. This is similar to the
templates we have previously created, but note the ``{% for %}`` loop
that creates all rows in the history table. ``{% for %}`` is part of the
Django template language.

.. code-block:: html+django

    {% extends "global/Base.html" %}
    {% load staticfiles otree_tags %}

    {% block title %}
        Round {{ subsession.round_number }} of {{ Constants.num_rounds }}
    {% endblock %}

    {% block content %}

        <h4>Instructions</h4>
        <p>
            This is a matching pennies game.
            Player 1 is the 'Mismatcher' and wins if the choices mismatch;
            Player 2 is the 'Matcher' and wins if they match.

        </p>

        <p>
            At the end, a random round will be chosen for payment.
        </p>

        <h4>Round history</h4>
        <table class="table">
            <tr>
                <th>Round</th>
                <th>Player and outcome</th>
            </tr>
            {% for p in player_in_previous_rounds %}
                <tr>
                    <td>{{ p.subsession.round_number }}</td>
                    <td>
                        You were the {{ p.role }} and {% if p.is_winner %}
                        won {% else %} lost {% endif %}
                    </td>
                </tr>
            {% endfor %}
        </table>

        <p>
            In this round, you are the {{ player.role }}.
        </p>

        {% formfield player.penny_side with label="I choose:" %}

        {% next_button %}

    {% endblock %}

ResultsWaitPage
~~~~~~~~~~~~~~~

Before a player proceeds to the next
round's ``Choice`` page,  they need to wait for the other player to complete the ``Choice`` page as well.  So, as usual, we use a ``WaitPage``.
Also, once both players have arrived at the wait page, we call the ``set_payoffs``
method we defined earlier.

::

    class ResultsWaitPage(WaitPage):

        def after_all_players_arrive(self):
            self.group.set_payoffs()

ResultsSummary
~~~~~~~~~~~~~~

Let's create ``ResultsSummary.html``:

.. code-block:: html+django

    {% extends "global/Base.html" %}
    {% load staticfiles otree_tags %}

    {% block title %}
        Final results
    {% endblock %}

    {% block content %}

        <table class="table">
            <tr>
                <th>Round</th>
                <th>Player and outcome</th>
            </tr>
            {% for p in player_in_all_rounds %}
                <tr>
                    <td>{{ p.subsession.round_number }}</td>
                    <td>
                        You were the {{ p.role }} and {% if p.is_winner %} won
                        {% else %} lost {% endif %}
                    </td>
                </tr>
            {% endfor %}
        </table>

        <p>
            The paying round was {{ paying_round }}.
            Your total payoff is therefore {{ total_payoff }}.
        </p>


    {% endblock %}

Now we define the corresponding class in views.py.

-  It only gets shown in the last round, so we set ``is_displayed``
   accordingly.
-  We retrieve the value of ``paying_round`` from ``session.vars``
-  We get the user's total payoff by summing up how much they made in
   each round.
-  We pass the round history to the template with
   ``player.in_all_rounds()``

In the ``Choice`` page we used ``in_previous_rounds``, but here we use
``in_all_rounds``. This is because we also want to include the result of
the current round.

.. code-block:: python

    class ResultsSummary(Page):

        def is_displayed(self):
            return self.subsession.round_number == Constants.num_rounds

        def vars_for_template(self):

            return {
                'total_payoff': sum([p.payoff
                                     for p in self.player.in_all_rounds()]),
                'paying_round': self.session.vars['paying_round'],
                'player_in_all_rounds': self.player.in_all_rounds(),
            }

The payoff is calculated in a Python "list comprehension". These are
frequently used in the oTree sample games, so if you are curious you can
read online about how list comprehensions work. The same code could be
written as:

.. code-block:: python

    total_payoff = 0
    for p in self.player.in_all_rounds():
       total_payoff += p.payoff

    return {
        'total_payoff': total_payoff,
        ...

Page sequence
~~~~~~~~~~~~~

Now we define the ``page_sequence``:

.. code-block:: python

    page_sequence = [
        Choice,
        ResultsWaitPage,
        ResultsSummary
    ]

This page sequence will loop for each round. However, ``ResultsSummary``
is skipped in every round except the last, because of how we set
``is_displayed``, resulting in this sequence of pages:

-  Choice [Round 1]
-  ResultsWaitPage [Round 1]
-  Choice [Round 2]
-  ResultsWaitPage [Round 2]
-  Choice [Round 3]
-  ResultsWaitPage [Round 3]
-  Choice [Round 4]
-  ResultsWaitPage [Round 4]
-  ResultsSummary [Round 4]


Add an entry to ``SESSION_CONFIGS`` in ``settings.py``
------------------------------------------------------

When we run a real experiment in the lab, we will want multiple groups,
but to test the demo we just set ``num_demo_participants`` to 2, meaning
there will be 1 group.

.. code-block:: python

    {
        'name': 'my_matching_pennies',
        'display_name': "My Matching Pennies (tutorial version)",
        'num_demo_participants': 2,
        'app_sequence': [
            'my_matching_pennies',
        ],
    },

Reset the database and run
--------------------------

.. code-block:: bash

    $ otree resetdb
    $ otree runserver
