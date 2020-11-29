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

.. code-block:: html+django

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

 .. code-block:: html+django

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

.. code-block:: HTML+django

    <img src="{% static 'puppy.jpg' %}"/>

Above we saved our image in ``_static/puppy.jpg``,
But actually it's better to make a subfolder with the name of your app,
and save it as ``_static/your_app_name/puppy.jpg``, to keep files organized
and prevent name conflicts.

Then your HTML code becomes:

.. code-block:: HTML+django

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

.. code-block:: html+django

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
        def vars_for_template(self):
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

This section is more advanced and is for people who are comfortable with troubleshooting.

If your database already contains data and you want to update the structure
without running ``resetdb`` (which will delete existing data), you can use Django's migrations feature.
Below is a quick summary; for full info see the Django docs `here <https://docs.djangoproject.com/en/2.2/topics/migrations/#workflow>`__.

Importantly, these first steps have to be taken before you add any new fields to your database. If you have already added variables to your ``models.py`` files, comment them out before starting this process.

First, add an empty file ``otree_core_migrations/__init__.py``
in your project top-level folder.

Then, add the following line to settings.py::

    MIGRATION_MODULES = {'otree': 'otree_core_migrations'}

Then run::

    python manage.py makemigrations otree

Then run ``python manage.py makemigrations my_app_name`` (substituting your app's name),
for each app you are working on. This will create a ``migrations`` folder in your app.
Add this as well as the ``otree_core_migrations/__init__.py`` to your git repo, commit, and push to your server.

Instead of using ``otree resetdb`` on the server, run ``python manage.py migrate --fake`` (or ``otree migrate --fake``).
If using Heroku, you would do ``heroku run otree migrate --fake``.
This tells django to add these migrations to the list of applied migrations. Since nothing in your database has changed so far, it should not try to actually apply them however, hence the ``--fake``.

You can now make your database relevant changes locally (or uncomment the fields). Once you're done, run ``otree makemigrations`` again. The console output should reflect the changes you have made. A new migrations file will appear in your apps migrations folder. Again, add this to git, commit and push.

Now, on the server, you can run ``otree migrate your_app_name``.
This will update your database tables.

If you make further modifications to your apps or upgrade otree, you can run
``python manage.py makemigrations``. You don't need to specify the app names in this command;
migrations will be updated for every app that has a ``migrations`` folder.
Then commit, push, and run ``python manage.py migrate`` again as described above.

The migration files build on each other which means you should not delete your local copies of the files from the git repo as django might otherwise be unable to detect what has changed.

More info `here <https://docs.djangoproject.com/en/2.2/topics/migrations/#workflow>`__

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

Store yourfile.csv in your app, next to models.py.
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

You can also use the pathlib module to read files.