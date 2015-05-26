Setup
=====

See the installation instructions
`here <http://www.otree.org/download/>`__.

Or, clone this repo and run:

.. code-block:: bash

    $ pip install -r requirements_base.txt
    $ python otree resetdb
    $ python otree runserver

You should see the following output on the command line:

.. code-block:: bash

    Validating models...

    0 errors found
    |today| - 15:50:53
    Django version |version|, using settings 'settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Now that the server's running, visit ``http://127.0.0.1:8000/`` with
your Web browser.


PyCharm
-------

To ease the learning curve of oTree, we strongly recommend using
`PyCharm Professional <http://www.jetbrains.com/pycharm/>`__, even
though there are many other good editors for Python code. This is
because:

-  PyCharm has features that make oTree/Django development easier
-  oTree has special integration with PyCharm's code completion
   functionality
-  This documentation gives instructions assuming you are using PyCharm
-  oTree has been thoroughly tested with PyCharm

If you are a student, teacher, or professor, PyCharm Professional is
`free <https://www.jetbrains.com/student/>`__. Note: we recommend
PyCharm Professional rather than PyCharm Community Edition.
