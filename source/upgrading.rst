Upgrading/reinstalling oTree
============================

There are several alternatives for upgrading or reinstalling oTree.

(TODO: when to use which)

From-scratch reinstallation
---------------------------

-  On Windows: Browse to ``%APPDATA%`` and delete the folder
   ``otree-launcher``
-  On Mac/Linux: Delete the folder ``~/.otree-launcher``
-  Re-download the launcher according to the instructions on
   http://www.otree.org/download/

In-place upgrade
----------------

Start the launcher and click the "terminal" button to get your console.
Then type:

.. code-block:: bash

    $ git pull https://github.com/oTree-org/oTree.git master
    $ pip install -r requirements_base.txt
    $ python otree resetdb

Note: you may get merge conflicts if you have modified many files.

Upgrade oTree core libraries (minimal option)
---------------------------------------------

Start the launcher and click the "terminal" button to get your console.
Then type:

Modify ``otree-core`` version number in ``requirements_base.txt`` (the
latest version is
`here <https://github.com/oTree-org/oTree/blob/master/requirements_base.txt>`__),
then run:

.. code-block:: bash

    $ pip install -r requirements_base.txt
