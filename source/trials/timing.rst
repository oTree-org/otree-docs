.. _trials-timing:

Trials & timing
===============

Here are the different functionalities related to time measurement and timed execution.

Time measurement
----------------

To measure a user's reaction time, use startTimeMeasurement and stopTimeMeasurement.
Usually, you start the clock when the trial starts,
so you put ``startTimeMeasurement()`` in ``onTrial`` (or ``onPhase``):

.. code-block:: javascript

    ot.onTrial(function(trial) {
        ot.startTimeMeasurement();
    });

And ``stopTimeMeasurement`` usually goes in an ``onInput`` handler:

.. code-block:: javascript

    ot.onInput('response', function (value) {
        let reaction_ms = ot.stopTimeMeasurement();
        ot.sendTrialResponse({'response': response, 'reaction_ms': reaction_ms})
    });


The time-precision of these functions is currently ± few milliseconds.

Also, it is possible to measure several intervals in parallel, for instance total page time and each individual trials.
Use `ot.startTimeMeasurement("something")` and `ot.stopTimeMeasurement("something")`

Phases
------

Phases allow you to schedule a rapid sequence of events.

Let's say each trial involves showing a fixation cross for 1000ms,
then showing a stimulus for 500ms, and giving the user 2000ms to make a response.
You can program it like this:

.. code-block:: javascript

    ot.startPhases({
        'fixation': 1000,
        'stimulus': 500,
        'response': 2000,
    });

Usually this code will go inside your ``onTrial`` handler.

The variable ``vars.phase`` will automatically be set to the name of the current phase,
so you can display different content, e.g. using ``ot-if="phase == 'fixation'``.

You can also define ``onPhase`` handlers, which fire when a phase starts,
and ``onPhaseEnd`` handlers, which fire when a phase ends:

.. code-block:: javascript

    ot.onPhase('response', function() {
        ot.resetInputs();
    })

    ot.onPhaseEnd('response', function () {
        // default code that gets executed if the user doesn't react
        ot.sendTrialResponse({'pressed': false});
    });

If the last phase has no timeout, you can set it to ``null``:

.. code-block:: javascript

    ot.startPhases({
        'fixation': 1000,
        'stimulus': 500,
        'response': null,
    });

As soon as ``sendTrialResponse`` is called, phases abort execution.
To allow phases to continue, set ``ot.auto.cancelPhasesOnSendTrialResponse = false``.

Periodic timer
--------------

A timer generates an event every N milliseconds.
For example, let's say you want to animate a loading progress bar
whose value increases every 200ms.
First define a variable whose value increases every 200ms:

.. code-block:: javascript

    ot.onTrial(function() {
        vars.x = 0;
        ot.startTimer(200, 'increment_progress');
    }

    ot.onTimer('increment_progress', function(elapsed) {
        vars.x += 1;
    });

Then define an HTML element that uses this variable:

.. code-block:: html

    <progress ot-value="x" max="100">

Timers can be canceled:

.. code-block:: javascript

    /* cancel all the timers */
    ot.cancelTimers();

    /* cancel specified timer */
    ot.cancelTimer('increment_progress');


Delays & Timeouts
-----------------

The simplest way to delay some event is to use ``ot.delay``.
The argument is a function to execute after the specified time.
For example:

.. code-block:: javascript

    ot.delay(500, function () {
      vars.xyz = true;
    });

