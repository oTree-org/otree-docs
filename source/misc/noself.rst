The new app.py format
=====================

As of Jan 2021, there is a new optional format for oTree apps.
It replaces ``models.py`` and ``pages.py`` with a single ``app.py``.
It's only available in oTree Lite, which can run either format (models.py or app.py).

The new format unifies oTree's syntax.
For example, before, you needed to write either ``player.payoff``, ``self.payoff``,
or ``self.player.payoff``, depending on what part of the code you were in.
Now, you can always write ``player.payoff`.
In fact, the ``self`` keyword has been eliminated entirely
(this app.py format can also be called the "no-self" format).

**If you use oTree Studio**, you don't need to worry about this new format.
All changes will be handled automatically.

**If you use a text editor**, you can keep using the existing format, or use the new one if you wish.
They both have access to the same features. The models.py format will continue to be fully supported
and get access to the newest features.

About the new format
--------------------

1. "self" is totally gone from your app's code.
2. Whenever you want to refer to the player, you write player. Same for group and subsession.
3. Each method in oTree is changed to a function.
4. There is no more models.py and pages.py. The whole game fits into one file (app.py).
5. Everything else stays the same. All functions and features do the same thing as before.

Here is an example of an app.py in the "no self" format (with the dictator game):


.. code-block:: python

    class Subsession(BaseSubsession):
        pass


    class Group(BaseGroup):
        pass

    class Player(BasePlayer):
        kept = models.CurrencyField(
            min=0,
            max=Constants.endowment,
            label="I will keep",
        )


    # FUNCTIONS
    def set_payoffs(group):
        player1 = group.get_player_by_id(1)
        player2 = group.get_player_by_id(2)
        player1.payoff = group.kept
        player2.payoff = Constants.endowment - group.kept


    # PAGES
    class Introduction(Page):
        pass


    class Offer(Page):
        form_model = 'group'
        form_fields = ['kept']

        def is_displayed(player):
            return player.id_in_group == 1


    class ResultsWaitPage(WaitPage):
        after_all_players_arrive = 'set_payoffs'


    class Results(Page):
        def vars_for_template(player):
            group = player.group

            return dict(payoff=player.payoff, offer=Constants.endowment - group.kept)


So, what has changed?

#.  As you see, set_payoffs has changed from a group method to a regular function that takes "group" as its argument. This should be clearer to most people.
#.  is_displayed and vars_for_template are no longer page methods that take an argument 'self', but direct functions of the player. Now you can directly write 'player' without needing 'self.' in front of it. (If you are using a text editor like PyCharm, you should add @staticmethod before vars_for_template and is_displayed to indicate that they are not regular methods.)
#.  There is no longer any distinction between page methods and model methods. The is_displayed and vars_for_template can freely be moved up into the "FUNCTIONS" section, and reused between pages, or put inside a page class if they only pertain to that class.
#.  Bonus: we can simplify the app folder. Let's take a look at the original structure:

.. code-block::

    dictator/
        _builtin/
        templates/
            dictator/
                Decide.html
                Results.html
        __init__.py
        models.py
        pages.py

Now since we fit everything in app.py, this folder is smaller, so there is room for the templates to come live downstairs.
Also, that mysterious _builtin/ folder is not needed anymore.
So we end up with this:

.. code-block::

    dictator/
        __init__.py
        app.py
        Decide.html
        Results.html

Second bonus: The "import" section at the top is simplified.

Before:

.. code-block:: python

    # models.py
    from otree.api import (
        models,
        widgets,
        BaseConstants,
        BaseSubsession,
        BaseGroup,
        BasePlayer,
        Currency as c,
        currency_range
    )

    # pages.py
    from otree.api import Currency as c, currency_range
    from ._builtin import Page, WaitPage
    from .models import Constants


    After:

    # app.py
    from otree.api import (
        models,
        widgets,
        BaseConstants,
        BaseSubsession,
        BaseGroup,
        BasePlayer,
        Currency as c,
        currency_range,
        Page,
        WaitPage,
    )

How does this affect you?
-------------------------

1. If you use oTree Studio, your code will get automatically upgraded to the new format, behind the scenes. oTree Studio will look and function essentially the same.

2. If you use a text editor, you can choose to use whichever format you prefer.
It is fine for me to support both formats in the long term, since it is just a small internal component that loads your code from a different place (e.g. looking in models.Subsession.creating_session vs app.creating_session).
Both formats have access to the same features. You can keep developing new apps in the models.py format, and you will continue to benefit from new features.

This app.py format is only available with oTree Lite.
oTree Lite supports both formats. Within the same project, you can have some apps that use the models.py format, and some that use the app.py format.

There is a command "otree remove_self" that can automatically convert the models.py format to the app.py format. This is for people who are curious what their app would look like in the no-self format. Later, I will describe this command and how to use it.


FAQ
---

Q: Do I need to change my existing apps?

A: No, you can keep them as is. The "no-self" format is optional.


Q: Will I have to re-learn oTree for this new format?

A: No, you don't really need to relearn anything. Every function, from creating_session, to before_next_page, etc, does the same thing as before. And there are no changes to other parts of oTree like templates or settings.py.


Q: Why didn't you implement it this way originally?

A: The first reason is that oTree got its structure from Django. But now that I made oTree Lite which is not based on Django, I have more freedom to design the app structure the way I see fit. The second reason is that this is quite a tailored design. It was necessary to wait and see how oTree evolved and how people use oTree before I could come up with the most appropriate design.



How to use it
-------------

First, ensure that you are using oTree Lite::

    pip3 install -U "otree>=5a"

Then do one of the following:

a.  Convert your existing apps using ``otree remove_self``, as described in this page.
b.  Download `this <https://github.com/oTree-org/oTree/tree/noself-demo>`__ repo,
    which has all the sample games in the app.py format.
    When you next run ``otree startapp``, it will create an app in the app.py format.

There are now 2 branches of the documentation. These docs you are reading now are based on the app.py format
(see the note at the top of the page).

Try it out and send me any feedback!


The "otree remove_self" command
-------------------------------

If you prefer the app.py format, or are curious what your app would look like in this format, follow these steps.
First, then install oTree Lite::

    pip3 install -U "otree>=5a"

First, save a copy of your original code. Run::

    otree remove_self

Then check the output (app.py and tests_noself.py), then run ``otree remove_self_finalize``.
That will delete the old files and move your templates into the main folder.

Note this command pretty aggressively converts all your model methods to functions. For example, if you have this:

.. code-block:: python

    class Player(BasePlayer):
      def xyz(self):
        return 'whatever'

``otree remove_self`` will convert it to a function like:

.. code-block:: python

    class Player(BasePlayer):
      pass

    def xyz(player):
      return 'whatever'

If ``xyz`` is a built-in oTree method, then this is OK.
But if it's a method you are calling yourself like ``player.xyz()``,
then this might break your code. You would need to change ``player.xyz()`` to ``xyz(player)``.

If you are doing {{ player.xyz() }} in a template, you need to instead calculate ``xyz(player)`` in ``vars_for_template``
and pass it to your template as a separate variable.


Misc notes
----------

-   ``before_next_page`` now takes a second arg ``timeout_happened``.
-   You can optionally add a type hint to your function signatures. For example,
    change ``def xyz(player)`` to ``def xyz(player: Player)``. If you use PyCharm or VS Code,
    that will mean you get better autocompletion.
