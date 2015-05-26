Money and Points
================

In many experiments, participants play for currency: either virtual
points, or real money. oTree supports both scenarios. Participants can
be awarded a fixed base pay (i.e. participation fee). In addition, in
each subsession, they can be awarded an additional payoff.

You can specify the payment currency in ``settings.py``, by setting
``REAL_WORLD_CURRENCY_CODE`` to "USD", "EUR", "GBP", and so on. This
means that all currency amounts the participants see will be
automatically formatted in that currency, and at the end of the session
when you print out the payments page, amounts will be displayed in that
currency.

In oTree apps, currency values have their own data type. You can define
a currency value with the ``c()`` function, e.g. ``c(10)`` or ``c(0)``.
Correspondingly, there is a special model field for currency values:
``CurrencyField``. For example, each player has a ``payoff`` field,
which is a ``CurrencyField``. Currency values work just like numbers
(you can do mathematical operations like addition, multiplication, etc),
but when you pass them to an HTML template, they are automatically
formatted as currency. For example, if you set
``player.payoff = c(1.20)``, and then pass it to a template, it will be
formatted as ``$1.20`` or ``1,20 €``, etc., depending on your
``REAL_WORLD_CURRENCY_CODE`` and ``LANGUAGE_CODE`` settings.

Note: instead of using Python's built-in ``range`` function, you should
use oTree's ``currency_range`` with currency values. It takes 3
arguments (start, stop, step), just like range. However, note that it is
an inclusive range. For example,
``currency_range(c(0), c(0.10), c(0.02))`` returns something like:

.. code:: python

    [Money($0.00), Money($0.02), Money($0.04), Money($0.06), Money($0.08), Money($0.10)]


Assigning payoffs
-----------------

Each player has a ``payoff`` field, which is a ``CurrencyField``. If
your player makes money, you should store it in this field.
``player.participant.payoff`` is the sum of the payoffs a participant
made in each subsession. At the end of the experiment, a participant's
total profit is calculated by adding the fixed base pay to the
``payoff`` that participant earned as a player in each subsession.


Points (i.e. "experimental currency")
-------------------------------------

Sometimes it is preferable for players to play games for points or
"experimental currency units", which are converted to real money at the
end of the session. You can set ``USE_POINTS = True`` in
``settings.py``, and then in-game currency amounts will be expressed in
points rather than real money.

For example, ``c(10)`` is displayed as ``10 points``. You can specify
the conversion rate to real money in ``settings.py`` by providing a
``real_world_currency_per_point`` key in the session type dictionary.
For example, if you pay the user 2 cents per point, you would set
``real_world_currency_per_point = 0.02``.

You can convert a point amount to money using the
``to_real_world_currency()`` method, which takes as an argument the
current session (this is necessary because different sessions can have
different conversion rates).

Let's say ``real_world_currency_per_point = 0.02``

.. code:: python

    c(10) # evaluates to Currency(10 points)
    c(10).to_real_world_currency(self.session) # evaluates to $0.20
