.. _py3-migration

Migrating an existing project to Python 3
=========================================

If you already created an oTree project with Python 2 and would like to switch to Python 3,
you should first install Python 3.5,
and then make the following changes to your project files.

Fixing syntax
-------------

In ``ultimatum/views.py``, find this line in ``Constants``::

    keep_give_amounts = [(offer, endowment - offer) for offer in offer_choices]

You should change it to::

    keep_give_amounts = []
        for offer in offer_choices:
        keep_give_amounts.append((offer, endowment - offer))

Fixing for Heroku
-----------------

If you are running your app on Heroku,
You need to tell Heroku to use Python 3 instead of Python 2.
You can do this by creating a file in the project root dir ``runtime.txt`` that contains the following::

    python-3.5.1
