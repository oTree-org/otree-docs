Version history
```````````````

Version 2.3
===========

-   Various improvements to performance, stability, and ease of use.
-   oTree now requires Python 3.7
-   oTree extensions written for old versions of oTree & Channels (such otree_tools, mturkotreeutils, etc)
    may not work until they are upgraded to the new version.
-   Django Channels has been upgraded to version 2.x. If you are the developer of an extension based on
    Channels, see more info here: :ref:`channels`.
-   Chinese/Japanese/Korean currencies are displayed as 元/円/원 instead of ¥/₩.
-   On Windows, ``runprodserver`` just launches 1 worker process. If you want more processes,
    you should use a process manager. (This is due to a limitation of the ASGI server)
-   ``runprodserver`` uses Uvicorn/Hypercorn instead of Daphne
-   Experimental feature: You can do MTurk sandbox testing locally. Install Redis then run
    ``otree runprodserver 8001 --dev-https`` then go to ``https://127.0.0.1:8001``.
    You will get a security warning but it's OK because the site is on your own computer.
-   update_my_code has been removed

Version 2.2
===========

-   support for the ``otreezip`` format
    (``otree zip``, ``otree unzip``, ``otree runzip``)
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
    You can disable this by setting ``_allow_custom_attributes=True`` on the page class.
    See `here <https://groups.google.com/forum/#!topic/otree/_yzlaTMfJKs>`__
    for more details.
-   CSV/Excel data export is done asynchronously, which will fix
    timeout issues for large files on Heroku.
-   Better performance, especially for "Monitor" and "Data" tab in admin interface


