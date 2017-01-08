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

Let's say you've got the following code (note that ``Page1`` passes an extra
variable ``'d'``):

.. code-block:: python

    class Page1(Page):
        def vars_for_template(self):
            return {
                'a': 1,
                'b': 2,
                'c': 3,
                'd': 4
            }

    class Page2(Page):
        def vars_for_template(self):
            return {
                'a': 1,
                'b': 2,
                'c': 3
            }

    class Page3(Page):
        def vars_for_template(self):
            return {
                'a': 1,
                'b': 2,
                'c': 3
            }


You can refactor this as follows:

.. code-block:: python

    class BasePage(Page):
        def vars_for_template(self):
            v = {
                'a': 1,
                'b': 2,
                'c': 3
            }
            v.update(self.extra_vars_for_template())
            return v

        def extra_vars_for_template(self):
            return {}


    class Page1(BasePage):
        def extra_vars_for_template(self):
            return {'d': 4}

    class Page2(BasePage):
        pass

    class Page3(BasePage):
        pass

