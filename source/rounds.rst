Apps & rounds
^^^^^^^^^^^^^

Apps
====

In oTree (and Django), an app is a folder containing Python and HTML code. When
you create your oTree project, it comes pre-loaded with various apps such as
``public_goods`` and ``dictator``. A session is basically a sequence of
apps that are played one after the other.

Creating an app
---------------

Enter::

    $ otree startapp your_app_name

This will create a new app folder based on a oTree template, with most
of the structure already set up for you.

The key files are ``models.py``, ``views.py``, and the HTML files
under the ``templates/`` directory.

Think of this as a skeleton to which you can add as much as you want.
You can add your own classes, functions, methods, and attributes, or
import any 3rd-party modules.

Then go to ``settings.py`` and create an entry for your app in
``SESSION_CONFIGS`` that looks like the other entries.

Combining apps
--------------

In your :ref:`SESSION_CONFIGS <SESSION_CONFIGS>`, you can combine apps
by setting ``'app_sequence'``.

Passing data between apps
-------------------------

See :ref:`participant.vars <vars>` and :ref:`session.vars <session_vars>`.


.. _rounds:

Rounds
======

You can make a game run for multiple rounds by setting ``Constants.num_rounds``
in models.py. For example, if your session config's ``app_sequence`` is ``['app1', 'app2']``,
where ``app1`` has ``num_rounds = 3`` and ``app2`` has ``num_rounds = 1``,
then your sessions will contain 4 subsessions.


Round numbers
-------------

You can get the current round number with ``self.round_number``
(this attribute is present on subsession, group, player, and page objects).
Round numbers start from 1.

.. _in_rounds:

Passing data between rounds or apps
-----------------------------------

Each round has separate ``Subsession``, ``Group``, and ``Player`` objects.
For example, let's say you set ``self.player.my_field = True`` in round 1.
In round 2, if you try to access ``self.player.my_field``,
you will find its value is ``None``
(assuming that is the default value of the field).
This is because the ``Player`` objects
in round 1 are separate from ``Player`` objects in round 2.

To access data from a previous round or app,
you can use one of the techniques described below.

in_rounds, in_previous_rounds, in_round, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Player, group, and subsession objects have the following methods, which work
similarly:

-   in_previous_rounds()
-   in_all_rounds()
-   in_rounds()
-   in_round()

``player.in_previous_rounds()`` and ``player.in_all_rounds()``
each return a list of players representing the same participant in
previous rounds of the same app. The difference is that ``in_all_rounds()``
includes the current round's player.

For example, if you wanted to calculate a participant's payoff for all previous
rounds of a game, plus the current one:

.. code-block:: python

    cumulative_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

``player.in_rounds(m, n)`` returns a list of players representing the same participant from rounds ``m`` to ``n``.

``player.in_round(m)`` returns just the player in round ``m``.
For example, to get the player's payoff in the previous round,
you would do ``self.player.in_round(self.round_number - 1).payoff``.

Similarly, subsession objects have methods ``in_previous_rounds()``,
``in_all_rounds()``, ``in_rounds(m,n)`` and ``in_round(m)`` that work the same way.

Group objects also have methods ``in_previous_rounds()``, ``in_all_rounds()``, ``in_rounds(m,n)`` and ``in_round(m)``,
but note that if you re-shuffle groups between rounds,
then these methods may not return anything meaningful.

.. _vars:

participant.vars
----------------

``in_all_rounds()`` only is useful when you need to access data from a previous
round of the same app.
If you want to pass data between different apps,
you should store this data on the participant,
which persists across apps (see :ref:`participants_and_players`).

``participant.vars`` is is a dictionary that can store any data.
For example, you can set an attribute like this:

    self.participant.vars['name'] = 'John'

Later in the session (e.g. in a separate app),
you can retrieve it like this::

    self.participant.vars['name'] # returns 'John'

If your key may or may not exist, you can use the ``.get()`` method.
For example, ``self.participant.vars.get('my_var')``.
More `here <https://docs.python.org/3/library/stdtypes.html#dict.get>`__.

or you can test if ``'my_var'`` exists with ``'my_var' in self.participant.vars``.

As described :ref:`here <object_model>`, the current participant can be
accessed from a ``Page`` or ``Player``:

.. code-block:: python

    # in views.py
    class MyPage(Page):
        def before_next_page(self):
            self.participant.vars['foo'] = 1

.. code-block:: python

    # in models.py
    class Player(BasePlayer):
        def some_method(self):
            self.participant.vars['foo'] = 1

You can also access it from ``Group`` or ``Subsession``, as long as you retrieve
a ``Player`` instance (e.g. using ``get_players()`` or ``get_player_by_role()``,
etc.).

.. code-block:: python

    class Group(BaseGroup):
        def some_method(self):
            for p in self.get_players():
                p.participant.vars['foo'] = 1


.. _session_vars:

session.vars
~~~~~~~~~~~~

For global variables that are the same for all participants in the session,
you can use ``self.session.vars``.
This is a dictionary just like ``participant.vars``. The difference is that
if you set a variable in ``self.session.vars``, it will apply
to all participants in the session, not just one.

As described :ref:`here <object_model>`, the ``session`` object can be
accessed from a ``Page`` object or any of the models (``Player``, ``Group``,
``Subsession``, etc.).


Variable number of rounds
-------------------------

If you want a variable number of rounds, consider setting ``num_rounds``
to some high number, and then in your app, conditionally hide the
``{% next_button %}`` element, so that the user cannot proceed to the next
page.
