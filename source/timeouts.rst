.. _timeouts:

Timeouts
========

Basics
------

.. _timeout_seconds:

timeout_seconds
~~~~~~~~~~~~~~~

To set a time limit on your page, add ``timeout_seconds``:

.. code-block:: python

    class Page1(Page):
        timeout_seconds = 60

After the time runs out, the page auto-submits.

If you are running the production server (``runprodserver``),
the page will always submit, even if the user closes their browser window.
However, this does not occur if you are running the development server
(``zipserver`` or ``devserver``).

If you need the timeout to be dynamically determined, use :ref:`get_timeout_seconds`.

.. _timeout_happened:

timeout_happened
~~~~~~~~~~~~~~~~

You can check if the page was submitted by timeout:

.. code-block:: python

    class Page1(Page):
        timeout_seconds = 60

        def before_next_page(self):
            if self.timeout_happened:
                self.player.xyz = True


``timeout_happened`` only exists in ``before_next_page``.

.. _get_timeout_seconds:

get_timeout_seconds
~~~~~~~~~~~~~~~~~~~

This is a more flexible alternative to ``timeout_seconds``,
so that you can make the timeout depend on ``self.player``, ``self.session``, etc.

For example:

.. code-block:: python

    class MyPage(Page):

        def get_timeout_seconds(self):
            return self.player.my_page_timeout_seconds


Or, using a custom session config parameter (see :ref:`session_config_treatments`).

.. code-block:: python

    class MyPage(Page):

        def get_timeout_seconds(self):
            return self.session.config['my_page_timeout_seconds']


Advanced techniques
-------------------

.. _timeout_form:

Forms submitted by timeout
~~~~~~~~~~~~~~~~~~~~~~~~~~

If a form is auto-submitted because of a timeout,
oTree will try to save whichever fields were filled out at the time of submission.
If a field in the form has an error because it is missing or invalid,
it will be set to ``0`` for numeric fields, ``False`` for boolean fields, and the empty
string ``''`` for string fields.

If you want to discard the auto-submitted values, you can just
check if ``self.timeout_happened``, and if so, overwrite the values.

If the ``error_message()`` method fails, then the whole form might be invalid,
so the whole form will be discarded.

Timeouts that span multiple pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use ``get_timeout_seconds`` to create timeouts that span multiple
pages, or even the entire session. The trick is to define a fixed "expiration time",
and then on each page, make ``get_timeout_seconds`` return the number of seconds
until that expiration time.

First, choose a place to start the timer. This could be a page called
"Start" that displays text like "Press the button when you're ready to start".
When the user clicks the "next" button, ``before_next_page`` will be executed:

.. code-block:: python

    class Start(Page):

        def is_displayed(self):
            return self.round_number == 1

        def before_next_page(self):
            import time
            # user has 5 minutes to complete as many pages as possible
            self.participant.vars['expiry'] = time.time() + 5*60

(You could also start the timer in ``after_all_players_arrive`` or ``creating_session``,
and it could be stored in ``session.vars`` if it's the same for everyone in the session.)

Then, each page's ``get_timeout_seconds`` should be the number of seconds
until that expiration time:

.. code-block:: python

    class Page1(Page):
        def get_timeout_seconds(self):
            return self.participant.vars['expiry'] - time.time()

When time runs out, ``get_timeout_seconds`` will return 0 or a negative value,
which will result in the page loading and being auto-submitted right away.
This means all the remaining pages will quickly flash on the participant's screen,
which is usually undesired. So, you should use
``is_displayed`` to skip the page if there's not enough time
for the participant to realistically read the whole page.

.. code-block:: python

    class Page1(Page):
        def get_timeout_seconds(self):
            return self.participant.vars['expiry'] - time.time()

        def is_displayed(self):
            return self.get_timeout_seconds() > 3

(If you are curious how to avoid repeating this code on every page, see the section on :ref:`composition <composition>` for some hints.)

The default text on the timer says "Time left to complete this page:".
But if your timeout spans multiple pages, you should word it more accurately,
by setting ``timer_text``:

.. code-block:: python

    class Page1(Page):

        timer_text = 'Time left to complete this section:'

        def get_timeout_seconds(self):
            return self.participant.vars['expiry'] - time.time()


Customizing the timer
~~~~~~~~~~~~~~~~~~~~~

Hiding the timer
^^^^^^^^^^^^^^^^

If you want to hide the timer,
use this CSS:

.. code-block:: css

    .otree-timer {
        display: none;
    }


Changing the timer's behavior
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The timer's functionality is provided by
`jQuery Countdown <http://hilios.github.io/jQuery.countdown/documentation.html>`__.
You can change its behavior by attaching and removing event handlers
with jQuery's ``.on()`` and ``off()``.

oTree sets handlers for the events ``update.countdown`` and ``finish.countdown``,
so if you want to modify those, you can detach them with ``off()``,
and/or add your own handler with ``on()``.
The countdown element is ``.otree-timer__time-left``.

For example, to hide the timer until there is only 10 seconds left,

.. code-block:: html+django

    <style>
        .otree-timer {
            display: none;
        }
    </style>

    <script>
        $(function () {
            $('.otree-timer__time-left').on('update.countdown', function (event) {
                if (event.offset.totalSeconds === 10) {
                    $('.otree-timer').show();
                }
            });
        });
    </script>

(To apply this to all pages, see the instructions in :ref:`base-template`.)

Note: even if you turn off the ``finish.countdown`` event handler from submitting
the page, if you are running the timeoutworker, the page will be submitted on the server
side. So, instead you should use the technique described in :ref:`soft-timeout`.

.. _soft-timeout:

Timeout that doesn't submit the page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you just want a soft timeout, you don't need to use the built-in
timer at all. Instead, make your own with JavaScript, for example:

.. code-block:: javascript

    setTimeout(
        function () {
            alert("Time has run out. Please make your decision.");
        },
        60*1000 // 60 seconds
    );

Minimum time on page
~~~~~~~~~~~~~~~~~~~~

If you want to require the user to spend *at least* a certain amount of time
on a page, you can use some simple JavaScript: hide the next button
(use the ``.otree-btn-next`` selector),
then use ``setTimeout`` to re-display it after a certain amount of time.

In addition, you can also use ref:`error_message <error_message>`.
Assuming you previously set a field like ``expiry_time`` on the player,
then use this:

.. code-block:: python

    def error_message(self, values):
        import time
        if time.time() < self.player.expiry_time:
            return 'You submitted the page early'
