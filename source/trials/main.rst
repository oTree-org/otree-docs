Trials
======

.. note::

    This feature is new in oTree 6.

The Trials feature is designed for experiments with repeated stimulus/response, such as::

-   Psychology experiments (Stroop, priming, etc)
-   Data entry

You show the user a sequence of stimuli (text, images, etc.),
and for each stimulus to prompt some response from the user (e.g. click a button, select an image, type some text).
The task may be timing sensitive, e.g. measuring the user's reaction time, or showing stimuli at specific timing intervals.

This is done with HTML and JavaScript code.
In the templates, you will see the prefix ``ot``, which stands for "oTree Trials".

This is different from oTree's regular template syntax, which uses ``{{ }}``, for example:

.. list-table::
   :header-rows: 1

   * - oTree template syntax
     - oTree Trials syntax
   * - ``{{ if is_correct }}<p>correct!</p>{{ endif }}```
     - ``<p ot-if="vars.is_correct == true">correct!</p>``
   * - ``<p>{{ question }}</p>``
     - ``<p ot-text="vars.question"></p>``

The difference is that oTree template syntax is rendered only once, when the page is loaded.
The variables inside the ``{{ ... }}`` come from your Python code.
Whereas oTree Trials syntax is updated live, and the variables in the ``ot-xyz="..."`` come from your JavaScript
code.

About JavaScript
----------------

oTree trials require you to write some JavaScript code in your templates.
JavaScript code is placed inside a ``<script>`` tag.

While developing, you should keep your browser's JavaScript console open.
In most browsers (Chrome / Edge / Firefox) you can open the developer console by pressing
``F12`` or ``Fn+F12``.
This is where most errors will be reported, and where you can see the output of your ``console.log()`` statements
(which are the equivalent of ``print()`` statements in Python).

Basic example
-------------

Let's say you want to show the user a sequence of 20 random numbers, then for each number ask them whether
the number is even or odd.

In your Python code, define a Trial:

.. code-block::python

    class Trial(BaseTrial):
        number = models.IntegerField()
        answered_even = models.BooleanField()


In ``creating_session``, create instances of this model:

.. code-block::python


    def creating_session(subsession):
        import random
        for p in subsession.get_players():
            for i in range(20):
                Trial.create(player=p, number=random.randint(0, 100))

Then define a page with these 3 attributes:

.. code-block::python

    class Main(Page):
        trial_model = Trial
        trial_stimulus_fields = ['number']
        trial_response_fields = ['answered_even']

oTree will now automatically define a ``trial`` variable,
which is stored in the ``vars`` global JavaScript variable,
which you can access from your ``ot-`` attributes
and your JavaScript code. It refers to the current trial being presented to the user, and it contains whatever
attributes are included in ``trial_stimulus_fields``.

In your template, put this code, which says to display the 'number' field of each trial,
with 2 buttons to let the user select if it's even or odd:

.. code-block:: html

    <div ot-text="vars.trial.number"></div>

    <button ot-input="vars.answered_even = true">Even</button>
    <button ot-input="vars.answered_even = false">Odd</button>

Also in your template, put this JavaScript:

.. code-block:: javascript

        ot.onInput('answered_even', function(value) {
           ot.sendTrialResponse({answered_even: value});
        });

This means that whenever the ``answered_even`` input is made, we save the trial response into the database,
in the corresponding field defined in ``trial_response_fields``. oTree automatically handles proceeding to the next
trial.

vars
----

``vars`` contains any custom variables you define in your JavaScript code,
as well as the following built-in attributes:

-   `vars.trial`: the current trial object.
-   ``vars.numTrials``: the total number of trials
-   ``vars.numTrialsCompleted``: the number of trials completed so far
-   ``vars.numTrialsRemaining``: the number of trials remaining

You can also define additional members of ``vars``.

Display
-------

There are various ``ot-*`` directives to make your content dynamic.
For example, ``ot-if``, ``ot-text``, ``ot-class``, etc.

See :ref:`trials-display`.

Lifecycle
---------

Here is a summary of how oTree automatically cycles through trials:

1.  Page is loaded.
2.  First trial is displayed.
3.  Player submits their response.
    Once your code calls ``sendTrialResponse()``
    and the data is sent to the server.
4.  Feedback is displayed to the participant
5.  The next trial is displayed, repeating steps 2-4.
6.  Once all trials have been completed, the page is automatically submitted.

To customize/override this behavior, see :ref:`trials-lifecycle`.



Server-side evaluation
----------------------

Server-side evaluation is an optional Trials feature.

With server-side evaluation, each response is sent to the server for evaluation,
before deciding what to do next.

Feedback
--------

After each trial, you may want to display feedback to users.
Feedback can be calculated in your ``onInput`` handler.

    ot.onInput('is_even', function (value) {
        ot.sendTrialResponse({is_even: value});
        
    });


            vars.feedback = isCorrect;


You can control the duration of feedback by setting ``ot.auto.interTrialInterval`` to the number of milliseconds.




To set the inter-trial interval, set ``ot.auto.interTrialInterval = 500;`` (for e.g. 500 msec).


If you use ref:`server-side evaluation <trials-sse>`,
