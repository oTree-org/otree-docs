:orphan:

.. _install-macos:

Installing oTree on macOS
=========================

Important note
--------------

If you publish research conducted using oTree,
you are required by the oTree license to cite
`this paper <http://dx.doi.org/10.1016/j.jbef.2015.12.001>`__.
(Citation: Chen, D.L., Schonger, M., Wickens, C., 2016. oTree - An open-source
platform for laboratory, online and field experiments.
Journal of Behavioral and Experimental Finance, vol 9: 88-97)

If the below steps don't work for you, please email chris@otree.org with details.

Step 1: Install Python
----------------------

*   Download and install the latest `Python <https://www.python.org/ftp/python/3.6.4/python-3.6.4-macosx10.6.pkg>`__.

*   In Finder, search for and open the "Terminal" app:

.. figure:: _static/setup/macos-terminal.png

*   Enter::

    /Applications/Python\ 3.6/Install\ Certificates.command


Step 2: Install oTree
---------------------

Enter this:

.. code-block:: bash

    pip3 install -U otree


Step 3: Run oTree
-----------------

Create your project folder::

    otree startproject oTree

When it asks you "Include sample games?" choose yes.

Move into the folder you just created::

    cd oTree

Run the server::

    otree devserver

Open your browser to `http://localhost:8000/ <http://localhost:8000/>`__.
You should see the oTree demo site.

To stop the server, press ``Control + C`` at your command line.


Step 4: Install a Python editor (PyCharm)
-----------------------------------------

Install `PyCharm <https://www.jetbrains.com/pycharm/download/>`__,
which you will use for editing your Python files.

After installing, open PyCharm, go to "File -> Open..." and select your project folder.

Then click on ``PyCharm -> Preferences``,
and click through the following steps:

-   "Project -> Project interpreter"
-   Click the "gear" icon
-   Add...
-   System Interpreter

And set it to the location of your Python executable,
something like:
``/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6``).
Once it's configured, the imports at the top of an app's ``models.py`` should look
like
`this <_static/setup/pycharm-correct.png>`__
, not
`this <_static/setup/pycharm-incorrect.png>`__.


If PyCharm displays this warning, select "Ignore requirements":

.. figure:: _static/setup/pycharm-psycopg2-warning.png

PyCharm's autocompletion makes learning oTree much easier:

.. figure:: _static/setup/pycharm-autocomplete.gif


Upgrading/reinstalling oTree
----------------------------

We recommend you upgrade on a weekly basis,
so that you can get the latest bug fixes and features.
This will also ensure that you are using a version that is consistent with the current documentation.

The command to upgrade is the same as the command to install:

.. code-block:: bash

    pip3 install -U otree

If there is a problem with the upgrade, uninstall then reinstall:

    pip3 uninstall otree
    pip3 install -U otree