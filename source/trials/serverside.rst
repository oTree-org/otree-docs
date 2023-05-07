.. _trials-sse:

Server-side evaluation of trials
================================

Server-side evaluation is an optional Trials feature.

With server-side evaluation, each response is sent to the server for evaluation,
before deciding what to do next.

Advantages:

-   Better safeguarding of sensitive data (such as the correct answers to test questions)
-   You can make tasks where trials don't proceed linearly,
    but rather get dynamically skipped, reordered, or repeated (e.g. retries until you get the correct answer).
-   You can generate new trials on the fly, allowing you to implement infinitely repeating tasks.

Disadvantages:

-   The roundtrips to the server add a small delay between trials
-   The code is a bit more complex.

Synopsis
--------

How to enable
~~~~~~~~~~~~~

On your page, instead of defining ``trial_response_fields``, define a function ``evaluate_trial()``,
as in the following examples.

Use case: preventing cheating
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you have a task where users need to solve some puzzles.
After each response you tell the user whether they gave the correct answer.

..
    You have a ``Trial`` model like this:
    code-block:: python

    class Trial(BaseTrial):
        image = models.StringField()
        question = models.StringField()
        response = models.IntegerField()
        solution = models.IntegerField()

With a typical client-side implementation, you need to store each trial's solution in the browser,
where the solutions may be found by tech-savvy users.

With server-side evaluation, the solution is not exposed.

Instead, the user's response is sent to the Python server, where ``evaluate_trial`` is run:

.. code-block:: python

    def evaluate_trial(trial: Trial, response):
        trial.answer = response['answer']
        is_correct = (trial.answer == trial.solution)
        trial.queue_position = None
        return dict(is_correct=is_correct)

The arguments to ``evaluate_trial`` are the trial (your Trial instance)
and the ``response`` dict that you sent from ``sendTrialResponse()``.
The return value is the feedback you want to send back to the page.
To proceed to the next trial, you need to take the current trial out of the queue by setting
``queue_position = None``. (If you forget to do this, it will keep showing the current trial
again and again.)

Use case: retries
~~~~~~~~~~~~~~~~~

Let's say you want the player to have 3 chances to answer each question correctly.
This can be done as follows:

.. code-block:: python

    def evaluate_trial(trial: Trial, response):
        trial.answer = response['answer']
        is_correct = (trial.answer == trial.solution)
        trial.attempts += 1
        if is_correct or trial.attempts >= 3:
            trial.is_correct = is_correct
            trial.queue_position = None
        return dict(is_correct=is_correct)

Notes
~~~~~

You can put any code you want in ``evaluate_trial``, such as recording each wrong attempt
(maybe stored in an ``ExtraModel``).

Note also that the ``player`` instance can be accessed with ``trial.player``.

Tracking progress
-----------------

You can define the function ``trial_page_vars`` to keep track of the user's progress.
With each trial, this function will be run and its values will be stored into the JavaScript ``vars``
variable.

For example:

.. code-block:: python

    @staticmethod
    def trial_page_vars(player):
        return dict(
            num_correct=player.num_correct,
            num_incorrect=player.num_incorrect,
        )

Then in your JavaScript code you can do ``vars.num_correct``.

The alternative is to keep track of it in JavaScript code, e.g. setting ``vars.num_correct += 1``
in your ``onComplete`` handler, but if the page is refreshed, all of ``vars`` gets reset to its initial state.
So keeping track of it on the server side is more reliable.

Reference
---------

queue_position
~~~~~~~~~~~~~~

When you create a ``Trial``, oTree will automatically assign a consecutive ``queue_position``.
oTree iterates through trials from lowest to highest ``queue_position``.
You can also explicitly set a queue position, either when creating the trial
(e.g. ``Trial.create(queue_position=i, ...)``),
or you can move an existing trial in the queue by setting ``trial.queue_position = i``.
To move an item to the front of the queue, you can assign ``queue_position = 0``
(oTree's automatic numbering starts at 1).
