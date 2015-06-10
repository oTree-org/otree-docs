Forms
=====

Each page in oTree can contain a form, which the player should fill out
and submit by clicking the "Next" button. To create a form, first you
should go to models.py and define fields on your Player or Group. Then,
in your Page class, you can define ``form_models`` to specify the model
that this form modifies (either ``models.Player`` or ``models.Group``),
and ``form_fields``, which is list of the fields from that model.

When the user submits the form, the submitted data is automatically
saved back to the field in your model.

Forms in templates
------------------

You should include form fields by using a ``{% formfield %}`` element.
You generally do not need to write raw HTML for forms (e.g.
``<input type="text" id="...">``).

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

You can specify additional validation. For example, here is how you would require integer to be between
12 and 24:

.. code:: python

    offer = models.PositiveIntegerField(min=12, max=24)

You can constrain the user to a predefined list of choices by using ``choices``:

.. code:: python

    year_in_school = models.CharField(choices=['Freshman', 'Sophomore', 'Junior', 'Senior'])

The user will then be presented a dropdown menu instead of free text input.

If you would like a specially formatted value displayed to the user that
is different from the values stored internally, ``choices`` can be a list
consisting itself of tuples of two items.
The first element in each tuple is the value and the second element is the human-readable label.
For example:

.. code:: python

    year_in_school = models.CharField(
        choices=[
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
        ]
    )

After the field has been set, you can access the human-readable name
using
`get\_FOO\_display <https://docs.djangoproject.com/en/1.8/ref/models/instances/#django.db.models.Model.get_FOO_display>`__
, like this:
``self.get_year_in_school_display() # returns e.g. 'Sophomore'``

If a field is optional, you can do:

.. code:: python

    offer = models.PositiveIntegerField(blank=True)

Dynamic validation
~~~~~~~~~~~~~~~~~~

If you need a form's choices or validation logic to depend on some
dynamic calculation, then you can instead define one of the below
methods in your ``Page`` class in ``views.py``.

-  ``def {field_name}_choices(self)``

Example:

.. code:: python

    def offer_choices(self):
        return currency_range(0, self.player.endowment, 1)

-  ``def {field_name}_min(self)``

The dynamic alternative to ``min``.

-  ``def {field_name}_max(self)``

The dynamic alternative to ``max``.

-  ``def {field_name}_error_message(self, value)``

This is the most flexible method for validating a field.

For example, let's say your form has an integer field called
``odd_negative``, which must be odd and negative: You would enforce this
as follows:

.. code:: python

    def odd_negative_error_message(self, value):
        if not (value < 0 and value % 2):
            return 'Must be odd and negative'

Validating multiple fields together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you have 3 integer fields in your form whose names are
``int1``, ``int2``, and ``int3``, and the values submitted must sum to
100. You would define the ``error_message`` method in your Page class:

.. code:: python

    def error_message(self, values):
        if values["int1"] + values["int2"] + values["int3"] != 100:
            return 'The numbers must add up to 100'

Determining the list of form fields dynamically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need the list of form fields to be dynamic, instead of
``form_fields`` you can define a method ``get_form_fields(self)`` that
returns the list. But if you do this, you must make sure your template
also contains conditional logic so that the right ``formfield`` elements are included.

You can do this by looping through each field in the form.
oTree passes a variable ``form`` to each template, which you can loop through like this:

.. code::

    {% for field in form %}
        {% formfield field %}
    {% endfor %}

``form`` is a special variable.
It is a Django form object, which is an iterable whose elements are Django form field objects.
``formfield`` can take as an argument a Django field object,
or it can be an expression like ``{% formfield player.foo %}`` and ``{% formfield group.foo %}``,
but ``player.foo`` must be written as a literal rather than assigning ``somevar = player.foo``
and then doing ``{% formfield somevar %}``.

If you use this technique and want a custom label on each field, you can add a ``verbose_name`` to the model field,
as described in the Django documentation, e.g.:

.. code:: python

    contribution = models.CurrencyField(verbose_name="How much will you contribute?")


Widgets
-------

The full list of form input widgets offered by Django is
`here <https://docs.djangoproject.com/en/1.7/ref/forms/widgets/#built-in-widgets>`__.

oTree additionally offers
- ``RadioSelectHorizontal`` (same as ``RadioSelect`` but with a horizontal layout, as you would see with a Likert scale)
- ``SliderInput`` (you can specify the step size like this: ``SliderInput(attrs={'step': '0.01'})``)


Custom widgets and hidden fields
--------------------------------

It's not mandatory to use the ``{% formfield %}`` element; you can write
the raw HTML for any form input if you wish to customize its behavior or
appearance. Just include an ``<input>`` element with the same ``name``
attribute as the field. For example, if you want a hidden input, you can
do this:

.. code-block:: python

    # models.py
    my_hidden_input = models.PositiveIntegerField()

    # views.py
    form_fields = ['my_hidden_input', 'some_other_field']

    # HTML template
    <input type="hidden" name="my_hidden_input" value="5" id="id_my_hidden_input"/>


Then you can use JavaScript to set the value of that input, by selecting
the element by id ``id_my_hidden_input``.

For simple widgets you can use jQuery; for more complex or custom form
interfaces, you can use a front-end framework with databinding, like
React or Polymer.

If you want your custom widget's style to look like the rest of the
oTree widgets, you should look at the generated HTML from the
``{% formfield %}`` tag. You can copy and paste the markup into the template
and use that as a starting point for modifications.
