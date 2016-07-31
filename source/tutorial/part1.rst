Part 1: Public goods game
=========================

We will now create a simple `public goods game <https://en.wikipedia.org/wiki/Public_goods_game>`__.

This is a three player game where each player is initially endowed with 100 points.
Each player individually makes a decision about how many of their points they want to contribute to the group.
The combined contributions are multiplied by 1.8, and then divided evenly three ways and redistributed back to the players.

The full code for the app we will write is
`here <https://github.com/oTree-org/oTree/tree/master/public_goods_simple>`__.

Upgrade oTree
-------------

To ensure you are using the latest version of oTree, open your command window and run:

.. code-block:: bash

    $ pip3 install --upgrade otree-core
    $ otree resetdb


Create the app
--------------

Use your command line to ``cd`` to the oTree project folder you created,
the one that contains ``requirements_base.txt``.

In this directory, create the public goods app with this shell command:

.. code-block:: bash

    $ otree startapp my_public_goods

Then go to the folder ``my_public_goods`` that was created.

Define models.py
----------------

Open ``models.py``. This file contains definitions of the game's data models (player, group, subsession),
as well as the constants used for configuration of the game.

First, let's modify the ``Constants`` class to define our constants and
parameters -- things that are the same for all players in all games.
(For more info, see :ref:`constants`.)

-  There are 3 players per group. So, let's change ``players_per_group``
   to 3. oTree will then automatically divide players into groups of 3.
-  The endowment to each player is 100 points. So, let's define
   ``endowment`` and set it to ``c(100)``. (``c()`` means it is a
   currency amount; see :ref:`currency`).
-  Each contribution is multiplied by 1.8. So let's define
   ``efficiency_factor`` and set it to 1.8:

Now we have:

.. code-block:: Python

    class Constants(BaseConstants):
        name_in_url = 'my_public_goods'
        players_per_group = 3
        num_rounds = 1

        endowment = c(100)
        efficiency_factor = 1.8

Now let's think about the main entities in this game: the Player and the
Group.

What data points are we interested in recording about each player? The
main thing is how much they contributed. So, we define a field
``contribution``, which is a currency (see :ref:`currency`):

.. code-block:: python

    class Player(BasePlayer):

        contribution = models.CurrencyField(min=0, max=Constants.endowment)


What data points are we interested in recording about each group? We
might be interested in knowing the total contributions to the group, and
the individual share returned to each player. So, we define those 2
fields:

.. code-block:: python

    class Group(BaseGroup):

        total_contribution = models.CurrencyField()
        individual_share = models.CurrencyField()

Now let's define a method that calculates the payoff (and other fields like ``total_contribution`` and ``individual_share``).
Let's call it ``set_payoffs``:


.. code-block:: python

    class Group(BaseGroup):

        total_contribution = models.CurrencyField()
        individual_share = models.CurrencyField()

        def set_payoffs(self):
            self.total_contribution = sum([p.contribution for p in self.get_players()])
            self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
            for p in self.get_players():
                p.payoff = Constants.endowment - p.contribution + self.individual_share

Define the template
-------------------

This game consists of a sequence of 2 pages:

-  Page 1: players decide how much to contribute
-  Page 2: players are told the results

In this section we will define the HTML templates to display the game.

So, let's make 2 HTML files under ``templates/my_public_goods/``.

The first is ``Contribute.html``, which contains a brief explanation of
the game, and a form field where the player can enter their
contribution.

.. code-block:: html+django

    {% extends "global/Base.html" %} {% load staticfiles otree_tags %}

    {% block title %} Contribute {% endblock %}

    {% block content %}

    <p>
        This is a public goods game with
        {{ Constants.players_per_group }} players per group,
        an endowment of {{ Constants.endowment }},
        and an efficiency factor of {{ Constants.efficiency_factor }}.
    </p>


    {% formfield player.contribution with label="How much will you contribute?" %}

    {% next_button %}

    {% endblock %}


(For more info on how to write a template, see :ref:`templates`.)

The second template will be called ``Results.html``.

.. code-block:: html+django

    {% extends "global/Base.html" %} {% load staticfiles otree_tags %}

    {% block title %} Results {% endblock %}

    {% block content %}

    <p>
        You started with an endowment of {{ Constants.endowment }},
        of which you contributed {{ player.contribution }}.
        Your group contributed {{ group.total_contribution }},
        resulting in an individual share of {{ group.individual_share }}.
        Your profit is therefore {{ player.payoff }}.
    </p>

    {% next_button %}

    {% endblock %}



Define views.py
---------------

Now we define our views, which contain the logic for how to display the
HTML templates. (For more info, see :ref:`views`.)

Since we have 2 templates, we need 2 ``Page`` classes in ``views.py``.
The names should match those of the templates (``Contribute`` and
``Results``).

First let's define ``Contribute``. This page contains a form, so
we need to define ``form_model`` and ``form_fields``.
Specifically, this form should let you set the ``contribution``
field on the player. (For more info, see :ref:`forms`.)

.. code-block:: python

    class Contribute(Page):

        form_model = models.Player
        form_fields = ['contribution']

Now we define ``Results``. This page doesn't have a form so our class
definition can be empty (with the ``pass`` keyword).

.. code-block:: python

    class Results(Page):
        pass


We are almost done, but one more page is needed. After a player makes a
contribution, they cannot see the results page right away; they first
need to wait for the other players to contribute. You therefore need to
add a ``WaitPage``. When a player arrives at a wait page,
they must wait until all other players in the group have arrived.
Then everyone can proceed to the next page. (For more info, see :ref:`wait_pages`).

When all players have
completed the ``Contribute`` page, the players' payoffs can be
calculated. You can trigger this calculation inside the the
``after_all_players_arrive`` method on the ``WaitPage``, which
automatically gets called when all players have arrived at the wait
page. Another advantage of putting the code here is that it only gets
executed once, rather than being executed separately for each
participant, which is redundant.

We write ``self.group.set_payoffs()`` because earlier we decided to name
the payoff calculation method ``set_payoffs``, and it's a method under
the ``Group`` class. That's why we prefix it with ``self.group``.

.. code-block:: python

    class ResultsWaitPage(WaitPage):

        def after_all_players_arrive(self):
            self.group.set_payoffs()

Now we define ``page_sequence`` to specify the order in which the pages
are shown:

.. code-block:: python

    page_sequence = [
        Contribute,
        ResultsWaitPage,
        Results
    ]


Define the session config in settings.py
----------------------------------------

Now we go to ``settings.py`` in the project's root directory and add an entry to ``SESSION_CONFIGS``.

In lab experiments, it's typical for users to fill out an exit survey, and
then see how much money they made. So let's do this by adding the
existing "exit survey" and "payment info" apps to ``app_sequence``.

.. code-block:: python

    SESSION_CONFIGS = [
        {
            'name': 'my_public_goods',
            'display_name': "My Public Goods (Simple Version)",
            'num_demo_participants': 3,
            'app_sequence': ['my_public_goods', 'survey', 'payment_info'],
        },
        # other session configs ...
    ]


Reset the database and run
--------------------------

Enter:

.. code-block:: bash

    $ otree resetdb
    $ otree runserver

Then open your browser to ``http://127.0.0.1:8000`` to play the game.

Fix any errors
--------------

If there is an error in your code, the command line will display a "traceback" (error message) that is formatted something like this::

    C:\oTree\chris> otree resetdb
    Traceback (most recent call last):
      File "C:\oTree\chris\manage.py", line 10, in <module>
        execute_from_command_line(sys.argv, script_file=__file__)
      File "c:\otree\core\otree\management\cli.py", line 170, in execute_from_command_line
        utility.execute()
      File "C:\oTree\venv\lib\site-packages\django\core\management\__init__.py", line 328, in execute
        django.setup()
      File "C:\oTree\venv\lib\site-packages\django\__init__.py", line 18, in setup
        apps.populate(settings.INSTALLED_APPS)
      File "C:\oTree\venv\lib\site-packages\django\apps\registry.py", line 108, in populate
        app_config.import_models(all_models)
      File "C:\oTree\venv\lib\site-packages\django\apps\config.py", line 198, in import_models
        self.models_module = import_module(models_module_name)
      File "C:\Python27\Lib\importlib\__init__.py", line 37, in import_module
        __import__(name)
      File "C:\oTree\chris\public_goods_simple\models.py", line 40
        self.total_contribution = sum([p.contribution for p in self.get_players()])
           ^
    IndentationError: expected an indented block


Your first step should be to look at the last lines of the message.
Specifically, find the file and line number of the last entry.
In the above example, it's ``"C:\oTree\chris\public_goods_simple\models.py", line 40``.
Open that file and go to that line number to see if there is a problem there.
Specifically, look for the problem mentioned at the last line of the traceback.
In this example, it is ``IndentationError: expected an indented block``
(which indicates that the problem has to do with code indentation).
Python editors like PyCharm usually underline errors in red to make them easier to find.
Try to fix the error then run the command again.

Sometimes the last line of the traceback refers to a file that is not part of your code.
For example, in the below traceback, the last line refers to ``/site-packages/easymoney.py``,
which is not part of my app, but rather an external package::

    Traceback:
    File "/usr/local/lib/python3.5/site-packages/django/core/handlers/base.py" in get_response
      132.                     response = wrapped_callback(request, *callback_args, **callback_kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/views/generic/base.py" in view
      71.             return self.dispatch(request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/utils/decorators.py" in _wrapper
      34.             return bound_func(*args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/views/decorators/cache.py" in _wrapped_view_func
      57.         response = view_func(request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/utils/decorators.py" in bound_func
      30.                 return func.__get__(self, type(self))(*args2, **kwargs2)
    File "/usr/local/lib/python3.5/site-packages/django/utils/decorators.py" in _wrapper
      34.             return bound_func(*args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/views/decorators/cache.py" in _cache_controlled
      43.             response = viewfunc(request, *args, **kw)
    File "/usr/local/lib/python3.5/site-packages/django/utils/decorators.py" in bound_func
      30.                 return func.__get__(self, type(self))(*args2, **kwargs2)
    File "/usr/local/lib/python3.5/site-packages/otree/views/abstract.py" in dispatch
      315.                 request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/views/generic/base.py" in dispatch
      89.         return handler(request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/otree/views/abstract.py" in get
      814.         return super(FormPageMixin, self).get(request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/vanilla/model_views.py" in get
      294.         context = self.get_context_data(form=form)
    File "/usr/local/lib/python3.5/site-packages/otree/views/abstract.py" in get_context_data
      193.         vars_for_template = self.resolve_vars_for_template()
    File "/usr/local/lib/python3.5/site-packages/otree/views/abstract.py" in resolve_vars_for_template
      212.         context.update(self.vars_for_template() or {})
    File "/Users/chris/oTree/public_goods/views.py" in vars_for_template
      108.             'total_payoff': self.player.payoff + Constants.fixed_pay}
    File "/usr/local/lib/python3.5/site-packages/easymoney.py" in <lambda>
      36.     return lambda self, other, context=None: self.__class__(method(self, _to_decimal(other)))
    File "/usr/local/lib/python3.5/site-packages/easymoney.py" in _to_decimal
      24.         return Decimal(amount)

    Exception Type: TypeError at /p/j0p7dxqo/public_goods/ResultsFinal/8/
    Exception Value: conversion from NoneType to Decimal is not supported

In these situations, look to see if any of your code is contained in the traceback.
Above we can see that the traceback goes through the file ``/Users/chris/oTree/public_goods/views.py``,
which is part of my project. The bug is on line 108, as indicated.

