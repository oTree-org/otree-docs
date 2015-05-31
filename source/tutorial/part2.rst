Part 2: Trust game
==================

Now let's create a Trust game, and learn some
more features of oTree.

This is a trust game with 2 players.
To start, Player 1 receives 10 points; Player 2 receives nothing. Player
1 can send some or all of his points to Player 2. Before P2 receives
these points they will be tripled. Once P2 receives the tripled points he
can decide to send some or all of his points to P1.

The completed app is
`here <https://github.com/oTree-org/oTree/tree/master/trust_simple>`__.

Create the app
--------------

.. code-block:: bash

    $ python otree startapp trust_simple


Define models.py
----------------

First we define our app's constants. The endowment is 10 points and the
donation gets tripled.


.. code-block:: python

    class Constants:
        name_in_url = 'trust_simple'
        players_per_group = 2
        num_rounds = 1

        endowment = c(10)
        multiplication_factor = 3

Then we think about how to define fields on the data model. There are 2
critical data points to capture: the "sent" amount from P1, and the
"sent back" amount from P2.

Your first instinct may be to define the fields on the Player like this:

.. code-block:: python

    class Player(otree.models.BasePlayer):

        # <built-in>
        ...
        # </built-in>

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

    class Group(otree.models.BaseGroup):

        # <built-in>
        ...
        # </built-in>

        sent_amount = models.CurrencyField()
        sent_back_amount = models.CurrencyField()

Even though it may not seem that important at this point, modeling our
data correctly will make the rest of our work easier.

Let's let P1 choose from a dropdown menu how
much to donate, rather than entering free text. To do this, we use the
``choices=`` argument, as well as the ``currency_range`` function:

.. code-block:: python

    sent_amount = models.CurrencyField(
        choices=currency_range(0, Constants.endowment, c(1)),
    )


We'd also like P2 to use a dropdown menu to choose how much to send
back, but we can't specify a fixed list of ``choices``, because P2's
available choices depend on how much P1 donated. I'll show a bit later
how we can make this list dynamic.

Also, let's define the payoff function on the group:

.. code-block:: python

        def set_payoffs(self):
            p1 = self.get_player_by_id(1)
            p2 = self.get_player_by_id(2)
            p1.payoff = (
                Constants.endowment -
                self.sent_amount +
                self.sent_back_amount
            )
            p2.payoff = (
                self.sent_amount *
                Constants.multiplication_factor -
                self.sent_back_amount
            )


Define the templates and views
------------------------------

We need 3 pages:

-  P1's "Send" page
-  P2's "Send back" page
-  "Results" page that both users see.

It would also be good if game instructions appeared on each page so that
players are clear how the game works. We can define a file
``Instructions.html`` that gets included on each page.

Instructions.html
~~~~~~~~~~~~~~~~~

This template uses Django's template inheritance with the
``{% extends %}`` command. The file it inherits from is located at
 ``_templates/global/Instructions.html``.

For basic apps you don't need to know the
details of how template inheritance works.

.. code-block:: django

    {% extends "global/Instructions.html" %}

    {% block instructions %}
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
    {% endblock %}

Send
~~~~

This page looks like the templates we have seen so far. Note the use of
``{% include %}`` to automatically insert another template.

.. code-block:: django

    {% extends "global/Base.html" %}
    {% load staticfiles otree_tags %}

    {% block title %}
        Trust Game: Your Choice
    {% endblock %}

    {% block content %}

        {% include 'trust_simple/Instructions.html' %}

        <p>
        You are Participant A. Now you have {{Constants.endowment}}.
        </p>

        {% formfield group.sent_amount with label="How much do you want to send to participant B?" %}

        {% next_button %}

    {% endblock %}

We also define the view in views.py:

.. code-block:: python

    class Send(Page):

        form_model = models.Group
        form_fields = ['sent_amount']

        def is_displayed(self):
            return self.player.id_in_group == 1

The ``{% formfield %}`` in the template must match the ``form_model``
and ``form_fields`` in the view.

Also, we use ``is_displayed`` to only show this to P1; P2 skips the
page.

SendBack
~~~~~~~~

This is the page that P2 sees to send money back. Here is the template:

.. code-block:: django

    {% extends "global/Base.html" %}
    {% load staticfiles otree_tags %}

    {% block title %}
        Trust Game: Your Choice
    {% endblock %}

    {% block content %}

        {% include 'trust_simple/Instructions.html' %}

    <p>
    You are Participant B. Participant A sent you {{group.sent_amount}} and you received {{tripled_amount}}.
    </p>

        {% formfield group.sent_back_amount with label="How much do you want to send back?" %}

        {% next_button %}

    {% endblock %}

Here is the code from views.py. Notes:

-  We use ``vars_for_template`` to pass the variable ``tripled_amount``
   to the template. Django does not let you do calculations directly in
   a template, so this number needs to be calculated in Python code and
   passed to the template.
-  We define a method ``sent_back_amount_choices`` to populate the
   dropdown menu dynamically. This is the feature called
   ``{field_name}_choices``, which is explained in the reference
   documentation.

.. code-block:: python

    class SendBack(Page):

        form_model = models.Group
        form_fields = ['sent_back_amount']

        def is_displayed(self):
            return self.player.id_in_group == 2

        def vars_for_template(self):
            return {
                'tripled_amount': self.group.sent_amount *
                                  Constants.multiplication_factor
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

.. code-block:: django

    {% extends "global/Base.html" %}
    {% load staticfiles otree_tags %}

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
        Therefore, your total payoff is {{player.payoff}}.
        </p>

        {% include 'trust_simple/Instructions.html' %}

    {% endblock %}

Here is the Python code for this page in views.py:

.. code-block:: python

    class Results(Page):

        def vars_for_template(self):
            return {
                'tripled_amount': self.group.sent_amount *
                                  Constants.multiplication_factor
            }

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
            self.group.set_payoffs()

Then we define the page sequence:

.. code-block:: python

    page_sequence = [
        Send,
        WaitForP1,
        SendBack,
        ResultsWaitPage,
        Results,
    ]

Add an entry to ``SESSION_TYPES`` in ``settings.py``
----------------------------------------------------

.. code-block:: python

    {
        'name': 'trust_simple',
        'display_name': "Trust Game (simple version from tutorial)",
        'num_demo_participants': 2,
        'app_sequence': ['trust_simple'],
    },

Reset the database and run
--------------------------

If you are on the command line, enter:

.. code-block:: bash

    $ python otree resetdb
    $ python otree runserver

If you are using the launcher, click the button equivalents to these
commands.

Then open your browser to ``http://127.0.0.1:8000`` to play the game.
