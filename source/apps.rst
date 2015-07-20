Applications
============

In oTree (and Django), an app is a folder containing Python and HTML code. When
you create your oTree project, it comes pre-loaded with various apps such as
``public_goods`` and ``dictator``. A session is basically a sequence of
apps that are played one after the other.

Creating an app
---------------

From the oTree launcher, click the "Terminal" button. (If the button is
disabled, make sure you have stopped the server.) When the console
window appears, type this:

.. code-block:: bash

    $ python otree startapp your_app_name

This will create a new app folder based on a oTree template, with most
of the structure already set up for you.

The key files are ``models.py``, ``views.py``, and the HTML files
under the ``templates/`` directory.

Think of this as a skeleton to which you can add as much as you want.
You can add your own classes, functions, methods, and attributes, or
import any 3rd-party modules.

Then go to ``settings.py`` and create an entry for your app in
``SESSION_CONFIGS`` that looks like the other entries.

