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

TemplateEncodingError
---------------------

If you get this error:

.. code-block:: bash

    TemplateEncodingError: Templates can only be constructed from unicode or
    UTF-8 strings.

This is an old oTree bug; upgrade your version of otree-core (see :ref:`upgrade-otree-core`).

``otree: command not found``
----------------------------

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
