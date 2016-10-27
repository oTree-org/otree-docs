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

        <script>
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
        <script src="{% static "my_app/script.js" %}"></script>
    {% endblock %}


The reasons for putting scripts and styles in separate blocks are:

-   It keeps your code organized
-   jQuery may only be loaded at the bottom of the page,
    so if you reference the jQuery ``$`` variable in the ``content`` block,
    it could be undefined.

Customizing the base template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For all apps
^^^^^^^^^^^^

If you want to apply a style or script to all pages in all games,
you should modify the template ``_templates/global/Base.html``.
You should put any scripts inside ``{% block global_scripts %}...{% endblock %}``,
and any styles inside ``{% block global_styles %}...{% endblock %}``.


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
to draw pie charts, line graphs, bar charts, time series,
and other types of plots.

Some of oTree's sample games use HighCharts.

First, include the HighCharts JavaScript in your page's ``scripts`` block::

    {% block scripts %}
        <script src="https://code.highcharts.com/highcharts.js"></script>
    {% endblock %}

If you will be using HighCharts in many places, you can also put it in
``app_scripts`` or ``global_scripts``; see above for more info.
(But note that HighCharts slows down page rendering time somewhat.)

To make a chart, first go to the HighCharts `demo site <http://www.highcharts.com/demo>`__
and find the chart type that you want to make.
Then click "edit in JSFiddle" to edit it to your liking.

To pass data like a list of values from Python to HighCharts, you should
first pass it through the ``otree.api.safe_json()`` function. This
converts to the correct JSON syntax and also uses ``mark_safe`` for the
template.

Example:

.. code-block:: python

    >>> a = [0, 1, 2, 3, 4, None]
    >>> from otree.api import safe_json
    >>> safe_json(a)
    '[0, 1, 2, 3, 4, null]'



LaTeX
^^^^^

If you want to put LaTeX formulas in your app,
you can try `KaTeX <http://khan.github.io/KaTeX/>`__.


oTree on mobile devices
~~~~~~~~~~~~~~~~~~~~~~~

oTree's HTML interface is based on `Bootstrap <http://getbootstrap.com/components/>`__,
which works on any modern browser (Chrome/Internet Explorer/Firefox/Safari).

Bootstrap also tries to shows a "mobile friendly" version
when viewed on a smartphone or tablet.

Custom template filters
~~~~~~~~~~~~~~~~~~~~~~~

In addition to the filters available with Django's template language,
oTree has the ``|c`` filter, which is equivalent to the ``c()`` function.
For example, ``{{ 20|c }}`` displays as ``20 points``.

Also, the ``|abs`` filter lets you take the absolute value.
So, doing ``{{ -20|abs }}`` would output ``20``.