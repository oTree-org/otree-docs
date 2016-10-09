.. _forms:

Forms
=====

Each page in oTree can contain a form, which the player should fill out
and submit by clicking the "Next" button. To create a form, first you
should go to models.py and define fields on your Player or Group. Then,
in your Page class, you can define ``form_model`` to specify the model
that this form modifies (either ``models.Player`` or ``models.Group``),
and ``form_fields``, which is a list of the fields from that model.

When the user submits the form, the submitted data is automatically
saved back to the field in your model.


Forms in templates
------------------

You should include form fields by using a ``{% formfield %}`` element.
You generally do not need to write raw HTML for forms (e.g.
``<input type="text" id="...">``).

Form field labels
~~~~~~~~~~~~~~~~~

You can set the label on a form field like this:

.. code-block:: html+django

    ``{% formfield player.contribution with label="How much do you want to contribute?" %}``

Note there is no space around the label's ``=``.

If the label should contain a variable, you can construct the string in ``views.py``:

.. code-block:: python

    class Contribute(Page):
        form_model = models.Player
        form_fields = ['contribution']

        def vars_for_template(self):
            return {
                'contribution_label': 'How much of your {} do you want to contribute?'.format(self.player.endowment)
            }

Then in the template, set the label to this variable:

.. code-block:: html+django

    ``{% formfield player.contribution with label=contribution_label %}``

If you use this technique, you may also want to use :ref:`dynamic_validation`.

.. _form-validation:

User Input Validation
---------------------

The player must submit a valid form before they get routed to the next
page. If the form they submit is invalid (e.g. missing or incorrect
values), it will be re-displayed to them along with the list of errors
they need to correct.

*Example 1:*

.. image:: _static/forms/Sz34h7d.png
    :align: center
    :scale: 100 %


*Example 2:*

.. image:: _static/forms/BtG8ZHX.png
    :align: center
    :scale: 100 %


oTree automatically validates all input submitted by the user. For
example, if you have a form containing a ``PositiveIntegerField``, oTree
will not let the user submit values that are not positive integers, like
``-1``, ``1.5``, or ``hello``.

You can specify additional validation. For example, here is how you would
require an integer to be between 12 and 24:

.. code-block:: python

    # in models.py
    offer = models.PositiveIntegerField(min=12, max=24)

If the max/min are not fixed, you should use :ref:`FOO_max`

.. _choices:

You can constrain the user to a predefined list of choices by using
``choices=``:

.. code-block:: python

    # in models.py
    level = models.PositiveIntegerField(
        choices=[1, 2, 3],
    )

The user will then be presented a dropdown menu instead of free text input.

If the choices are not fixed, you should use :ref:`FOO_choices`

If you would like a specially formatted value displayed to the user that
is different from the values stored internally, ``choices=`` can be a list
consisting itself of tuples of two items.
The first element in each tuple is the value and the second element is the
human-readable label.

For example:

.. code-block:: python

    # in models.py
    level = models.PositiveIntegerField(
        choices=[
            [1, 'Low'],
            [2, 'Medium'],
            [3, 'High'],
        ]
    )

After the field has been set, you can access the human-readable name
using
`get_FOO_display <https://docs.djangoproject.com/en/1.8/ref/models/instances/#django.db.models.Model.get_FOO_display>`__
, like this:
``self.get_level_display() # returns e.g. 'Medium'``.
However, if you define the choices dynamically with :ref:`FOO_choices`,
in order to use ``get_*_display()`` you need to also define the ``*_choices``
method in your models.py.

If a field is optional, you can use ``blank=True`` like this:

.. code-block:: python

    # in models.py
    offer = models.PositiveIntegerField(blank=True)

Then the HTML field will not have the ``required`` attribute.

.. _dynamic_validation:

Dynamic validation
~~~~~~~~~~~~~~~~~~

If you need a form's choices or validation logic to depend on some
dynamic calculation, then you can instead define one of the below
methods in your ``Page`` class in ``views.py``.

.. _FOO_choices:

{field_name}_choices()
''''''''''''''''''''''

Like setting ``choices=`` in models.py, this will set the choices for the form field
(e.g. the dropdown menu or radio buttons).

Example:

.. code-block:: python

    class MyPage(Page):

        form_model = models.Player
        form_fields = ['offer']

        def offer_choices(self):
            return currency_range(0, self.player.endowment, 1)


.. _FOO_max:

{field_name}_max()
''''''''''''''''''

The dynamic alternative to setting ``max=`` in models.py. For example:

.. code-block:: python

    class MyPage(Page):

        form_model = models.Player
        form_fields = ['offer']

        def offer_max(self):
            return self.player.endowment


{field_name}_min()
''''''''''''''''''

The dynamic alternative to setting ``min`` in models.py.

.. _FOO_error_message:

{field_name}_error_message()
''''''''''''''''''''''''''''

This is the most flexible method for validating a field.

For example, let's say your form has an integer field called
``odd_negative``, which must be odd and negative: You would enforce this
as follows:

.. code-block:: python

    class MyPage(Page):

        form_model = models.Player
        form_fields = ['odd_negative']

        def odd_negative_error_message(self, value):
            if not (value < 0 and value % 2):
                return 'Must be odd and negative'

Validating multiple fields together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you have 3 integer fields in your form whose names are
``int1``, ``int2``, and ``int3``, and the values submitted must sum to
100. You can enforce this with the ``error_message`` method:

.. code-block:: python

    class MyPage(Page):

        form_model = models.Player
        form_fields = ['int1', 'int2', 'int3']

        def error_message(self, values):
            if values["int1"] + values["int2"] + values["int3"] != 100:
                return 'The numbers must add up to 100'

Timeouts
--------

To control what happens if there is a timeout on the page,
see :ref:`timeout_submission` and :ref:`timeout_happened`.

Determining form fields dynamically
-----------------------------------

If you need the list of form fields to be dynamic, instead of
``form_fields`` you can define a method ``get_form_fields(self)`` that
returns the list. But if you do this, you must make sure your template
also contains conditional logic so that the right ``formfield`` elements
are included.

You can do this by looping through each field in the form.
oTree passes a variable ``form`` to each template, which you can loop through
like this:

.. code-block:: django

    <!-- in your HTML template -->
    {% for field in form %}
        {% formfield field %}
    {% endfor %}

(If you need more complex looping logic than this,
then consider not using ``{% formfield %}`` and instead writing the
raw HTML for the ``<input>`` elements; see :ref:`radio-table`.)

``form`` is a special variable.
It is a Django form object, which is an iterable whose elements are Django form
field objects. ``formfield`` can take as an argument a Django field object,
or it can be an expression like ``{% formfield player.foo %}`` and
``{% formfield group.foo %}``, but ``player.foo`` must be written explicitly
rather than assigning ``somevar = player.foo`` and then doing
``{% formfield somevar %}``.

If you use this technique and want a custom label on each field, you can add a
``verbose_name`` to the model field,
as described in the Django documentation, e.g.:

.. code-block:: python

    # in models.py
    contribution = models.CurrencyField(
        verbose_name="How much will you contribute?")

This is essentially equivalent to setting ``label="How much will you contribute?"``
in the ``{% formfield %}``.

Forms with a dynamic vector of fields
-------------------------------------

Let's say you want a form with a vector of n fields that are identical, except for some numerical index, e.g.:

.. code-block:: python

    contribution[1], contribution[2], ..., contribution[n]

Furthermore, suppose n is variable (can range from 1 to N).

Currently in oTree, you can only define a fixed number of fields in a model.
So, you should define in ``models.py`` N fields (``contribution_1...contribution_N...``),
and then use ``get_form_fields`` as described above to dynamically return a list with the desired subset of these fields.

For example, let's say the above variable ``n`` is actually an ``IntegerField`` on the player,
which gets set dynamically at some point in the game. You can use ``get_form_fields``
like this:

.. code-block:: python

    class MyPage(Page):

        form_model = models.Player
        def get_form_fields(self):
            return ['contribution_{}'.format(i) for i in range(1, self.player.n + 1)]

Widgets
-------

The full list of form input widgets offered by Django is
`here <https://docs.djangoproject.com/en/1.7/ref/forms/widgets/#built-in-widgets>`__.

oTree additionally offers

-   ``RadioSelectHorizontal`` (same as ``RadioSelect`` but with a horizontal
    layout, as you would see with a Likert scale)
-   ``SliderInput``

    -   To specify the step size, do: ``SliderInput(attrs={'step': '0.01'})``
    -   To disable the current value from being displayed, do:
        ``SliderInput(show_value=False)``


Alternatives to oTree's ``{% formfield %}``
-------------------------------------------

It's not mandatory to use oTree's ``{% formfield %}`` element.
If your want to customize the appearance or behavior of your widgets,
you can use one of the approaches below.

Django widgets
~~~~~~~~~~~~~~

If the widget rendered by the ``{% formfield %}`` tag is not to your liking,
you can use Django's built-in widget rendering,
described `here <https://docs.djangoproject.com/en/1.9/topics/forms/#rendering-fields-manually>`__.

To make the formatting consistent with oTree's built-in widgets,
have a look at the HTML generated by a ``{% formfield %}`` element
(e.g. the structure ``<div>``s and ``class`` attributes).


Raw HTML widgets
~~~~~~~~~~~~~~~~

For maximum flexibility, you can skip ``{% formfield %}``
and Django's form widgets, and write the raw HTML for any form input.
Just ensure that each field in your Page's ``form_fields``
has a corresponding ``<input>`` element whose ``name`` attribute matches it.

.. _radio-table:

Raw HTML example: table of radio buttons
''''''''''''''''''''''''''''''''''''''''
Let's say you have a set of ``BooleanField`` in your model:

.. code-block:: python

    class Player(BasePlayer):

        offer_1 = models.BooleanField()
        offer_2 = models.BooleanField()
        offer_3 = models.BooleanField()
        offer_4 = models.BooleanField()
        offer_5 = models.BooleanField()

And you'd like to present them as a table of yes/no radio buttons like this:

.. image:: _static/forms/radio-table.png
    :align: center
    :scale: 100 %

Because the yes/no options must be in separate table cells,
the ordinary ``RadioSelectHorizontal`` widget will not work here.
So, you can skip using ``{% formfield %}`` entirely,
and write the raw HTML in your template:

.. code-block:: html+django

    <table class="table">
        <tr>
            <th>Offer</th><th>Accept</th><th>Reject</th>
        </tr>
        {% for number in offer_numbers %}
        <tr>
            <td>{{ number }}</td>
            <td><input type="radio" name="offer_{{ number }}" value="True" required></td>
            <td><input type="radio" name="offer_{{ number }}" value="False" required></td>
        </tr>
        {% endfor %}
    </table>

Finally, in ``views.py``, set ``form_fields`` and ``vars_for_template`` as follows:

.. code-block:: python

    class MyPage(Page):
        form_model = models.Player
        form_fields = ['offer_{}'.format(i) for i in range(1, 6)]

        def vars_for_template(self):
            return {'offer_numbers': range(1, 6)}


Raw HTML example: custom user interface with JavaScript
'''''''''''''''''''''''''''''''''''''''''''''''''''''''

Let's say you don't want users to fill out form fields,
but instead interact with some sort of visual app, like a clicking on a chart
or playing a graphical game. Or, you want to record extra data like how long
they spent on part of the page, how many times they clicked, etc.

You can build these interfaces in any front-end framework you want.
Simple ones can be done with jQuery; more complex ones would use something
like React or Polymer.

Then, use JavaScript to record the relevant data points and store it in a
hidden form field. For example:

.. code-block:: python

    # models.py
    my_hidden_input = models.PositiveIntegerField()

    # views.py
    form_fields = ['my_hidden_input']

    # HTML template
    <input type="hidden" name="my_hidden_input"
        value="5" id="id_my_hidden_input"/>

Then you can use JavaScript to set the value of that input, by selecting
the element by id ``id_my_hidden_input``, and setting its ``value`` attribute.

When the page is submitted, the value of your hidden input will be recorded
in oTree like any other form field.

Buttons
-------

If you have a ``<button>`` widget on your page,
clicking it will submit the form, unless you specify ``type="button"``:

.. code-block:: html+django

    {% block content %}

        <button>Clicking this will submit the form</button>

        <button type="button">Clicking this will not submit the form</button>

    {% endblock %}

