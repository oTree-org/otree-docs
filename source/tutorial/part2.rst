Part 2: Public goods game
=========================

(A video of this tutorial is on
`YouTube <https://www.youtube.com/channel/UCR9BIa4PqQJt1bjXoe7ffPg/videos>`__
)

We will now create a simple `public goods game <https://en.wikipedia.org/wiki/Public_goods_game>`__.
The public goods game is a classic game in economics.

This is a three player game where each player is initially endowed with 100 points.
Each player individually makes a decision about how many of their points they want to contribute to the group.
The combined contributions are multiplied by 2, and then divided evenly three ways and redistributed back to the players.

The full code for the app we will write is
`here <https://github.com/oTree-org/oTree/tree/master/public_goods_simple>`__.


Create the app
--------------

Just as in the previous part of the tutorial, create another app, called ``my_public_goods``.


Constants
---------

Go to your app's Constants.
(For more info, see :ref:`constants`.)

-   Set ``players_per_group`` to 3.
    oTree will then automatically divide players into groups of 3.
-   The endowment to each player is 1000 points. So, let's define
    ``endowment`` and set it to a currency value of ``1000``.
-   Each contribution is multiplied by 2. So define an integer
    constant called ``multiplier = 2``:

Now we have the following constants:

.. code-block:: Python

    players_per_group = 3
    num_rounds = 1
    endowment = c(1000) # c() means it's a currency
    multiplier = 2


After the game is played,
what data points will we need about each player?
It's important to record how much each person contributed.
So, go to the Player model and define a ``contribution`` column:

.. code-block:: python

    class Player(BasePlayer):
        contribution = models.CurrencyField(
            min=0,
            max=Constants.endowment,
            label="How much will you contribute?"
        )

We also need to record the payoff the user makes at the end of the game,
but we don't need to explicitly define a ``payoff`` field,
because in oTree, the Player already contains a ``payoff`` column.

What data points are we interested in recording about each group? We
might be interested in knowing the total contributions to the group, and
the individual share returned to each player. So, we define those 2
fields on the Group:

.. code-block:: python

    class Group(BaseGroup):
        total_contribution = models.CurrencyField()
        individual_share = models.CurrencyField()


Pages
-----

This game has 3 pages:

-  Page 1: players decide how much to contribute
-  Page 2: Wait page: players wait for others in their group
-  Page 3: players are told the results

Page 1: Contribute
~~~~~~~~~~~~~~~~~~

First let's define ``Contribute``. This page contains a form, so
we need to define ``form_model`` and ``form_fields``.
Specifically, this form should let you set the ``contribution``
field on the player. (For more info, see :ref:`forms`.)

.. code-block:: python

    class Contribute(Page):

        form_model = 'player'
        form_fields = ['contribution']

Now, we create the HTML template.

Set the ``title`` block to ``Contribute``, 
and the ``content`` block to:

.. code-block:: html+django

    <p>
        This is a public goods game with
        {{ Constants.players_per_group }} players per group,
        an endowment of {{ Constants.endowment }},
        and a multiplier of {{ Constants.multiplier }}.
    </p>

    {% formfields %}

    {% next_button %}


Page 2: ResultsWaitPage
~~~~~~~~~~~~~~~~~~~~~~~

When all players have completed the ``Contribute`` page,
the players' payoffs can be calculated.
Go to your Group model and add a method called ``set_payoffs``
(note that ``self`` refers to the group):

.. code-block:: python

    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = self.total_contribution * Constants.multiplier / Constants.players_per_group
        for p in players:
            p.payoff = Constants.endowment - p.contribution + self.individual_share

After a player makes a
contribution, they cannot see the results page right away; they first
need to wait for the other players to contribute. You therefore need to
add a ``WaitPage``. Let's call it ``ResultsWaitPage``.
When a player arrives at a wait page,
they must wait until all other players in the group have arrived.
Then everyone can proceed to the next page. (For more info, see :ref:`wait_pages`).

Add ``after_all_players_arrive`` method to ``ResultsWaitPage``,
and set it to trigger the ``set_payoffs`` method:

.. code-block:: python

    after_all_players_arrive = 'set_payoffs'

Page 3: Results
~~~~~~~~~~~~~~~

Now we create a page called ``Results``.
Set the template's content to:

.. code-block:: html+django

    <p>
        You started with an endowment of {{ Constants.endowment }},
        of which you contributed {{ player.contribution }}.
        Your group contributed {{ group.total_contribution }},
        resulting in an individual share of {{ group.individual_share }}.
        Your profit is therefore {{ player.payoff }}.
    </p>

    {% next_button %}

Page sequence
-------------

Make sure your page_sequence is correct:

.. code-block:: python

    page_sequence = [
        Contribute,
        ResultsWaitPage,
        Results
    ]


Define the session config
-------------------------

We add another session config with ``my_public_goods`` in the app sequence.


Run the code
------------

Load the project again then open your browser to ``http://localhost:8000``.

.. _print_debugging:

Troubleshoot with print()
-------------------------

I often read messages on programming forums like,
"My program is not working. I can't find the mistake,
even though I have spent hours looking at my code".

The solution is not to re-read the code until you find an error;
it's to interactively **test** your program.

The simplest way is using ``print()`` statements.
If you don't learn this technique, you won't be able to program games effectively.

You just need to insert a line in your code like this:

.. code-block:: python

    print('group.total_contribution is', self.group.total_contribution)

Put this line in the part of your code that's not working,
such as the payoff method defined above.
When you play the game in your browser and that code gets executed,
your print statement will be displayed in your command prompt window
(not in your web browser).

You can sprinkle lots of prints in your code

.. code-block:: python

    print('in payoff function')
    contributions = [p.contribution for p in players]
    print('contributions:', contributions)
    group.total_contribution = sum(contributions)
    group.individual_share = group.total_contribution * Constants.multiplier / Constants.players_per_group
    print('individual share', group.individual_share)
    for p in players:
        print('payoff before', p.payoff)
        p.payoff = Constants.endowment - p.contribution + group.individual_share
        print('payoff after', p.payoff)


If you don't see the output in your console window,
that means your code is not getting executed! (Which is why it isn't working.)

Maybe it's because your code is inside an "if" statement that is always ``False``.
Or maybe your code is in a method that never gets called (executed).
