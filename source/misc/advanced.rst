Advanced features
=================

These are advanced features that are mostly unsupported in oTree Studio.

Templates
---------

template_name
~~~~~~~~~~~~~

If the template needs to have a different name from your
page class (e.g. you are sharing the same template for multiple pages),
set ``template_name``. Example:

.. code-block:: python

    class Page1(Page):
        template_name = 'app_name/MyPage.html'

.. _base-template:

CSS/JS and base templates
~~~~~~~~~~~~~~~~~~~~~~~~~

To include the same JS/CSS in all pages of an app,
make a base template for the app.

For example, if your app's name is ``public_goods``,
create ``public_goods/templates/public_goods/Page.html``:

.. code-block:: html

    {% extends "global/Page.html" %}
    {% load otree %}

    {% block app_styles %}
        <style>
            ...
        </style>
    {% endblock %}

    {% block app_scripts %}
        <script>
            ...
        </script>
    {% endblock %}

Then make each template inherit from this template:

 .. code-block:: html

    {% extends "public_goods/Page.html" %}
    {% load otree %}
    ...

To include the same JS/CSS in *all apps* of a project,
modify ``_templates/global/Page.html``.
In that file, you will find the blocks ``global_scripts`` and ``global_styles``.

.. _staticfiles:

Static files
------------


Here is how to include images (or any other static file like .css, .js, etc.) in your pages.

At the root of your oTree project, there is a ``_static/`` folder.
Put a file there, for example ``puppy.jpg``.
Then, in your template, you can get the URL to that file with
``{% static 'puppy.jpg' %}``.

To display an image, use the ``<img>`` tag, like this:

.. code-block:: html

    <img src="{% static 'puppy.jpg' %}"/>

Above we saved our image in ``_static/puppy.jpg``,
But actually it's better to make a subfolder with the name of your app,
and save it as ``_static/your_app_name/puppy.jpg``, to keep files organized
and prevent name conflicts.

Then your HTML code becomes:

.. code-block:: html

    <img src="{% static "your_app_name/puppy.jpg" %}"/>

(If you prefer, you can also put static files inside your app folder,
in a subfolder called ``static/your_app_name``.)

If a static file is not updating even after you changed it,
this is because your browser cached the file. Do a full page reload
(usually Ctrl+F5)

If you have videos or high-resolution images,
it's preferable to store them somewhere online and reference them by URL
because the large file size can make uploading your
.otreezip file much slower.


Wait pages
----------

.. _customize_wait_page:

Custom wait page template
~~~~~~~~~~~~~~~~~~~~~~~~~

You can make a custom wait page template.
For example, save this to ``your_app_name/templates/your_app_name/MyWaitPage.html``:

.. code-block:: html

    {% extends 'otree/WaitPage.html' %}
    {% load otree %}
    {% block title %}{{ title_text }}{% endblock %}
    {% block content %}
        {{ body_text }}
        <p>
            My custom content here.
        </p>
    {% endblock %}

Then tell your wait page to use this template:

.. code-block:: python

    class MyWaitPage(WaitPage):
        template_name = 'your_app_name/MyWaitPage.html'

Then you can use ``vars_for_template`` in the usual way.
Actually, the ``body_text`` and ``title_text`` attributes
are just shorthand for setting ``vars_for_template``;
the following 2 code snippets are equivalent:

.. code-block:: python

    class MyWaitPage(WaitPage):
        body_text = "foo"

.. code-block:: python

    class MyWaitPage(WaitPage):

        @staticmethod
        def vars_for_template(player):
            return dict(body_text="foo")

If you want to apply your custom wait page template globally,
save it to ``_templates/global/WaitPage.html``.
oTree will then automatically use it everywhere instead of the built-in wait page.

CSS and JavaScript in Wait Pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wait pages have the same block structure as regular pages
(``global_scripts``, ``app_scripts``, ``scripts``, etc...),
so you can follow the same instructions described in :ref:`base-template`
and :ref:`selectors`.

For example, to apply CSS to your custom wait page at ``_templates/global/WaitPage.html``,
put a block ``global_scripts`` in the template.

You can even make other custom wait pages inherit from ``_templates/global/WaitPage.html``,
just the way regular pages inherit from ``_templates/global/Page.html``,
and they can define the blocks ``app_scripts`` and ``scripts``, etc.

.. _migrations:

Modifying an existing database
------------------------------

If your database already contains data and you want to update the structure
without running ``resetdb`` (which will delete existing data),
see `here <https://github.com/oTree-org/otree-docs/blob/f3c6ceca5346b988b194dad5f805a06814ebea68/source/misc/advanced.rst#modifying-an-existing-database>`__

Currency
--------

To customize the name "points" to something else like "tokens" or "credits",
set ``POINTS_CUSTOM_NAME``, e.g. ``POINTS_CUSTOM_NAME = 'tokens'``.

You can change the number of decimal places in real world currency amounts
with the setting ``REAL_WORLD_CURRENCY_DECIMAL_PLACES``.
If the extra decimal places show up but are always 0,
then you should reset the database.

Reading CSV or other files
--------------------------

Store yourfile.csv in your app folder.
Then put this code anywhere you want to read the file
(in a method or in Constants):

.. code-block:: python

    import csv
    with open('yourapp/yourfile.csv', encoding='utf-8') as file:
        rows = list(csv.DictReader(file))

If it's not CSV and you just want to read the file contents as a string,
this gets simplified to:

.. code-block:: python

    with open('yourapp/yourfile.txt', encoding='utf-8') as file:
        txt = file.read()
