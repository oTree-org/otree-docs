Troubleshooting
===============

How to read a traceback
-----------------------

If there is an error in your code, the command line will display a "traceback" (error message) that is formatted something like this::

    C:\oTree\lyon> otree resetdb
    Traceback (most recent call last):
      File "C:\oTree\lyon\manage.py", line 10, in <module>
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
      File "C:\oTree\lyon\public_goods_simple\models.py", line 40
        self.total_contribution = sum([p.contribution for p in self.get_players()])
           ^
    IndentationError: expected an indented block


Your first step should be to look at the last lines of the message.
Specifically, find the file and line number of the last entry.
In the above example, it's ``"C:\oTree\lyon\public_goods_simple\models.py", line 40``.
Open that file and go to that line number to see if there is a problem there.
Specifically, look for the problem mentioned at the last line of the traceback.
In this example, it is ``IndentationError: expected an indented block``
(which indicates that the problem has to do with code indentation).
Python editors like PyCharm usually underline errors in red to make them easier to find.
Try to fix the error then run the command again.

Error pages
-----------

If the error occurs when you are loading a page,
you will instead see the error in a yellow Django error page:

.. figure:: _static/yellow-error-page.png

The section "Traceback" shows the same type of traceback as described above,
just with some special formatting; you can troubleshoot it the same way as described above
(e.g. look at the last line, particularly the lines highlighted in dark gray).

If you can't figure out the error message,
you can send it to the oTree `mailing list <https://groups.google.com/forum/#!forum/otree>`__.
It's best to use to "copy and paste view" to get the raw traceback,
which is more useful than sending a screenshot of the yellow page.

