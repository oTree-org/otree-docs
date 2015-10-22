Automated testing (bots)
========================

Your app's ``tests.py`` lets you define "bots" that simulate multiple players simultaneously
playing your app.

Tests with dozens of bots complete with in seconds, and afterward
automated tests can be run to verify correctness of the app (e.g. to
ensure that payoffs are being calculated correctly).

This automated test system saves the programmer the effort of having to
re-test the application every time something is changed.

Launching tests
~~~~~~~~~~~~~~~

oTree tests entire sessions, rather that individual apps in isolation.
This is to make sure the entire session runs, just as participants will
play it in the lab.

Let's say you want to test the session named ``ultimatum`` in
``settings.py``. To test, click the "Terminal" button in the oTree
launcher run the following command from your project's root directory:

.. code-block:: bash

    $ otree test ultimatum_game

This command will test the session, with the number of participants
specified in ``settings.py``. For example, ``num_bots`` is 30, then when
you run the tests, 30 bots will be instantiated and will play
concurrently.

To run tests for all sessions in ``settings.py``, run:

.. code-block:: bash

    $ otree test


Writing tests
~~~~~~~~~~~~~

Tests are contained in your app's ``tests.py``. Fill out the
``play_round()`` method of your ``PlayerBot``. It should simulate each page
submission. For example:

.. code-block:: python

    self.submit(views.Start)
    self.submit(views.Offer, {'offer_amount': 50})

Here, we first submit the ``Start`` page, which does not contain a form.
The next page is ``Offer``, which contains a form whose field is called
``offer_amount``, which we set to ``50``.

If a page contains several submissions, the synthax looks like

.. code-block:: python

    self.submit(views.Offer, {'first_offer_amount': 50, 'second_offer_amount': 150, 'third_offer_amount': 150})


The test system will raise an error if the bot submits invalid input for a page,
or if it submits pages in the wrong order.

Rather than programming many separate bots, you program one bot that can
play any variation of the game, using conditional logic.
For example, here is how you would play if
one treatment group sees a "threshold" page but the other treatment
group should see an "accept" page:

.. code-block:: python

    if self.group.threshold:
        self.submit(views.Threshold, {'offer_accept_threshold': 30})
    else:
        self.submit(views.Accept, {'offer_accepted': True})


To get the maximal benefit, your bot should thoroughly test all parts of
your code. Here are some ways you can test your app:

-  Ensure that it correctly rejects invalid input. For example, if you
   ask the user to enter a number that is a multiple of 3, you can
   verify that entering 4 will be rejected by using the
   ``submit_invalid`` method as follows. This line of code will raise an
   error if the submission is *accepted*:

   ``self.submit_invalid(views.EnterNumber, {'multiple_of_3': 4})``

-  You can put assert statements in the bot's ``validate_play()`` method
   to check that the correct values are being stored in the database.
   For example, if a player's bonus is defined to be 100 minus their
   offer, you can check your program is calculating it correctly as
   follows:

   ``self.submit(views.Offer, {'offer': 30})``

   ``assert self.player.bonus == 70``

-  You can use random amounts to test that your program can handle any
   type of random input:

   ``self.submit(views.Offer, {'offer': random.randint(0,100)})``

Bots can either be programmed to simulate playing the game according to
an ordinary strategy, or to test "boundary conditions" (e.g. by entering
invalid input to see if the application correctly rejects it). Or yet
the bot can enter random input on each page.

