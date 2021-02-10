.. _bots_advanced:

Bots: advanced features
=======================

These are advanced features that are mostly unsupported in oTree Studio.

.. _cli-bots:

Command line bots
-----------------

An alternative to running bots in your web browser is to run them in the command line.
Command line bots run faster and require less setup.

Run this::

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


Command-line browser bots
-------------------------

You can launch browser bots from the command line, using ``otree browser_bots``.

-   Make sure Google Chrome is installed, or set ``BROWSER_COMMAND`` in ``settings.py``
    (more info below).
-   Set ``OTREE_REST_KEY`` env var as described in :ref:`rest`.
-   Run your server
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

.. _cases:

Test cases
----------

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

.. note::

    If you use cases, it's better to use :ref:`cli-bots` since browser bots will only execute a single case.

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


.. _error_fields:

error_fields
------------

When using ``SubmissionMustFail`` on forms with multiple fields, you can
use ``error_fields`` for extra thoroughness.

For example, let's say we a submit a valid ``age``, but
an invalid ``weight`` and ``height``:

.. code-block:: python

    yield SubmissionMustFail(
        pages.Survey,
        dict(
            age=20,
            weight=-1,
            height=-1,
        )
    )

What's missing is that the bot system doesn't tell us exactly *why*
the submission fails. Is it an invalid ``weight``, ``height``, or both?
``error_fields`` can resolve the ambiguity:

.. code-block:: python

    yield SubmissionMustFail(
        pages.Survey,
        dict(
            age=20,
            weight=-1,
            height=-1,
        ),
        error_fields=['weight', 'height']
    )

This will verify that ``weight`` and ``height`` contained errors,
but ``age`` did not.

If :ref:`error_message <error_message>` returns an error,
then ``error_fields`` will be ``['__all__']``.

Misc note
---------

In bots, it is risky to assign
``player = self.player`` (or ``participant = self.participant``, etc),
even though that kind of code is encouraged elsewhere.

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

Live pages
----------

To test live methods with bots, define ``call_live_method`` as a top-level function in ``tests.py``.
(Not available in oTree Studio.)
This function should simulate the sequence of calls to your ``live_method``.
The argument ``method`` simulates the live method on your Player model.
For example, ``method(3, 'hello')`` calls the live method on Player 3 with ``data`` set to ``'hello'``.
For example:

.. code-block:: python

    def call_live_method(method, **kwargs):
        method(1, {"offer": 50})
        method(2, {"accepted": False})
        method(1, {"offer": 60})
        retval = method(2, {"accepted": True})
        # you can do asserts on retval

``kwargs`` contains at least the following parameters.

-   ``case`` as described in :ref:`cases`.
-   ``page_class``: the current page class, e.g. ``pages.MyPage``.
-   ``round_number``

``call_live_method`` will be automatically executed when the fastest bot in the group
arrives on a page with ``live_method``.
(Other bots may be on previous pages at that point, unless you restrict this with a WaitPage.)
