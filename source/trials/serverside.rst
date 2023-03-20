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


How to enable
~~~~~~~~~~~~~

On your page, instead of defining ``trial_response_fields``, define a function ``evaluate_trial()``,
as in the following examples.

Use case: preventing cheating
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you have a task where users need to count how many triangles are in each image.
After each response you tell the user whether they gave the correct answer.

..
    You have a ``Trial`` model like this:
    code-block:: python

    class Trial(ExtraModel):
        # mandatory fields
        player = models.Link(Player)
        queue_position = models.IntegerField()

        # user-defined fields
        image = models.StringField()
        question = models.StringField()
        response = models.IntegerField()
        solution = models.IntegerField()


With a typical client-side implementation, each trial is stored in the browser,
where the solutions can be viewed by tech-savvy users in source code like this:

.. code-block:: javascript

    {
        'image': 'img1.jpg',
        'question': "How many triangles are there in this image?",
        'solution': 15
    }

With server-side evaluation, the solution is not exposed:

.. code-block:: javascript

    {
        'image': 'img1.jpg',
        'question': "How many triangles are there in this image?",
    }

Instead, the user's response is sent to the Python server, where ``evaluate_trial`` is run:

.. code-block:: python

    def evaluate_trial(trial: Trial, response):
        trial.answer = response['answer']
        is_correct = (trial.answer == trial.solution)
        trial.queue_position = None
        return dict(is_correct=is_correct)

The arguments to ``evaluate_trial`` are the trial (your ExtraModel instance)
and the ``response`` dict that you sent from ``sendTrialResponse()``.
The return value is the feedback you want to send back to the page.
To proceed to the next trial, you need to take the current trial out of the queue by setting
``queue_position = None``.

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

You can put any code you want in ``evaluate_trial``, such as recording each wrong answer
(maybe stored in an additional ``ExtraModel``).

Note also that the ``player`` instance can be accessed with ``trial.player``.