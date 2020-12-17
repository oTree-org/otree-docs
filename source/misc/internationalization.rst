.. _i18n:

Localization
============

Changing the language setting
-----------------------------

Go to your settings and change ``LANGUAGE_CODE``:.

For example::

    LANGUAGE_CODE = 'fr' # French
    LANGUAGE_CODE = 'zh-hans' # Chinese (simplified)

This will customize certain things such validation messages and formatting of numbers.

Writing your app in multiple languages
--------------------------------------

You may want your own app to work in multiple languages.
For example, let's say you want to run the same experiment with English, French, and Chinese participants.

oTree 3.x (regular version)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this, you can use Django's `translation <https://docs.djangoproject.com/en/2.2/topics/i18n/translation/>`__
system.

A quick summary:

-   In your settings, change ``LANGUAGE_CODE``, and restart the server.
    Examples::

        LANGUAGE_CODE = 'fr'
        LANGUAGE_CODE = 'zh-hans'
-   Create a folder ``locale`` in each app you are translating, e.g. ``public_goods/locale``.
    (If you forget to create this folder, the translations will go into your root folder's ``locale`` folder.)
-   At the top of your templates, add ``{% load i18n %}``. Then use ``{% blocktrans trimmed %}...{% endblocktrans %}``.
    There are some things you can't use inside a ``blocktrans``,
    such as variables containing dots (e.g. ``{{ Constants.foo }}``),
    or tags (e.g. ``{% if %}``). More info `here <https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#std:templatetag-blocktrans>`__.
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

oTree Lite
~~~~~~~~~~

Here are the instructions for people using :ref:`otreelite`.

In your Python files, any strings that you want to be translated should be wrapped in ``gettext()``.
For example:

.. code-block:: python

    from gettext import gettext
    msg = gettext('This string will be translated')

In your templates, any translatable strings should be inside a ``trans`` tag, for example::

    {% trans 'this is inside a trans tag' %}

(blocktrans is not supported.)

Install Babel with ``pip install babel``.
Create ``babel.ini`` in your project root, containing::

    [extractors]
    otreetemplate = otree.api:extract_otreetemplate

    [otreetemplate: **.html]
    [python: **.py]

Now run this command, listing all your app names::

    pybabel extract -F babel.ini trustgame auction -o messages.pot -k trans

This will create a ``messages.pot`` file with your translatable strings.
Translate that using poedit.

Create the following folder::

    mkdir _locale/fr/LC_MESSAGES/  # if french
    mkdir _locale/zh_Hans/LC_MESSAGES/  # if chinese

Then create the .mo file::

    pybabel compile -i messages.pot -d _locale -l fr -f

This will add a ``messages.mo`` to that folder.
Now, change your project's ``LANGUAGE_CODE``, and your translated messages should appear.