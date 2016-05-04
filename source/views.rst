.. _views:

Views
=====

Each page that your players see is defined by a ``Page`` class in
``views.py``. (You can think of "views" as a synonym for "pages".)

For example, if 1 round of your game involves showing the player a
sequence of 5 pages, your ``views.py`` should contain 5 page classes.

At the bottom of your ``views.py``, you must have a ``page_sequence``
variable that specifies the order in which players are routed through
your pages. For example:

.. code-block:: python

    page_sequence=[Start, Offer, Accept, Results]

Pages
-----

Each ``Page`` class has these methods and attributes:

.. _vars_for_template:

``def vars_for_template(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A dictionary of variable names and their values, which is passed to the
template. Example:

.. code-block:: python

    def vars_for_template(self):
        return {'a': 1 + 1, 'b': self.player.foo * 10}

.. code-block:: html+django

    Variables {{ a }} and {{ b }} ...

.. note::

    oTree automatically passes group, player, subsession, participant, session, and Constants
    objects to the template, which you can access in the template, e.g.:
    ``{{Constants.payoff_if_rejected}}``.

.. _is_displayed:

``def is_displayed(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Should return ``True`` if the page should be shown, and False if the page
should be skipped. If omitted, the page will be shown.

For example, if you only want a page to be shown to P2 in each group:

.. code-block:: python

    def is_displayed(self):
        return self.player.id_in_group == 2

``template_name``
~~~~~~~~~~~~~~~~~

The name of the HTML template to display. This can be omitted if the
template has the same name as the Page class.

Example:

.. code-block:: python

    # This will look inside:
    # 'app_name/templates/app_name/MyView.html'
    # (Note that app_name is repeated)
    template_name = 'app_name/MyView.html'

``timeout_seconds`` (Remaining time)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The number of seconds the user has to
complete the page. After the time runs out, the page auto-submits.

Example: ``timeout_seconds = 20``

When there are 60 seconds left, the page displays a timer warning the participant.

.. note::

    If you are running the production server (``runprodserver``),
    the page will always submit, even if the user closes their browser window.
    However, this does not occur if you are running the test server
    (``runserver``).


.. _timeout_submission:

``timeout_submission``
~~~~~~~~~~~~~~~~~~~~~~

A dictionary where the keys are the elements of
``form_fields``, with the values to be
submitted in case of a timeout, or if the experimenter moves the
participant forward.

If omitted, then oTree will default to
``0`` for numeric fields, ``False`` for boolean fields, and the empty
string for text/character fields.

Example: ``timeout_submission = {'accept': True}``

If the values submitted ``timeout_submission`` need to be computed dynamically,
you can check :ref:`timeout_happened` and set the values in ``before_next_page``.

.. _timeout_happened:

``timeout_happened``
~~~~~~~~~~~~~~~~~~~~

This boolean attribute is ``True`` if the page was submitted by timeout.
It can be accessed in ``before_next_page``:

.. code-block:: python

    def before_next_page(self):
        if self.timeout_happened:
            self.player.my_random_variable = random.random()


This variable is undefined in other methods like ``vars_for_template``,
because the timeout countdown only starts after the page is rendered.

The fields that were filled out at the moment the page was submitted are contained
in a dict called ``self.request.POST``, which you can access like this:

.. code-block:: python

    def before_next_page(self):
        if self.timeout_happened:
            post_dict = self.request.POST
            my_value = post_dict.get('my_field')
            # do something with my_value...

Note: the contents of ``self.request.POST`` have not been validated.
For example, suppose ``my_field`` is an ``IntegerField``. There is no guarantee that ``self.request.POST['my_field']``
contains an integer, that the integer is between your field's ``max`` and ``min``,
or that this field exists at all, which is why we need to use ``post_dict.get('my_field')`` method
rather than ``post_dict['my_field']``. (Python's dict ``.get()`` method also lets you provide a second argument like
``post_dict.get('my_field', 10)``, which will return the entry ``'my_field'`` if it exists in the dict;
if that entry is missing, it will return the default of 10.)


``def before_next_page(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here you define any code that should be executed
after form validation, before the player proceeds to the next page.

If the page is skipped with ``is_displayed``,
then ``before_next_page`` will be skipped as well.


``def vars_for_all_templates(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is not a method on the Page class, but rather a top-level function
in views.py. It is useful when you need certain variables to be passed
to multiple pages in your app. Instead of repeating the same values in
each ``vars_for_template``, you can define it in this function.


.. _wait_pages:

Wait pages
----------

Wait pages are necessary when one player needs to wait for
others to take some action before they can proceed. For example,
in an ultimatum game, player 2 cannot accept or reject before they have
seen player 1's offer.

If you have a ``WaitPage`` in your sequence of pages,
then oTree waits until all players in the group have
arrived at that point in the sequence, and then all players are allowed
to proceed.

If your subsession has multiple groups playing simultaneously, and you
would like a wait page that waits for all groups (i.e. all players in
the subsession), you can set the attribute
``wait_for_all_groups = True`` on the wait page.

For more information on groups, see :ref:`groups`.

Wait pages can define the following methods:

-  ``def after_all_players_arrive(self)``

This code will be executed once all players have arrived at the wait
page. For example, this method can determine the winner of an auction
and set each player's payoff.

- ``def is_displayed(self)``

If this returns ``False`` then the player skips the wait page.

If all players in the group skip the wait page,
then ``after_all_players_arrive()`` will not be run.

.. _customize_wait_page:

Customizing the wait page's appearance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can customize the text that appears on a wait page
by setting the ``title_text`` and ``body_text`` attributes, e.g.:

.. code-block:: python

    class MyWaitPage(WaitPage):
        title_text = "Custom title text"
        body_text = "Custom body text"

To customize further, such as adding HTML content,
you can set the ``template_name`` attribute to reference an HTML file
that extends ``otree/WaitPage.html``.

For example:

.. code-block:: html+django

    {% extends 'otree/WaitPage.html' %}
    {% load staticfiles otree_tags %}
    {% block title %}{{ title_text }}{% endblock %}
    {% block content %}
        {{ body_text }}
        <p>My custom content here</p>
    {% endblock %}


Then you can use ``vars_for_template`` in the usual way.
Actually, the ``body_text`` and ``title_text`` attributes are just shorthand for setting ``vars_for_template``;
the following 2 code snippets are equivalent:

.. code-block:: python

    class MyWaitPage(WaitPage):
        body_text = "foo"

.. code-block:: python

    class MyWaitPage(WaitPage):
        def vars_for_template(self):
            return {'body_text': "foo"}

To apply your custom wait page template globally, save it to ``_templates/global/WaitPage.html``.
