.. _currency:

Currency and Decimal
====================

Currency
--------

In many experiments, participants play for currency:
either real money, or points. oTree supports both;
you can switch from points to real money by setting ``USE_POINTS = False``
in your settings.

You can write ``cu(42)`` to represent "42 currency units".
It works just like a number
(e.g. ``cu(0.1) + cu(0.2) == cu(0.3)``).
The advantage is that when it's displayed to users, it will automatically
be formatted as ``$0.30`` or ``0,30 €``, etc., depending on your
``REAL_WORLD_CURRENCY_CODE`` and ``LANGUAGE_CODE`` settings.

.. note::

    ``cu()`` is new in oTree 5. Previously, ``c()`` was used to denote currencies.
    Code that already uses ``c()`` will continue to work.
    More info `here <https://groups.google.com/g/otree/c/Bwv67asPIlo>`__.

Use ``CurrencyField`` to store currencies in the database.
For example:

.. code-block:: python

    class Player(BasePlayer):
        random_bonus = models.CurrencyField()

To make a list of currency amounts, use ``currency_range``:

.. code-block:: python

    currency_range(0, 0.10, 0.02)
    # this gives:
    # [$0.00, $0.02, $0.04, $0.06, $0.08, $0.10]

In templates, instead of using the ``cu()`` function, you should use the
``|cu`` filter.
For example, ``{{ 20|cu }}`` displays as ``20 points``.


.. _payoff:

payoffs
-------

Each player has a ``payoff`` field.
If your player makes money, you should store it in this field.
``participant.payoff`` automatically stores the sum of payoffs
from all subsessions. You can modify ``participant.payoff`` directly,
e.g. to round the final payoff to a whole number.

At the end of the experiment, a participant's
total profit can be accessed by ``participant.payoff_plus_participation_fee()``;
it is calculated by converting ``participant.payoff`` to real-world currency
(if ``USE_POINTS`` is ``True``), and then adding
``session.config['participation_fee']``.

.. _points:

Points (i.e. "experimental currency")
-------------------------------------

If you set ``USE_POINTS = True``, then currency amounts will be points instead of dollars/euros/etc.
For example, ``cu(10)`` is displayed as ``10 points`` (or ``10 puntos``, etc.)

You can decide the conversion rate to real money
by adding a ``real_world_currency_per_point`` entry to your session config.

Converting points to real world currency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can convert a points amount to money using the method
``.to_real_world_currency``. For example:

.. code-block:: python

    cu(10).to_real_world_currency(session)

(The ``session`` is necessary because
different sessions can have different conversion rates).

Decimal places
--------------

Money amounts are displayed with 2 decimal places.

On the other hand, points are integers.
This means amounts will get rounded to whole numbers,
like ``10`` divided by ``3`` is ``3``.
So, we recommend using point magnitudes high enough that you don't care about rounding error.
For example, set the endowment of a game to 1000 points, rather than 100.

.. _DecimalField:

DecimalField
============

.. note::

    To use this, you must install :ref:`v60` (``pip install otree --upgrade --pre``)

``DecimalField`` is based on the Python ``Decimal`` datatype,
which can represent base-10 numbers exactly and therefore avoids annoying arithmetic errors that occur with ``float``.
(You can find lots of info online about this subject.)
``DecimalField`` is a more flexible generalization of oTree's currency datatype.

When defining a ``DecimalField``, you specify a ``config_name`` that indicates what entity it represents:

.. code-block:: python

    gold = models.DecimalField(config_name='grams')

Define your configs in ``settings.py``:

.. code-block:: python

    DECIMAL_CONFIGS = [
        dict(
            name='grams',
            places=6,
            display=dict(max_places=4, min_places=0),
            form=dict(places=2, units_label='grams'),
        ),
    ]


-   ``places`` is the number of decimal places used internally (for database storage and calculations).
    If you set ``places=6``, then ``1/3`` will be stored as ``0.333333``.
-   The ``display`` properties apply when displaying the content in a template.
    If you set ``max_places=2`` and ``min_places=0``, then ``9.876`` will display as ``9.87``.
    but ``9.000`` will display as ``9`` (remove trailing zeros).
-   The ``display`` dict can also have an entry called ``function``
    that should be a function with 2 args: the formatted value as a string, and the original
    decimal value. If defined, it will be called to generate the display value.
    You can append currency symbols, units, or even wrap the number in an HTML tag.
-   The ``form`` properties are relevant if the field is included in a form.
    If you set ``places=0``, then the user must input a whole number.
    ``units_label`` sets the label on the right edge of the number input.

Decimal datatype
----------------

Apart from database fields,
you can define decimal values throughout your code wih ``dec()``.
For example ``my_weight = dec(1.23, 'grams')``.