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
