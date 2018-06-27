.. _templates:

Templates
=========

Your app's ``templates/`` folder will contain the templates for the
HTML that gets displayed to the player.

Template syntax
---------------

Variables
~~~~~~~~~

You can display a variable like this:

.. code-block:: django

     Your payoff is {{ player.payoff }}.

The following variables are available in templates:

-   ``player``: the player currently viewing the page
-   ``group``: the group the current player belongs to
-   ``subsession``: the subsession the current player belongs to
-   ``participant``: the participant the current player belongs to
-   ``session``: the current session
-   ``Constants``: constants you defined in ``models.py``
-   Any variables you passed with :ref:`vars_for_template`.

Conditions ("if")
~~~~~~~~~~~~~~~~~

.. code-block:: django

    {% if player.is_winner %} you won! {% endif %}

With an 'else' clause:

.. code-block:: django

    {% if some_number >= 0 %}
        positive
    {% else %}
        negative
    {% endif %}

Loops ("for")
~~~~~~~~~~~~~

.. code-block:: django

    {% for item in some_list %}
        {{ item }}
    {% endfor %}


Method calls
~~~~~~~~~~~~

To call a method from one of your models, make sure to omit the parentheses
(unlike regular Python code).

.. code-block:: python

    class Player(BasePlayer):
        def doubled_payoff(self):
            return self.payoff * 2

.. code-block:: django

    Your doubled payoff is {{ player.doubled_payoff }}.

Accessing items in a list or dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Whereas in Python code you do ``my_list[0]`` and ``my_dict['foo']``,
in a template you would do ``{{ my_list.0 }}`` and ``{{ my_dict.foo }}``.

Comments
~~~~~~~~

.. code-block:: django


    {% comment %}
    This is a
    multi-line comment
    {% endcomment %}


Template filters
~~~~~~~~~~~~~~~~

In addition to the filters available with Django's template language,
oTree has the ``|c`` filter, which is equivalent to the ``c()`` function.
For example, ``{{ 20|c }}`` displays as ``20 points``.

Also, the ``|abs`` filter lets you take the absolute value.
So, doing ``{{ -20|abs }}`` would output ``20``.

If you get an "Invalid filter" error,
make sure you have ``{% load otree %}``
at the top of your template.

Things you can't do
~~~~~~~~~~~~~~~~~~~

The template language is designed for simply displaying and looping over values.
Most other things are not supported; for example,
you can't do math (``+``, ``*``, ``/``, ``-``)
or otherwise modify numbers, lists, strings, etc.
If you need to do that, you should do so in :ref:`vars_for_template`.

How templates work: an example
------------------------------

oTree templates are a mix of 2 languages:

-   *HTML* (which uses angle brackets like ``<this>`` and ``</this>``.
-   *Django template tags*
    (which use curly braces like ``{% this %}`` and ``{{ this }}``

Here is an example of how the two languages work together.
In this example, let's say your template looks like this:

.. code-block:: html+django

    <p>Your payoff this round was {{ player.payoff }}.</p>

    {% if subsession.round_number > 1 %}
        <p>
            Your payoff in the previous round was {{ last_round_payoff }}.
        </p>
    {% endif %}

    {% next_button %}


Step 1: oTree scans Django tags, produces HTML (a.k.a. "server side")
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

oTree uses the current values of the variables
(provided by :ref:`vars_for_template`) to convert the above Django code to
plain HTML, like this:

.. code-block:: html+django

    <p>Your payoff this round was $10.</p>

        <p>
            Your payoff in the previous round was $5.
        </p>

    <button class="otree-btn-next btn btn-primary">Next</button>


Step 2: Browser scans HTML tags, produces a webpage (a.k.a. "client side")
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The oTree server then sends this HTML to the user's computer,
where their web browser can read the code and display it
as a formatted web page:

.. figure:: _static/template-example.png

Note that the browser never sees the Django tags.

The key point
~~~~~~~~~~~~~

The key insight you can take from this example is
that if one of your pages doesn't look the way you want,
you can isolate which of the above steps went wrong.
In your browser, right-click and "view source".
(Note: "view source" may not work in split-screen mode.)

You can then see the pure
HTML that was generated (along with any JavaScript or CSS).

-   If the HTML code doesn't look the way you expect, then something
    went wrong on the server side. Look for mistakes in your ``vars_for_template``
    or your Django template tags.
-   If there was no error in generating the HTML code,
    then it is probably an issue with how you are using
    HTML (or JavaScript) syntax.
    Try pasting the problematic part of the HTML back into a template,
    without the Django tags, and edit it until it produces the right output.
    Then put the Django tags back in, to make it dynamic again.


Template blocks
---------------

Instead of writing the full HTML of your page, for example:

.. code-block:: html

    <!DOCTYPE html>
        <html lang="en">
            <head>
                <!-- and so on... -->


You define 2 blocks:

.. code-block:: django

    {% block title %} Title goes here {% endblock %}

    {% block content %}
        Body HTML goes here.

        {% formfield player.contribution label="What is your contribution?" %}

        {% next_button %}
    {% endblock %}


Images, videos, CSS, JavaScript, etc. (static files)
----------------------------------------------------

Here is how to include static files (.png, .jpg, .mp4, .css, .js, etc.) in your pages.

There is a ``_static/`` folder in your project folder.
Create a subfolder with any name you want (or use the existing ``global/`` subfolder),
and put your files there.

Let's say you have an image in ``_static/my_app/my_image.png``.
To display it, you need to use an ``<img>`` tag whose ``src`` is set to that image's URL,
which you can retrieve with the ``{% static %}`` tag:

.. code-block:: HTML+django

    <img src="{% static "my_app/my_image.png" %}"/>


If the file is in ``_static/global/my_image.png``, you would do:

.. code-block:: HTML+django

    <img src="{% static "global/my_image.png" %}"/>

(If you prefer, you can also put static files inside your app folder,
in a subfolder called ``static/your_app_name``.)

Notes:

-   If you get an error "invalid block tag: static", then make sure you have ``{% load static %}``
    at the top of your template.
-   If a static file is not updating even after you changed it,
    this is because your browser cached the file. Do a full page reload
    (usually Ctrl+F5)

Dynamic images
~~~~~~~~~~~~~~

If the image/video path is variable (like showing a different image each round),
you can construct it in ``pages.py`` and pass it to the template, e.g.:

.. code-block:: python

    class MyPage(Page):

        def vars_for_template(self):
            return {
                'image_path': 'my_app/{}.png'.format(self.round_number)
            }

Then in the template:

.. code-block:: HTML+django

    <img src="{% static image_path %}"/>


.. _base-template:

JavaScript and CSS
------------------

Where to put JavaScript/CSS code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It depends whether you want your JS/CSS code to be applied (a) globally,
(b) in just one app, or (c) in just one page.

Globally
^^^^^^^^

To apply a style or script to all pages in all games,
modify the template ``_templates/global/Page.html``.
Put any scripts inside ``{% block global_scripts %}...{% endblock %}``,
and any styles inside ``{% block global_styles %}...{% endblock %}``.


For one app
^^^^^^^^^^^

To apply a style or script to all pages in one app,
create a base template for all templates in your app,
and put blocks called ``app_styles`` or ``app_scripts`` in this base template.

For example, if your app's name is ``public_goods``,
then you would create a file called ``public_goods/templates/public_goods/Page.html``,
and put this inside it:

.. code-block:: html+django

    {% extends "global/Page.html" %}
    {% load static otree %}

    {% block app_styles %}

        <style type="text/css">
            ...
        </style>

    {% endblock %}


Then each ``public_goods`` template would inherit from this template:

 .. code-block:: html+django

    {% extends "public_goods/Page.html" %}
    {% load static otree %}
    ...

Just one page
^^^^^^^^^^^^^

If you have JavaScript and/or CSS code that just applies to a single page,
you can put it directly in the ``content`` block, or for better organization,
put it in blocks called ``scripts`` and ``styles``.
They should be located outside the ``content`` block, like this:

.. code-block:: HTML+django

    {% block content %}
        <p>This is some HTML.</p>
    {% endblock %}

    {% block styles %}

        <!-- define a style -->
        <style type="text/css">
            ...
        </style>

        <!-- or reference a static file -->
        <link href="{% static "my_app/style.css" %}" rel="stylesheet">

    {% endblock %}

    {% block scripts %}

        <!-- define a script -->
        <script>
            ...
        </script>

        <!-- or reference a static file -->
        <script src="{% static "my_app/script.js" %}"></script>
    {% endblock %}


It's not mandatory to do this, but:

-   It keeps your code organized
-   It ensures that things are loaded in the correct order
    (CSS, then your page content, then JavaScript).

.. _selectors:

Customizing the theme
~~~~~~~~~~~~~~~~~~~~~

If you want to customize the appearance of an oTree element,
here is the list of CSS selectors:

=========================   ================================================
Element                     CSS/jQuery selector
=========================   ================================================
Page body                   ``.otree-body``
Page title                  ``.otree-title``
Wait page (entire dialog)   ``.otree-wait-page``
Wait page dialog title      ``.otree-wait-page__title``
Wait page dialog body       ``.otree-wait-page__body``
Timer                       ``.otree-timer``
Next button                 ``.otree-btn-next``
Form errors alert           ``.otree-form-errors``
=========================   ================================================

For example, to change the page width, put CSS in your base template like this:

.. code-block:: HTML

    <style>
        .otree-body {
            max-width:800px
        }
    </style>

To get more info, in your browser, right-click the element you want to modify and select
"Inspect". Then you can navigate to see the different elements and
try modifying their styles:

.. figure:: _static/dom-inspector.png

When possible, use one of the official selectors above.
Don't use any selector that starts with ``_otree``, and don't select based on Bootstrap classes like
``btn-primary`` or ``card``, because those are unstable.

.. _json:

Passing data from Python to JavaScript (json)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to insert a variable into to your JavaScript code,
write it as ``{{ my_variable|json }}`` rather than just ``{{ my_variable }}``.

For example, if you need to pass the player's payoff to a script,
write it like this:

.. code-block:: HTML+django

    <script>
        var payoff = {{ player.payoff|json }};
        ...
    </script>


If you don't use ``|json``,
the variable might not be valid JavaScript.
Examples:

=============  ===================================  ==================
In Python      In template, without ``|json``       With ``|json``
=============  ===================================  ==================
``None``       ``None``                             ``null``
``3.14``       ``3,14`` (depends on LANGUAGE_CODE)  ``3.14``
``c(3.14)``    ``$3.14`` or ``$3,14``               ``3.14``
``True``       ``True``                             ``true``
``"a"``        ``a``                                ``"a"``
``{'a': 1}``   ``{&#39;a&#39;: 1}``                 ``{"a": 1}``
``['a']``      ``[&#39;a&#39;]``                    ``["a"]``
=============  ===================================  ==================

``|json`` can be used on simple values like ``1``,
or a nesting of dictionaries and lists like ``{'a': [1,2]}``, etc.

``|json`` converts to JSON and marks the data as safe (trusted)
so that Django does not auto-escape it.

As shown in the above table, ``|json`` will automatically put
quotes around strings, so you don't need to add them manually:

.. code-block:: HTML+django

        // correct
        var my_string = {{ my_string|json }};

        // incorrect
        var my_string = "{{ my_string|json }}";

If you get an "Invalid filter" error, make sure you have ``{% load otree %}``
at the top of your template.

Note: The ``|json`` template filter replaces the old ``safe_json``
function. However, ``safe_json`` still works.
Just use one or the other, not both.


Bootstrap
---------

oTree comes with `Bootstrap <https://getbootstrap.com/docs/4.0/components/alerts/>`__, a
popular library for customizing a website's user interface.

.. note::

    As of oTree 2.0 (January 2018), oTree upgraded from Bootstrap 3 to
    Bootstrap 4. See :ref:`v20` for more info.

You can use it if you want a `custom style <http://getbootstrap.com/css/>`__, or
a `specific component <http://getbootstrap.com/components/>`__ like a table,
alert, progress bar, label, etc. You can even make your page dynamic with
elements like `popovers <https://getbootstrap.com/docs/4.0/components/popovers/>`__,
`modals <https://getbootstrap.com/docs/4.0/components/modal/>`__, and
`collapsible text <https://getbootstrap.com/docs/4.0/components/collapse/>`__.

To use Bootstrap, usually you add a ``class=`` attribute to your HTML
element.

For example, the following HTML will create a "Success" alert:

.. code-block:: HTML

        <div class="alert alert-success">Great job!</div>

Mobile devices
~~~~~~~~~~~~~~

Bootstrap tries to show a "mobile friendly" version
when viewed on a smartphone or tablet.


Charts
------

You can use any HTML/JavaScript library for adding charts to your app.

We particularly recommend `HighCharts <http://www.highcharts.com/demo>`__,
to draw pie charts, line graphs, bar charts, time series, etc.
Some of oTree's sample games use HighCharts.

First, include the HighCharts JavaScript::

    <script src="https://code.highcharts.com/highcharts.js"></script>

If you will be using HighCharts in many places, you can also put it in
``app_scripts`` or ``global_scripts``; see above for more info.
(But note that HighCharts can make your pages slower.)

Go to the HighCharts `demo site <http://www.highcharts.com/demo>`__
and find the chart type that you want to make.
Then click "edit in JSFiddle" to edit it to your liking,
using hardcoded data.

Then, copy-paste the JS and HTML into your template,
and load the page. If you don't see your chart, it may be because
your HTML is missing the ``<div>`` that your JS code is trying to insert the chart
into.

Once your chart is loading properly, you can replace the hardcoded data
like ``series`` and ``categories`` with dynamically generated variables.

For example, change this::

    series: [{
        name: 'Tokyo',
        data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
    }, {
        name: 'New York',
        data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
    }]

To this::

    series: {{ highcharts_series|json }}

In the page's ``vars_for_template``, generate the nested data structure in Python
(the above example is a list of dictionaries),
pass it to the template, and remember to use the :ref:`|json <json>` filter`` on any variables
you insert in JavaScript.

If your chart is not loading, click "View Source" in your browser
and check if there is something wrong with the data you dynamically generated.
If it looks all garbled like ``{&#39;a&#39;: 1}``,
you may have forgotten to use the ``|json`` filter.


Note about PyCharm Professional
-------------------------------

If you are using the regular edition of PyCharm
(Community Edition), consider upgrading to PyCharm Professional Edition,
because it provides syntax highlighting of Django templates
and JavaScript.

PyCharm Professional is free if you are a student, teacher, or professor.

Once you've installed Professional Edition, in settings,
navigate to ``Languages & Frameworks -> Django``,
check "Enable Django Support" and set your oTree folder as the Django project root,
with your ``manage.py`` and ``settings.py``.
