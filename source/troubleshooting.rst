Troubleshooting
===============

Common errors
~~~~~~~~~~~~~

Python not installed
--------------------

.. code-block:: bash

    'python' is not recognized as an internal or external command, operable
    program or batch file.

Solution: make sure Python 2.7 is installed and add it to your ``Path``.


otree: command not found
------------------------

If you are using the launcher, click the "Terminal" button. This will ensure your terminal opens with the correct programs loaded.
Also, if you are using a version of ``otree-core`` older than 0.3.20, you need to upgrade (see :ref:`upgrade-otree-core`).


'with' in formfield tag needs at least one keyword argument
-----------------------------------------------------------

.. code-block:: bash

    django.template.base.TemplateSyntaxError: 'with' in formfield tag needs at least one keyword argument.

This is usually caused by a `formfield` tag with a space after `label`, e.g.:

.. code-block:: html+django

    {% formfield player.contribution with label = "How much will you contribute?" %}

You should remove the space around the ``=`` like this:

.. code-block:: html+django

    {% formfield player.contribution with label="How much will you contribute?" %}


TypeError: can only concatenate list (not "tuple") to list
----------------------------------------------------------

You can fix this problem by upgrading otree-core to the latest version (see :ref:`upgrade-otree-core`)
