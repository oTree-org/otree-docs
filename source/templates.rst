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
the file ``_templates/global/Base.html``.

JavaScript and CSS
~~~~~~~~~~~~~~~~~~

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

        <script type="text/javascript">
        jQuery(document).ready(function ($) {
            var PRIVATE_VALUE = {{ player.private_value.to_number|escapejs }};

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
        <script type="text/javascript" src="{% static "my_app/script.js" %}"></script>
    {% endblock %}


The reasons for putting scripts and styles in separate blocks are:

- It keeps your code organized
- jQuery is only loaded at the bottom of the page, so if you reference the jQuery ``$`` variable in the ``content`` block, it will be undefined.

Customizing the base template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For all apps
^^^^^^^^^^^^

If you want to apply a style or script to all pages in all games,
you should modify the template ``_templates/global/Base.html``.
You should put any scripts in the ``global_scripts`` block,
and any styles in the ``global_styles`` block.

You can also modify ``_static/global/custom.js`` and ``_static/global/custom.js``,
which as you can see are loaded by ``_templates/global/Base.html``.

.. note::

    If you downloaded oTree prior to September 7, 2015, you need to update ``_templates/global/Base.html`` to the latest version
    `here <https://github.com/oTree-org/oTree/blob/master/_templates/global/Base.html>`__.

    Old versions have a bug where ``custom.js`` was not being loaded. See `here <https://github.com/oTree-org/oTree/pull/48>`__
    for more info.


For one app
^^^^^^^^^^^

If you want to apply a style or script to all pages in one app,
you should create a base template for all templates in your app,
and put blocks called ``app_styles`` or ``app_scripts`` in this base template.

For example, if your app's name is ``public_goods``,
then you would create a file called ``public_goods/templates/public_goods/Base.html``,
and put this inside it:

.. code-block:: html+django

    {% extends "global/Base.html" %}
    {% load staticfiles otree_tags %}

    {% block app_styles %}

        <style type="text/css">
            /* custom styles go here */
        </style>

    {% endblock %}


Then each ``public_goods`` template would inherit from this template:

 .. code-block:: html+django

     {% extends "public_goods/Base.html" %}
     {% load staticfiles otree_tags %}
     ...


Static content (images, videos, CSS, JavaScript)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To include images, CSS, or JavaScript in your pages, make sure your template
has loaded ``staticfiles``.

Then create a ``static/`` folder in your app (next to ``templates/``).
Like ``templates/``, it should also have a subfolder with your app's name.

Put your files in that subfolder. You can then reference them in a template
like this:

.. code-block:: HTML+django

    <img src="{% static "my_app/my_image.png" %}"/>


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

oTree comes pre-loaded with `HighCharts <http://www.highcharts.com/demo>`__,
which you can use to draw pie charts, line graphs, bar charts, time series,
and other types of plots.

Some of oTree's sample games use HighCharts.

To make a chart, first go to the HighCharts `demo site <http://www.highcharts.com/demo>`__
and find the chart type that you want to make.
Then click "edit in JSFiddle" to edit it to your liking.


To pass data like a list of values from Python to HighCharts, you should
first pass it through the ``otree.common.safe_json()`` function. This
converts to the correct JSON syntax and also uses ``mark_safe`` for the
template.

Example:

.. code-block:: python

    >>> a = [0, 1, 2, 3, 4, None]
    >>> safe_json(a)
    '[0, 1, 2, 3, 4, null]'



LaTeX
^^^^^

LaTeX used to be built-in to oTree but has been removed.
If you want to put LaTeX formulas in your app,
you can try `KaTeX <http://khan.github.io/KaTeX/>`__.


oTree on mobile devices
~~~~~~~~~~~~~~~~~~~~~~~

Since oTree uses Bootstrap for its user interface, your oTree app should
work on all major browsers (Chrome/Internet Explorer/Firefox/Safari).
When participants visit on a smartphone or tablet (e.g.
iOS/Android/etc.), they should see an appropriately scaled down "mobile
friendly" version of the site. This will generally not require much
effort on your part since Bootstrap does it automatically, but if you
plan to deploy your app to participants on mobile devices, you should
test it out on a mobile device during development, since some HTML code
doesn't look good on mobile devices.

Custom template filters
~~~~~~~~~~~~~~~~~~~~~~~

In addition to the filters available with Django's template language,
oTree has the ``|c`` filter, which is equivalent to the ``c()`` function.
For example, ``{{ 20|c }}`` displays as ``20 points``.

Also, the ``|abs`` filter lets you take the absolute value.
So, doing ``{{ -20|abs }}`` would output ``20``.