Version history
```````````````

For each version below, this page lists that version's most important changes,
or any minor changes that I considered important to know about when upgrading.

.. _v0.7

Version 0.7 (beta)
==================

Version 0.7 beta is available. Install it like this (note the ``--pre`` flag,
since it is a pre-release)::

    pip3 install --upgrade --pre otree-core
    otree resetdb

The main new feature is :ref:`browser bots <browser-bots>`.
There are also some changes to the admin UI
(e.g. demo full-screen mode is now resizable).

.. _v0.6

Version 0.6
===========

Version 0.6 is available.
You can install it as usual::

    pip3 install --upgrade otree-core
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
