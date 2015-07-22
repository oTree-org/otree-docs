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

``def vars_for_template(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A dictionary of variable names and their values, which is passed to the
template.

.. note::

    oTree automatically passes group, player, subsession, and Constants
    objects to the template, which you can access in the template, e.g.:
    ``{{Constants.payoff_if_rejected}}``.

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



``timeout_submission``
~~~~~~~~~~~~~~~~~~~~~~

.. note::

    Prior to May 26, 2015, this was called ``auto_submit_values``.

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

.. versionadded:: 0.3.18

``def before_next_page(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here you define any code that should be executed
after form validation,
before the player proceeds to the next page.


``def vars_for_all_templates(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is not a method on the Page class, but rather a top-level function
in views.py. It is useful when you need certain variables to be passed
to multiple pages in your app. Instead of repeating the same values in
each ``vars_for_template``, you can define it in this function.


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

-  ``def title_text(self)``

The text in the title of the wait page.

-  ``def body_text(self)``

The text in the body of the wait page

- ``def is_displayed(self)``

If this returns ``False`` then the player skips the wait page.

If all players in the group skip the wait page,
then ``after_all_players_arrive()`` will not be run.

.. note::

    ``is_displayed`` on wait pages was added in otree-core 0.3.7

