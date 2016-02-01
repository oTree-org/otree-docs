.. _setup:

Download & Setup
================

Command line basics
-------------------

To use oTree, you need to use PowerShell (Windows) or Terminal (Mac).
In this documentation, we refer to these programs as your "command prompt" or "command line".
Sometimes, we write a command prefixed with a ``$`` like this::

    $ otree resetdb

The ``$`` is not part of the command. You should copy the command (in this example, ``otree resetdb``),
and then paste it at your command line. (In PowerShell, you should right-click to paste.)

A few tips:

* You can retrieve the previous command you entered by pressing your keyboard's "up" arrow
* If you get stuck running a command, you can press ``Control + C``.

Prerequisite: Python 2.7 (not 3.x)
----------------------------------

Install Python (Windows)
~~~~~~~~~~~~~~~~~~~~~~~~

* Download and install `Python 2.7 <https://www.python.org/downloads/release/python-2711/>`__. (oTree does not work with Python 3.)

  You need to adjust ``PATH`` environment variable to include paths to
  the Python executable and additional scripts. Open PowerShell and run this command (right-click to paste it)::

      c:\python27\python.exe c:\python27\tools\scripts\win_add2path.py

  Close the command prompt window and reopen it so changes take effect, run the
  following command::

      pip

It should list the available commands, like ``install`` and ``uninstall``.
If you instead get an error "command not found",
you should restart your computer and retry.


Install Python (Mac OSX)
~~~~~~~~~~~~~~~~~~~~~~~~

Although Mac OSX comes pre-installed with Python, we recommend not using the pre-installed Python,
and instead installing Python through Homebrew.

* Open your Terminal and run:

.. code-block:: bash

    xcode-select --install

When prompted, select to install the "command line developer tools".

* Then install `Homebrew <http://brew.sh/>`__:

.. code-block:: bash

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

* Update your ``PATH`` variable to state that homebrew packages should be
  used before system packages::

    echo "export PATH=/usr/local/bin:/usr/local/sbin:\$PATH" >> ~/.bash_profile

* Reload ``.bash_profile`` to ensure the changes have taken place::

    source ~/.bash_profile

* Install python::

    brew install python

* Then test that it worked::

    pip

* It should list the available commands, like ``install`` and ``uninstall``.


Linux/UNIX
~~~~~~~~~~

If Python is not already installed, use your system's package manager to install Python and pip.


oTree installation
~~~~~~~~~~~~~~~~~~

*   Open PowerShell (on Windows) or Terminal (on Mac OS X), and ``cd`` to the directory where you want to store your oTree code (such as ``Documents``).
*   Run this:

.. code-block:: bash

    pip install --upgrade otree-core
    otree startproject oTree

(If it's your first time, we recommend choosing the option to include the sample games.)

.. note::

    If you get a message like ``pip: command not found``, you need to download and run `get-pip.py <https://bootstrap.pypa.io/get-pip.py>`__.

Then change to the directory you just created:

.. code-block:: bash

    cd oTree

Then run:

.. code-block:: bash

    otree resetdb
    otree runserver

Then open your browser to `http://127.0.0.1:8000/ <http://127.0.0.1:8000/>`__.

.. _pycharm:

Installing a Python editor (PyCharm)
------------------------------------

You should install a text editor for writing your Python code.

We recommend using `PyCharm <https://www.jetbrains.com/pycharm/download/>`__.
Professional Editon is better than Community Edition because it has Django support.
PyCharm Professional is free if you are a student, teacher, or professor.

If you prefer another editor like Notepad++, TextWrangler, or Sublime Text, you can use that instead.

.. _upgrade:

Upgrading/reinstalling oTree
----------------------------

The oTree software has two components:

-  oTree-core: The engine that makes your apps run
-  oTree library: the folder of sample games and other files (e.g. settings.py) that you download from `here <https://github.com/oTree-org/oTree>`__ and customize to build your own project.

.. _upgrade-otree-core:

Upgrade oTree core
~~~~~~~~~~~~~~~~~~

We recommend you do this on a weekly basis,
so that you can get the latest bug fixes and features.
This will also ensure that you are using a version that is consistent with the current documentation.

Run:

.. code-block:: bash

    pip install --upgrade otree-core

If you are using the launcher, click "Upgrade otree-core" (or "Version select").
Then select the most recent version in the menu.

Upgrade oTree library
~~~~~~~~~~~~~~~~~~~~~

Run ``otree startproject [folder name]``. This will create a folder with the specified name and
download the latest version of the library there.

If you originally installed oTree over 2 months ago,
we recommend you run the above command and move your existing apps into the new project folder,
to ensure you have the latest ``settings.py``, etc.
