Trials
======

.. note::

    This feature is new in oTree 6.

The Trials feature is designed for experiments with repeated stimulus/response, such as::

-   Psychology experiments (Stroop, priming, etc)
-   Data entry

The general pattern is to show a sequence of stimuli (text, images, etc.),
and for each stimulus to prompt some response from the user (e.g. click a button, select an image, type some text).
The task may be timing sensitive, e.g. measuring the user's reaction time, or showing stimuli at specific timing intervals.

This is done with HTML and JavaScript code.
In the templates, you will see the prefix ``ot``, which stands for "oTree Trials".

This is different from oTree's regular template syntax, which uses ``{{ }}``, for example:

.. list-table::
   :header-rows: 1

   * - Regular oTree syntax
     - oTree Trials syntax
   * - ``{{ if is_correct }}<p>correct!</p>{{ endif }}```
     - ``<p ot-if="is_correct == true">correct!</p>``
   * - ``<p>{{ question }}</p>``
     - ``<p ot-text="question"></p>``

The difference is that oTree template syntax () is rendered only once, when the page is loaded.
The variables inside the ``{{ ... }}`` are from your Python code.
Whereas oTree Trials syntax is updated live, and the variables in the ``ot-xyz="..."`` come from your JavaScript
code.


Basic example
-------------

Let's say you want to show the user a sequence of 20 random numbers, then for each number ask them whether
the number is even or odd.

In your Python code, define an ExtraModel:

.. code-block::python

    class Trial(ExtraModel):
        # mandatory fields
        player = models.Link(Player)
        queue_position = models.IntegerField()

        # user-defined fields
        number = models.IntegerField()
        response_is_even = models.BooleanField()
        rt = models.FloatField()



In ``creating_session``, create instances of this model:

.. code-block::python


    def creating_session(subsession):
        import random
        for p in subsession.get_players():
            for i in range(20):
                Trial.create(player=p, queue_position=i, number=random.randint(0, 100))

Then define a page with these 3 attributes:

.. code-block::python

    class Main(Page):
        trial_model = Trial
        trial_stimulus_fields = ['number']
        trial_response_fields = ['response_is_even']

oTree will now automatically define a ``trial`` variable that you can access from your ``ot-`` attributes
and your JavaScript code. It refers to the current trial being presented to the user, and it contains whatever
attributes are included in ``trial_stimulus_fields``.

In your template, put this code, which says to display the 'number' field of each trial,
with 2 buttons to let the user select if it's even or odd:

.. code-block:: html

    <div ot-text="trial.number"></div>

    <button ot-input="response_is_even = true">Even</button>
    <button ot-input="response_is_even = false">Odd</button>

Also in your template, put this JavaScript:

.. code-block:: javascript

        ot.onInput('response_is_even', function(value) {
           ot.sendTrialResponse({response_is_even: value});
        });

This means that whenever the ``response_is_even`` input is made, we save the trial response into the database,
in the corresponding field defined in ``trial_response_fields``. oTree automatically handles proceeding to the next
trial.

Variables
---------

The following objects can be accessed from your ``ot-`` attributes
and your JavaScript code.

- `progress`: contains attributes ``current`` (the number of the current trial) and ``total`` (the total number of trials).
- `trial`: contains the attributes you set in ``trial_stimulus_fields``.
- `feedback`: see :ref:`server-feedback`.


Display
-------

ot-if
~~~~~

-   Purpose: conditionally display some HTML
-   Example code:

.. code-block:: html

    <!-- element is displayed only if my_bool is true -->
    <p ot-if="my_bool == true">correct!</p>

-   Example output:

.. code-block:: html

    <p>correct!</p>

ot-text
~~~~~~~

-   Purpose: set the inner text of an element
-   Example code:

.. code-block:: html

    <p ot-text="my_str"></p>

.. code-block:: html

    <p>hello world</p>

ot-html
~~~~~~~

-   Purpose: set the inner HTML of an element (like ``ot-text``, but supports values with HTML tags)
-   Example code:

.. code-block:: html

    <p ot-html="my_html_str"></p>

.. code-block:: html

    <p><i>Hamlet</i> by William Shakespeare</p>

ot-attr-*
~~~~~~~~~

-   Purpose: set an attribute on an HTML element. ``ot-attr-xyz=`` defines attribute ``xyz=``.
-   Example code:

.. code-block:: html

    <progress ot-attr-value="my_int" ot-attr-max="my_int2"></progress>

.. code-block:: html

    <progress value="9" max="10"></progress>

-   You can use ``ot-attr-`` with the following attributes: ``value``, ``min``, ``max``, ``width``, ``height``.
    For ``class``, use ``ot-class`` instead.

ot-class
~~~~~~~~

-   Purpose: Dynamically add/remove a class to an element.
    This lets you dynamically change the style/color/appearance of an element,
    (as long as you define CSS styles for your classes).

-   Example code:

.. code-block:: html

    <div ot-class="my_class"></div>

-   Example output:

.. code-block:: html

    <div class="success"></div>

``ot-class`` can be combined with a hardcoded ``class=`` attribute.

-   Example code:

.. code-block:: html

    <div class="alert" ot-class="my_class"></div>

-   Example output:

.. code-block:: html

    <div class="alert alert-success"></div>

ot-enabled
~~~~~~~~~~

-   Purpose: Enable/disable
    `<button>` or `<input>` (or anything with `ot-input`/`ot-event`).

-   Example code:

.. code-block:: html

    <!-- if my_bool is false, this button will be disabled -->
    <button type="button" ot-enabled="my_bool == true">confirm</button>

-   Example output:

.. code-block:: html

    <button type="button" disabled>confirm</button>

Inputs
------

To capture user input, set ``ot-input=`` on your inputs (buttons, text inputs, etc.).

For some input types, such as buttons and radios, you use the syntax ``ot-input="my_var = xyz".
For example, clicking on one of the below inputs will set ``ot.page.my_var = 'A'``:

.. code-block:: html

    <!-- button -->
    <button type="button" ot-input="my_var = 'A'">A</button>

    <!-- radio button -->
    <input type="radio" ot-input="my_var = 'A'">

For some other input types, such as text inputs and checkboxes,
you must use the syntax ``ot-input="var"``.
When there is input, the value of the input will be saved into to the specified variable.

For example, any text that is entered into this input will be saved into ``ot.page.my_var``:

.. code-block:: html

    <input type="text" ot-input="my_var">

You can respond to changes to an input by defining ``otInput``.

Below are some more details on the different input types.

Text/number input
~~~~~~~~~~~~~~~~~

Any text that is typed into this input will be saved into ``ot.page.my_var``:

.. code-block:: html

    <input type="text" ot-input="my_var">


The player must press ``Enter`` on the text field for the handler to run.
If you want it updated on every keypress, add ``autocommit``:

.. code-block:: html

    <input type="text" ot-input="my_var" autocommit>

You can also use the `autofocus` attribute to immediately place the cursor on this field.

Button
~~~~~~

Remember to add ``type="button"`` to your button inputs:

.. code-block:: html

    <button type="button" ot-input="choice = 'A'">A</button>

Radio buttons
~~~~~~~~~~~~~

Example:

```html
<label><input type="radio" ot-input="choice = 'A'">A</label>
<label><input type="radio" ot-input="choice = 'B'">B</label>
```

Checkbox
~~~~~~~~

When a checkbox is checked, the variable is set to ``true``. When unchecked, it's set to ``false``.

.. code-block:: html

    <label><input type="checkbox" ot-input="my_bool">My label</label>

Clickable images, divs, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can make basically any HTML element clickable by adding `ot-click` and `ot-input="var = val"`.
For example, a clickable image:

.. code-block:: html

    <div ot-click ot-input="favorite_animal = 'cat'"><img src="cat.jpg"></div>

Keyboard input
~~~~~~~~~~~~~~

Many experiments require the user to rapidly react by pressing a key on their keyboard, e.g.
``F``/``J`` to indicate left/right.

This can be implemented with ``ot-key``:

.. code-block:: html

    <p>
        Press
        <kbd ot-key="f" ot-input="direction = 'left'">F</kbd> to choose the left image
        <kbd ot-key="j" ot-input="direction = 'right'">J</kbd> to choose the right image.
    </p>

``ot-key`` can be attached to any element, not just ``kbd``.


The ``ot-key`` value can be either a character or a standard name from the
`keyboard code values <https://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_code_values>`__.

.. note::

    Keyboard layouts vary depending on a user's language.
    For example, ``Z`` and ``Y`` are swapped between English and German layouts.
    On the other hand, using keynames like `KeyZ` or `KeyY` refers to the same positions.


Handlers
--------

onInput
~~~~~~~

In combination with ``ot-input``, you should use ``onInput``
to trigger some action when a user makes an input.
Most often, this will be to submit the user's response to the server.
This is also where you can check if the user's response was correct (and set feedback),
calculate their response time, etc.

.. code-block:: javascript

    ot.onInput('response', function (value) {

        let data = {
            response: value,
            response_time: ot.endMeasurement(),
        }
        let is_correct = (value === 42);
        ot.page.feedback = {is_correct: is_correct};

        ot.sendTrialResponse(data);
    });



onUpdate
~~~~~~~~

This handler gets called whenever the specified variable is changed somewhere.

It's a way to make one variable depend on another.
For example, let's say you want to change an element from green to red, depending on whether
the user's answer was correct:

.. code-block:: javascript

    ot.onUpdate('feedback', function(feedback) {
        ot.page.feedback_style = (feedback.correct ? "text-success" : "text-danger");
    });

Then in the HTML you can have ``<div ot-class="feedback_style">...</div>``.

onDelete
~~~~~~~~

``onDelete`` gets called if a variable is deleted or set to ``null`` / ``NaN``.
For example, if you do ``delete ot.page.feedback``, then this handler would be called:

.. code-block:: javascript

    ot.onDelete('feedback', function() {
        delete ot.page.feedback_style;
    });


onIteration
~~~~~~~~~~~

This is an optional handler lets you customize what happens prior to each trial.

By default, on each iteration oTree simply cleans up data from the previous trial,
and starts the next trial (if there is one), like this:

.. code-block:: javascript

    ot.onIteration(function () {
        delete ot.page.trial;
        delete ot.page.response;
        delete ot.page.feedback;

        let nextTrial = ot.getNextTrial();
        if (nextTrial) {
            ot.startTrial(nextTrial);
        } else {
            ot.completePage();
        }
    });

However, you might sometimes want to show some other content rather than proceeding to the next trial
right away. For example, maybe after 10 trials you want to tell the user that they are
starting a new section, or give them feedback on their performance so far.
In this case, you can have code like this:

.. code-block:: javascript

    ot.onIteration(function () {
        delete ot.page.trial;
        delete ot.page.response;
        delete ot.page.feedback;

        let nextTrial = ot.getNextTrial();
        if (nextTrial) {
            if (ot.page.progress.current == 10) {
                ot.page.nextTrial = nextTrial;
                ot.page.intermission = true;
            } else {
                ot.startTrial(nextTrial);
            }
        } else {
            ot.completePage();
        }
    });

Then in your HTML you can some content that is only displayed during the intermission stage:

.. code-block:: html

    <div ot-if="intermission == true">
        You are finished with the first section.
        Now we will start a new section [...]
        <button type="button" ot-input="nextsection = true">Continue</button>
    </div>

.. code-block:: javascript

        ot.onInput('nextsection', function (value) {
            delete ot.page.intermission;
            ot.startTrial(ot.page.nextTrial);
        });

onTrial
~~~~~~~

This handler gets called when a new trial starts.
The default behavior is simple:

.. code-block:: javascript

    ot.onTrial(function (trial) {
        ot.page.trial = trial;
        ot.resetInputs();
    });

You can customize this to start a :ref:`timer <trials-timing>`.

Also, [reaction time measurement](measurement.md) shuold start right after the trial is shown.
For time-controlled mechanics, such as response timeout, the handler needs to start some [timers](timers.md).
