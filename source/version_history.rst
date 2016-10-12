Version history
```````````````

For each version below, this page lists that version's most important changes,
or any minor changes that I considered important to know about when upgrading.

.. _v10b:

Version 1.0 beta
================

Here are the main changes in 1.0 beta:

-   You can configure sessions in the admin interface
    (modifying ``SESSION_CONFIGS`` parameters without changing the source code).
    See :ref:`edit_config`.
-   Performance improvements
-   The default for the ``payoff`` field is now ``0``, not ``None``.

To install, run this (note the ``--pre`` in the command;
this means "pre-release")::

    pip install -U --pre otree-core
    otree resetdb

To revert back to the stable version of oTree-core::

    pip uninstall otree-core
    pip install otree-core

Please send feedback to chris@otree.org,
even just to say it works fine.

Version 0.8
===========

The bot system has been overhauled, and there are some changes to the bot API.
See the notes :ref:`here <bots>`.

Browser bots now work together with ``otree runserver``.

.. _v0.7:

Version 0.7
===========

Version 0.7 beta is available.

The main new feature is :ref:`browser bots <browser-bots>`.
There are also some changes to the admin UI
(e.g. demo full-screen mode is now resizable).

.. _v0.6

Version 0.6
===========

Version 0.6 is available.
You can install it as usual::

    pip3 install -U otree-core
    otree resetdb

Here are some changes:

-   The :ref:`rooms <rooms>` feature is more fully developed and functional.
-   Various improvements to the admin interface
-   If you update a template you don't have to reload the server
-   Chinese now uses the proper ``zh-hans`` language code
-   ``runprodserver`` now defaults to port 8000 (before was 5000)


.. _v0.5

Version 0.5
===========

What's new
----------

oTree 0.5 is now released.

It has a different architecture based on WebSockets.
It runs faster and supports more concurrent players.

It also has a "Server Check" feature in the admin interface
that checks if your server is set up properly.

Server deployment
-----------------

Redis needs to be installed on your server.
If using Heroku, you should install Heroku's `Redis add-on <https://elements.heroku.com/addons/heroku-redis>`__,
then run ``heroku restart``.

Then update your ``requirements_base.txt`` so it contains the right version of ``otree-core``.
This will tell Heroku which version of oTree to install.
(The currently installed version of ``otree-core`` is listed in the output of ``pip3 freeze``).

In your project's root directory, find the file ``Procfile``,
change its contents to the following, and if using Heroku, turn on both dynos:

.. code-block:: bash

    web: otree webandworkers
    timeoutworker: otree timeoutworker
