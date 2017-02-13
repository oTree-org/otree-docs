.. _views:

Views
=====

Each page that your players see is defined by a ``Page`` class in
``views.py`` ("views" is basically a synonym for "pages").

Your ``views.py`` must have a ``page_sequence``
variable that gives the order of the pages. For example:

.. code-block:: python

    page_sequence=[Start, Offer, Accept, Results]

If your game has multiple rounds, this sequence will be repeated.
See :ref:`rounds` for more info.

Pages
-----

A ``Page`` class can have any of the following optional methods and attributes:

.. _is_displayed:

is_displayed()
~~~~~~~~~~~~~~

You can define this function to return ``True`` if the page should be shown,
and False if the page should be skipped.
If omitted, the page will be shown.

For example, to only show the page to P2 in each group:

.. code-block:: python

    class Page1(Page):
        def is_displayed(self):
            return self.player.id_in_group == 2

Or only show the page in round 1:

.. code-block:: python

    class Page1(Page):
        def is_displayed(self):
            return self.round_number == 1

.. _vars_for_template:

vars_for_template()
~~~~~~~~~~~~~~~~~~~

You can use this to return a dictionary of variable names and their values,
which is passed to the template. Example:

.. code-block:: python

    class Page1(Page):
        def vars_for_template(self):
            return {'a': 1 + 1, 'b': self.player.foo * 10}

Then in the template you can access ``a`` and ``b`` like this:

.. code-block:: html+django

    Variables {{ a }} and {{ b }} ...

oTree automatically passes the following objects to the template:
``player``, ``group``, ``subsession``, ``participant``, ``session``, and ``Constants``.
You can access them in the template like this: ``{{ Constants.blah }}`` or ``{{ player.blah }}``.

.. note::

    You generally shouldn't generate random values in ``vars_for_template``,
    because if the user refreshes their page, ``vars_for_template`` will be executed again,
    and the random calculation might return a different value.
    Instead, you should calculate random values in either ``before_session_starts``,
    ``before_next_page``, or ``after_all_players_arrive``, each of which
    only executes once.

.. _before_next_page:

before_next_page()
~~~~~~~~~~~~~~~~~~

Here you define any code that should be executed
after form validation, before the player proceeds to the next page.

If the page is skipped with ``is_displayed``,
then ``before_next_page`` will be skipped as well.

Example:

.. code-block:: python

    class Page1(Page):
        def before_next_page(self):
            self.player.tripled_payoff = self.player.bonus * 3

template_name
~~~~~~~~~~~~~

Each Page should have a file in ``templates/`` with the same name.
For example, if your app has this page in ``my_app/views.py``:

.. code-block:: python

    class Page1(Page):
        pass

Then you should create a file ``my_app/templates/my_app/Page1.html``,
(note that app_name is repeated).
See :ref:`templates` for info on how to write an HTML template.

If the template needs to have a different name from your
view class (e.g. you are sharing the same template for multiple views),
set ``template_name``. Example:

.. code-block:: python

    class Page1(Page):
        template_name = 'app_name/MyView.html'

timeout_seconds (Remaining time)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The number of seconds the user has to
complete the page. After the time runs out, the page auto-submits.

Example: ``timeout_seconds = 20``

When there are 60 seconds left, the page displays a timer warning the participant.

.. note::

    If you are running the production server (``runprodserver``)
    or using ``timeoutworker``,
    the page will always submit, even if the user closes their browser window.
    However, this does not occur if you are running the test server
    (``runserver``).

.. _timeout_submission:

timeout_submission
~~~~~~~~~~~~~~~~~~

You can use ``timeout_submission`` to define what values
should be submitted for a page if a timeout occurs,
or if the experimenter moves the
participant forward.

Example:

.. code-block:: python

    class Page1(Page):
        form_model = models.Player
        form_fields = ['accept']

        timeout_seconds = 60
        timeout_submission = {'accept': True}

If omitted, then oTree will default to
``0`` for numeric fields, ``False`` for boolean fields, and the empty
string ``''`` for text/character fields.

If the values submitted ``timeout_submission`` need to be computed dynamically,
you can check :ref:`timeout_happened` and set the values in ``before_next_page``.

.. _timeout_happened:

timeout_happened
~~~~~~~~~~~~~~~~

This attribute is automatically set to ``True``
if the page was submitted by timeout.
It can be accessed in ``before_next_page``.
For example:

.. code-block:: python

    class Page1(Page):
        timeout_seconds = 60

        def before_next_page(self):
            if self.timeout_happened:
                self.player.my_random_variable = random.random()


``timeout_happened`` is undefined in other methods like ``vars_for_template``,
because the timeout countdown only starts after the page is rendered.

The fields that were filled out at the moment the page was submitted are contained
in ``self.request.POST``, which you can access like this:

.. code-block:: python

    def before_next_page(self):
        if self.timeout_happened:
            post_dict = self.request.POST.dict()
            my_value = post_dict.get('my_field')
            # assuming my_value is an int
            self.player.my_value = int(my_value)

            # you can also loop through self.form_fields and self.timeout_submission

Note: ``self.request.POST`` just contains whatever the user put there,
whether valid or not.
For example, supposing ``my_field`` is an ``IntegerField``, there is no guarantee
that ``post_dict.get('my_field')``
contains an integer, that the integer is between your field's ``max`` and ``min``,
or even that that the post dict contains an entry for
this form field (e.g. it may have been left blank), which is why we need to use ``post_dict.get('my_field')`` method
rather than ``post_dict['my_field']``. (Python's dict ``.get()`` method also lets you provide a second argument like
``post_dict.get('my_field', 10)``, which will return 10 as a fallback in case
``my_field`` is not found if that entry is missing, it will return the default of 10.)


def vars_for_all_templates(self)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
``wait_for_all_groups = True`` on the wait page, e.g.:

.. code-block:: python

    class NormalWaitPage(WaitPage):
        pass

    class AllGroupsWaitPage(WaitPage):
        wait_for_all_groups = True

For more information on groups, see :ref:`groups`.

Wait pages can define the following methods:

after_all_players_arrive()
~~~~~~~~~~~~~~~~~~~~~~~~~~

Any code you define here will be executed once all players have arrived at the wait
page. For example, this method can determine the winner
and set each player's payoff.

.. code-block:: python

    class ResultsWaitPage(WaitPage):
        def after_all_players_arrive(self):
            self.group.set_payoffs()

Note, you can't reference ``self.player`` inside ``after_all_players_arrive``,
because the code is executed once for the entire group,
not for each individual player.
(However, you can use ``self.player`` in a wait page's ``is_displayed``.)

.. _group_by_arrival_time:

group_by_arrival_time
~~~~~~~~~~~~~~~~~~~~~

.. note::

    This is a new feature
    only available in otree-core 1.1 or higher (Dec 2016).

If you set ``group_by_arrival_time = True`` on a WaitPage,
players will be grouped in the order they arrive at that wait page:

.. code-block:: python

    class MyWaitPage(WaitPage):
        group_by_arrival_time = True

For example, if ``players_per_group = 2``, the first 2 players to arrive
at the wait page will be grouped together, then the next 2 players, and so on.

This is useful in sessions where some participants
might drop out (e.g. online experiments,
or experiments with consent pages that let the participant quit early), or
sessions where some participants take much longer than others.

A typical way to use ``group_by_arrival_time`` is to put it after an app
that filters out participants. For example, if your session has a consent page
that gives participants the chance to opt out of the study, you can make a "consent" app
that just contains the consent pages, and
then have an ``app_sequence`` like ``['consent', 'my_game']``,
where ``my_game`` uses ``group_by_arrival_time``.
This means that if someone opts out in ``consent``,
they will be excluded from the grouping in ``my_game``.

If a game has multiple rounds,
you may want to only group by arrival time in round 1:

.. code-block:: python

    class MyWaitPage(WaitPage):
        group_by_arrival_time = True

        def is_displayed(self):
            self.round_number == 1

If you do this, then subsequent rounds will keep the same group structure as
round 1. Otherwise, players will be re-grouped by their arrival time
in each round.
(``group_by_arrival_time`` copies the group structure to future rounds.)

Notes:

-   ``id_in_group`` is not necessarily assigned in the order players arrived at the page.
-   ``group_by_arrival_time`` can only be used if the wait page is the first page in ``page_sequence``
-   If you use ``is_displayed`` on a page with ``group_by_arrival_time``,
    it should only be based on the round number. Don't use ``is_displayed``
    to show the page to some players but not others.

is_displayed()
~~~~~~~~~~~~~~

Works the same way as with regular pages.
If this returns ``False`` then the player skips the wait page.

If some or all players in the group skip the wait page,
then ``after_all_players_arrive()`` may not be run.

.. _customize_wait_page:

Customizing the wait page's appearance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can customize the text that appears on a wait page
by setting the ``title_text`` and ``body_text`` attributes, e.g.:

.. code-block:: python

    class MyWaitPage(WaitPage):
        title_text = "Custom title text"
        body_text = "Custom body text"

You can also make a custom wait page template.
For example, save this to ``my_app/templates/my_app/MyWaitPage.html``
(this template must extend 'otree/WaitPage.html'):

.. code-block:: html+django

    {% extends 'otree/WaitPage.html' %}
    {% load staticfiles otree_tags %}
    {% block title %}{{ title_text }}{% endblock %}
    {% block content %}
        {{ body_text }}
        <p>
            My custom content here.
        </p>
    {% endblock %}

Then tell your wait page to use this template:

.. code-block:: python

    class MyWaitPage(WaitPage):
        template_name = 'my_app/MyWaitPage.html'

Then you can use ``vars_for_template`` in the usual way.
Actually, the ``body_text`` and ``title_text`` attributes
are just shorthand for setting ``vars_for_template``;
the following 2 code snippets are equivalent:

.. code-block:: python

    class MyWaitPage(WaitPage):
        body_text = "foo"

.. code-block:: python

    class MyWaitPage(WaitPage):
        def vars_for_template(self):
            return {'body_text': "foo"}

If you want to apply your custom wait page template globally,
save it to ``_templates/global/WaitPage.html``.
oTree will then automatically use it everywhere instead of the built-in wait page.
