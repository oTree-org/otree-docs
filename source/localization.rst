Localization
============

oTree's participant interface is has been translated to the following languages:

- German
- Spanish
- French
- Russian

.. note::

    If you downloaded oTree prior to June 20, 2015, you need to upgrade
    ``otree-core`` to get this language support. See :ref:`upgrade-otree-core`.

This means that all built-in text that gets displayed to participants is
available in these languages. This includes things like:

-   Form validation messages
-   Wait page messages
-   Dates, times and numbers (e.g. "1.5" vs "1,5")

So, as long as you write your app's text in one of these languages,
all text that participants will see will be in that language.
For more information, see the Django documentation on
`translation <https://docs.djangoproject.com/en/1.8/topics/i18n/translation/>`__
and `format localization <https://docs.djangoproject.com/en/1.8/topics/i18n/formatting/>`__.


However, oTree's admin/experimenter interface is currently only available in English,
and the existing sample games have not been translated to any other languages.

Changing the language setting
-----------------------------

Go to ``settings.py``, change ``LANGUAGE_CODE``, and restart the server.

Writing your app in multiple languages
--------------------------------------

You may want your own app to work in multiple languages.
For example, let's say you want to run the same experiment with English and Chinese participants.

For this, you can use Django's `translation <https://docs.djangoproject.com/en/1.8/topics/i18n/translation/>`__
system.

A quick summary:

- In templates, use ``{% blocktrans trimmed %}...{% endblocktrans %}``
- In Python code, use ``ugettext``.
- Run ``django-admin makemessages`` to create the ``.po`` files
- Edit the ``.po`` file in `Poedit <http://poedit.net/>`__
- Run ``django-admin compilemessages``
- Go to ``settings.py``, change ``LANGUAGE_CODE``, and restart the server.

Volunteering to localize oTree
------------------------------

You are invited to contribute support for your own language in oTree.

It's a simple task; you provide translations of about 20 English phrases.

`Here <https://github.com/oTree-org/otree-core/blob/master/otree/locale/fr/LC_MESSAGES/django.po>`__
is an example of an already completed translation to French.

We are especially looking for volunteers to translate the following files to their respective languages:

- `Chinese <https://github.com/oTree-org/otree-core/raw/master/otree/locale/zh_CN/LC_MESSAGES/django.po>`__
- `Korean <https://github.com/oTree-org/otree-core/raw/master/otree/locale/ko/LC_MESSAGES/django.po>`__
- `Japanese <https://github.com/oTree-org/otree-core/raw/master/otree/locale/ja/LC_MESSAGES/django.po>`__
- `Italian <https://github.com/oTree-org/otree-core/raw/master/otree/locale/it/LC_MESSAGES/django.po>`__

You can download the file and edit it directly in your text editor, or use `Poedit <https://poedit.net/>`__.

Please contact chris@otree.org.

