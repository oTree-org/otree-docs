.. _setup:

Download & Setup
================

Prerequisite: Python 2.7 (not 3.x)
----------------------------------

Windows
~~~~~~~

*   On Windows: download and install
    `Python 2.7 <https://www.python.org/downloads/>`__. (oTree does not work with Python 3.)
    Then add Python to
    your ``Path`` environment variable:

    *   Open the Windows Start menu
    *   Search for "Edit the system environment variables", and then click it.
    *   Click ``Environment Variables``
    *   Select ``Path`` in the ``System variables`` section
    *   Click ``Edit``
    *   Add ``;C:\Python27;C:\Python27\Scripts`` to the end of the list
        (the paths are separated by semicolons). For example:
        ``C:\Windows;C:\Windows\System32;C:\Python27;C:\Python27\Scripts``
    *   (This assumes that Python was installed to ``C:\Python27``.)

Verify that it worked by opening your command prompt and
entering ``python``. You should see the "``>>>``" prompt.


Mac OSX
~~~~~~~

These instructions are for installing Python through Homebrew, which is our recommended method.
(Other ways are possible also.)

Open your Terminal and run:

.. code-block:: bash

    xcode-select --install

You will then be asked whether you want to install "Xcode" or the "command line developer tools".
Select just "command line developer tools".

Then install Homebrew:

.. code-block:: bash

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Then use Homebrew to install Python:

.. code-block:: bash

    brew install python

Verify that it worked by opening your command prompt and
entering ``python``. You should see the "``>>>``" prompt.

Linux/UNIX
~~~~~~~~~~

If Python is not already installed, use your system's package manager to install Python and pip.


oTree installation
~~~~~~~~~~~~~~~~~~

*   Download `oTree <https://github.com/oTree-org/oTree/archive/master.zip>`__
    and unzip it to a convenient location (such as your "Documents" folder).
*   In your command line, go to the root directory of the unzipped folder
    where ``requirements_base.txt`` is

    .. note::

        if you cannot find ``requirements_base.txt``
        make sure you have downloaded ``oTree-master.zip``, not
        ``otree-launcher-master.zip``, which is a different download.

*   Run this:

.. code-block:: bash

    $ pip install -r requirements_base.txt

If you get a permissions error, you can add the ``--user`` flag to install inside your home directory:

.. code-block:: bash

    $ pip install -r requirements_base.txt --user

Then run:

.. code-block:: bash

    $ otree resetdb
    $ otree runserver

Then open your browser to ``http://127.0.0.1:8000/``.


Explanation: oTree & Django
---------------------------

oTree is built on top of Django.

The ``oTree`` folder is a Django project, as explained
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

.. _upgrade:

Upgrading/reinstalling oTree
----------------------------

The oTree software has two components:

-  oTree-core: The engine that makes your apps run
-  oTree library: the folder of sample games and other files (e.g. settings.py) that you download from `here <https://github.com/oTree-org/oTree>`__ and customize to build your own project.

You can either upgrade these components individually,
or do a complete reinstallation to upgrade all of them at once.

These components are being updated regularly,
but oTree-core is updated the most frequently, and contains the most important bugfixes.
So, we recommend updating it the most frequently.

However, if you originally installed oTree over 2 months ago,
we recommend a complete reinstallation,
to get all the latest features and bug fixes.

.. _upgrade-otree-core:

Upgrade oTree core libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We recommend you do this on a weekly basis,
so that you can get the latest bug fixes and features.
This will also ensure that you are using a version that is consistent with the current documentation.

Run:

.. code-block:: bash

    pip install --upgrade otree-core

If you are using the launcher, click "Upgrade otree-core" (or "Version select").
Then select the most recent version in the menu.

