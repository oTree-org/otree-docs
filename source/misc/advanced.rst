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

.. _migrations:

Modifying an existing database
------------------------------

This section is more advanced and is for people who are comfortable with troubleshooting.

If your database already contains data and you want to update the structure
without running ``resetdb`` (which will delete existing data), you can use Django's migrations feature.
Below is a quick summary; for full info see the Django docs `here <https://docs.djangoproject.com/en/1.9/topics/migrations/#workflow>`__.

First, add an empty file ``otree_core_migrations/__init__.py``
in your project top-level folder.

Then, add the following line to settings.py::

    MIGRATION_MODULES = {'otree': 'otree_core_migrations'}

Then run::

    python manage.py makemigrations otree

Then run ``python manage.py makemigrations my_app_name`` (substituting your app's name),
for each app you are working on. This will create a ``migrations`` folder in your app,
which you should add to your git repo, commit, and push to your server.

Instead of using ``otree resetdb`` on the server, run ``python manage.py migrate`` (or ``otree migrate``).
If using Heroku, you would do ``heroku run otree migrate``.
This will update your database tables.

If you make further modifications to your apps or upgrade otree, you can run
``python manage.py makemigrations``. You don't need to specify the app names in this command;
migrations will be updated for every app that has a ``migrations`` folder.
Then commit, push, and run ``python manage.py migrate`` again as described above.

More info `here <https://docs.djangoproject.com/en/1.9/topics/migrations/#workflow>`__
