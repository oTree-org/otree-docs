Localization
============

Changing the language setting
-----------------------------

Go to your settings and change ``LANGUAGE_CODE``:.

For example::

    LANGUAGE_CODE = 'fr' # French
    LANGUAGE_CODE = 'zh-hans' # Chinese (simplified)

This will customize certain things such validation messages and formatting of numbers.
For more information, see the Django documentation on translation and localization.

Writing your app in multiple languages
--------------------------------------

You may want your own app to work in multiple languages.
For example, let's say you want to run the same experiment with English, French, and Chinese participants.

For this, you can use Django's `translation <https://docs.djangoproject.com/en/1.11/topics/i18n/translation/>`__
system.

A quick summary:

-   Go to ``settings.py``, change ``LANGUAGE_CODE``, and restart the server.
    Examples::

        LANGUAGE_CODE = 'fr'
        LANGUAGE_CODE = 'zh-hans'
-   Create a folder ``locale`` in each app you are translating, e.g. ``public_goods/locale``.
    (If you forget to create this folder, the translations will go into your root folder's ``locale`` folder.)
-   At the top of your templates, add ``{% load i18n %}``. Then use ``{% blocktrans trimmed %}...{% endblocktrans %}``.
    There are some things you can't use inside a ``blocktrans``,
    such as variables containing dots (e.g. ``{{ Constants.foo }}``),
    or tags (e.g. ``{% if %}``). More info `here <https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#std:templatetag-blocktrans>`__.
-   If you have localizable strings in your Python code, use ``ugettext``.
-   Use ``makemessages`` to create the ``.po`` files in your app's ``locale`` folder.
    Examples::

        django-admin makemessages -l fr
        django-admin makemessages -l zh_Hans

-   Edit the ``.po`` file in `Poedit <http://poedit.net/>`__
-   Run ``django-admin compilemessages`` to create ``.mo`` files
    next to your ``.po`` files. If it doesn't work, try running the command
    inside the app folder containing the ``locale/`` folder.

If you localize the files under ``_templates/global``,
you need to create a folder ``locale`` in the root of the project.
