Part 2: Trust game
==================

Now let's create a 2-player `Trust game <https://en.wikibooks.org/wiki/Bestiary_of_Behavioral_Economics/Trust_Game>`__,
and learn some more features of oTree.

To start, Player 1 receives 10 points; Player 2 receives nothing. Player
1 can send some or all of his points to Player 2. Before P2 receives
these points they will be tripled. Once P2 receives the tripled points he
can decide to send some or all of his points to P1.

The completed app is
`here <https://github.com/oTree-org/oTree/tree/master/trust_simple>`__.

Create the app
--------------

.. code-block:: bash

    $ otree startapp my_trust


Define models.py
----------------

First we define our app's constants. The endowment is 10 points and the
donation gets tripled.


.. code-block:: python

    class Constants(BaseConstants):
        name_in_url = 'my_trust'
        players_per_group = 2
        num_rounds = 1

        endowment = c(10)
        multiplication_factor = 3

Then we add fields to player and group. There are 2
critical data points to record: the "sent" amount from P1, and the
"sent back" amount from P2.

Your first instinct may be to define the fields on the Player like this:

.. code-block:: python

    # Don't copy paste this...see below
    class Player(BasePlayer):

        sent_amount = models.CurrencyField()
        sent_back_amount = models.CurrencyField()

The problem with this model is that ``sent_amount`` only applies to P1,
and ``sent_back_amount`` only applies to P2. It does not make sense that
P1 should have a field called ``sent_back_amount``. How can we make our
data model more accurate?

We can do it by defining those fields at the ``Group`` level. This makes
sense because each group has exactly 1 ``sent_amount`` and exactly 1
``sent_back_amount``:

.. code-block:: python

    class Group(BaseGroup):

        sent_amount = models.CurrencyField()
        sent_back_amount = models.CurrencyField()

Let's let P1 choose from a dropdown menu how
much to donate, rather than entering free text. To do this, we use the
:ref:`choices <choices>` argument, as well as the :ref:`currency_range <currency>` function:

.. code-block:: python

    sent_amount = models.CurrencyField(
        choices=currency_range(0, Constants.endowment, c(1)),
    )


Define the templates and pages
------------------------------

We need 3 pages:

-  P1's "Send" page
-  P2's "Send back" page
-  "Results" page that both users see.

It would also be good if game instructions appeared on each page so that
players are clear how the game works.

Instructions.html
~~~~~~~~~~~~~~~~~

To create the instructions, we can define a file
``Instructions.html`` that gets included on each page.


.. code-block:: html+django

    {% load otree staticfiles %}

    <div class="instructions well well-lg">

        <h3 class="panel-sub-heading">
            Instructions
        </h3>
    <p>
        This is a trust game with 2 players.
    </p>
    <p>
        To start, participant A receives {{ Constants.endowment }};
        participant B receives nothing.
        Participant A can send some or all of his {{ Constants.endowment }} to participant B.
        Before B receives these points they will be tripled.
        Once B receives the tripled points he can decide to send some or all of his points to A.
    </p>
    </div>


Send.html
~~~~~~~~~

This page looks like the templates we have seen so far. Note the use of
``{% include %}`` to automatically insert another template.

.. code-block:: django

    {% extends "global/Page.html" %}
    {% load staticfiles otree %}

    {% block title %}
        Trust Game: Your Choice
    {% endblock %}

    {% block content %}

        {% include 'my_trust/Instructions.html' %}

        <p>
        You are Participant A. Now you have {{Constants.endowment}}.
        </p>

        {% formfield group.sent_amount label="How much do you want to send to participant B?" %}

        {% next_button %}

    {% endblock %}

We also define the page in pages.py:

.. code-block:: python

    class Send(Page):

        form_model = 'group'
        form_fields = ['sent_amount']

        def is_displayed(self):
            return self.player.id_in_group == 1

The ``{% formfield %}`` in the template must match the ``form_model``
and ``form_fields`` in the page.

Also, we use :ref:`is_displayed` to only show this to P1; P2 skips the
page. For more info on ``id_in_group``, see :ref:`groups`.

SendBack.html
~~~~~~~~~~~~~

This is the page that P2 sees to send money back. Here is the template:

.. code-block:: html+django

    {% extends "global/Page.html" %}
    {% load staticfiles otree %}

    {% block title %}
        Trust Game: Your Choice
    {% endblock %}

    {% block content %}

        {% include 'my_trust/Instructions.html' %}

        <p>
            You are Participant B. Participant A sent you {{group.sent_amount}}
            and you received {{tripled_amount}}.
        </p>

        {% formfield group.sent_back_amount label="How much do you want to send back?" %}

        {% next_button %}

    {% endblock %}

Here is the code from pages.py. Notes:

-  We use :ref:`vars_for_template` to pass the variable ``tripled_amount``
   to the template. Django does not let you do calculations directly in
   a template, so this number needs to be calculated in Python code and
   passed to the template.
-  We define a method ``sent_back_amount_choices`` to populate the
   dropdown menu dynamically. This is the feature called
   ``{field_name}_choices``, which is explained here: :ref:`dynamic_validation`.

.. code-block:: python

    class SendBack(Page):

        form_model = 'group'
        form_fields = ['sent_back_amount']

        def is_displayed(self):
            return self.player.id_in_group == 2

        def vars_for_template(self):
            return {
                'tripled_amount': self.group.sent_amount * Constants.multiplication_factor
            }

        def sent_back_amount_choices(self):
            return currency_range(
                c(0),
                self.group.sent_amount * Constants.multiplication_factor,
                c(1)
            )

Results
~~~~~~~

The results page needs to look slightly different for P1 vs. P2. So, we
use the ``{% if %}`` statement (part of `Django's template
language <https://docs.djangoproject.com/en/1.7/topics/templates/>`__)
to condition on the current player's ``id_in_group``.

.. code-block:: html+django

    {% extends "global/Page.html" %}
    {% load staticfiles otree %}

    {% block title %}
        Results
    {% endblock %}

    {% block content %}

    {% if player.id_in_group == 1 %}
        <p>
            You sent Participant B {{ group.sent_amount }}.
            Participant B returned {{group.sent_back_amount}}.
        </p>
    {% else %}
        <p>
            Participant A sent you {{ group.sent_amount }}.
            You returned {{group.sent_back_amount}}.
        </p>

    {% endif %}

        <p>
        Therefore, your total payoff is {{ player.payoff }}.
        </p>

        {% include 'my_trust/Instructions.html' %}

    {% endblock %}

In pages.py, simply define the page like this:

.. code-block:: python

    class Results(Page):
        pass


Wait pages and page sequence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This game has 2 wait pages:

-  P2 needs to wait while P1 decides how much to send
-  P1 needs to wait while P2 decides how much to send back

After the second wait page, we should calculate the payoffs. So, we use
``after_all_players_arrive``.

So, we define these pages:

.. code-block:: python

    class WaitForP1(WaitPage):
        pass

    class ResultsWaitPage(WaitPage):

        def after_all_players_arrive(self):
            group = self.group
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p1.payoff = Constants.endowment - group.sent_amount + group.sent_back_amount
            p2.payoff = group.sent_amount * Constants.multiplication_factor - group.sent_back_amount

.. note::

    An equivalent way would be to define
    the payoff function in ``models.py`` like this
    (note that the group is called ``self`` in this context):

    .. code-block:: python

        class Group(BaseGroup):

            def set_payoffs(self):
                p1 = self.get_player_by_id(1)
                p2 = self.get_player_by_id(2)
                p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
                p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount

    Then, we could call it ("trigger it")
    in ``after_all_players_arrive`` like this:

    .. code-block:: python

        def after_all_players_arrive(self):
            self.group.set_payoffs()

    This is actually the technique that's used more in the sample games.
    Although it looks a bit more complex, you will see over time that putting your
    game's logic in ``models.py`` helps with organization.

    (Also note that the name ``set_payoffs`` is arbitrary.)

Then we define the page sequence:

.. code-block:: python

    page_sequence = [
        Send,
        WaitForP1,
        SendBack,
        ResultsWaitPage,
        Results,
    ]

Add an entry to ``SESSION_CONFIGS`` in ``settings.py``
------------------------------------------------------

.. code-block:: python

    {
        'name': 'my_trust',
        'display_name': "My Trust Game (simple version from tutorial)",
        'num_demo_participants': 2,
        'app_sequence': ['my_trust'],
    },

Run the server
--------------

Enter::

    otree devserver

Then open your browser to ``http://localhost:8000`` to play the game.
