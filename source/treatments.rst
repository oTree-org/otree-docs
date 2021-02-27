.. _treatments:
.. _creating_session:

Treatments
==========

To assign participants to different treatment groups, you
can use ``creating_session``. For example:

.. code-block:: python

    class Player(BasePlayer):
        color = models.StringField()

    def creating_session(subsession):
        # randomize to treatments
        for player in subsession.get_players():
            player.color = random.choice(['blue', 'red'])
            print('set player.color to', player.color)

You can also assign treatments at the group level (put the ``StringField``
in ``Group`` and change the above code to use ``get_groups()`` and ``group.color``).

``creating_session`` is run immediately when you click the "create session" button,
even if the app is not first in the ``app_sequence``.

Treatment groups & multiple rounds
----------------------------------

If your game has multiple rounds, a player could have different colors in different rounds,
because ``creating_session`` gets executed for each round independently.
To prevent this, set it on the participant, rather than the player.
Add ``'color'`` to ``PARTICIPANT_FIELDS``, then do this:

.. code-block:: python

    def creating_session(subsession):
        if subsession.round_number == 1:
            for player in subsession.get_players():
                participant = player.participant
                participant.color = random.choice(['blue', 'red'])

Then elsewhere in your code, you can access the participant's color with
``participant.color``.

For more on vars, see :ref:`vars`.

Balanced treatment groups
-------------------------

The above code makes a random drawing independently for each player,
so you may end up with an imbalance between "blue" and "red".
To solve this, you can use ``itertools.cycle``:

.. code-block:: python

    def creating_session(subsession):
        import itertools
        colors = itertools.cycle(['blue', 'red'])
        for player in subsession.get_players():
            player.color = next(colors)


.. _session_config_treatments:

Choosing which treatment to play
--------------------------------

In a live experiment, you often want to give a player a random treatment.
But when you are testing your game, it is often useful to choose explicitly which treatment to play.
Let's say you are developing the game from the above example and want to show your
colleagues both treatments (red and blue). You can create 2 session
configs that are the same,
except for ``color`` (in oTree Studio, add a "custom parameter"):

.. code-block:: python

    SESSION_CONFIGS = [
        dict(
            name='my_game_blue',
            app_sequence=['my_game'],
            num_demo_participants=1,
            color='blue'
        ),
        dict(
            name='my_game_red',
            app_sequence=['my_game'],
            num_demo_participants=1,
            color='red'
        ),
    ]

Then in your code you can get the current session's color with ``session.config['color'].``

You can even combine this with the randomization approach. You can check
``if 'color' in session.config:``; if yes, then use that color; if no,
then choose it randomly.

.. _edit_config:

Configure sessions
------------------

You can make your session configurable,
so that you can adjust the game's parameters in the admin interface.

.. image:: _static/admin/edit-config.png
    :align: center

For example, let's say you have a "num_apples" parameter.
The usual approach would be to define it in ``Constants``,
e.g. ``Constants.num_apples``.
But to make it configurable, you can instead define it in your session config.
For example:

.. code-block:: python

    dict(
        name='my_session_config',
        display_name='My Session Config',
        num_demo_participants=2,
        app_sequence=['my_app_1', 'my_app_2'],
        num_apples=10
    ),

When you create a session in the admin interface, there will be a text box to change this number.
You can also add help text with ``'doc'``:

.. code-block:: python

    dict(
        name='my_session_config',
        display_name='My Session Config',
        num_demo_participants=2,
        app_sequence=['my_app_1', 'my_app_2'],
        num_apples=10,
        doc="""
        Edit the 'num_apples' parameter to change the factor by which
        contributions to the group are multiplied.
        """
    ),

In your app's code, you can do ``session.config['num_apples']``.

Notes:

-   For a parameter to be configurable, its value must be a number, boolean, or string.
-   On the "Demo" section of the admin, sessions are not configurable.
    It's only available when creating a session in "Sessions" or "Rooms".
