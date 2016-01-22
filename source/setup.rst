.. _setup:

Download & Setup
================

Prerequisite: Python 2.7 (not 3.x)
----------------------------------

Windows
~~~~~~~

* Download and install `Python 2.7 <https://www.python.org/downloads/>`__. (oTree does not work with Python 3.)

  You need to adjust ``PATH`` environment variable to include paths to
  the Python executable and additional scripts. The following paths need to be
  added to ``PATH``::

      C:\Python27\;C:\Python27\Scripts\;

  To update the ``PATH`` open a Command prompt and run::

      c:\python27\python.exe c:\python27\tools\scripts\win_add2path.py

  Close the command prompt window and reopen it so changes take effect, run the
  following command and check it shows the expected Python version::

      python --version



Mac OSX
~~~~~~~

These instructions are for installing Python through Homebrew, which is our recommended method.
(Other ways are possible also.)

* Open your Terminal and run:

.. code-block:: bash

    xcode-select --install

You will then be asked whether you want to install "Xcode" or the "command line developer tools".
Select just "command line developer tools".

* Then install `Homebrew <http://brew.sh/>`__:

.. code-block:: bash

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

* Update your ``PATH`` variable to state that homebrew packages should be
  used before system packages (Change ``.bashrc`` to ``.zshrc`` accordantly
  if you're using `zsh`_ as default shell)::

    echo "export PATH=/usr/local/bin:/usr/local/sbin:$PATH" >> ~/.bashrc

* Reload ``.bashrc`` to ensure the changes have taken place::

    source ~/.bashrc

* Install python::

    brew install python


Linux/UNIX
~~~~~~~~~~

If Python is not already installed, use your system's package manager to install Python and pip.


oTree installation
~~~~~~~~~~~~~~~~~~

*   In your command line, go to the directory where you want to store your oTree code (such as your "Documents" folder).
*   Run this:

.. code-block:: bash

    $ pip install --upgrade otree-core
    $ otree startproject oTree

(If it's your first time, we recommend choosing the option to include the sample games.)

Then run:

.. code-block:: bash

    $ otree resetdb
    $ otree runserver

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
