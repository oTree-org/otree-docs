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

In your Python files, any strings that you want to be translated should be wrapped in ``gettext()``.
For example:

.. code-block:: python

    from gettext import gettext
    msg = gettext('This string will be translated')

In your templates, any translatable strings should be inside a ``trans`` tag, for example::

    {{ trans 'this is inside a trans tag' }}

(blocktrans is not supported. If you want to translate large sections of text,
put them in separate includable templates and use an `if` statement to decide which language
should be shown.)

Install Babel with ``pip install babel``.
Create ``babel.ini`` in your project root, containing::

    [extractors]
    otreetemplate = otree.api:extract_otreetemplate

    [otreetemplate: **.html]
    [python: **.py]

Now run this command::

    pybabel extract . -F babel.ini -o messages.pot -k trans

This will create a ``messages.pot`` file with your translatable strings.
Translate that using poedit.

Create the following folder::

    _locale/fr/LC_MESSAGES/  # if french
    _locale/zh_Hans/LC_MESSAGES/  # if chinese

Then create the .mo file::

    pybabel compile -i messages.pot -d _locale -l fr -f

This will add a ``messages.mo`` to that folder.
Now, change your project's ``LANGUAGE_CODE``, and your translated messages should appear.
