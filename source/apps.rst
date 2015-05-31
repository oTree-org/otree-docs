Applications
============

In oTree (and Django), an app is a folder containing Python and HTML code. When you
create your oTree project, it comes pre-loaded with various apps such as
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

Think of this as a skeleton to which you can add as much as you want.
You can add your own classes, functions, methods, and attributes, or
import any 3rd-party modules.

Then go to ``settings.py`` and create an entry for your app in
``SESSION_TYPES`` that looks like the other entries.

models.py
---------

This is where you store your data models.

Model hierarchy
~~~~~~~~~~~~~~~

Every oTree app needs the following 3 models:

-  Subsession
-  Group
-  Player

A player is part of a group, which is part of a subsession.


Models and database tables
~~~~~~~~~~~~~~~~~~~~~~~~~~

For example, let's say you are programming an ultimatum game, where in
each two-person group, one player makes a monetary offer (say, 0-100
cents), and another player either rejects or accepts the offer. When you
analyze your data, you will want your "Group" table to look something
like this:

::

    +----------+----------------+----------------+
    | Group ID | Amount offered | Offer accepted |
    +==========+================+================+
    | 1        | 50             | TRUE           |
    +----------+----------------+----------------+
    | 2        | 25             | FALSE          |
    +----------+----------------+----------------+
    | 3        | 50             | TRUE           |
    +----------+----------------+----------------+
    | 4        | 0              | FALSE          |
    +----------+----------------+----------------+
    | 5        | 60             | TRUE           |
    +----------+----------------+----------------+

You need to define a Python class that defines the structure of this
database table. You define what fields (columns) are in the table, what
their data types are, and so on. When you run your experiment, the SQL
tables will get automatically generated, and each time users visit, new
rows will get added to the tables.

Here is how to define the above table structure:

.. code-block:: python

    class Group(otree.models.BaseGroup):
        ...
        amount_offered = models.CurrencyField()
        offer_accepted = models.BooleanField()

Every time you add, remove, or change a field in ``models.py``, you need
to run ``python otree resetdb`` (or, in the launcher, click "Clear
Database").

The full list of available fields is in the Django documentation
`here <https://docs.djangoproject.com/en/1.7/ref/models/fields/#field-types>`__.

Additionally, oTree has ``CurrencyField``; see :ref:`money`.

Constants
~~~~~~~~~

The ``Constants`` class is the recommended place to put your app's
parameters and constants that do not vary from player
to player.

Here are the required constants:

-  ``name_in_url`` specifies the name used to identify your app in the participant's URL.
For example, if you set it to ``public_goods``, a participant's URL might look like this:
``http://otree-demo.herokuapp.com/p/zuzepona/public_goods/Introduction/1/``
-  ``players_per_group`` (described in :ref:`groups`)
-  ``num_rounds`` (described elsewhere in the documentation)

views.py
--------

Each page that your players see is defined by a ``Page`` class in
``views.py``. (You can think of "views" as a synonym for "pages".)

For example, if 1 round of your game involves showing the player a
sequence of 5 pages, your ``views.py`` should contain 5 page classes.

At the bottom of your ``views.py``, you must have a ``page_sequence``
variable that specifies the order in which players are routed through
your pages. For example:

.. code-block:: python

    page_sequence=[Start, Offer, Accept, Results]

Each ``Page`` class has these methods and attributes:

``def vars_for_template(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A dictionary of variable names and their values, which is passed to the template.

Note: oTree automatically passes group, player, subsession, and Constants
objects to the template, which you can access in the template, e.g.: ``{{Constants.payoff_if_rejected}}``.

``def is_displayed(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Should return True if the page should be shown, and False if the page
should be skipped. Default behavior is to show the page.

For example, if you only want a page to be shown to P2 in each group:

.. code-block:: python

    def is_displayed(self):
        return self.player.id_in_group == 2

``template_name``
~~~~~~~~~~~~~~~~~

The name of the HTML template to display. This can be omitted if the
template has the same name as the Page class.

Example:

.. code-block:: python

    # This will look inside your app under the 'templates' directory,
    # to '/app_name/MyView.html'
    template_name = 'app_name/MyView.html'

``timeout_seconds``
~~~~~~~~~~~~~~~~~~~

The number of seconds the user has to
complete the page. After the time runs out, the page auto-submits.

Example: ``timeout_seconds = 20``

``timeout_submission``
~~~~~~~~~~~~~~~~~~~~~~

.. note::

    Prior to May 26, 2015, this was called ``auto_submit_values``.

A dictionary where the keys are the elements of
``form_fields``, with the values to be
submitted in case of a timeout, or if the experimenter moves the
participant forward.

If omitted, then oTree will default to
``0`` for numeric fields, ``False`` for boolean fields, and the empty
string for text/character fields.


``def before_next_page(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here you define any code that should be executed
after form validation,
before the player proceeds to the next page.


``def vars_for_all_templates(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is not a method on the Page class, but rather a top-level function
in views.py. It is useful when you need certain variables to be passed
to multiple pages in your app. Instead of repeating the same values in
each ``vars_for_template``, you can define it in this function.
