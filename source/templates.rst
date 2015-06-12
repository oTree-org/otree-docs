
Templates
=========

Your app's ``templates/`` directory will contain the templates for the
HTML that gets displayed to the player.

oTree uses `Django's template system
<https://docs.djangoproject.com/en/dev/topics/templates/>`_.


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

Images, videos, CSS, JavaScript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To include images, CSS, or JavaScript in your pages, make sure your template has loaded ``staticfiles``.

Then create a `static/` folder in your app (next to ``templates/``).
Like ``templates/``, it should also have a subfolder with your app's name.

Put your files in that subfolder. You can then reference them in a template like this:

.. code:: HTML

    <img src="{% static "my_app/my_image.png" %}"/>


Plugins
~~~~~~~

oTree comes pre-loaded with the following plugins and libraries.

Bootstrap
^^^^^^^^^

oTree comes with `Bootstrap <http://getbootstrap.com/>`__, a
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

.. code:: HTML

        <div class="alert alert-success">Great job!</div>

Graphs and charts with HighCharts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

oTree comes pre-loaded with `HighCharts <http://www.highcharts.com/demo>`__,
which you can use to draw pie charts, line graphs, bar charts, time series, and other types of plots.

You can find examples in the library of how to use it.

To pass data like a list of values from Python to HighCharts, you should
first pass it through the ``otree.common.safe_json()`` function. This
converts to the correct JSON syntax and also uses ``mark_safe`` for the
template.

Example:

.. code-block:: python

    >>> a = [0, 1, 2, 3, 4, None]
    >>> safe_json(a)
    '[0, 1, 2, 3, 4, null]'


jQuery
^^^^^^

oTree comes pre-loaded with `jQuery <http://jquery.com/>`__, a
JavaScript library that lets you make your pages dynamic. You can
include a script and reference the standard ``$`` variable.

LaTeX
^^^^^

oTree comes pre-loaded with `KaTeX <http://khan.github.io/KaTeX/>`__; you
can insert LaTeX equations like this:

.. code-block:: html

    <span class="latex">
        1 + i = (1 + r)(1 + \pi)
    </span>

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
