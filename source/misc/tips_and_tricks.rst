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
and then checking for ``self.session.config['treatment']`` in your app's code.

Templates: prevent code duplication by using a base template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are copy-pasting the same JavaScript or CSS to multiple templates,
you should instead put it in one of the following blocks in a base template:

-   ``{% block global_styles %}``
-   ``{% block global_scripts %}``
-   ``{% block app_styles %}``
-   ``{% block app_scripts %}``

Read more in :ref:`base-template`.

views.py: prevent code duplication by using multiple rounds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your ``views.py`` has many pages that are almost the same,
consider just having 1 page and looping it for multiple rounds.
One sign that your code can be simplified is if it looks
something like this:

.. code-block:: python

    # [pages 1 through 7....]

    class Decision8(Page):
        form_model = models.Player
        form_fields = ['decision8']

    class Decision9(Page):
        form_model = models.Player
        form_fields = ['decision9']

    # etc...

See the `quiz <https://github.com/oTree-org/oTree/tree/master/quiz>`__
or `real effort <https://github.com/oTree-org/oTree/tree/master/real_effort>`__
sample games for examples of how to just have 1 page that gets looped over many rounds,
varying the question that gets displayed with each round.

.. _composition:

views.py: prevent code duplication by moving code to ``models.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You should try to move as much code as possible into ``models.py``.
This will prevent you from repeating the same code on every page.

.. _skip_many:

Example 1: is_displayed
```````````````````````

For example, let's say that your page classes all
repeat some of the code. For example, you use ``is_displayed`` to skip
the rest of the app once a certain participant var is set:

.. code-block:: python

    class Page1(Page):
        def is_displayed(self):
            return self.participant.vars.get('consented') and not self.participant.vars.get('finished')

    class Page2(Page):
        def is_displayed(self):
            return self.participant.vars.get('consented') and not self.participant.vars.get('finished')

    class Page3(Page):
        def is_displayed(self):
            if self.participant.vars.get('consented') and not self.participant.vars.get('finished'):
                if self.player.id_in_group == 1:
                    return True
            return False

    page_sequence = [
        Page1,
        Page2,
        Page3,
    ]

You can eliminate this repetition by moving the ``is_displayed`` code into
``models.py``:

.. code-block:: python

    class Player(BasePlayer):
        def is_playing(self):
            pvars = self.participant.vars
            return pvars.get('consented') and not pvars.get('finished')

Then in ``views.py``:

.. code-block:: python

    class Page1(Page):
        def is_displayed(self):
            return self.player.is_playing()

    class Page2(Page):
        def is_displayed(self):
            return self.player.is_playing()

    class Page3(Page):
        def is_displayed(self):
            return self.player.is_playing() and self.player.id_in_group == 1

    page_sequence = [
        Page1,
        Page2,
        Page3,
    ]


.. _vars_for_many_templates:

Example 2: vars_for_template
````````````````````````````

Let's say you've got the following code (note that ``Page3`` passes extra
variables ``d`` and ``e``):

.. code-block:: python

    class Page1(Page):
    def vars_for_template(self):
        return {
            'a': 1,
            'b': 2,
            'c': 3,
        }

    class Page2(Page):
        def vars_for_template(self):
            return {
                'a': 1,
                'b': 2,
                'c': 3,
            }


    class Page3(Page):
        def vars_for_template(self):
            if self.player.id_in_group == 1:
                return {
                    'a': 1,
                    'b': 2,
                    'c': 3,
                    'd': 4,
                    'e': 5,
                }
            else:
                return {
                    'a': 1,
                    'b': 2,
                    'c': 3,
                }


You can simplify this by making a method in ``models.py``:

.. code-block:: python

    class Player(BasePlayer):
        def vars_for_template(self):
            return {
                'a': 1,
                'b': 2,
                'c': 3,
            }

Then in ``views.py``:

.. code-block:: python

    class Page1(Page):
        def vars_for_template(self):
            return self.player.vars_for_template()

    class Page2(Page):
        def vars_for_template(self):
            return self.player.vars_for_template()

    class Page3(Page):
        def vars_for_template(self):
            context = self.player.vars_for_template()
            if self.player.id_in_group == 1:
                context.update({'d': 4, 'e': 5})
            return context


Improving code performance
--------------------------

You should avoid redundant use of ``get_players()``, ``get_player_by_id()``, ``in_*_rounds()``,
``get_others_in_group()``, or any other methods that return a player or list of players.
These methods all require a database query,
which can be slow.

For example, this code has a redundant query because it asks the database
5 times for the exact same player:

.. code-block:: python

    class MyPage(Page):
        def vars_for_template(self):
            return {
                'a': self.player.in_round(1).a,
                'b': self.player.in_round(1).b,
                'c': self.player.in_round(1).c,
                'd': self.player.in_round(1).d,
                'e': self.player.in_round(1).e,
            }

It should be simplified to this:

.. code-block:: python

    class MyPage(Page):
        def vars_for_template(self):
            round_1_player = self.player.in_round(1)
            return {
                'a': round_1_player.a,
                'b': round_1_player.b,
                'c': round_1_player.c,
                'd': round_1_player.d,
                'e': round_1_player.e,
            }

As an added benefit, this usually makes the code more readable.