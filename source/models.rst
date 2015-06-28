Models
------

This is where you store your data models.

Model hierarchy
~~~~~~~~~~~~~~~

Every oTree app needs the following 3 models:

-  Subsession
-  Group
-  Player

A player is part of a group, which is part of a subsession.


Models and database tables
~~~~~~~~~~~~~~~~~~~~~~~~~~

For example, let's say you are programming an ultimatum game, where in
each two-person group, one player makes a monetary offer (say, 0-100
cents), and another player either rejects or accepts the offer. When you
analyze your data, you will want your "Group" table to look something
like this:

::

    +----------+----------------+----------------+
    | Group ID | Amount offered | Offer accepted |
    +==========+================+================+
    | 1        | 50             | TRUE           |
    +----------+----------------+----------------+
    | 2        | 25             | FALSE          |
    +----------+----------------+----------------+
    | 3        | 50             | TRUE           |
    +----------+----------------+----------------+
    | 4        | 0              | FALSE          |
    +----------+----------------+----------------+
    | 5        | 60             | TRUE           |
    +----------+----------------+----------------+

You need to define a Python class that defines the structure of this
database table. You define what fields (columns) are in the table, what
their data types are, and so on. When you run your experiment, the SQL
tables will get automatically generated, and each time users visit, new
rows will get added to the tables.

Here is how to define the above table structure:

.. code-block:: python

    class Group(otree.models.BaseGroup):
        ...
        amount_offered = models.CurrencyField()
        offer_accepted = models.BooleanField()

Every time you add, remove, or change a field in ``models.py``, you need
to run ``python otree resetdb`` (or, in the launcher, click "Clear
Database").

The full list of available fields is in the Django documentation
`here <https://docs.djangoproject.com/en/1.7/ref/models/fields/#field-types>`__.

Additionally, oTree has ``CurrencyField``; see :ref:`money`.

Constants
~~~~~~~~~

The ``Constants`` class is the recommended place to put your app's
parameters and constants that do not vary from player
to player.

Here are the required constants:

-  ``name_in_url`` specifies the name used to identify your app in the participant's URL.
For example, if you set it to ``public_goods``, a participant's URL might look like this:
``http://otree-demo.herokuapp.com/p/zuzepona/public_goods/Introduction/1/``

-  ``players_per_group`` (described in :ref:`groups`)

-  ``num_rounds`` (described in :ref:`rounds`)
