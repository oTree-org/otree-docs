.. _bots:

Bots
====

You can write "bots" that simulate participants playing your app,
to test that it works properly and can handle the traffic of a real experiment.

Each time you make a change to your app,
you can just re-run your tests. It's a great time saver.

.. _browser-bots:

Running bots
------------

-   In your session config, set ``use_browser_bots=True``.
-   Run your server and create a session. The pages will auto-play
    with browser bots, once the start links are opened.
-   If using Heroku, make sure the second dyno is enabled.

Writing tests
-------------

If you are using oTree Studio, go to the "Tests" section of your app.

If you are using a text editor, go to ``tests.py``.

Submitting pages
~~~~~~~~~~~~~~~~

You should make one ``yield`` per page submission. For example:

.. code-block:: python

    yield pages.Start
    yield pages.Survey(name="Bob", age=20)

Here, we first submit the ``Start`` page, which does not contain a form.
The following page has 2 form fields, so we submit a dict.

The test system will raise an error if the bot submits invalid input for a page,
or if it submits pages in the wrong order.

You use ``if`` statements to play any player or round number. For example:

.. code-block:: python

    if self.round_number == 1:
        yield pages.Introduction
    if self.player.id_in_group == 1:
        yield pages.Offer, dict(offer=30)
    else:
        yield pages.Accept, dict(offer_accepted=True)


Your ``if`` statements can depend on ``self.player``, ``self.group``,
``self.round_number``, etc.

Ignore wait pages when writing bots. The bot will wait
until any wait pages are cleared, then it will execute the next ``yield``.

Rounds
~~~~~~

Your bot code should just play 1 round at a time.
oTree will automatically execute it ``num_rounds`` times.

expect()
~~~~~~~~

.. note::

    The ``expect()`` function was introduced in September 2019.
    Previously we recommended using ``assert`` statements, which are still OK
    but when ``assert`` is used with browser bots, the error is not reported clearly.

You can use ``expect`` statements to ensure that your code is working as you expect.

For example:

.. code-block:: python

    from otree.api import expect

    expect(self.player.num_apples, 100)
    yield pages.Eat, dict(apples_eaten=1)
    expect(self.player.num_apples, 99)

If ``self.player.num_apples`` is not 99, then you will be alerted with an error.

You can also use expect with 3 arguments, like ``expect(self.player.budget, '<', 100)``.
This will verify that ``self.player.budget`` is less than 100.
You can use the following operators:
``'<'``,
``'<='``,
``'=='``,
``'>='``,
``'>'``,
``'!='``,
``'in'``,
``'not in'``.

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

    from otree.api SubmissionMustFail

    yield SubmissionMustFail(pages.MyPage, dict(int1=99, int2=0))
    yield pages.MyPage, dict(int1=99, int2=1)

The bot will submit ``MyPage`` twice. If the first submission **succeeds**,
an error will be raised, because it is not supposed to succeed.


Checking the HTML
~~~~~~~~~~~~~~~~~

``self.html`` contains the HTML of the page you are about to submit.
You can use this together with ``expect()``:

.. code-block:: python

    from otree.api import expect

    if self.player.id_in_group == 1:
        expect(self.player.is_winner, True)
        print(self.html)
        expect('you won the game', 'in', self.html)
    else:
        expect(self.player.is_winner, False)
        expect('you did not win', 'in', self.html)
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

    yield pages.MyPage, dict(foo=99)

to this:

.. code-block:: python

    from otree.api import Submission
    yield Submission(pages.MyPage, dict(foo=99), check_html=False)

(If you used ``Submission`` without ``check_html=False``,
the two code samples would be equivalent.)

.. _bot_timeout:

Simulate a page timeout
~~~~~~~~~~~~~~~~~~~~~~~

You can use ``Submission`` with ``timeout_happened=True``:

.. code-block:: python

    from otree.api import Submission
    yield Submission(pages.MyPage, dict(foo=99), timeout_happened=True)

Misc note
~~~~~~~~~

In bots, it is risky to assign
``player = self.player`` (or ``participant = self.participant``, etc),
even though that kind of code is encouraged in ``pages.py``.

Because if there is a ``yield`` in between, the data can be stale:

.. code-block:: python

    from otree.api import expect

    player = self.player
    expect(player.money_left, c(10))
    yield pages.Contribute, dict(contribution=c(1))
    # don't do this!
    # "player" variable still has the data from BEFORE pages.Contribute was submitted.
    expect(player.money_left, c(9))

It's safer to use ``self.player.money_left`` directly,
because doing ``self.player`` gets the most recent data from the database.

Advanced features
-----------------

See :ref:`bots_advanced`

