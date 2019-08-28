.. _bots:

Bots
====

You can write "bots" that simulate participants playing your app,
so that you can test that it functions properly and can handle the traffic of a real experiment.

A lot of oTree users skip writing bots because they think it's complicated
or because they are too busy.
But bots are possibly the easiest part of oTree.
For a game with 2 pages, it's just 2 yield statements:

.. code-block:: python

    class PlayerBot(Bot):

        def play_round(self):
            yield (pages.Contribute, {'contribution': 10})
            yield (pages.Results)

Then, each time you make a change to your app,
you can just re-run this test. It's a great time saver.

Running tests
-------------

Let's say you have this session config:

.. code-block:: python

    dict(
        name='mysession',
        app_sequence=['ultimatum', 'survey'],
        num_demo_participants=1,
    ),

If each app in the ``app_sequence`` has bots, you can run them with::

    otree test mysession

To test with a specific number of participants
(otherwise it will default to ``num_demo_participants``)::

    otree test mysession 6

To run tests for all session configs::

    otree test

Exporting data
~~~~~~~~~~~~~~

Use the ``--export`` flag to export the results to a CSV file::

    otree test mysession --export

To specify the folder where the data is saved, do::

    otree test mysession --export=myfolder


Writing tests
-------------

Submitting pages
~~~~~~~~~~~~~~~~

Go to your app's ``tests.py``. It should make one ``yield`` per page
submission. For example:

.. code-block:: python

    class PlayerBot(Bot):
        def play_round(self):
            yield (pages.Start)
            yield (pages.Offer, {'offer_amount': 50})

Here, we first submit the ``Start`` page, which does not contain a form.
The next page is ``Offer``, which contains a form whose field is called
``offer_amount``, which we set to ``50``.

We use ``yield``, because in Python,
``yield`` means to produce or generate a value.
You could think of the bot as a machine that yields (i.e. generates) submissions.

If a page contains several fields, use a dictionary with multiple items:

.. code-block:: python

    yield (pages.Offer, {'first_offer_amount': 50, 'second_offer_amount': 150, 'third_offer_amount': 150})


The test system will raise an error if the bot submits invalid input for a page,
or if it submits pages in the wrong order.

You use ``if`` statements to play any player or round number. For example:

.. code-block:: python

    if self.round_number == 1:
        yield (pages.Introduction)
    if self.player.id_in_group == 1:
        yield (pages.Offer, {'offer': 30})
    else:
        yield (pages.Accept, {'offer_accepted': True})


Your ``if`` statements can depend on ``self.player``, ``self.group``,
``self.round_number``, etc.

You should ignore wait pages when writing bots. Just write a ``yield`` for every page
that is submitted. The bot will wait
until any wait pages are cleared, then it will execute the next ``yield``.

Rounds
~~~~~~

As the name indicates, ``play_round()`` should just play 1 round at a time.
oTree will automatically execute it ``num_rounds`` times.

Asserts
~~~~~~~

You can use ``assert`` statements to ensure that your code is working as you expect.

For example:

.. code-block:: python

    class PlayerBot(Bot):

        def play_round(self):
            assert self.player.money_left == c(10)
            yield (pages.Contribute, {'contribution': c(1)})
            assert self.player.money_left == c(9)
            yield (pages.Results)

If the asserted condition does not hold, an error will be raised.
(You can read about ``assert`` in the Python documentation.)

The ``assert`` statements are executed immediately before submitting the following page.
For example, let's imagine the ``page_sequence`` for the game in the above example is
``[Contribute, ResultsWaitPage, Results]``. The bot submits ``pages.Contribute``,
is redirected to the wait page, and is then redirected to the ``Results`` page.
At that point, the ``Results`` page is displayed, and then the line
``assert self.player.money_left == c(9)`` is executed.

Testing form validation
~~~~~~~~~~~~~~~~~~~~~~~

If you use :ref:`form validation <form-validation>`,
you should test that your app is correctly rejecting invalid input from the user,
by using ``SubmissionMustFail()``.

For example, let's say you have this page:

.. code-block:: python

    class MyPage(Page):

        form_model = 'player'
        form_fields = ['int1', 'int2']

        def error_message(self, values):
            if values["int1"] + values["int2"] != 100:
                return 'The numbers must add up to 100'

Here is how to test that it is working properly:

.. code-block:: python


    from . import pages
    from otree.api import Bot, SubmissionMustFail

    class PlayerBot(Bot):

        def play_round(self):
            yield SubmissionMustFail(pages.MyPage, {'int1': 0, 'int2': 0})
            yield SubmissionMustFail(pages.MyPage, {'int1': 101, 'int2': 0})
            yield (pages.MyPage, {'int1': 99, 'int2': 1})
            ...

The bot will submit ``MyPage`` 3 times. If one of the first 2 submissions **succeeds**,
an error will be raised, because it is not supposed to succeed.

.. _error_fields:

error_fields
''''''''''''

When using ``SubmissionMustFail`` on forms with multiple fields, you can
use ``error_fields`` for extra thoroughness.

For example, let's say we a submit a valid ``age``, but
an invalid ``weight`` and ``height``:

.. code-block:: python

        yield SubmissionMustFail(
            pages.Survey,
            {
                'age': 20,
                'weight': -1,
                'height': -1,
            }
        )

What's missing is that the bot system doesn't tell us exactly *why*
the submission fails. Is it an invalid ``weight``, ``height``, or both?
``error_fields`` can resolve the ambiguity:

.. code-block:: python

        yield SubmissionMustFail(
            pages.Survey,
            {
                'age': 20,
                'weight': -1,
                'height': -1,
            },
            error_fields=['weight', 'height']
        )

This will verify that ``weight`` and ``height`` contained errors,
but ``age`` did not.

If :ref:`error_message <error_message>` returns an error,
then ``error_fields`` will be ``['__all__']``.

Test cases
~~~~~~~~~~

You can define an attribute ``cases`` on your PlayerBot class
that lists different test cases.
For example, in a public goods game, you may want to test 3 scenarios:

-   All players contribute half their endowment
-   All players contribute nothing
-   All players contribute their entire endowment (100 points)

We can call these 3 test cases "basic", "min", and "max", respectively,
and put them in ``cases``. Then, oTree will execute the bot 3 times, once for
each test case. Each time, a different value from ``cases`` will be assigned to ``self.case``
in the bot.

For example:

.. code-block:: python

    from . import pages
    from otree.api import Bot, SubmissionMustFail


    class PlayerBot(Bot):

        cases = ['basic', 'min', 'max']

        def play_round(self):
            yield (pages.Introduction)

            if self.case == 'basic':
                assert self.player.payoff == None

            if self.case == 'basic':
                if self.player.id_in_group == 1:
                    for invalid_contribution in [-1, 101]:
                        yield SubmissionMustFail(pages.Contribute, {'contribution': invalid_contribution})
            contribution = {
                'min': 0,
                'max': 100,
                'basic': 50,
            }[self.case]

            yield (pages.Contribute, {"contribution": contribution})
            yield (pages.Results)

            if self.player.id_in_group == 1:

                if self.case == 'min':
                    expected_payoff = 110
                elif self.case == 'max':
                    expected_payoff = 190
                else:
                    expected_payoff = 150
                assert self.player.payoff == expected_payoff

``cases`` needs to be a list, but it can contain any data type, such as strings,
integers, or even dictionaries. Here is a trust game bot that uses dictionaries
as cases.

.. code-block:: python

    from . import pages
    from otree.api import Bot, SubmissionMustFail


    class PlayerBot(Bot):

        cases = [
            {'offer': 0, 'return': 0, 'p1_payoff': 10, 'p2_payoff': 0},
            {'offer': 5, 'return': 10, 'p1_payoff': 15, 'p2_payoff': 5},
            {'offer': 10, 'return': 30, 'p1_payoff': 30, 'p2_payoff': 0}
        ]

        def play_round(self):
            case = self.case
            if self.player.id_in_group == 1:
                yield (pages.Send, {"sent_amount": case['offer']})

            else:
                for invalid_return in [-1, case['offer'] * Constants.multiplication_factor + 1]:
                    yield SubmissionMustFail(pages.SendBack, {'sent_back_amount': invalid_return})
                yield (pages.SendBack, {'sent_back_amount': case['return']})

            yield (pages.Results)


            if self.player.id_in_group == 1:
                expected_payoff = case['p1_payoff']
            else:
                expected_payoff = case['p2_payoff']

            assert self.player.payoff == expected_payoff

Checking the HTML
~~~~~~~~~~~~~~~~~

In the bot, ``self.html`` will be a string
containing the HTML of the page you are about to submit.
This is useful for asserts:

.. code-block:: python

    if self.player.id_in_group == 1:
        assert self.player.is_winner
        assert 'you won the game' in self.html
    else:
        assert not self.player.is_winner
        assert 'you did not win' in self.html
    yield pages.Results
    # etc...

``self.html`` is updated with the next page's HTML, after every ``yield`` statement.
Linebreaks and extra spaces are ignored.

Automatic HTML checks
~~~~~~~~~~~~~~~~~~~~~

An error will be raised if the bot is trying to submit form fields that are not actually found
in the page's HTML, or if the page's HTML is missing a submit button.

However, the bot system is not able to see fields and buttons that are added dynamically with JavaScript.
In these cases, you should disable the HTML check by using ``Submission``
with ``check_html=False``. For example, change this:

.. code-block:: python

    class PlayerBot(Bot)
        def play_round(self):
            yield (pages.MyPage, {'foo': 99})

to this:

.. code-block:: python

    from otree.api import Submission

    class PlayerBot(Bot)
        def play_round(self):
            yield Submission(pages.MyPage, {'foo': 99}, check_html=False)

(If you used ``Submission`` without ``check_html=False``,
the two code samples would be equivalent.)

If many of your pages incorrectly fail the static HTML checks,
you can bypass these checks globally by setting ``BOTS_CHECK_HTML = False``
in ``settings.py``.

.. _bot_timeout:

Simulate a page timeout
~~~~~~~~~~~~~~~~~~~~~~~

You can use ``Submission`` with ``timeout_happened=True``:

.. code-block:: python

    from otree.api import Submission

    class PlayerBot(Bot)
        def play_round(self):
            yield Submission(pages.MyPage, {'foo': 99}, timeout_happened=True)

Misc note
~~~~~~~~~

In bots, it is risky to assign
``player = self.player`` (or ``participant = self.participant``, etc),
even though that kind of code is encouraged in ``pages.py``.

Because if there is a ``yield`` in between, the data can be stale:

.. code-block:: python

        def play_round(self):
            player = self.player
            assert player.money_left == c(10) # OK
            yield (pages.Contribute, {'contribution': c(1)})
            # don't do this!
            # "player" variable still has the data from BEFORE pages.Contribute was submitted.
            assert player.money_left == c(9)

It's safer to use ``self.player.money_left`` directly,
because doing ``self.player`` gets the most recent data from the database.


.. _browser-bots:

Browser bots
------------

Bots can run in the browser.
They run the same way as command-line bots.

The advantage is that they test the app in a more full and realistic
way, because they use a real web browser.
Also, while it's playing you can briefly see
each page and notice if there are visual errors.

Basic use
~~~~~~~~~

-   Write your ``tests.py`` as described above.
-   In ``settings.py``, set ``use_browser_bots=True`` for your session config(s).
-   Run your server and create a session. The pages will auto-play
    with browser bots, once the start links are opened.
-   If using Heroku, make sure the ``runprodserver2of2`` dyno is enabled.

Command-line browser bots (running locally)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can launch browser bots from the command line, using ``otree browser_bots``.

-   Make sure Google Chrome is installed, or set ``BROWSER_COMMAND`` in ``settings.py``
    (more info below).
-   Run your server (e.g. ``otree devserver``)
-   Close all Chrome windows.
-   Run this::

        otree browser_bots mysession

This will launch several Chrome tabs and run the bots.
When finished, the tabs will close, and you will see a report in
your terminal window.

If Chrome doesn't close windows properly,
make sure you closed all Chrome windows prior to launching the command.

Command-line browser bots on a remote server (e.g. Heroku)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the server is running on a host/port other than the usual ``http://localhost:8000``,
you need to pass ``--server-url``.
For example, if it's on Heroku, you would do like this::

    otree browser_bots mysession --server-url=https://YOUR-SITE.herokuapp.com


Performance
~~~~~~~~~~~

On my PC, running the default public_goods session with 3 participants takes about 4-5 seconds,
and with 9 participants takes about 10 seconds.

Choosing session configs and sizes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify the number of participants::

    otree browser_bots mysession 6

To test all session configs, just run this::

    otree browser_bots


Browser bots: misc notes
~~~~~~~~~~~~~~~~~~~~~~~~

You can use a browser other than Chrome by setting ``BROWSER_COMMAND``
in ``settings.py``. Then, oTree will open the browser by doing something like
``subprocess.Popen(settings.BROWSER_COMMAND)``.

(Optional) To make the bots run more quickly, disable most/all add-ons, especially ad-blockers.
Or `create a fresh Chrome profile <https://support.google.com/chrome/answer/142059?hl=en>`__
that you use just for browser testing. When oTree launches Chrome,
it should use the last profile you had open.

