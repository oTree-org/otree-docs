.. _templates:

Templates
=========

Your app's ``templates/`` directory will contain the templates for the
HTML that gets displayed to the player.

oTree uses `Django's template system
<https://docs.djangoproject.com/en/1.8/ref/templates/language/>`_.


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

        {% formfield player.contribution with label="What is your contribution?" %}

        {% next_button %}
    {% endblock %}


.. _base-template:

JavaScript and CSS
------------------

Where to put JavaScript/CSS code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It depends whether you want your JS/CSS code to be applied (a) globally,
(b) in just one app, or (c) in just one page.

Globally
^^^^^^^^

If you want to apply a style or script to all pages in all games,
you should modify the template ``_templates/global/Page.html``.
You should put any scripts inside ``{% block global_scripts %}...{% endblock %}``,
and any styles inside ``{% block global_styles %}...{% endblock %}``.

.. note::

    ``Page.html`` used to be called ``Base.html``.
    If your project contains a file ``_templates/global/Base.html``,
    you should rename it to ``Page.html``.
    Then, if any templates extend ``global/Base.html``,
    you should instead make them extend ``global/Page.html``

For one app
^^^^^^^^^^^

If you want to apply a style or script to all pages in one app,
you should create a base template for all templates in your app,
and put blocks called ``app_styles`` or ``app_scripts`` in this base template.

For example, if your app's name is ``public_goods``,
then you would create a file called ``public_goods/templates/public_goods/Page.html``,
and put this inside it:

.. code-block:: html+django

    {% extends "global/Page.html" %}
    {% load staticfiles otree_tags %}

    {% block app_styles %}

        <style type="text/css">
            /* custom styles go here */
        </style>

    {% endblock %}


Then each ``public_goods`` template would inherit from this template:

 .. code-block:: html+django

    {% extends "public_goods/Page.html" %}
    {% load staticfiles otree_tags %}
    ...

Just one page
^^^^^^^^^^^^^

If you have JavaScript and/or CSS code that just applies to a single page,
you should put them in blocks called ``scripts``
and ``styles``.
They should be located outside the ``content`` block, like this:

.. code-block:: HTML+django

    {% block content %}
        <p>This is some HTML.</p>
    {% endblock %}

    {% block styles %}

        <!-- define a style -->
        <style type="text/css">
            /* CSS goes here */
        </style>

        <!-- or reference a static file -->
        <link href="{% static "my_app/style.css" %}" rel="stylesheet">

    {% endblock %}

    {% block scripts %}

        <!-- define a script -->
        <script>
            /* JS goes here */
        </script>

        <!-- or reference a static file -->
        <script src="{% static "my_app/script.js" %}"></script>
    {% endblock %}


The reasons for putting scripts and styles in separate blocks are:

-   It keeps your code organized
-   jQuery may only be loaded at the bottom of the page,
    so if you reference the jQuery ``$`` variable in the ``content`` block,
    it could be undefined.

Customizing the theme
~~~~~~~~~~~~~~~~~~~~~

.. note::

    These selectors are new in otree-core 1.4 (August 2017).

If you want to customize the appearance of an oTree element,
here is the list of CSS selectors:

=========================   ================================================
Element                     CSS/jQuery selector
=========================   ================================================
Page body                   ``.otree-body``
Page title                  ``.otree-title``
Wait page (entire dialog)   ``.otree-wait-page``
Wait page dialog title      ``.otree-wait-page__title``
Wait page dialg body  .     ``.otree-wait-page__body``
Timer                       ``.otree-timer``
Next button                 ``.otree-btn-next``
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
Don't use any selector that starts with ``_otree`` because those are
private.

.. _json:

Passing data from Python to JavaScript (json)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    The ``|json`` template filter is new in otree-core 1.2.2
    (released March 1, 2017). The old way was to use the ``safe_json``
    function in your Python code. ``safe_json`` still works,
    but most people will probably find ``json`` easier to use.
    Just use one or the other, not both.

If you need to insert a variable into to your JavaScript code,
write it as ``{{ my_variable|json }}`` rather than just ``{{ my_variable }}``.

For example, if you need to pass the player's payoff to a script,
write it like this:

.. code-block:: HTML+django

    <script>
        var payoff = {{ payoff|json }};
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

If you get an "Invalid filter" error, make sure you have ``{% load otree_tags %}``
at the top of your template.


Static content (images, videos, CSS, JavaScript)
------------------------------------------------

To include static files (.png, .jpg, .mp4, .css, .js, etc.) in your pages,
make sure your template has ``{% load staticfiles %}`` at the top.

Then create a ``static/`` folder in your app (next to ``templates/``).
Like ``templates/``, it should also have a subfolder with your app's name,
e.g. ``static/my_app``.

Put your files in that subfolder. You can then reference them in a template
like this:

.. code-block:: HTML+django

    <img src="{% static "my_app/my_image.png" %}"/>

If the image/video path is variable (like showing a different image each round),
you can construct it in ``views.py`` and pass it to the template, e.g.:

.. code-block:: python

    class MyPage(Page):

        def vars_for_template(self):
            return {'image_path': 'my_app/{}.png'.format(self.round_number),

Then in the template:

.. code-block:: HTML+django

    <img src="{% static image_path %}"/>


Plugins
-------

oTree comes pre-loaded with the following plugins and libraries.

Bootstrap
~~~~~~~~~

oTree comes with `Bootstrap <http://getbootstrap.com/components/>`__, a
popular library for customizing a website's user interface.

You can use it if you want a `custom style <http://getbootstrap.com/css/>`_, or
a `specific component <http://getbootstrap.com/components/>`_ like a table,
alert, progress bar, label, etc. You can even make your page dynamic with
elements like `popovers <http://getbootstrap.com/javascript/#popovers>`__,
`modals <http://getbootstrap.com/javascript/#modals>`_, and
`collapsible text <http://getbootstrap.com/javascript/#collapse>`_.

To use Bootstrap, usually you add a ``class=`` attributes to your HTML
element.

For example, the following HTML will create a "Success" alert:

.. code-block:: HTML

        <div class="alert alert-success">Great job!</div>

Graphs and charts with HighCharts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use `HighCharts <http://www.highcharts.com/demo>`__,
to draw pie charts, line graphs, bar charts, time series, etc.
Some of oTree's sample games use HighCharts.

First, include the HighCharts JavaScript in your page's ``scripts`` block::

    {% block scripts %}
        <script src="https://code.highcharts.com/highcharts.js"></script>
    {% endblock %}

If you will be using HighCharts in many places, you can also put it in
``app_scripts`` or ``global_scripts``; see above for more info.
(But note that HighCharts can make your pages slower.)

Go to the HighCharts `demo site <http://www.highcharts.com/demo>`__
and find the chart type that you want to make.
Then click "edit in JSFiddle" to edit it to your liking,
using dummy data.

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

Mobile devices
--------------

oTree's HTML interface is based on `Bootstrap <http://getbootstrap.com/components/>`__,
which works on any modern browser (Chrome/Internet Explorer/Firefox/Safari).

Bootstrap also tries to shows a "mobile friendly" version
when viewed on a smartphone or tablet.

Template filters
----------------

In addition to the filters available with Django's template language,
oTree has the ``|c`` filter, which is equivalent to the ``c()`` function.
For example, ``{{ 20|c }}`` displays as ``20 points``.

Also, the ``|abs`` filter lets you take the absolute value.
So, doing ``{{ -20|abs }}`` would output ``20``.

If you get an "Invalid filter" error,
make sure you have ``{% load otree_tags %}``
at the top of your template.
