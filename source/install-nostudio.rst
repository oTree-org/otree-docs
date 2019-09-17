:orphan:

.. _install-nostudio:

oTree Setup (text editor)
=========================

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

Install a text editor
---------------------

Install a text editor like `PyCharm <https://www.jetbrains.com/pycharm/download/>`__
or `Visual Studio Code <https://code.visualstudio.com/>`__
which you will use for editing your Python files.
You can find up-to-date instructions on installing those editors on their websites.
Then launch the text editor and open your entire project folder.

.. _upgrade:
.. _upgrade-otree-core:

Upgrading/reinstalling oTree
----------------------------

We recommend upgrading every couple of weeks.
It's the same command:

.. code-block:: bash

    pip3 install -U otree

