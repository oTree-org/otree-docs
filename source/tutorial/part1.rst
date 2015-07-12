Part 1: Public goods game
=========================

We will now create a simple public goods game. The completed app is
`here <https://github.com/oTree-org/oTree/tree/master/public_goods_simple>`__.

Create the app
--------------

If you are running the oTree launcher, click the "terminal" button which will open your command window.
Otherwise, open the ``oTree`` folder you downloaded, the one that contains ``requirements_base.txt``.

In this directory, create the public goods app with this shell command:

.. code-block:: bash

    $ python otree startapp public_goods_simple

Then go to the folder ``public_goods_simple`` that was created.

Define models.py
----------------

Let's define our data model in ``models.py``.

First, let's modify the ``Constants`` class to define our constants and
parameters -- things that are the same for all players in all games.

-  There are 3 players per group. So, let's change ``players_per_group``
   to 3. oTree will then automatically divide players into groups of 3.
-  The endowment to each player is 100 points. So, let's define
   ``endowment`` and set it to ``c(100)``. (``c()`` means it is a
   currency amount; see the docs for more info).
-  Each contribution is multiplied by 1.8. So let's define
   ``efficiency_factor`` and set it to 1.8:

Now we have:

.. code-block:: Python

    class Constants:
        name_in_url = 'public_goods_simple'
        players_per_group = 3
        num_rounds = 1

        endowment = c(100)
        efficiency_factor = 1.8

Now let's think about the main entities in this game: the Player and the
Group.

What data points are we interested in recording about each player? The
main thing is how much they contributed. So, we define a field
``contribution``:

.. code-block:: python

        class Player(otree.models.BasePlayer):

        # ...

        contribution = models.CurrencyField(min=0, max=Constants.endowment)


What data points are we interested in recording about each group? We
might be interested in knowing the total contributions to the group, and
the individual share returned to each player. So, we define those 2
fields:

.. code-block:: python

        class Group(otree.models.BaseGroup):

        # ...

        total_contribution = models.CurrencyField()
        individual_share = models.CurrencyField()

We also need to define the logic for how these fields get calculated.
Let's define a method on the group called ``set_payoffs``:


.. code-block:: python

    class Group(otree.models.BaseGroup):

        # ...

        total_contribution = models.CurrencyField()
        individual_share = models.CurrencyField()

        def set_payoffs(self):
            self.total_contribution = sum([p.contribution
                                           for p in self.get_players()])
            self.individual_share = (
                self.total_contribution *
                Constants.efficiency_factor /
                Constants.players_per_group
            )
            for p in self.get_players():
                p.payoff = (
                    Constants.endowment -
                    p.contribution +
                    self.individual_share
                )

Define the template
-------------------

This game will have 2 pages.

-  Page 1: players decide how much to contribute
-  Page 2: players are told the results

So, let's make 2 HTML files under ``templates/public_goods_simple/``.

The first is ``Contribute.html``, which contains a brief explanation of
the game, and a form field where the player can enter their
contribution.

.. code-block:: html+django

    {% extends "global/Base.html" %} {% load staticfiles otree_tags %}

    {% block title %} Contribute {% endblock %}

    {% block content %}

    <p>
        This is a public goods game with
        {{ Constants.players_per_group }} players per group,
        an endowment of {{ Constants.endowment }},
        and an efficiency factor of {{ Constants.efficiency_factor }}.
    </p>


    {% formfield player.contribution with label="How much will you contribute?" %}

    {% next_button %}

    {% endblock %}


The second template will be called ``Results.html``.

.. code-block:: html+django

    {% extends "global/Base.html" %} {% load staticfiles otree_tags %}

    {% block title %} Results {% endblock %}

    {% block content %}

    <p>
        You started with an endowment of {{ Constants.endowment }},
        of which you contributed {{ player.contribution }}.
        Your group contributed {{ group.total_contribution }},
        resulting in an individual share of {{ group.individual_share }}.
        Your profit is therefore {{ player.payoff }}.
    </p>

    {% endblock %}



Define views.py
---------------

Now we define our views, which decide the logic for how to display the
HTML templates.

Since we have 2 templates, we need 2 ``Page`` classes in ``views.py``.
The names should match those of the templates (``Contribute`` and
``Results``).

First let's define ``Contribute``. We need to define ``form_model`` and
``form_fields`` to specify that this page contains a form letting you
set ``Player.contribution``:

.. code-block:: python

    class Contribute(Page):

        form_model = models.Player
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
Then everyone can proceed to the next page.

When all players have
completed the ``Contribute`` page, the players' payoffs can be
calculated. You can trigger this calculation inside the the
``after_all_players_arrive`` method on the ``WaitPage``, which
automatically gets called when all players have arrived at the wait
page. Another advantage of putting the code here is that it only gets
executed once, rather than being executed separately for each
participant, which is redundant.

We write ``self.group.set_payoffs()`` because earlier we decided to name
the payoff calculation method ``set_payoffs``, and it's a method under
the ``Group`` class. That's why we prefix it with ``self.group``.

.. code-block:: python

    class ResultsWaitPage(WaitPage):

        def after_all_players_arrive(self):
            self.group.set_payoffs()

Now we define ``page_sequence`` to specify the order in which the pages
are shown:

.. code-block:: python

    page_sequence = [
        Contribute,
        ResultsWaitPage,
        Results
    ]


Define the session config in settings.py
----------------------------------------

Now we go to ``settings.py`` and add an entry to ``SESSION_CONFIGS``.

.. note::

    Prior to oTree-core 0.3.11, "session config" was known as "session type".
    After you upgrade, you can rename ``SESSION_TYPES`` to ``SESSION_CONFIGS``,
    and so on.

In lab experiments, it's typical for users to fill out an exit survey, and
then see how much money they made. So let's do this by adding the
existing "exit survey" and "payment info" apps to ``app_sequence``.

.. code-block:: python

    SESSION_CONFIGS = [
        {
            'name': 'public_goods_simple',
            'display_name': "Public Goods (Simple Version)",
            'num_demo_participants': 3,
            'app_sequence': ['public_goods_simple', 'survey', 'payment_info'],
        },
        # ...

However, we must also remember to add a ``{% next_button %}`` element to
the ``Results.html``, so the user can click a button taking them to the
next app in the sequence.

Reset the database and run
--------------------------

Before you run the server, you need to reset the database. In the
launcher, click the button "clear the database". Or, on the command
line, run ``python otree resetdb``.

Every time you add, change, or remove a field in ``models.py`` This is
because we have defined new fields in ``models.py``, and the SQL
database needs to be re-generated to create these tables and columns.

Then, run the server and open your browser to http://127.0.0.1:8000 to
play the game.
