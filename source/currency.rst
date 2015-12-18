.. _currency:

Money and Points
================

In many experiments, participants play for currency:
either virtual points, or real money. oTree supports both scenarios;
you can switch from points to real money by setting ``USE_POINTS = False``
in ``settings.py``.

You can specify the payment currency in ``settings.py``, by setting
``REAL_WORLD_CURRENCY_CODE`` to "USD", "EUR", "GBP", and so on. This
means that all currency amounts the participants see will be
automatically formatted in that currency, and at the end of the session
when you print out the payments page, amounts will be displayed in that
currency. The session's ``participation_fee`` is also displayed in this
currency code.

In oTree apps, currency values have their own data type. You can define
a currency value with the ``c()`` function, e.g. ``c(10)`` or ``c(0)``.
Correspondingly, there is a special model field for currency values:
``CurrencyField``.

Each player has a ``payoff`` field,
which is a ``CurrencyField``. Its initial value is ``None``.
If you want to initialize it to 0, you should do so in
``before_session_starts``, e.g.:

.. code-block:: python

  def before_session_starts(self):
      for p in self.get_players():
          p.payoff = 0

Currency values work just like numbers
(you can do mathematical operations like addition, multiplication, etc),
but when you pass them to an HTML template, they are automatically
formatted as currency. For example, if you set
``player.payoff = c(1.20)``, and then pass it to a template, it will be
formatted as ``$1.20`` or ``1,20 €``, etc., depending on your
``REAL_WORLD_CURRENCY_CODE`` and ``LANGUAGE_CODE`` settings.

Money amounts are expressed with 2 decimal places by default;
you can change this with the setting ``REAL_WORLD_CURRENCY_DECIMAL_PLACES``.

Note: instead of using Python's built-in ``range`` function, you should
use oTree's ``currency_range`` with currency values. It takes 3
arguments (start, stop, step), just like range. However, note that it is
an inclusive range. For example,
``currency_range(c(0), c(0.10), c(0.02))`` returns something like:

.. code-block:: python

    [Money($0.00), Money($0.02), Money($0.04),
     Money($0.06), Money($0.08), Money($0.10)]


In templates, instead of using the ``c()`` function, you should use the
``|c`` filter.
For example, ``{{ 20|c }}`` displays as ``20 points``.


Assigning payoffs
-----------------

Each player has a ``payoff`` field, which is a ``CurrencyField``. If
your player makes money, you should store it in this field.
``player.participant.payoff`` is the sum of the payoffs a participant
made in each subsession (either in points or real money).
At the end of the experiment, a participant's
total profit can be accessed by ``participant.money_to_pay()``; it is
calculated by converting ``participant.payoff`` to real-world currency
(if ``USE_POINTS`` is ``True``), and then adding
``self.session.config['participation_fee']``.


Points (i.e. "experimental currency")
-------------------------------------

Sometimes it is preferable for players to play games for points or
"experimental currency units", which are converted to real money at the
end of the session. You can set ``USE_POINTS = True`` in
``settings.py``, and then in-game currency amounts will be expressed in
points rather than dollars or euros, etc.

For example, ``c(10)`` is displayed as ``10 points``. You can specify
the conversion rate to real money in ``settings.py`` by providing a
``real_world_currency_per_point`` key in the session config dictionary.
For example, if you pay the user 2 cents per point, you would set
``real_world_currency_per_point = 0.02``.

Points are integers by default. You can change this by setting ``POINTS_DECIMAL_PLACES``
in ``settings.py``.
(e.g. set it to 2 if you want 2 decimal places, so you can get amounts like ``3.14 points``).

You can change the name "points" to something else like "tokens" or "credits", by setting ``POINTS_CUSTOM_NAME``.
(However, if you switch your language setting to one of oTree's supported languages, the name "points" is automatically translated,
e.g. "puntos" in Spanish.)

.. versionadded:: 0.3.30

Converting points to real world currency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can convert a point amount to money using the
``to_real_world_currency()`` method. In the above example, that would be:

.. code-block:: python

    >>> c(10).to_real_world_currency(self.session)
    $0.20

This method requires that ``self.session`` be passed as an argument, because
different sessions can have different conversion rates).
