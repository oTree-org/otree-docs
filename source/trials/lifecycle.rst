.. _trials-lifecycle:

Trials: iteration cycle
=======================

You can change/disable the above behavior.


Starting the next trial
-----------------------

oTree automatically proceeds to the next trial when the page is first loaded,
and then after a trial is completed.

If you want to disable this behavior, set ``ot.auto.iterateNext = false``.

For example, you may want the player to press a button before proceeding to the next trial.

.. code-block:: html

    <button type="button" name="next" value="next" ot-key="Space" ot-if="showNextButton == true">
        click here or press the spacebar to start the next trial
    </button>

    <script>

        ot.auto.iterateNext = false;
        ot.showNextButton = true;

        ot.onInput('next', function () {
            ot.iterateNext();
            ot.showNextButton = false;
        });

        ot.onComplete(function () {
            ot.showNextButton = true;
        });
    </script>

Resetting inputs
----------------

oTree automatically resets inputs to blank after each trial.


Unfreezing inputs
-----------------

oTree automatically resets inputs to blank after each trial.


Freezing inputs
---------------



You can customize what happens at each step by defining handler functions.
Here are the handlers corresponding to each above step,
along with some example tasks you might do.


1.  `onPageLoaded`:
    -   Initialize page-wide variables (such as progress bar)
    -   Pre-load image stimuli so that there is no loading delay during the trial
    -   Prevent the trials from being shown right away (e.g. show a "press the spacebar to begin")
2.  `onIteration`:
    -   Pause the loop (e.g. to show an intro screen or section transition screen)
    -   Break out of the loop early and complete the page.
3.  `onTrial`:
    -   Start a timer
4.  `onInput`:
    -   Check validity of player's response
    -   Submit player's response to the server
5.  `onComplete`:
    -   Show feedback for a dynamic amount of time (or don't show feedback at all)
    -   Suspend iteration to the next page.
    -   Update/tally page-wide variables (such as progress bar).
        (This can also be done in ``onInput`` after calling ``ot.sendTrialResponse()``.)

..

    onIteration
    ~~~~~~~~~~~

    This is an optional handler lets you customize what happens prior to each trial.
    It gets triggered when ``ot.nextIteration()`` is called
    (which usually happens from ``ot.onTrialCompleted()``).

    By default, on each iteration oTree simply cleans up data from the previous trial,
    and starts the next trial (if there is one), like this:

    .. code-block:: javascript

        ot.onIteration(function () {
            delete vars.trial;
            delete vars.feedback;

            let trial = ot.getPlayableTrial();
            if (trial) {
                vars.trial = trial;
                ot.startTrial();
            } else {
                ot.completePage();
            }
        });



Practice phases & multiple blocks
---------------------------------

If your task has multiple blocks/phases with a break in between trials,
such as a practice block followed by an experimental block
(with some feedback being shown after the practice block),
you should split them between multiple pages.

In the below example, the practice block is almost identical to the real block,
so we set its ``template_name`` to use the same template,
and set the ``trial_*`` attributes the same.
You can use ``vars_for_template`` so that the template code
can show slightly different content in practice mode.

When you use ``Trial.create()``, you should set the built-in attribute ``page_name``
to tell oTree on which page to display that trial.

.. code-block:: python


    def creating_session(subsession: Subsession):
        for p in subsession.get_players():

            # 5 practice trials
            for i in range(5):
                Trial.create(
                    player=p,
                    # this is how you tell oTree to display this trial on the practice page
                    # only.
                    page_name='PracticeBlock',
                    # ...
                )

            # 20 real trials
            for i in range(20):
                Trial.create(
                    player=p,
                    page_name='RealBlock',
                    # ...
                )


    class PracticeBlock(Page):
        template_name = '{}/RealBlock.html'.format(__name__)
        trial_model = Trial
        trial_stimulus_fields = C.TRIAL_STIMULUS_FIELDS
        trial_response_fields = C.TRIAL_RESPONSE_FIELDS

        @staticmethod
        def vars_for_template(player: Player):
            return dict(is_practice=True)


    class PracticeFeedback(Page):
        #
        @staticmethod
        def vars_for_template(player: Player):
            return dict(
                # display some statistics on the practice block.
            )


    class RealBlock(Page):
        trial_model = Trial
        trial_stimulus_fields = C.TRIAL_STIMULUS_FIELDS
        trial_response_fields = C.TRIAL_RESPONSE_FIELDS

        @staticmethod
        def vars_for_template(player: Player):
            return dict(is_practice=False)


If you have many blocks,
consider setting ``C.NUM_ROUNDS`` to the number of blocks,
so that you can have 1 trial page that loops repeatedly.

Feedback & inter-trial interval
-------------------------------

To set the inter-trial interval, set ``ot.auto.interTrialInterval = 500;`` (for e.g. 500 msec).

If you set ``ot.auto.iterateNext = false``, then you must manually write the code to trigger the next trial:

.. code-block:: javascript

      ot.onComplete(function () {
        ot.delay(500, function () {
          ot.startIteration();
        });
      });
