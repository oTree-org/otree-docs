oTree & Django
--------------

``otree`` command
~~~~~~~~~~~~~~~~~

The ``otree`` command is a customized version of Django's ``manage.py``.

For example, ``otree runserver`` is basically equivalent to ``python manage.py runserver``.

In addition to the built-in `Django management commands <https://docs.djangoproject.com/en/1.9/ref/django-admin/>`__ like ``runserver`` and ``startapp``,
oTree defines a few extra ones like ``resetdb``, ``create_session``, and ``runprodserver``.

For the list of available commands, enter ``otree help``.
For information about a specific command, enter ``otree help [command]``, e.g. ``otree help test``.

Project folder
~~~~~~~~~~~~~~

The folder containing your games is a Django project, as explained
`here <https://docs.djangoproject.com/en/1.8/intro/tutorial01/#creating-a-project>`__.

It comes pre-configured with all the files,
settings and dependencies so that it works right away.
You should create your apps inside this folder.

If you want, you can delete all the existing example games
(like ``asset_market``, ``bargaining``, etc).
Just delete the folders and the corresponding entries in ``SESSION_CONFIGS``.
Just keep the directories ``_static`` and ``_templates``.

When you install oTree (either using the launcher or running
``pip install -r requirements_base.txt``),
``otree-core`` gets automatically installed as a dependency.

Differences between oTree and Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Models
^^^^^^

-  Field labels should go in the template formfield, rather than the
   model field's ``verbose_name``.
-  ``null=True`` and ``default=None`` are not necessary in your model
   field declarations; in oTree fields are null by default.
-  On ``CharField``\ s, ``max_length`` is not required.
