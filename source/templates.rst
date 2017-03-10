.. _templates:

Templates
=========

Your app's ``templates/`` directory will contain the templates for the
HTML that gets displayed to the player.

oTree uses `Django's template system
<https://docs.djangoproject.com/en/1.8/ref/templates/language/>`_.


Template blocks
~~~~~~~~~~~~~~~

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



You may want to customize the appearance or functionality of all pages
in your app (e.g. by adding custom CSS or JavaScript). To do this, edit
the file ``_templates/global/Page.html``.

JavaScript and CSS
~~~~~~~~~~~~~~~~~~

Where to put scripts and CSS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have JavaScript and/or CSS in your page, you should put them in blocks called ``scripts``
and ``styles``, respectively. They should be located outside the ``content`` block, like this:

.. code-block:: HTML+django

    {% block content %}
        <p>This is some HTML.</p>
    {% endblock %}

    {% block styles %}

        <!-- define a style -->
        <style type="text/css">
            .bid-slider {
                margin: 1.5em auto;
                width: 70%;
            }
        </style>

        <!-- or reference a static file -->
        <link href="{% static "my_app/style.css" %}" rel="stylesheet">

    {% endblock %}

    {% block scripts %}

        <!-- define a script -->

        <script>
            var input = $('#id_bid_amount');

            $('.bid-slider').slider({
                min: 0,
                max: 100,
                slide: function (event, ui) {
                    input.val(ui.value);
                    updateBidValue();
                },
            });
        </script>

        <!-- or reference a static file -->
        <script src="{% static "my_app/script.js" %}"></script>
    {% endblock %}


The reasons for putting scripts and styles in separate blocks are:

-   It keeps your code organized
-   jQuery may only be loaded at the bottom of the page,
    so if you reference the jQuery ``$`` variable in the ``content`` block,
    it could be undefined.

.. _safe_json:

Passing data from Python to JavaScript (safe_json)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to generate a variable that will be used in JavaScript code,
you should first pass it through the ``safe_json()`` function
to convert the data to JavaScript format (JSON).

For example, if you need to pass the player's payoff to a script:

.. code-block:: HTML+django

    <script>
        var payoff = {{ payoff }};
        ...
    </script>

You should use ``safe_json``:

.. code-block:: python

    from otree.api import safe_json

    class MyPage(Page):
        def vars_for_template(self):
            return {'payoff': safe_json(self.player.payoff)}


If you don't use ``safe_json``,
the variable might not be valid JavaScript.
Examples:

=============  ===================================  ==================
In Python      In template, without safe_json       With safe_json
=============  ===================================  ==================
``None``       ``None``                             ``null``
``3.14``       ``3,14`` (depends on LANGUAGE_CODE)  ``3.14``
``c(3.14)``    ``$3.14`` or ``$3,14``               ``3.14``
``True``       ``True``                             ``true``
``{'a': 1}``   ``{&#39;a&#39;: 1}``                 ``{"a": 1}``
``['a']``      ``[&#39;a&#39;]``                    ``["a"]``
=============  ===================================  ==================

The input to ``safe_json`` can be a simple value like ``1``,
or a nesting of dictionaries and lists like ``{'a': [1,2]}``, etc.

``safe_json`` converts to JSON and marks the data as safe (trusted)
so that Django does not auto-escape it.

Customizing the base template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For all apps
^^^^^^^^^^^^

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

.. note::

    There was a bug in recent versions of otree-core
    that prevented ``global_scripts`` or ``global_styles``
    from working properly. You should upgrade to the latest release
    (bug fixed on 2017-01-19).

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


Customizing the theme
^^^^^^^^^^^^^^^^^^^^^

Let's say you want to change some aspect of oTree's template.
For example, you may want to change the page width,
or change a font.

In your browser, right-click the element you want to modify and select
"Inspect". Then you can navigate to see the different elements and
try modifying their styles. For example, to remove the thin line below the page title,
you can click on the title to discover it's wrapped in a ``<div>`` whose
class is ``page-header`` and which has ``border-bottom: 1px``:

.. figure:: _static/dom-inspector.png

So, you can remove this line by adding the following style to your base template:

.. code-block:: HTML

    <style>
        .page-header {
            border-bottom: none;
        }
    </style>


Static content (images, videos, CSS, JavaScript)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~

oTree comes pre-loaded with the following plugins and libraries.

Bootstrap
^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

    series: {{ highcharts_series }}

In the page's ``vars_for_template``, generate the nested data structure in Python
(the above example is a list of dictionaries),
pass it through :ref:`safe_json <safe_json>` to convert to JavaScript,
and pass it to the template.

If your chart is not loading, click "View Source" in your browser
and check if there is something wrong with the data you dynamically generated.
If it looks all garbled like ``{&#39;a&#39;: 1}``,
you may have forgotten to use :ref:`safe_json <safe_json>`.

LaTeX
^^^^^

If you want to put LaTeX formulas in your app,
you can try `KaTeX <http://khan.github.io/KaTeX/>`__.


Mobile devices
~~~~~~~~~~~~~~

oTree's HTML interface is based on `Bootstrap <http://getbootstrap.com/components/>`__,
which works on any modern browser (Chrome/Internet Explorer/Firefox/Safari).

Bootstrap also tries to shows a "mobile friendly" version
when viewed on a smartphone or tablet.

Template filters
~~~~~~~~~~~~~~~~

In addition to the filters available with Django's template language,
oTree has the ``|c`` filter, which is equivalent to the ``c()`` function.
For example, ``{{ 20|c }}`` displays as ``20 points``.

Also, the ``|abs`` filter lets you take the absolute value.
So, doing ``{{ -20|abs }}`` would output ``20``.