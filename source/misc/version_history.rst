Version history
```````````````

For each version below, this page lists that version's most important changes,
or any minor changes that I considered important to know about when upgrading.

.. _v21:

Version 2.1
===========

-   oTree now raises an error if you use an undefined variable in your template.
    This will help catch typos like
    ``{{ Player.payoff }}`` or ``{% if player.id_in_gruop %}``.
    This means that apps that previously worked may now get a template error
    (previously, it failed silently).
    If you can't remove the offending variable,
    you can apply the ``|default`` filter, like: ``{{ my_undefined_variable|default:None }}``
-   oTree now warns you if you use an invalid attribute on a Page/WaitPage.
    You can disable this by setting ``_allow_custom_attributes=True`` on the page class.
    See `here <https://groups.google.com/forum/#!topic/otree/_yzlaTMfJKs>`__
    for more details.
-   CSV/Excel data export is done asynchronously, which will fix
    timeout issues for large files on Heroku.
-   Better performance, especially for "Monitor" and "Data" tab in admin interface


Version 2.0
===========

See :ref:`v20`.


.. _v14:

Version 1.4
===========

Here are the main changes in 1.4:

-   MTurk: improved stability, and upgrade from boto2 to boto3.
    See the :ref:`MTurk page <v14_mturk>` for details.
-   ``group_by_arrival_time`` now filters out participants who have disconnected
    or dropped out. See :ref:`group_by_arrival_time`.
-   Upgrade timeout JavaScript library (jQuery countdown)

To install, run this::

    pip3 install -U otree-core
    otree resetdb


.. _v13:

Version 1.3
===========

Here are the main changes in 1.3:

-   ``get_timeout_seconds`` lets you set timeouts dynamically,
    and create timeouts that span multiple pages or rounds. See :ref:`get_timeout_seconds`.
-   ``get_players_for_group`` lets you control how ``group_by_arrival_time``
    assigns players to groups. See :ref:`get_players_for_group`
-   Bots: you can now simulate & test a page timeout. See :ref:`bot_timeout`.
-   ``DEMO_PAGE_TITLE`` setting added. See :ref:`DEMO_PAGE_TITLE`.

To install, run this::

    pip3 install -U otree-core
    otree resetdb

Please send feedback to chris@otree.org.

.. _v12:

Version 1.2
===========

-   If a page is submitted automatically by a timeout,
    oTree will attempt to save the incomplete form.
    See :ref:`timeout_form`
-   The :ref:`|json <json>` filter was added, as an alternative to ``safe_json``.

.. _v11b:

Version 1.1
===========

Here are the changes in oTree-core 1.1:

-   :ref:`group_by_arrival_time`
-   :ref:`admin_report`
-   ``botworker`` is automatically launched as part of ``timeoutworker`` or ``runprodserver``


Version 1.0
===========

Here are the main changes in 1.0:

-   You can configure sessions in the admin interface
    (modifying ``SESSION_CONFIGS`` parameters without changing the source code).
    See :ref:`edit_config`.
-   Performance improvements
-   The default for the ``payoff`` field is now ``0``, not ``None``.
    (Make sure your code doesn't rely on ``payoff`` being ``None``.)


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
There are also some changes to the admin UI.

.. _v0.6:

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
