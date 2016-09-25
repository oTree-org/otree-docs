Tips and tricks
===============


Don't modify values in ``Constants``
------------------------------------

As its name implies, ``Constants`` is for values that don't change -- they are the same for all participants
across all sessions. So, you shouldn't do something like this:

.. code-block:: python

    def my_method(self):
        Constants.my_list.append(1)

``Constants`` has global scope, so when you do this, your modification will "leak" to all other sessions,
until the server is restarted. Instead, if you want a variable that is the same for all players in your session,
you should set a field on the subsession, or use :ref:`session_vars`.

In Player/Group/Subsession, use fields instead of class attributes
------------------------------------------------------------------

For the same reason as with Constants above,
you shouldn't assign to class attributes on your models.
For example, don't do this:

.. code-block:: python

    class Player(BasePlayer):


        my_list = [] # wrong

        def foo(self):
            self.my_list.append(1)

The problem with the above is that the current value of ``my_list``
will be shared by all player instances.

Equally, you should not do this:

.. code-block:: python

    class Player(BasePlayer):

        my_int = 0 # wrong

        def foo(self):
            self.my_int += 1

Instead you should do this:

.. code-block:: python

    class Player(BasePlayer):

        my_int = models.IntegerField(initial=1) # right

        def foo(self):
            self.my_int += 1

Only generate random values inside methods
------------------------------------------

If you want a field whose initial value is random,
you might initially try this incorrect approach:

.. code-block:: python

    class Player(BasePlayer):

        factor = models.FloatField(initial=random.random()) # wrong

Python loads this code only once each time you run the ``otree`` command (e.g. ``resetdb`` or ``runserver``, etc.).
So ``random.random()`` is just evaluated once globally, not for each new session or player.
That means every player will end up with the same "random" value,
until you restart the server.

Instead, you should generate the random variables in :ref:`before_session_starts`.

For the same reason, this will not work either:

.. code-block:: python

    class Constants(BaseConstants):
        factor = random.random() # wrong


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

views.py: prevent code duplication by using inheritance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you can't merge your code into 1 Page as suggested above,
but your code still has a lot of repetition, you can use
Python inheritance to define the common code on a base class.

Basic example
`````````````

For example, let's say that your page classes all
repeat some of the code, e.g. the ``is_displayed`` condition:

.. code-block:: python

    class Page1(Page):
        def is_displayed(self):
            return self.player.foo

        ...

    class Page2(Page):
        def is_displayed(self):
            return self.player.foo

        ...

    class Page3(Page):
        def is_displayed(self):
            return self.player.foo

        ...

    page_sequence = [
        Page1,
        Page2,
        Page3,
    ]

You can eliminate this repetition as follows:

.. code-block:: python

    class BasePage(Page):
        def is_displayed(self):
            return self.player.foo

    class Page1(BasePage):
        pass

    class Page2(BasePage):
        pass

    class Page3(BasePage):
        pass

    page_sequence = [
        Page1,
        Page2,
        Page3,
    ]

(This is not a special oTree feature;
it is simply using Python class inheritance.)

More complex example
````````````````````

Let's change the above example slightly,
so that ``Page1`` has an extra condition in ``is_displayed``:

.. code-block:: python

    class Page1(Page):
        def is_displayed(self):
            return self.player.foo and self.player.bar

        ...

    class Page2(Page):
        def is_displayed(self):
            return self.player.foo

        ...

    class Page3(Page):
        def is_displayed(self):
            return self.player.foo

        ...

    page_sequence = [
        Page1,
        Page2,
        Page3,
    ]


You can refactor this as follows:

.. code-block:: python

    class BasePage(Page):
        def is_displayed(self):
            return self.player.foo and self.extra_is_displayed()

        def extra_is_displayed(self):
            return True

    class Page1(BasePage):
        def extra_is_displayed(self):
            return self.player.bar

    class Page2(BasePage):
        pass

    class Page3(BasePage):
        pass

    page_sequence = [
        Page1,
        Page2,
        Page3,
    ]

You can use the same approach with ``vars_for_template``, ``before_next_page``,
etc.