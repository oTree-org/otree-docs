Version history
```````````````
.. _v26:

Version 2.6 beta
================

Install the beta with: ``pip3 install -U otree --pre`` and send feedback to chris@otree.org.
In your requirements_base.txt, put ``otree>=2.6.0b1`` (or whatever version of the beta you installed).

Live pages
----------

See :ref:`live`.

REST API
--------

See :ref:`rest`

Custom data export
------------------

See :ref:`custom-export`.

Extra models
------------

oTree now supports defining extra models in addition to Player/Group/Subsession.
See :ref:`aux-models`.


Player.start()
--------------

If you define a method called ``start`` on your Player model,
you can specify actions to be taken when the player starts the round.
For example:

.. code-block:: python

    class Player(BasePlayer):
        endowment = models.CurrencyField()

        def start(self):
            self.endowment = self.participant.vars['endowment']

Here you can setup/initialize the player by passing data from previous rounds or apps.
The differences between ``Player.start`` and ``Subsession.creating_session`` are:

-   ``start`` is run when the player reaches the first page of the round,
    whereas ``creating_session`` is run before the whole session even starts
-   ``start`` is run individually for each player,
    whereas ``creating_session`` is run once for the whole subsession (since it's a Subsession method).

``start()`` is skipped if the round is being skipped with ``app_after_this_page``.
Otherwise, it is always run, even if the player skips all the pages in that round.

Other things
------------

-   You can now download a single session's data as Excel or CSV (through session's Data tab)
-   The text "Please correct the errors in the form" has been removed.
-   When browser bots complete, they keep the last page open
-   group_by_arrival_time: quicker detection if a participant goes offline
-   Minor bugfixes
-   Browser bots launched through CLI ``browser_bots`` command require ``OTREE_REST_KEY`` to be set
    (see :ref:`rest`).
-   ``models.ForeignKey`` has changed implementation. If you were previously using it,
    you may want to import it directly from Django to keep using the old one.


Version 2.5
===========
-   Removed old ``runserver`` command.
-   Deprecated non-oTree widgets and model fields. See `here <https://groups.google.com/forum/#!topic/otree/vsvsQ7njjY8>`__.

Version 2.4
===========

-   ``zipserver`` command
-   New MTurk format
-   oTree no longer records participants' IP addresses.

Version 2.3
===========

-   Various improvements to performance, stability, and ease of use.
-   oTree now requires Python 3.7
-   oTree extensions written for old versions of oTree (such otree_tools, mturkotreeutils, etc)
    may not work until they are upgraded to the new version of Django & Channels.
    more info
    `here <https://groups.google.com/d/msg/otree/FGwgNYDp8TQ/zClOFHbGEwAJ>`__,
    `here <https://groups.google.com/d/msg/otree/hCV7j03TP_o/_-snq3QEAgAJ>`__, and
    :ref:`here <channels>`.
-   oTree now uses Django 2.2.
-   Chinese/Japanese/Korean currencies are displayed as 元/円/원 instead of ¥/₩.
-   On Windows, ``runprodserver`` just launches 1 worker process. If you want more processes,
    you should use a process manager. (This is due to a limitation of the ASGI server)
-   ``runprodserver`` uses Uvicorn/Hypercorn instead of Daphne
-   update_my_code has been removed

Version 2.2
===========

-   support for the ``otreezip`` format
    (``otree zip``, ``otree unzip``)
-   MTurk: in sandbox mode, don't grant qualifications
    or check qualification requirements
-   MTurk: before paying participants, check if there is adequate
    account balance.
-   "next button" is disabled after clicking, to prevent congesting the server
    with duplicate page loads.
-   Upgrade to the latest version of Sentry
-   Form validation methods should go on the model, not the page.
    See :ref:`dynamic_validation`
-   :ref:`app_after_this_page`
-   Various performance and stability improvements

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
-   CSV/Excel data export is done asynchronously, which will fix
    timeout issues for large files on Heroku.
-   Better performance, especially for "Monitor" and "Data" tab in admin interface


.. _dynamic-validation-new-format:

New format for form validation
------------------------------

As of May 2019, it is recommended to define the following methods on the Player
(or Group) model, not the Page:

-   FIELD_min
-   FIELD_max
-   FIELD_choices
-   FIELD_error_message

For example, here is the old format:

.. code-block:: python

    class MyPage(Page):

        form_model = 'player'
        form_fields = ['offer']

        def offer_max(self):
            return self.player.endowment

To change this to the new format, you move ``offer_max`` into the Player model:

.. code-block:: python

    class Player(BasePlayer):

        offer = models.CurrencyField()

        def offer_max(self):
            return self.endowment

Note that we change ``return self.player.endowment`` to just ``self.endowment``,
because ``self`` *is* the player.

The old format will continue to work, so it is not urgent for you to make this change.


