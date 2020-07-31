.. _forms:

Forms
=====

Each page in oTree can contain a form, which the player should fill out
and submit by clicking the "Next" button. To create a form, first
you need fields on the player model, for example:

.. code-block:: python

    class Player(BasePlayer):
        name = models.StringField(label="Your name:")
        age = models.IntegerField(label="Your age:")

Then, in your Page class, set ``form_model`` and ``form_fields``:

.. code-block:: python

    class Page1(Page):
        form_model = 'player'
        form_fields = ['name', 'age'] # this means player.name, player.age

When the user submits the form, the submitted data is automatically
saved to the corresponding fields on the player model.

.. _label:

Forms in templates
------------------

In your template, you can display the form with:

.. code-block:: html+django

    {% formfields %}

If you want to position the fields individually,
you can instead use ``{% formfield %}``:

.. code-block:: html+django

    {% formfield player.contribution %}

You can also put the ``label`` in directly in the template:

.. code-block:: html+django

    {% formfield player.contribution label="How much do you want to contribute?" %}


.. _form-validation:

Simple form field validation
----------------------------

min and max
~~~~~~~~~~~

To require an integer to be between 12 and 24:

.. code-block:: python

    offer = models.IntegerField(min=12, max=24)

If the max/min are not fixed, you should use :ref:`FOO_max`

.. _choices:

choices
~~~~~~~

If you want a field to be a dropdown menu with a list of choices,
set ``choices=``:

.. code-block:: python

    level = models.IntegerField(
        choices=[1, 2, 3],
    )

To use radio buttons instead of a dropdown menu,
you should set the ``widget`` to ``RadioSelect`` or ``RadioSelectHorizontal``:

.. code-block:: python

    level = models.IntegerField(
        choices=[1, 2, 3],
        widget=widgets.RadioSelect
    )

If the list of choices needs to be determined dynamically, use :ref:`FOO_choices`

You can also set display names for each choice
by making a list of [value, display] pairs:

.. code-block:: python

    level = models.IntegerField(
        choices=[
            [1, 'Low'],
            [2, 'Medium'],
            [3, 'High'],
        ]
    )

If you do this, users will just see a menu with "Low", "Medium", "High",
but their responses will be recorded as 1, 2, or 3.

You can do this for ``BooleanField``, ``StringField``, etc.:

.. code-block:: python

    cooperated = models.BooleanField(
        choices=[
            [False, 'Defect'],
            [True, 'Cooperate'],
        ]
    )


After the field has been set, you can access the human-readable name
using
`get_FOO_display <https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model.get_FOO_display>`__
, like this:
``player.get_level_display() # returns e.g. 'Medium'``.

Optional fields
~~~~~~~~~~~~~~~

If a field is optional, you can use ``blank=True`` like this:

.. code-block:: python

    offer = models.IntegerField(blank=True)

.. _dynamic_validation:

Dynamic form field validation
-----------------------------

The ``min``, ``max``, and ``choices`` described above are only
for fixed (constant) values.
 
If you want them to be determined dynamically
(e.g. different from player to player),
then you can instead define one of the below
methods on your Page.

Note: if you have apps written before May 2019, the recommended format for these validation methods
has changed. See :ref:`dynamic-validation-new-format`.

.. _FOO_choices:

{field_name}_choices()
~~~~~~~~~~~~~~~~~~~~~~

Like setting ``choices=``,
this will set the choices for the form field
(e.g. the dropdown menu or radio buttons).

Example:

.. code-block:: python

    class Player(BasePlayer):

        fruit = models.StringField()

        def fruit_choices(self):
            import random
            choices = ['apple', 'kiwi', 'mango']
            random.shuffle(choices)
            return choices

.. _FOO_max:

{field_name}_max()
~~~~~~~~~~~~~~~~~~

The dynamic alternative to setting ``max=`` in the model field. For example:

.. code-block:: python

    class Player(BasePlayer):

        offer = models.CurrencyField()

        def offer_max(self):
            return self.budget

        budget = models.CurrencyField()


{field_name}_min()
~~~~~~~~~~~~~~~~~~

The dynamic alternative to setting ``min=`` on the model field.

.. _FOO_error_message:

{field_name}_error_message()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the most flexible method for validating a field.

.. code-block:: python

    class Player(BasePlayer):

        offer = models.CurrencyField()

        def offer_error_message(self, value):
            print('value is', value)
            if value > self.budget / 2:
                return 'Cannot offer more than half your remaining budget'

        budget = models.CurrencyField()


.. _error_message:

Validating multiple fields together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you have 3 integer fields in your form whose names are
``int1``, ``int2``, and ``int3``, and the values submitted must sum to
100. You can enforce this with the ``error_message`` method, which goes on the *page*, not the Player model:

.. code-block:: python

    class MyPage(Page):

        form_model = 'player'
        form_fields = ['int1', 'int2', 'int3']

        def error_message(self, values):
            print('values is', values)
            if values['int1'] + values['int2'] + values['int3'] != 100:
                return 'The numbers must add up to 100'

Notes:

-   If a field was left blank (and you set ``blank=True``), its value here will be ``None``.
-   This method is only executed if there are no other errors in the form.
-   You can also return a dict that maps field names to error messages.
    This way, you don't need to write many repetitive FIELD_error_message methods.

.. _get_form_fields:

Determining form fields dynamically
-----------------------------------

If you need the list of form fields to be dynamic, instead of
``form_fields`` you can define a method ``get_form_fields``:

.. code-block:: python

    def get_form_fields(self):
        if self.player.num_bids == 3:
            return ['bid_1', 'bid_2', 'bid_3']
        else:
            return ['bid_1', 'bid_2']

But if you do this, you have to be sure to also include the same
``{% formfield %}`` elements in your template. The easiest way is to use
``{% formfields %}``.

Widgets
-------

You can set a model field's ``widget`` to ``RadioSelect`` or ``RadioSelectHorizontal`` if you want choices
to be displayed with radio buttons, instead of a dropdown menu.


.. _django-forms:

Customizing a field's appearance
--------------------------------

``{% formfields %}`` and ``{% formfield %}`` are easy to use because they automatically output
all necessary parts of a form field (the input, the label, and any error messages),
with Bootstrap styling.

However, if you want more control over the appearance and layout,
you can use Django's manual field rendering. Instead of ``{% formfield player.my_field %}``,
do ``{{ form.my_field }}``, to get just the input element.
Just remember to also include ``{{ form.my_field.errors }}``.

More info `here <https://docs.djangoproject.com/en/2.2/topics/forms/#rendering-fields-manually>`__.

.. _radio-table:
.. _subwidgets:

Example: Radio buttons in tables and other custom layouts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you have a set of ``IntegerField`` in your model:

.. code-block:: python

    class Player(BasePlayer):

        offer_1 = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3])
        offer_2 = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3])
        offer_3 = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3])
        offer_4 = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3])
        offer_5 = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3])

And you'd like to present them as a likert scale, where each option is
in a separate column.

(First, try to reduce the code duplication in models.py by following
the instructions in :ref:`many-fields`.)

Because the options must be in separate table cells,
the ordinary ``RadioSelectHorizontal`` widget will not work here.

Instead, you should simply loop over the choices in the field as follows:

.. code-block:: html+django

    <tr>
        <td>{{ form.offer_1.label }}</td>
        {% for choice in form.offer_1 %}
            <td>{{ choice }}</td>
        {% endfor %}
    </tr>

If you have many fields with the same number of choices,
you can arrange them in a table:

.. code-block:: html+django

    <table class="table">
        {% for field in form %}
            <tr>
                <th>{{ field.label }}</th>
                {% for choice in field %}
                    <td>{{ choice }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </table>

You can also get choices individually by using their 0-based index,
e.g. ``{{ form.my_field.0 }}`` gives you the radio button of the first choice.
For more granular control, as described `here <https://docs.djangoproject.com/en/2.2/ref/forms/widgets/#radioselect>`__,
you can use the ``choice_label`` and ``tag`` attributes on a field choice.


.. _raw_html:

Raw HTML widgets
----------------

If ``{% formfield %}`` and :ref:`manual field rendering <django-forms>`
don't give you the appearance you want,
you can write your own widget in raw HTML.
However, you will lose the convenient features handled
automatically by oTree. For example, if the form has an error and the page
re-loads, all entries by the user may be wiped out.

First, add an ``<input>`` element.
For example, if your ``form_fields`` includes ``my_field``,
you can do ``<input name="my_field" type="checkbox" />``
(consult the HTML documentation on ``<input>``'s available ``type`` values).

Second, you should usually include ``{{ form.my_field.errors }}``,
so that if the participant submits an incorrect or missing value),
they can see the error message.


Raw HTML example: slider
~~~~~~~~~~~~~~~~~~~~~~~~

If you want a slider, instead of ``{% formfield %}``,
put HTML like this in your template:

.. code-block:: html

    <label class="col-form-label">
        Pizza is the best food:
    </label>

    <div class="input-group">
        <div class="input-group-prepend">
            <span class="input-group-text">Disagree</span>
        </div>

        <input type="range" name="pizza" min="-2" max="2" step="1">

        <div class="input-group-append">
            <span class="input-group-text">Agree</span>
        </div>
    </div>

If you want to show the current numeric value, or hide the knob until the slider is clicked
(to avoid anchoring), you could do that with JavaScript,
but consider using the ``RadioSelectHorizontal`` widget instead.

(oTree also has a ``Slider`` widget but its customizability is limited.)

Raw HTML example: custom user interface with JavaScript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you don't want users to fill out form fields,
but instead interact with some sort of visual app, like a clicking on a chart
or playing a graphical game. Or, you want to record extra data like how long
they spent on part of the page, how many times they clicked, etc.

You can build these interfaces in any front-end framework you want.
Simple ones can be done with plain JavaScript; more complex ones would use something
like React or Vue.js.

Then, use JavaScript to record the relevant data points and store it in a
hidden form field. For example:

.. code-block:: python

    # Player class
    my_hidden_input = models.IntegerField()

    # page
    form_fields = ['my_hidden_input']

    # HTML template
    <input type="hidden" name="my_hidden_input" />

Then you can use JavaScript to set the value of that input, by selecting
the element by name ``my_hidden_input``, and setting its ``value`` attribute.

When the page is submitted, the value of your hidden input will be recorded
in oTree like any other form field.

Buttons
-------

Button that submits the form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your page only contains 1 decision,
you could omit the ``{% next_button %}``
and instead have the user click on one of several buttons
to go to the next page.

For example, let's say your Player model has ``offer_accepted = models.BooleanField()``,
and rather than a radio button you'd like to present it as a button like this:

.. image:: _static/forms/yes-no-buttons.png
    :align: center

First, put ``offer_accepted`` in your Page's ``form_fields`` as usual.
Then put this code in the template:

.. code-block:: html+django

    <p>Do you wish to accept the offer?</p>
    <div>
        <button name="offer_accepted" value="True">Yes</button>
        <button name="offer_accepted" value="False">No</button>
    </div>

You can use this technique for any type of field,
not just ``BooleanField``.

Button that doesn't submit the form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the button has some purpose other than submitting the form,
add ``type="button"``:

.. code-block:: html+django

    <button>
        Clicking this will submit the form
    </button>

    <button type="button">
        Clicking this will not submit the form
    </button>


Miscellaneous & advanced
------------------------

Form fields with dynamic labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the label should contain a variable, you can construct the string in your page:

.. code-block:: python

    class Contribute(Page):
        form_model = 'player'
        form_fields = ['contribution']

        def vars_for_template(self):
            return dict(
                contribution_label='How much of your {} do you want to contribute?'.format(self.player.endowment)
            )

Then in the template, set the label to this variable:

.. code-block:: html+django

    {% formfield player.contribution label=contribution_label %}

If you use this technique, you may also want to use :ref:`dynamic_validation`.
