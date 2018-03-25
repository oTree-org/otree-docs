Part 1: Public goods game
=========================

We will now create a simple `public goods game <https://en.wikipedia.org/wiki/Public_goods_game>`__.
The public goods game is a classic game in economics.

This is a three player game where each player is initially endowed with 100 points.
Each player individually makes a decision about how many of their points they want to contribute to the group.
The combined contributions are multiplied by 2, and then divided evenly three ways and redistributed back to the players.

The full code for the app we will write is
`here <https://github.com/oTree-org/oTree/tree/master/public_goods_simple>`__.

Upgrade oTree
-------------

To ensure you are using the latest version of oTree, open your command window and run:

.. code-block:: bash

    pip3 install -U otree

Create the app
--------------

Use your command line to ``cd`` to the oTree project folder you created,
the one that contains ``requirements_base.txt``.

In this folder, create the public goods app:

.. code-block:: bash

    $ otree startapp my_public_goods

Then in PyCharm, go to the folder ``my_public_goods`` that was created.

Define models.py
----------------

Open ``models.py``. This file contains the game's data models (player, group, subsession)
and constant parameters.

First, let's modify the ``Constants`` class to define our constants and
parameters -- things that are the same for all players in all games.
(For more info, see :ref:`constants`.)

-  There are 3 players per group. So, change ``players_per_group``
   to 3. oTree will then automatically divide players into groups of 3.
-  The endowment to each player is 100 points. So, let's define
   ``endowment`` and set it to ``c(100)``. (``c()`` means it is a
   currency amount; see :ref:`currency`).
-  Each contribution is multiplied by 2. So let's define
   ``multiplier`` and set it to 2:

Now we have:

.. code-block:: Python

    class Constants(BaseConstants):
        name_in_url = 'my_public_goods'
        players_per_group = 3
        num_rounds = 1

        endowment = c(100)
        multiplier = 2

Now let's think about the main entities in this game: the Player and the
Group.

After the game is played,
what data points will we need about each player?
It's important to record how much each person contributed.
So, we define a field ``contribution``,
which is a currency (see :ref:`currency`):

.. code-block:: python

    class Player(BasePlayer):
        contribution = models.CurrencyField(min=0, max=Constants.endowment)

We also need to record the payoff the user makes at the end of the game,
but we don't need to explicitly define a ``payoff`` field, because it's automatically
added to every ``Player`` model.

What data points are we interested in recording about each group? We
might be interested in knowing the total contributions to the group, and
the individual share returned to each player. So, we define those 2
fields:

.. code-block:: python

    class Group(BaseGroup):
        total_contribution = models.CurrencyField()
        individual_share = models.CurrencyField()


Define the template
-------------------

This game has 2 pages:

-  Page 1: players decide how much to contribute
-  Page 2: players are told the results

In this section we will define the HTML templates to display the game.

So, let's make 2 HTML files under ``templates/my_public_goods/``.

The first is ``Contribute.html``, which contains a brief explanation of
the game, and a form field where the player can enter their
contribution.

.. code-block:: html+django

    {% extends "global/Page.html" %}
    {% load staticfiles otree %}

    {% block title %} Contribute {% endblock %}

    {% block content %}

        <p>
            This is a public goods game with
            {{ Constants.players_per_group }} players per group,
            an endowment of {{ Constants.endowment }},
            and a multiplier of {{ Constants.multiplier }}.
        </p>


        {% formfield player.contribution label="How much will you contribute?" %}

        {% next_button %}

    {% endblock %}


(For more info on how to write a template, see :ref:`templates`.)

The second template will be called ``Results.html``.
This page will be shown after the game finished,
after we have determined the user's payoff.
(later in this tutorial, we will define this payoff function).


.. code-block:: html+django

    {% extends "global/Page.html" %}
    {% load staticfiles otree %}

    {% block title %} Results {% endblock %}

    {% block content %}

        <p>
            You started with an endowment of {{ Constants.endowment }},
            of which you contributed {{ player.contribution }}.
            Your group contributed {{ group.total_contribution }},
            resulting in an individual share of {{ group.individual_share }}.
            Your profit is therefore {{ player.payoff }}.
        </p>

        {% next_button %}

    {% endblock %}



Define pages.py
---------------

Now we define our pages, which contain the logic for how to display the
HTML templates. (For more info, see :ref:`pages`.)

Since we have 2 templates, we need 2 ``Page`` classes in ``pages.py``.
The names should match those of the templates (``Contribute`` and
``Results``).

First let's define ``Contribute``. This page contains a form, so
we need to define ``form_model`` and ``form_fields``.
Specifically, this form should let you set the ``contribution``
field on the player. (For more info, see :ref:`forms`.)

.. code-block:: python

    class Contribute(Page):

        form_model = 'player'
        form_fields = ['contribution']

Now we define ``Results``. This page doesn't have a form so our class
definition can be empty (with the ``pass`` keyword).

.. code-block:: python

    class Results(Page):
        pass


We are almost done, but one more page is needed. After a player makes a
contribution, they cannot see the results page right away; they first
need to wait for the other players to contribute. You therefore need to
add a ``WaitPage``. When a player arrives at a wait page,
they must wait until all other players in the group have arrived.
Then everyone can proceed to the next page. (For more info, see :ref:`wait_pages`).

When all players have completed the ``Contribute`` page,
the players' payoffs can be calculated.
You can trigger this calculation inside the the
``after_all_players_arrive`` method on the ``WaitPage``, which
automatically gets called when all players have arrived at the wait
page. We can access the current group with ``self.group`` (for more info about
``self``, see :ref:`conceptual_overview`).

.. code-block:: python

    class ResultsWaitPage(WaitPage):

        def after_all_players_arrive(self):
            group = self.group
            players = group.get_players()
            contributions = [p.contribution for p in players]
            group.total_contribution = sum(contributions)
            group.individual_share = group.total_contribution * Constants.multiplier / Constants.players_per_group
            for p in players:
                p.payoff = Constants.endowment - p.contribution + group.individual_share


Now we specify the order in which the pages are shown:

.. code-block:: python

    page_sequence = [
        Contribute,
        ResultsWaitPage,
        Results
    ]


Define the session config in settings.py
----------------------------------------

Go to ``settings.py`` in the project's root folder and add an entry to ``SESSION_CONFIGS``.

.. code-block:: python

    SESSION_CONFIGS = [
        {
            'name': 'my_public_goods',
            'display_name': "My Public Goods (Simple Version)",
            'num_demo_participants': 3,
            'app_sequence': ['my_public_goods'],
        },
        # other session configs ...
    ]


Sync the database and run
-------------------------

Enter:

.. code-block:: bash

    $ otree devserver

Then open your browser to ``http://localhost:8000`` to play the game.

.. _print_debugging:

Troubleshoot with print()
-------------------------

I often read messages on programming forums like,
"My program is not working. I can't find the mistake,
even though I have spent hours looking at my code".

When an experienced programmer encounters an error in their program, they don't
just re-read the code until they find an error; they interactively **test**
their program.

The simplest way is using ``print()`` statements.
If you don't learn this technique, you won't be able to program games effectively.

You just need to insert a line in your code like this:

.. code-block:: python

    print('group.total_contribution is', self.group.total_contribution)

Put this line in the part of your code that's not working,
such as the payoff function defined above.
When you play the game in your browser and that code gets executed,
your print statement will be displayed in your command prompt window
(not in your web browser).

You can sprinkle lots of prints in your code
(I like to print extra characters like ``@@@``, to make it easier to
find the print statements in my server output):

.. code-block:: python

    print('@@@@ in payoff function')
    contributions = [p.contribution for p in players]
    print('@@@@ contributions:', contributions)
    group.total_contribution = sum(contributions)
    group.individual_share = group.total_contribution * Constants.multiplier / Constants.players_per_group
    print('@@@ individual share', group.individual_share)
    for p in players:
        print('@@@ payoff before', p.payoff)
        p.payoff = Constants.endowment - p.contribution + group.individual_share
        print('@@@ payoff after', p.payoff)


If you don't see the output in your console window,
that means your code is not getting executed! (Which is why it isn't working.)

Maybe it's because your code is inside an "if" statement that is always ``False``.
Or maybe your code is in a function that never gets called (executed).


Make changes while the server is running
----------------------------------------

Once you have the server running, try changing some text in
``Contribute.html`` or ``Results.html``,
then save the file and refresh your page. You will see the changes immediately.

Write a bot
-----------

Let's write a bot that simulates a player playing the game we just programmed.
Having a bot will save us a lot of work, because it can automatically test
that the game still works each time we make changes.

Go to ``tests.py``, and add this code in ``PlayerBot``:

.. code-block:: python

    class PlayerBot(Bot):

        def play_round(self):
            yield (pages.Contribute, {'contribution': c(42)})
            yield (pages.Results)

This bot first submits the Contribute page with a contribution of 42,
then submits the results page (to proceed to the next app).

From your command line, run::

    otree test my_public_goods

You will see the output of the bots in the command line.

To make the bot play in your web browser, go to ``settings.py``
and add ``'use_browser_bots': True`` to the session config, like this:

.. code-block:: python

    SESSION_CONFIGS = [
        {
            'name': 'my_public_goods',
            'display_name': "My Public Goods (Simple Version)",
            'num_demo_participants': 3,
            'app_sequence': ['my_public_goods'],
            'use_browser_bots': True
        },
        # other session configs ...
    ]

Now, when you create a new session and open the start links,
it will play automatically.

