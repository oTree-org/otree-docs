Part 3: Trust game
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

Just as in the previous part of the tutorial, create another app, called ``my_trust``.

Constants
---------

Go to your app's Constants.

First we define our app's constants. The endowment is 10 points and the
donation gets tripled.


.. code-block:: python

    class Constants(BaseConstants):
        name_in_url = 'my_trust'
        players_per_group = 2
        num_rounds = 1

        endowment = c(10)
        multiplication_factor = 3

Models
------

Then we add fields to player and group. There are 2
critical data points to record: the "sent" amount from P1, and the
"sent back" amount from P2.

Your first instinct may be to define the fields on the Player like this:

.. code-block:: python

    # Don't copy paste this
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

        sent_amount = models.CurrencyField(
            label="How much do you want to send to participant B?"
        )
        sent_back_amount = models.CurrencyField(
            label="How much do you want to send back?"
        )

We also define a method called ``sent_back_amount_choices`` to populate the
dropdown menu dynamically. This is the feature called
``{field_name}_choices``, which is explained here: :ref:`dynamic_validation`.

.. code-block:: python

        def sent_back_amount_choices(self):
            return currency_range(
                c(0),
                self.sent_amount * Constants.multiplication_factor,
                c(1)
            )

Define the templates and pages
------------------------------

We need 3 pages:

-  P1's "Send" page
-  P2's "Send back" page
-  "Results" page that both users see.

Send page
~~~~~~~~~

.. code-block:: python

    class Send(Page):

        form_model = 'group'
        form_fields = ['sent_amount']

        def is_displayed(self):
            return self.player.id_in_group == 1

We use :ref:`is_displayed` to only show this to P1; P2 skips the
page. For more info on ``id_in_group``, see :ref:`groups`.

For the template, set the ``title`` to ``Trust Game: Your Choice``,
and ``content`` to:

.. code-block:: django

    <p>
    You are Participant A. Now you have {{Constants.endowment}}.
    </p>

    {% formfields %}

    {% next_button %}


SendBack.html
~~~~~~~~~~~~~

This is the page that P2 sees to send money back.
Set the ``title`` block to ``Trust Game: Your Choice``, 
and the ``content`` block to:

.. code-block:: html+django

    <p>
        You are Participant B. Participant A sent you {{group.sent_amount}}
        and you received {{tripled_amount}}.
    </p>

    {% formfields %}

    {% next_button %}


Here is the page code. Notes:

-  We use :ref:`vars_for_template` to pass the variable ``tripled_amount``
   to the template. You cannot do calculations directly in the HTML code,
   so this number needs to be calculated in Python code and
   passed to the template.

.. code-block:: python

    class SendBack(Page):

        form_model = 'group'
        form_fields = ['sent_back_amount']

        def is_displayed(self):
            return self.player.id_in_group == 2

        def vars_for_template(self):
            return dict(
                tripled_amount=self.group.sent_amount * Constants.multiplication_factor
            )

Results
~~~~~~~

The results page needs to look slightly different for P1 vs. P2. So, we
use the ``{% if %}`` statement
to condition on the current player's ``id_in_group``.
Set the ``title`` block to ``Results``, and the content block to:

.. code-block:: html+django

    {% if player.id_in_group == 1 %}
        <p>
            You sent Participant B {{ group.sent_amount }}.
            Participant B returned {{ group.sent_back_amount }}.
        </p>
    {% else %}
        <p>
            Participant A sent you {{ group.sent_amount }}.
            You returned {{ group.sent_back_amount }}.
        </p>

    {% endif %}

    <p>
    Therefore, your total payoff is {{ player.payoff }}.
    </p>

.. code-block:: python

    class Results(Page):
        pass


Wait pages and page sequence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add 2 wait pages:

-  ``WaitForP1`` (P2 needs to wait while P1 decides how much to send)
-  ``ResultsWaitPage`` (P1 needs to wait while P2 decides how much to send back)

After the second wait page, we should calculate the payoffs.
So, we define a method on the Group called ``set_payoffs``:

.. code-block:: python

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount

Then in ``ResultsWaitPage``, set ``after_all_players_arrive``:

.. code-block:: python

    after_all_players_arrive = 'set_payoffs'

Make sure they are ordered correctly in the page_sequence:

.. code-block:: python

    page_sequence = [
        Send,
        WaitForP1,
        SendBack,
        ResultsWaitPage,
        Results,
    ]

Add an entry to your ``SESSION_CONFIGS``
----------------------------------------

Create a session config with ``my_trust`` in the app sequence.

Run the server
--------------

Load the project again then open your browser to ``http://localhost:8000``.
