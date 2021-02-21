Tips and tricks
===============

Preventing code duplication
---------------------------

As much as possible, it's good to avoid copy-pasting the same code in
multiple places. Although it sometimes takes a bit of thinking to figure
out how to avoid copy-pasting code, you will see that having your code in
only one place usually saves you
a lot of effort later when you need to change the design of your code
or fix bugs.

Below are some techniques to achieve code reuse.

Don't make multiple copies of your app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If possible, you should avoid copying an app's folder to make a slightly different version, because then you have
duplicated code that is harder to maintain.

If you need multiple rounds, set ``num_rounds``.
If you need slightly different versions (e.g. different treatments),
then you should use the techniques described in :ref:`treatments`,
such as making 2 session configs that have a different
``'treatment'`` parameter,
and then checking for ``session.config['treatment']`` in your app's code.


.. _many-fields:

How to make many fields
~~~~~~~~~~~~~~~~~~~~~~~

Let's say your app has many fields that are almost the same, such as:

.. code-block:: python

    class Player(BasePlayer):

        f1 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f2 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f3 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f4 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f5 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f6 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f7 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f8 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f9 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )
        f10 = models.IntegerField(
            choices=[-1, 0, 1], widget=widgets.RadioSelect,
            blank=True, initial=0
        )

        # etc...

This is quite complex; you should look for a way to simplify.

Are the fields all displayed on separate pages? If so, consider converting
this to a 10-round game with just one field. See the
`real effort <https://github.com/oTree-org/oTree/tree/master/real_effort>`__
sample game for an example of how to just have 1 page that gets looped over many rounds,
varying the question that gets displayed with each round.

If that's not possible, then you can reduce the amount of repeated code
by defining a method that returns a field:

.. code-block:: python

    def make_field(label):
        return models.IntegerField(
            choices=[1,2,3,4,5],
            label=label,
            widget=widgets.RadioSelect,
        )

    class Player(BasePlayer):

        q1 = make_field('I am quick to understand things.')
        q2 = make_field('I use difficult words.')
        q3 = make_field('I am full of ideas.')
        q4 = make_field('I have excellent ideas.')


Prevent duplicate pages by using multiple rounds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have many many pages that are almost the same,
consider just having 1 page and looping it for multiple rounds.
One sign that your code can be simplified is if it looks
something like this:

.. code-block:: python

    # [pages 1 through 7....]

    class Decision8(Page):
        form_model = 'player'
        form_fields = ['decision8']

    class Decision9(Page):
        form_model = 'player'
        form_fields = ['decision9']

    # etc...

See the `quiz <https://github.com/oTree-org/oTree/tree/master/quiz>`__
or `real effort <https://github.com/oTree-org/oTree/tree/master/real_effort>`__
sample games for examples of how to just have 1 page that gets looped over many rounds,
varying the question that gets displayed with each round.

Improving code performance
--------------------------

You should avoid redundant use of ``get_players()``, ``get_player_by_id()``, ``in_*_rounds()``,
``get_others_in_group()``, or any other methods that return a player or list of players.
These methods all require a database query,
which can be slow.

For example, this code has a redundant query because it asks the database
5 times for the exact same player:

.. code-block:: python

    def vars_for_template(player):
        return dict(
            a=player.in_round(1).a,
            b=player.in_round(1).b,
            c=player.in_round(1).c,
            d=player.in_round(1).d,
            e=player.in_round(1).e
        )


It should be simplified to this:

.. code-block:: python

    def vars_for_template(player):
        round_1_player = player.in_round(1)
        return dict(
            a=round_1_player.a,
            b=round_1_player.b,
            c=round_1_player.c,
            d=round_1_player.d,
            e=round_1_player.e
        )


As an added benefit, this usually makes the code more readable.

Use BooleanField instead of StringField, where possible
-------------------------------------------------------

Many ``StringFields`` should be broken down into ``BooleanFields``, especially
if they only have 2 distinct values.

Suppose you have a field called ``treatment``:

.. code-block:: python

    treatment = models.StringField()

And let's say ``treatment`` it can only have 4 different values:

-   ``high_income_high_tax``
-   ``high_income_low_tax``
-   ``low_income_high_tax``
-   ``low_income_low_tax``

In your pages, you might use it like this:

.. code-block:: python

    class HighIncome(Page):
        @staticmethod
        def is_displayed(player):
            return player.treatment == 'high_income_high_tax' or player.treatment == 'high_income_low_tax'

    class HighTax(Page):
        @staticmethod
        def is_displayed(player):
            return player.treatment == 'high_income_high_tax' or player.treatment == 'low_income_high_tax'


It would be much better to break this to 2 separate BooleanFields::

    high_income = models.BooleanField()
    high_tax = models.BooleanField()

Then your pages could be simplified to:

.. code-block:: python

    class HighIncome(Page):
        @staticmethod
        def is_displayed(player):
            return player.high_income

    class HighTax(Page):
        @staticmethod
        def is_displayed(player):
            return player.high_tax



.. _duplicate_validation_methods:

Avoid duplicated validation methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have many repetitive :ref:`FIELD_error_message <FOO_error_message>` methods,
you can replace them with a single :ref:`error_message <error_message>` method.
For example:

.. code-block:: python

    def quiz1_error_message(player, value):
        if value != 42:
            return 'Wrong answer'

    def quiz2_error_message(player, value):
        if value != 'Ottawa':
            return 'Wrong answer'

    def quiz3_error_message(player, value):
        if value != 3.14:
            return 'Wrong answer'

    def quiz4_error_message(player, value):
        if value != 'George Washington':
            return 'Wrong answer'

You can instead define this method on your page (not Player class):

.. code-block:: python

    def error_message(player, values):
        solutions = dict(
            quiz1=42,
            quiz2='Ottawa',
            quiz3='3.14',
            quiz4='George Washington'
        )

        error_messages = dict()

        for field_name in solutions:
            if values[field_name] != solutions[field_name]:
                error_messages[field_name] = 'Wrong answer'

        return error_messages

(Usually ``error_message`` is used to return a single error message as a string, but you can also return a dict.)