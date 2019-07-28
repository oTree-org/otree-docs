.. _server_final_steps:

Server deployment: final steps
==============================

Look at your server check
-------------------------

In the oTree admin interface, click "Server Check" in the header bar.


Testing with browser bots
-------------------------

Before launching a study, it's advisable to test your apps with bots,
especially browser bots. See the section :ref:`bots`.

.. _sentry:

Sentry service
--------------

As of 2018-11-20,
our Sentry service has been replaced by the much more comprehensive
`oTree Hub <https://www.otreehub.com/>`__, which includes automatic Sentry
setup. Currently, oTree Hub is for Heroku only.


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
