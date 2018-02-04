Troubleshooting
===============

.. _traceback:

How to read a traceback
-----------------------

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

Error pages
-----------

If the error occurs when you are loading a page,
you will instead see the error in a yellow Django error page:

.. figure:: ../_static/yellow-error-page.png

The section "Traceback" shows the same type of traceback as described above,
just with some special formatting; you can troubleshoot it the same way as described above
(e.g. look at the last line, particularly the lines highlighted in dark gray).

If you can't figure out the error message,
you can send it to the oTree `mailing list <https://groups.google.com/forum/#!forum/otree>`__.
It's best to use to "copy and paste view" to get the raw traceback,
which is more useful than sending a screenshot of the yellow page.

.. _print_debugging:

Debugging with print statements
-------------------------------

If your code is not behaving properly,
you can isolate the problem using ``print()``
just as you would to debug any Python program.
For example, you could add some print statements to your payoff function:

.. code-block:: python

      print('@@@@@@participant.vars is', self.participant.vars)

The output will be displayed in the console window where you ran ``otree devserver``
(not in your web browser).

Debugging with PyCharm
----------------------

PyCharm has an excellent debugger that you might want to try using.
You can insert a breakpoint into your code by clicking in the left-hand
margin on a line of code. You will see a little red dot. Then reload the
page and the debugger will pause when it hits your line of code. At this
point you can inspect the state of all the local variables, execute
print statements in the built-in intepreter, and step through the code
line by line.

More on the PyCharm debugger
`here <http://www.jetbrains.com/pycharm/webhelp/debugging.html>`__.

Debugging in the command shell
------------------------------

To test your app from an interactive Python shell, do:

.. code-block:: shell

   $ otree shell

Then you can debug your code and inspect objects in your database.
For example, if you already ran a "public goods game" session in your browser,
you can access the database objects in Python like this:

.. code-block:: python

   >>> from public_goods.models import Player
   >>> players = Player.objects.all()
   >>> ...

