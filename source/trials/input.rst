Input
=====

To capture user input, set ``ot-input=`` on your inputs (buttons, text inputs, etc.).

For some input types, such as buttons and radios, you use the syntax ``ot-input="my_var = xyz".
For example, clicking on one of the below inputs will set ``vars.my_var = 'A'``:

.. code-block:: html

    <!-- button -->
    <button type="button" ot-input="my_var = 'A'">A</button>

    <!-- radio button -->
    <input type="radio" ot-input="my_var = 'A'">

For some other input types, such as text inputs and checkboxes,
you must use the syntax ``ot-input="var"``.
When there is input, the value of the input will be saved into to the specified variable.

For example, any text that is entered into this input will be saved into ``vars.my_var``:

.. code-block:: html

    <input type="text" ot-input="my_var">

You can respond to changes to an input by defining ``onInput``.

onInput and sendTrialResponse
-----------------------------

In combination with ``ot-input``, you should use ``onInput``
to trigger some action when a user's input is submitted.
Most often, this will be to submit the user's response to the server.
This is also where you can check if the user's response was correct (and set feedback),
calculate their response time, etc.

For example:

.. code-block:: html

    <input type="text" name="response">

.. code-block:: javascript

    /* the first arg to onInput is the name of the input */
    ot.onInput('response', function (value) {
        ot.sendTrialResponse({response: value});
    });




sendTrialResponse()
~~~~~~~~~~~~~~~~~~~

Call this to send your data to the server.

-   It also triggers ``reportValidity()``.
-   freezes all inputs
-   Causes ``numCompleted`` to be incremented
-   and causes ``onComplete`` to be run.


List of input types
-------------------

Below are some more details on the different input types.

Text/number input
~~~~~~~~~~~~~~~~~

Any text that is typed into this input will be saved into ``vars.my_var``:

.. code-block:: html

    <input type="text" ot-input="my_var">

The player must press ``Enter`` on the text field for onInput to run.
If you want it updated on every keypress, add ``autocommit``:

.. code-block:: html

    <input type="text" ot-input="my_var" autocommit>

You can also use the `autofocus` attribute to immediately place the cursor on this field.

Button
~~~~~~

Remember to add ``type="button"`` to your button inputs:

.. code-block:: html

    <button type="button" ot-input="choice = 'A'">A</button>

You can also trigger the button on pressing Enter, by adding ``ot-key="Enter"``.

Radio buttons
~~~~~~~~~~~~~

Example:

.. code-block:: html

    <label><input type="radio" ot-input="choice = 'A'">A</label>
    <label><input type="radio" ot-input="choice = 'B'">B</label>

Checkbox
~~~~~~~~

When a checkbox is checked, the variable is set to ``true``. When unchecked, it's set to ``false``.

.. code-block:: html

    <label><input type="checkbox" ot-input="my_bool">My label</label>

Keyboard input
~~~~~~~~~~~~~~

Many experiments require the user to rapidly react by pressing a key on their keyboard, e.g.
``f``/``j`` to indicate left/right.

This can be implemented with ``ot-key``:

.. code-block:: html

    <p>
        Press
        <button type="button" ot-key="f" ot-input="direction = 'left'">F</button> to choose the left image
        <button type="button" ot-key="j" ot-input="direction = 'right'">J</button> to choose the right image.
    </p>

``ot-key`` can be attached to any element, not just ``button``.

The ``ot-key`` value can be either a character or a standard name from the
`keyboard code values <https://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_code_values>`__.

.. note::

    Keyboard layouts vary depending on a user's language.
    For example, ``z`` and ``y`` are swapped between English and German layouts.
    On the other hand, using keynames like `KeyZ` or `KeyY` refers to the same positions.

Clickable images / text / etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can make any element clickable by placing it inside a ``<button>``.

For example, if you want the user to choose an image by clicking on it,
you can use this code:




Disabling inputs
~~~~~~~~~~~~~~~~

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


Input validation
~~~~~~~~~~~~~~~~

You can set validation attributes on your ``<input>`` elements like
``required``, ``min``, ``max``, ``pattern``,
``step``, ``minlength``, ``maxlength``, etc. For example:

.. code-block:: javascript

    <input type="number" name="xyz" min="0" max="10" required>

Then trigger validation by calling ``ot.form.reportValidity()``.

For example, let's say you want to trigger validation when the user clicks a submit button.
The ``return`` statement ensures that if the form is not valid, then you don't submit the trial.

.. code-block:: javascript

    ot.onInput('submit', function (value) {

        let isValid = ot.form.reportValidity();
        if (!isValid) return;

        ot.sendTrialResponse(whatever);
    });

Another reason to run validation is to ensure fields contain valid values before you use them in calculations.
In the below example, you can ensure that fields ``a`` and ``b``
both contain numbers and that ``b`` is not zero:

.. code-block:: javascript

    let isValid = ot.form.reportValidity();
    if (!isValid) return;

    vars.c = vars.a / vars.b;
    ...


If the form is invalid, ``reportValidity()`` will display a
message next to the input such as "this field is required".
If you don't want to show the user these messages, replace ``reportValidity()`` with ``checkValidity()``.

If you just want to validate an individual field,
use ``forminputs.yourfield.reportValidity()``

(You can read about these standard validation functions here.)

Styling
------

Consult the Bootstrap documentation's
`https://getbootstrap.com/docs/5.0/forms/overview/ <forms section>`__
for information on how to write the raw HTML to style your form inputs.
