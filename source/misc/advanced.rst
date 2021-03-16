Advanced features
=================

These are advanced features that are mostly unsupported in oTree Studio.

.. _ExtraModel:

ExtraModel
----------

.. note::

    This feature is new as of March 2021 and is currently in beta.

An ExtraModel is useful when you need to store dozens or hundreds of data points about a single player.
For example, a list of bids, or a list of stimuli and reaction times.
They are frequently used together with :ref:`live`.

An ExtraModel should link to another model:

.. code-block:: python

    class Bid(ExtraModel):
        player = models.Link(Player)
        amount = models.CurrencyField()

Each time the user makes a bid, you store it in the database:

.. code-block:: python

    Bid.create(player=player, amount=500)

Later, you can retrieve the list of a player's bids:

.. code-block:: python

    bids = Bid.filter(player=player)

An ExtraModel can have multiple links:

.. code-block:: python

    class Offer(ExtraModel):
        sender = models.Link(Player)
        receiver = models.Link(Player)
        group = models.Link(Group)
        amount = models.CurrencyField()
        accepted = models.BooleanField()

Then you can query it in various ways:

.. code-block:: python

    this_group_offers = Offer.filter(group=group)
    offers_i_accepted = Offer.filter(receiver=player, accepted=True)

For more complex filters and sorting, you should use list operations:

.. code-block:: python

    offers_over_500 = [o for o in Offer.filter(group=group) if o.amount > 500]

See the example psychology games such as the Stroop task,
which show how to generate ExtraModel data from each row of a CSV spreadsheet.

Templates
---------

template_name
~~~~~~~~~~~~~

If the template needs to have a different name from your
page class (e.g. you are sharing the same template for multiple pages),
set ``template_name``. Example:

.. code-block:: python

    class Page1(Page):
        template_name = 'app_name/MyPage.html'

.. _base-template:

CSS/JS and base templates
~~~~~~~~~~~~~~~~~~~~~~~~~

To include the same JS/CSS in all pages of an app, either put it in a ref:`static file <staticfiles>`
or put it in an includable template.

.. _staticfiles:

Static files
------------

Here is how to include images (or any other static file like .css, .js, etc.) in your pages.

At the root of your oTree project, there is a ``_static/`` folder.
Put a file there, for example ``puppy.jpg``.
Then, in your template, you can get the URL to that file with
``{{ static 'puppy.jpg' }}``.

To display an image, use the ``<img>`` tag, like this:

.. code-block:: html

    <img src="{{ static 'puppy.jpg' }}"/>

Above we saved our image in ``_static/puppy.jpg``,
But actually it's better to make a subfolder with the name of your app,
and save it as ``_static/your_app_name/puppy.jpg``, to keep files organized
and prevent name conflicts.

Then your HTML code becomes:

.. code-block:: html

    <img src="{{ static 'your_app_name/puppy.jpg }}"/>

(If you prefer, you can also put static files inside your app folder,
in a subfolder called ``static/your_app_name``.)

If a static file is not updating even after you changed it,
this is because your browser cached the file. Do a full page reload
(usually Ctrl+F5)

If you have videos or high-resolution images,
it's preferable to store them somewhere online and reference them by URL
because the large file size can make uploading your
.otreezip file much slower.


Wait pages
----------

.. _customize_wait_page:

Custom wait page template
~~~~~~~~~~~~~~~~~~~~~~~~~

You can make a custom wait page template.
For example, save this to ``your_app_name/templates/your_app_name/MyWaitPage.html``:

.. code-block:: html

    {{ block title }}{{ title_text }}{{ endblock }}
    {{ block content }}
        {{ body_text }}
        <p>
            My custom content here.
        </p>
    {{ endblock }}

Then tell your wait page to use this template:

.. code-block:: python

    class MyWaitPage(WaitPage):
        template_name = 'your_app_name/MyWaitPage.html'

Then you can use ``vars_for_template`` in the usual way.
Actually, the ``body_text`` and ``title_text`` attributes
are just shorthand for setting ``vars_for_template``;
the following 2 code snippets are equivalent:

.. code-block:: python

    class MyWaitPage(WaitPage):
        body_text = "foo"

.. code-block:: python

    class MyWaitPage(WaitPage):

        @staticmethod
        def vars_for_template(player):
            return dict(body_text="foo")

If you want to apply your custom wait page template globally,
save it to ``_templates/global/WaitPage.html``.
oTree will then automatically use it everywhere instead of the built-in wait page.


Currency
--------

To customize the name "points" to something else like "tokens" or "credits",
set ``POINTS_CUSTOM_NAME``, e.g. ``POINTS_CUSTOM_NAME = 'tokens'``.

You can change the number of decimal places in real world currency amounts
with the setting ``REAL_WORLD_CURRENCY_DECIMAL_PLACES``.
If the extra decimal places show up but are always 0,
then you should reset the database.

Reading CSV or other files
--------------------------

Store yourfile.csv in your app folder.
Then put this code anywhere you want to read the file
(in a method or in Constants):

.. code-block:: python

    import csv
    with open('yourapp/yourfile.csv', encoding='utf-8') as file:
        rows = list(csv.DictReader(file))

If it's not CSV and you just want to read the file contents as a string,
this gets simplified to:

.. code-block:: python

    with open('yourapp/yourfile.txt', encoding='utf-8') as file:
        txt = file.read()
