.. _trials-display:

Trials: Displaying content
==========================

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

-   You can use ``ot-attr-`` with the following attributes: ``value``, ``min``, ``max``, ``width``, ``height``, ``src``.
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

onUpdate
~~~~~~~~

This handler gets called whenever the specified variable is changed somewhere.

It's typically used to do some calculations, store the result of the calculation in a different
variable, and then updating the UI with that variable.

For example, let's say you want to change an element from green to red, depending on whether
the user's answer was correct (boolean):

.. code-block:: javascript

    ot.onUpdate('is_correct', function(value) {
        vars.feedback_style = (value ? "text-success" : "text-danger");
    });

Then in the HTML you can have ``<div ot-class="vars.feedback_style">...</div>``.

Note::

    ``onUpdate`` only gets run *after* your event handlers finish running.
    For example if you have code like this:

    .. code-block:: javascript

        ot.onUpdate('a', function(value) {
            vars.aNeg = -value;
        });

    If you have code like the below, you will see it doesn't get updated right away.

    .. code-block:: javascript

        vars.a = 1
        console.log(vars.aNeg); // Will NOT be updated to -1 yet.


onDelete
~~~~~~~~

``onDelete`` gets called if a variable is deleted or set to ``null`` / ``NaN``.
For example, if you do ``delete vars.feedback``, then this handler would be called:

.. code-block:: javascript

    ot.onDelete('feedback', function() {
        delete vars.feedback_style;
    });
