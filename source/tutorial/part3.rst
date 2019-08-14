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
`here <https://github.com/oTree-org/oTree/tree/master/matching_pennies>`__.


Create the app
--------------

Create an app called ``my_matching_pennies``.


Constants
---------

We define our constants as we have previously. Matching pennies is a
2-person game and the payoff for winning a paying round is 1000 points.
In this case, the game has 4 rounds, so we set ``num_rounds`` (see :ref:`rounds`).

.. code-block:: python

    class Constants(BaseConstants):
        name_in_url = 'my_matching_pennies'
        players_per_group = 2
        num_rounds = 4
        stakes = c(1000)

Player
------

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
        penny_side = models.StringField(
            choices=['Heads', 'Tails'],
            widget=widgets.RadioSelect
        )

        is_winner = models.BooleanField()

        def role(self):
            if self.id_in_group == 1:
                return 'Mismatcher'
            if self.id_in_group == 2:
                return 'Matcher'

Subsession
----------

Now let's define the code to randomly choose a round for payment.

Create a method on the Subsession called ``creating_session``
(see :ref:`creating_session`).

We start by choosing a random integer between 1 and 4:

.. code-block:: python

    class Subsession(BaseSubsession):

        def creating_session(self):
            import random
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
            print('set the paying round to', paying_round)

There is a slight mistake, however. Because there are 4 rounds (i.e.
subsessions), this code will get executed 4 times, e.g.::

    set the paying round to 2
    set the paying round to 4
    set the paying round to 3
    set the paying round to 1

Each time, it will unnecessarily overwrite the previous value of
``session.vars['paying_round']``. We can fix this with an ``if`` statement:

.. code-block:: python

    class Subsession(BaseSubsession):

        def creating_session(self):
            import random
            print('in creating_session')
            if self.round_number == 1:
                paying_round = random.randint(1, Constants.num_rounds)
                self.session.vars['paying_round'] = paying_round
                print('set the paying round to', paying_round)

In round 3, let's swap roles,
and in round 4, use ``group_like_round(3)`` to copy the group structure from round 3.
(See :ref:`group_like_round <group_like_round>`):

.. code-block:: python

    class Subsession(BaseSubsession):

        def creating_session(self):
            import random
            print('in creating_session')
            if self.round_number == 1:
                paying_round = random.randint(1, Constants.num_rounds)
                self.session.vars['paying_round'] = paying_round
                print('set the paying round to', paying_round)
            if self.round_number == 3:
                # reverse the roles
                matrix = self.get_group_matrix()
                for row in matrix:
                    row.reverse()
                self.set_group_matrix(matrix)
            if self.round_number > 3:
                self.group_like_round(3)

(You can learn more about group shuffling in :ref:`shuffling`.)

Group
-----

Go to your ``Group`` class and add a method called ``set_payoffs``
(you can choose another name).
Below we use ``get_player_by_role`` to fetch each of the 2 players in the group,
and decide the winner:

.. code-block:: python

    class Group(BaseGroup):
        def set_payoffs(self):
            print('in set_payoffs')
            matcher = self.get_player_by_role('Matcher')
            mismatcher = self.get_player_by_role('Mismatcher')

            if matcher.penny_side == mismatcher.penny_side:
                matcher.is_winner = True
                mismatcher.is_winner = False
            else:
                matcher.is_winner = False
                mismatcher.is_winner = True

Now let's set payoffs.
A player should only receive a payoff if the current round is
the randomly chosen paying round.
So, we check the current round number and compare it against the
value we previously stored in ``session.vars``. We loop through both
players (``[P1,P2]``, or ``[mismatcher, matcher]``) and do the same
check for both of them.

.. code-block:: python

    class Group(BaseGroup):
        def set_payoffs(self):
            print('in set_payoffs')
            matcher = self.get_player_by_role('Matcher')
            mismatcher = self.get_player_by_role('Mismatcher')

            if matcher.penny_side == mismatcher.penny_side:
                matcher.is_winner = True
                mismatcher.is_winner = False
            else:
                matcher.is_winner = False
                mismatcher.is_winner = True
            for player in [mismatcher, matcher]:
                if self.subsession.round_number == self.session.vars['paying_round'] and player.is_winner:
                    player.payoff = Constants.stakes
                else:
                    player.payoff = c(0)

Define the templates and pages
------------------------------

This game has 2 main pages:

-  A ``Choice`` page that gets repeated for each round. The user is asked to choose heads/tails, and they are
   also shown a "history box" showing the results of previous rounds.
-  A ``ResultsSummary`` page that only gets displayed once at the end, and
   tells the user their final payoff.

Choice page
~~~~~~~~~~~

Create a ``Choice`` page.
``vars_for_template`` returns a variable ``player_in_previous_rounds``,
so we can get the data for to get their data from rounds 1, 2, 3, etc.

.. code-block:: python

    class Choice(Page):
        form_model = 'player'
        form_fields = ['penny_side']

        def vars_for_template(self):
            return dict(
                player_in_previous_rounds=self.player.in_previous_rounds()
            )

Next, create the HTML template as before:
In the ``title`` block:

.. code-block:: html+django

    Round {{ subsession.round_number }} of {{ Constants.num_rounds }}

In the ``content`` block:

.. code-block:: html+django

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
                <td>{{ p.round_number }}</td>
                <td>You were the {{ p.role }} and {% if p.is_winner %} won {% else %} lost {% endif %}</td>
            </tr>
        {% endfor %}
    </table>

    <p>
        In this round, you are the {{ player.role }}.
    </p>

    {% formfield player.penny_side label="I choose:" %}

    {% next_button %}


ResultsWaitPage
~~~~~~~~~~~~~~~

Before a player proceeds to the next
round's ``Choice`` page,  they need to wait for the other player to complete the ``Choice`` page as well.
So, as usual, we use a ``WaitPage``.
Also, once both players have arrived at the wait page, we call the ``set_payoffs``
method we defined earlier.

.. code-block:: python

    class ResultsWaitPage(WaitPage):

        def after_all_players_arrive(self):
            self.group.set_payoffs()

ResultsSummary
~~~~~~~~~~~~~~

Create a page called "ResultsSummary".

Notes:

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
            return self.round_number == Constants.num_rounds

        def vars_for_template(self):
            return dict(
                total_payoff=sum([p.payoff for p in self.player.in_all_rounds()]),
                paying_round=self.session.vars['paying_round'],
                player_in_all_rounds=self.player.in_all_rounds()
            )

Now let's create the HTML template.
Set the ``title`` block to "Final results", and the ``content`` block to:

.. code-block:: html+django

    <table class="table">
        <tr>
            <th>Round</th>
            <th>Player and outcome</th>
        </tr>
        {% for p in player_in_all_rounds %}
            <tr>
                <td>{{ p.round_number }}</td>
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


Page sequence
~~~~~~~~~~~~~

Your ``page_sequence`` should look like this:

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


Add an entry to your ``SESSION_CONFIGS``
----------------------------------------

When we run a real experiment in the lab, we will want multiple groups,
but to test the demo we just set ``num_demo_participants`` to 2, meaning
there will be 1 group.

-   name: my_matching_pennies
-   display_name: My Matching Pennies (tutorial version)
-   num_demo_participants: 2
-   app_sequence: ['my_matching_pennies']
