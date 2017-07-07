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

If you need to repeat the same rule for many pages, see :ref:`here <skip_many>`.

``is_displayed()`` may be executed more than once, so beware of code that relies
on it only being executed once, e.g. incrementing a counter.

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

If you need the timeout to be dynamically determined, use :ref:`get_timeout_seconds`.

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

Timeouts and forms
~~~~~~~~~~~~~~~~~~

To control what happens with the page's form if a timeout occurs,
see :ref:`timeout_submission` and :ref:`timeout_happened`.

.. _get_timeout_seconds:

get_timeout_seconds
~~~~~~~~~~~~~~~~~~~

.. note::

    This is a new feature in otree-core 1.3 (May 2017).

This is a dynamic alternative to ``timeout_seconds``,
so that you can base the timeout on ``self.player``, ``self.session``, etc.:

For example, you can make the timeout for a page configurable by adding a parameter
to the session config (see :ref:`edit_config`) and referencing it in your page.
In ``settings.py`` add this:

.. code-block:: python

    SESSION_CONFIGS = [
        {
            'name': 'my_app',
            'num_demo_participants': 1,
            'app_sequence': ['my_app'],
            'my_page_timeout_seconds': 60,
        },
        # etc...
    ]

    class MyPage(Page):

        def get_timeout_seconds(self):
            return self.session.config['my_page_timeout_seconds']


Timeouts that span multiple pages
'''''''''''''''''''''''''''''''''

You can use ``get_timeout_seconds`` to create timeouts that span multiple
pages, or even the entire session. The trick is to define a fixed "expiration time",
and then on each page, make ``get_timeout_seconds`` return the number of seconds
until that expiration time.

First, choose a place to start the timer. This could be a page called
"Start" that displays text like "Press the button when you're ready to start".
When the user clicks the "next" button, ``before_next_page`` will be executed
and the expiry timestamp will be set:

.. code-block:: python

    import time

    class Start(Page):

        def is_displayed(self):
            return self.round_number == 1

        def before_next_page(self):
            # user has 5 minutes to complete as many pages as possible
            self.participant.vars['expiry_timestamp'] = time.time() + 5*60

(You could also start the timer in ``after_all_players_arrive`` or ``before_session_starts``,
and it could be stored in ``session.vars`` if it's the same for everyone in the session.)

Then, each page's ``get_timeout_seconds`` should be the number of seconds
until that expiration time:

.. code-block:: python

    class Page1(Page):
        def get_timeout_seconds(self):
            return self.participant.vars['expiry_timestamp'] - time.time()

When time runs out, ``get_timeout_seconds`` will return 0 or a negative value,
which will result in the page loading and being auto-submitted right away.
This means all the remaining pages will quickly flash on the participant's screen,
which is usually undesired. So, you should use
``is_displayed`` to skip the page if time has run out, or if there's only
a few seconds remaining (e.g. 3).

.. code-block:: python

    class Page1(Page):
        def get_timeout_seconds(self):
            return self.participant.vars['expiry_timestamp'] - time.time()

        def is_displayed(self):
            return self.participant.vars['expiry_timestamp'] - time.time() > 3

If you have multiple pages in your ``page_sequence`` that need to share
the timeout, rather than copy-pasting the above code to every page redundantly,
you can create a base class for all pages:

.. code-block:: python

    class BasePage(Page):

        def get_timeout_seconds(self):
            return self.participant.vars['expiry_timestamp'] - time.time()

        def is_displayed(self):
            return self.participant.vars['expiry_timestamp'] - time.time() > 3


    class Page1(BasePage):
        pass


    class Page2(BasePage):
        pass


    class Page3(BasePage):
        pass


    page_sequence = [
        Start,
        Page1, Page2, Page3,
    ]

See the section on :ref:`inheritance <inheritance>` for more info.

The default text on the timer says "Time left to complete this page:".
But if your timeout spans multiple pages, you should word it more accurately,
by setting ``timer_text``:

.. code-block:: python

    class BasePage(Page):

        timer_text = 'Time left to complete this section:'

        def get_timeout_seconds(self):
            return self.participant.vars['expiry_timestamp'] - time.time()

        def is_displayed(self):
            return self.participant.vars['expiry_timestamp'] - time.time() > 3


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

.. _after_all_players_arrive:

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

is_displayed()
~~~~~~~~~~~~~~

Works the same way as with regular pages.
If this returns ``False`` then the player skips the wait page.

If some or all players in the group skip the wait page,
then ``after_all_players_arrive()`` may not be run.


.. _group_by_arrival_time:

group_by_arrival_time
~~~~~~~~~~~~~~~~~~~~~

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
            return self.round_number == 1

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

If you need further control on arranging players into groups,
use :ref:`get_players_for_group`.

.. _get_players_for_group:

get_players_for_group()
~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    This is a new feature in otree-core 1.3 (May 2017).

``get_players_for_group()`` can be used in addition to ``group_by_arrival_time``,
to control exactly which players are assigned together.

Let's say that in addition to grouping by arrival time, you need each group
group to consist of 1 man and 1 woman (or 2 "A" players and 2 "B" players, etc).

If you define a method called ``get_players_for_group``,
it will get called whenever a new player reaches the wait page.
The method's argument is the list of players who are waiting to be grouped,
ordered by the time they first arrived at the wait page.
If you select some of these players and return them as a list,
those players will be assigned to a group, and move forward.
If you don't return anything, then no grouping occurs.

Here's an example where each group has 2 A players, 2 B players.

.. code-block:: python

    class GroupingWaitPage(WaitPage):
        group_by_arrival_time = True

        def get_players_for_group(self, waiting_players):
            a_players = [p for p in waiting_players if p.participant.vars['type'] == 'A']
            b_players = [p for p in waiting_players if p.participant.vars['type'] == 'B']

            if len(a_players) >= 2 and len(b_players) >= 2:
                # this is a Python "list slice"
                return a_players[:2] + b_players[:2]

        def is_displayed(self):
            return self.round_number == 1


Here's an example of a where each player has a field ``treatment``, and 2 players
can only be assigned to the same 2-player group if they have the same treatment.
Note that we only need to check for possible groupings with the last player,
because if any of the other 2 players matched with each other, they would have
been grouped the previous time ``get_players_for_group`` was run.

.. code-block:: python

    class GroupByTreatment(WaitPage):
        group_by_arrival_time = True

        def get_players_for_group(self, waiting_players):

            # since the list is ordered by arrival time,
            # the last element is the newest player who just arrived
            newest_player = waiting_players[-1]

            # the players who were already waiting
            # (each of them was newest_player a previous time this method was called)
            already_waiting = waiting_players[:-1]

            # check if any of the already waiting players have the same treatment
            # as the newly arrived player
            possible_partners = [p for p in already_waiting if p.treament == newest_player.treatment]

            # if so, put them in a group together
            if possible_partners:
                return [possible_partners[0], newest_player]


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

Randomizing page sequence
-------------------------

You can randomize the order of pages using rounds.
An example is `here <https://github.com/oTree-org/random_page_order>`__.