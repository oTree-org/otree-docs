:orphan:

.. _install-nostudio:

oTree Setup (for PyCharm users)
===============================

.. note::

    You should first install oTree for
    :ref:`Windows <install-windows>` or
    :ref:`Mac <install-macos>`.

Run oTree
---------

If you're on MacOS, run::

    /Applications/Python\ 3.7/Install\ Certificates.command

(If you are not using version 3.7 of Python, edit the above command appropriately.)

From your command prompt, create your project folder::

    otree startproject oTree

When it asks you "Include sample games?" choose yes.

Move into the folder you just created::

    cd oTree

Run the server::

    otree devserver

Open your browser to `http://localhost:8000/ <http://localhost:8000/>`__.
You should see the oTree demo site.

To stop the server, press ``Control + C`` at your command line.

.. _pycharm:

Install PyCharm
---------------

Install `PyCharm <https://www.jetbrains.com/pycharm/download/>`__,
which you will use for editing your Python files.
PyCharm's autocompletion makes learning oTree easier:

.. figure:: _static/setup/pycharm-autocomplete.gif

PyCharm configuration (for Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After installing, open PyCharm, go to "File -> Open..." and select your project folder
(It's usually ``C:\Users\<your_username>\oTree``).

Then click ``File –> Settings`` (on MacOS: ``PyCharm -> Preferences``)
and click through the following steps:

-   "Project -> Project interpreter"
-   Click the "gear" icon
-   Add...
-   System Interpreter

And set it to the location of your Python executable,
which you can get in your command prompt by entering ``powershell -command "get-command python"``.
Usually it is
``C:\Program Files\Python37-64\python.exe``
or
``C:\Users\<your_username>\AppData\Local\Programs\Python\Python37-64\python.exe``.

Once it's configured, the imports at the top of an app's ``models.py`` should look
like
`this <_static/setup/pycharm-correct.png>`__
, not
`this <_static/setup/pycharm-incorrect.png>`__.

If PyCharm displays this warning, select "Ignore requirements":

.. figure:: _static/setup/pycharm-psycopg2-warning.png


PyCharm configuration (for MacOS)
---------------------------------

After installing, open PyCharm, go to "File -> Open..." and select your project folder.

Then click on ``PyCharm -> Preferences``,
and click through the following steps:

-   "Project -> Project interpreter"
-   Click the "gear" icon
-   Add...
-   System Interpreter

And set it to the location of your Python executable,
something like:
``/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7``).
Once it's configured, the imports at the top of an app's ``models.py`` should look
like
`this <_static/setup/pycharm-correct.png>`__
, not
`this <_static/setup/pycharm-incorrect.png>`__.


If PyCharm displays this warning, select "Ignore requirements":

.. figure:: _static/setup/pycharm-psycopg2-warning.png


.. _upgrade:
.. _upgrade-otree-core:

Upgrading/reinstalling oTree
----------------------------

We recommend you upgrade on a weekly basis,
so that you can get the latest bug fixes and features.
This will also ensure that you are using a version that is consistent with the current documentation.

The command to upgrade is the same as the command to install:

.. code-block:: bash

    pip3 install -U otree

If there is a problem with the upgrade, uninstall then reinstall::

    pip3 uninstall otree
    pip3 install -U otree
