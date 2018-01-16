Part 0: Simple survey
=====================

Let's create a simple survey -- on the first page, we ask the participant
for their name and age, then on the next page, display this info back to them.

Upgrade oTree
-------------

To ensure you are using the latest version of oTree, open your command window and run::

    pip3 install -U otree

Create the app
--------------

Use your command line to ``cd`` to the oTree project folder you created,
which contains ``requirements_base.txt``. Assuming you named the folder ``oTree``,
you would do::

    cd oTree

In this folder, create the public goods app::

    otree startapp my_simple_survey

Then in PyCharm, go to the folder ``my_simple_survey`` that was created.

Define models.py
----------------

Open ``models.py`` and scroll to the line that says ``class Player(BasePlayer):``.
Here we define the columns for the Player table in the database.
Let's add 2 fields:

-   ``name`` (which is a ``StringField``, meaning text characters)
-   ``age`` (which is a positive integer field)

.. code-block:: python

    class Player(BasePlayer):
        name = models.StringField()
        age = models.IntegerField()


Define the template
-------------------

This survey has 2 pages:

-  Page 1: players enter their name and age
-  Page 2: players see the data they entered on the previous page

In this section we will define the HTML templates that users see.

So, let's make 2 HTML files under ``templates/my_simple_survey/``.

Let's name the first page ``MyPage.html``, and put these contents inside:

.. code-block:: html+django

    {% extends "global/Page.html" %}
    {% load staticfiles otree %}

    {% block title %}
        Enter your information
    {% endblock %}

    {% block content %}

        {% formfield player.name label="Enter your name" %}

        {% formfield player.age label="Enter your age" %}

        {% next_button %}

    {% endblock %}

The second template will be called ``Results.html``.

.. code-block:: html+django

    {% extends "global/Page.html" %}
    {% load staticfiles otree %}

    {% block title %}
        Results
    {% endblock %}

    {% block content %}

        <p>Your name is {{ player.name }} and your age is {{ player.age }}.</p>

        {% next_button %}
    {% endblock %}


Define pages.py
---------------

Now we define our pages, which contain the logic for how to display the
HTML templates.

Since we have 2 templates, we need 2 ``Page`` classes in ``pages.py``.
The names should match those of the templates (``MyPage`` and
``Results``).

First let's define ``MyPage``. This page contains a form, so
we need to define ``form_model`` and ``form_fields``.
Specifically, this form should let you set the ``name`` and ``age`` fields
on the player.

.. code-block:: python

    class MyPage(Page):
        form_model = 'player'
        form_fields = ['name', 'age']

Now we define ``Results``. This page doesn't have a form so our class
definition can just say ``pass``.

.. code-block:: python

    class Results(Page):
        pass

If ``pages.py`` already has a ``WaitPage``, you can delete that,
because WaitPages are only necessary for multi-player games and more complex games.

Then, set your ``page_sequence`` to ``MyPage`` followed by ``Results``.
So, all in all, ``pages.py`` should contain this:

.. code-block:: python

    from otree.api import Currency as c, currency_range
    from . import models
    from ._builtin import Page, WaitPage
    from .models import Constants


    class MyPage(Page):
        form_model = 'player'
        form_fields = ['name', 'age']


    class Results(Page):
        pass


    page_sequence = [
        MyPage,
        Results
    ]


Define the session config in settings.py
----------------------------------------

Now we go to ``settings.py`` in the project's root folder and add an entry to ``SESSION_CONFIGS``.

.. code-block:: python

    SESSION_CONFIGS = [
        {
            'name': 'my_simple_survey',
            'display_name': "My Simple Survey",
            'num_demo_participants': 3,
            'app_sequence': ['my_simple_survey'],
        },
        # other session configs go here ...
    ]


Reset the database and run
--------------------------

Enter::

    otree resetdb
    otree runserver

Then open your browser to ``http://127.0.0.1:8000`` to try out the survey.


Fix any errors
--------------

If there is an error in your code, the command line will display a "traceback" (error message) that is formatted something like this::

    C:\oTree\chris> otree resetdb
    Traceback (most recent call last):
      File "C:\oTree\chris\manage.py", line 10, in <module>
        execute_from_command_line(sys.argv, script_file=__file__)
      File "c:\otree\core\otree\management\cli.py", line 170, in execute_from_command_line
        utility.execute()
      File "C:\oTree\venv\lib\site-packages\django\core\management\__init__.py", line 328, in execute
        django.setup()
      File "C:\oTree\venv\lib\site-packages\django\__init__.py", line 18, in setup
        apps.populate(settings.INSTALLED_APPS)
      File "C:\oTree\venv\lib\site-packages\django\apps\registry.py", line 108, in populate
        app_config.import_models(all_models)
      File "C:\oTree\venv\lib\site-packages\django\apps\config.py", line 198, in import_models
        self.models_module = import_module(models_module_name)
      File "C:\Python27\Lib\importlib\__init__.py", line 37, in import_module
        __import__(name)
      File "C:\oTree\chris\public_goods_simple\models.py", line 40
        self.total_contribution = sum([p.contribution for p in self.get_players()])
           ^
    IndentationError: expected an indented block


Your first step should be to look at the last lines of the message.
Specifically, find the file and line number of the last entry.
In the above example, it's ``"C:\oTree\chris\public_goods_simple\models.py", line 40``.
Open that file and go to that line number to see if there is a problem there.
Specifically, look for the problem mentioned at the last line of the traceback.
In this example, it is ``IndentationError: expected an indented block``
(which indicates that the problem has to do with code indentation).
Python editors like PyCharm usually underline errors in red to make them easier to find.
Try to fix the error then run the command again.

Sometimes the last line of the traceback refers to a file that is not part of your code.
For example, in the below traceback, the last line refers to ``/site-packages/easymoney.py``,
which is not part of my app, but rather an external package::

    Traceback:
    File "/usr/local/lib/python3.5/site-packages/django/core/handlers/base.py" in get_response
      132.                     response = wrapped_callback(request, *callback_args, **callback_kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/pages/generic/base.py" in view
      71.             return self.dispatch(request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/utils/decorators.py" in _wrapper
      34.             return bound_func(*args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/pages/decorators/cache.py" in _wrapped_view_func
      57.         response = view_func(request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/utils/decorators.py" in bound_func
      30.                 return func.__get__(self, type(self))(*args2, **kwargs2)
    File "/usr/local/lib/python3.5/site-packages/django/utils/decorators.py" in _wrapper
      34.             return bound_func(*args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/pages/decorators/cache.py" in _cache_controlled
      43.             response = viewfunc(request, *args, **kw)
    File "/usr/local/lib/python3.5/site-packages/django/utils/decorators.py" in bound_func
      30.                 return func.__get__(self, type(self))(*args2, **kwargs2)
    File "/usr/local/lib/python3.5/site-packages/otree/pages/abstract.py" in dispatch
      315.                 request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/django/pages/generic/base.py" in dispatch
      89.         return handler(request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/otree/pages/abstract.py" in get
      814.         return super(FormPageMixin, self).get(request, *args, **kwargs)
    File "/usr/local/lib/python3.5/site-packages/vanilla/model_views.py" in get
      294.         context = self.get_context_data(form=form)
    File "/usr/local/lib/python3.5/site-packages/otree/pages/abstract.py" in get_context_data
      193.         vars_for_template = self.resolve_vars_for_template()
    File "/usr/local/lib/python3.5/site-packages/otree/pages/abstract.py" in resolve_vars_for_template
      212.         context.update(self.vars_for_template() or {})
    File "/Users/chris/oTree/public_goods/pages.py" in vars_for_template
      108.             'total_payoff': self.player.payoff + Constants.fixed_pay}
    File "/usr/local/lib/python3.5/site-packages/easymoney.py" in <lambda>
      36.     return lambda self, other, context=None: self.__class__(method(self, _to_decimal(other)))
    File "/usr/local/lib/python3.5/site-packages/easymoney.py" in _to_decimal
      24.         return Decimal(amount)

    Exception Type: TypeError at /p/j0p7dxqo/public_goods/ResultsFinal/8/
    Exception Value: conversion from NoneType to Decimal is not supported

In these situations, look to see if any of your code is contained in the traceback.
Above we can see that the traceback goes through the file ``/Users/chris/oTree/public_goods/pages.py``,
which is part of my project. The bug is on line 108, as indicated.

If you can't figure out the cause of the error,
you can ask a question on the oTree
`discussion group <https://groups.google.com/forum/#!forum/otree>`__.
