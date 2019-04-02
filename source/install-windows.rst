:orphan:


.. _install-windows:

Installing oTree on Windows
===========================

.. note::

    If you want to try the beta of oTree Studio, which is a simplified graphical interface
    for creating oTree apps, sign up on `oTree Hub <https://www.otreehub.com/>`__
    and click the link "Studio" in the upper right corner of the page.
    (Heroku sign up is not necessary.)

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

Download and install `Python 3.6 <https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe>`__.
Check the box to add Python to PATH:

.. figure:: _static/setup/py-win-installer.png

Step 2: Install oTree
---------------------

Go to the folder where you want to create your oTree project.
Then click the "File" menu and open PowerShell:

.. figure:: _static/setup/open-powershell.png

Enter this command at the prompt:

.. code-block:: bash

    pip3 install -U otree

.. note::

    If you get an error like this::

        error: Microsoft Visual C++ is required (Unable to find vcvarsall.bat).

    To fix this, install the `Visual C++ Build Tools <http://go.microsoft.com/fwlink/?LinkId=691126>`__.


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

.. _pycharm:

Step 4: Install PyCharm
-----------------------

Install `PyCharm <https://www.jetbrains.com/pycharm/download/>`__,
which you will use for editing your Python files.

After installing, open PyCharm, go to "File -> Open..." and select your project folder
(It's usually ``C:\Users\<your_username>\oTree``).

Then click ``File –> Settings``
and click through the following steps:

-   "Project -> Project interpreter"
-   Click the "gear" icon
-   Add...
-   System Interpreter

And set it to the location of your Python executable,
which you can get in your command prompt by entering ``powershell -command "get-command python"``.
Usually it is
``C:\Program Files\Python36-64\python.exe``
or
``C:\Users\<your_username>\AppData\Local\Programs\Python\Python36-64\python.exe``.
Once it's configured, the imports at the top of an app's ``models.py`` should look
like
`this <_static/setup/pycharm-correct.png>`__
, not
`this <_static/setup/pycharm-incorrect.png>`__.


If PyCharm displays this warning, select "Ignore requirements":

.. figure:: _static/setup/pycharm-psycopg2-warning.png


Note: Even if you normally use another text editor,
we recommend at least trying PyCharm, because PyCharm's autocompletion
makes learning oTree much easier:

.. figure:: _static/setup/pycharm-autocomplete.gif


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