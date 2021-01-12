:orphan:

.. _install-nostudio:

oTree Setup (text editor)
=========================

Note: it's recommended to use `oTree Studio <https://www.otreehub.com/studio>`__
since it is specifically designed for building oTree apps.
You can easily switch to using a text editor later, by downloading your code.

.. note::

    You should first install oTree for
    :ref:`Windows <install-windows>` or
    :ref:`Mac <install-macos>`.

Run oTree
---------

If you're on MacOS, run::

    /Applications/Python\ 3.8/Install\ Certificates.command

(If you are not using version 3.8 of Python, edit the above command appropriately.)

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

Install a text editor
---------------------

Install a text editor like `PyCharm <https://www.jetbrains.com/pycharm/download/>`__
for editing your Python files.
See the PyCharm documentation on how to configure your interpreter so that you get
code completion.

Then launch the text editor and open your entire project folder.

.. _upgrade:
.. _upgrade-otree-core:

Upgrading/reinstalling oTree
----------------------------

We recommend upgrading every couple of weeks.
It's the same command:

.. code-block:: bash

    pip3 install -U otree

The best way to ensure that your apps continue to work after you upgrade is to
use only the functions described in this documentation.
Some code snippets you may find online were written by people who access oTree's internal functions
and "hack" them to do something different.
Although these snippets can enable some innovative new functionality,
be aware that they increase the chance of things breaking when you upgrade.
Because oTree's internal code layout changes from release to release.

For similar reasons, we also caution about directly using Django functionality,
apart from the few components linked in this documentation
(such as Django templates).
