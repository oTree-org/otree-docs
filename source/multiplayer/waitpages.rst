.. _wait_pages:

Wait pages
==========

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

.. _after_all_players_arrive:

after_all_players_arrive
------------------------

``after_all_players_arrive`` lets you run some calculations
once all players have arrived at the wait
page. This is a good place to set the players' payoffs
or determine the winner.
You should first define a method on your Group that does the desired calculations.
For example:

.. code-block:: python

    class Group(BaseGroup):
        def set_payoffs(self):
            for player in self.get_players():
                player.payoff = c(100)

Then trigger this method by doing:

.. code-block:: python

    class MyWaitPage(WaitPage):
        after_all_players_arrive = 'set_payoffs'

If you set ``wait_for_all_groups = True``,
then you should set ``after_all_players_arrive`` to the name of to a method on your *Subsession* model.

.. note::

    In oTree 2.3 and earlier, ``after_all_players_arrive`` was a method,
    i.e. ``def after_all_players_arrive(self):``.
    However, the new format is better and you should use it instead.

is_displayed()
--------------

Works the same way as with regular pages.

.. _group_by_arrival_time:

group_by_arrival_time
---------------------

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
-   If ``group_by_arrival_time = True``, then in ``creating_session``,
    all players will initially be in the same group. Groups are only created
    "on the fly" as players arrive at the wait page.

If you need further control on arranging players into groups,
use :ref:`group_by_arrival_time_method`.

.. _group_by_arrival_time_method:

group_by_arrival_time_method()
------------------------------

.. note::

    Before November 2019, this was a method called ``get_players_for_group``,
    and it was on the Page, not the Subsession.
    We recommend switching to the new format.

If you're using ``group_by_arrival_time`` and want more control over
which players are assigned together, you can also use ``group_by_arrival_time_method()``.

Let's say that in addition to grouping by arrival time, you need each group
to consist of 2 men and 2 women.

If you define a method called ``group_by_arrival_time_method`` on your Subsession,
it will get called whenever a new player reaches the wait page.
The method's argument is the list of players who are currently waiting at your wait page.
If you pick some of these players and return them as a list,
those players will be assigned to a group, and move forward.
If you don't return anything, then no grouping occurs.

Here's an example where each group has 2 men and 2 women.
It assumes that in a previous app, you assigned ``self.participant.vars['category']`` to each participant.

.. code-block:: python

    class Subsession(BaseSubsession):
        def group_by_arrival_time_method(self, waiting_players):
            print('in group_by_arrival_time_method')
            m_players = [p for p in waiting_players if p.participant.vars['category'] == 'M']
            f_players = [p for p in waiting_players if p.participant.vars['category'] == 'F']

            if len(m_players) >= 2 and len(f_players) >= 2:
                print('about to create a group')
                return [m_players[0], m_players[1], f_players[0], f_players[1]]
            print('not enough players yet to create a group')

The above example is hardcoded for only 2 categories (M and F).
The below example works for any number of categories.
It makes a group as soon as there are 3 players with the same category.

.. code-block:: python

    def group_by_arrival_time_method(self, waiting_players):
        from collections import defaultdict
        d = defaultdict(list)
        for p in waiting_players:
            category = p.participant.vars['category']
            players_with_this_category = d[category]
            players_with_this_category.append(p)
            if len(players_with_this_category) == 3:
                return players_with_this_category

You can also use ``group_by_arrival_time_method`` to put a timeout on the wait page,
for example to allow the participant to proceed individually if they have been waiting
longer than 5 minutes. First, you must record ``time.time()`` on the final page before the app with ``group_by_arrival_time``.
Store it in ``self.participant.vars``.

Then define a Player method:

.. code-block:: python

    def waiting_too_long(self):
        import time
        return time.time() - self.participant.vars['wait_page_arrival'] > 5*60

Now use this:

.. code-block:: python

    def group_by_arrival_time_method(self, waiting_players):
        if len(waiting_players) >= 3:
            return waiting_players[:3]
        for p in waiting_players:
            if p.waiting_too_long():
                # [p] means a single-player group.
                return [p]

This works because the wait page automatically refreshes once or twice a minute,
which re-executes ``group_by_arrival_time_method``.

.. _wait-page-stuck:

Preventing players from getting stuck on wait pages
---------------------------------------------------

A common problem especially with online experiments is players getting stuck
waiting for another player in their group who dropped out or is too slow.

Here are some things you can do to reduce this problem:

Use ``group_by_arrival_time``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As described above, you can use ``group_by_arrival_time`` so that only
players who are actively playing around the same time get grouped together.

``group_by_arrival_time`` works well if used after a "lock-in" task.
In other words, before your multiplayer game, you can have a
single-player effort task. The idea is that a
participant takes the effort to complete this initial task, they are
less likely to drop out after that point.

Use page timeouts
~~~~~~~~~~~~~~~~~

Use :ref:`timeout_seconds` on each page, so that if a player is slow or inactive,
their page will automatically advance. Or, you can manually force a timeout by clicking
the "Advance slowest participants" button in the admin interface.

Check timeout_happened
~~~~~~~~~~~~~~~~~~~~~~

You can tell users they must submit a page before its ``timeout_seconds``,
or else they will be counted as a dropout.
Even have a page that just says "click the next button to confirm you are still playing".
Then check :ref:`timeout_happened`. If it is True, you can do various things such as
set a field on that player/group to indicate the dropout, and skip the rest of the pages in the round.

Replacing dropped out player with a bot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's an example that combines some of the above techniques, so that even if a player drops out,
they continue to auto-play, like a bot. Just use ``get_timeout_seconds`` and ``before_next_page`` on every page,
like this:

.. code-block:: python

    class Page1(Page):
        form_model = 'player'
        form_fields = ['contribution']

        def get_timeout_seconds(self):
            if self.participant.vars.get('is_dropout'):
                return 1  # instant timeout, 1 second
            else:
                return 5*60

        def before_next_page(self):
            if self.timeout_happened:
                self.participant.vars['is_dropout'] = True
                self.player.contribution = c(100)

Notes:

-   If the player fails to submit the page on time, we set ``is_dropout`` to ``True``.
-   Once ``is_dropout`` is set, each page gets auto-submitted instantly.
-   When a page is auto-submitted, you use ``timeout_happened`` to decide what value gets submitted on the user's behalf.


Customizing the wait page's appearance
--------------------------------------

You can customize the text that appears on a wait page
by setting the ``title_text`` and ``body_text`` attributes, e.g.:

.. code-block:: python

    class MyWaitPage(WaitPage):
        title_text = "Custom title text"
        body_text = "Custom body text"

See also: :ref:`customize_wait_page`.