Advanced features
=================

These are advanced features that are mostly unsupported in oTree Studio.

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

To include the same JS/CSS in all pages of an app,
make a base template for the app.

For example, if your app's name is ``public_goods``,
create ``public_goods/templates/public_goods/Page.html``:

.. code-block:: html+django

    {% extends "global/Page.html" %}
    {% load otree %}

    {% block app_styles %}
        <style>
            ...
        </style>
    {% endblock %}

    {% block app_scripts %}
        <script>
            ...
        </script>
    {% endblock %}

Then make each template inherit from this template:

 .. code-block:: html+django

    {% extends "public_goods/Page.html" %}
    {% load otree %}
    ...

To include the same JS/CSS in *all apps* of a project,
modify ``_templates/global/Page.html``.
In that file, you will find the blocks ``global_scripts`` and ``global_styles``.

.. _staticfiles:

Static files
------------


Here is how to include images (or any other static file like .css, .js, etc.) in your pages.

At the root of your oTree project, there is a ``_static/`` folder.
Put a file there, for example ``puppy.jpg``.
Then, in your template, you can get the URL to that file with
``{% static 'puppy.jpg' %}``.

To display an image, use the ``<img>`` tag, like this:

.. code-block:: HTML+django

    <img src="{% static 'puppy.jpg' %}"/>

Above we saved our image in ``_static/puppy.jpg``,
But actually it's better to make a subfolder with the name of your app,
and save it as ``_static/your_app_name/puppy.jpg``, to keep files organized
and prevent name conflicts.

Then your HTML code becomes:

.. code-block:: HTML+django

    <img src="{% static "your_app_name/puppy.jpg" %}"/>

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

.. code-block:: html+django

    {% extends 'otree/WaitPage.html' %}
    {% load otree %}
    {% block title %}{{ title_text }}{% endblock %}
    {% block content %}
        {{ body_text }}
        <p>
            My custom content here.
        </p>
    {% endblock %}

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
        def vars_for_template(self):
            return dict(body_text="foo")

If you want to apply your custom wait page template globally,
save it to ``_templates/global/WaitPage.html``.
oTree will then automatically use it everywhere instead of the built-in wait page.

CSS and JavaScript in Wait Pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wait pages have the same block structure as regular pages
(``global_scripts``, ``app_scripts``, ``scripts``, etc...),
so you can follow the same instructions described in :ref:`base-template`
and :ref:`selectors`.

For example, to apply CSS to your custom wait page at ``_templates/global/WaitPage.html``,
put a block ``global_scripts`` in the template.

You can even make other custom wait pages inherit from ``_templates/global/WaitPage.html``,
just the way regular pages inherit from ``_templates/global/Page.html``,
and they can define the blocks ``app_scripts`` and ``scripts``, etc.

.. _aux-models:

Extra models
------------

.. note::

    New in :ref:`oTree 2.6 <v26>`.
    If you try using this feature on an older version of oTree,
    you will get an error about your ForeignKey like
    "TypeError: __init__() missing 1 required positional argument: 'on_delete'"

You can define extra models, in addition to ``Player``, ``Group``, and ``Subsession``.
This is useful especially when using :ref:`live`,
where each player may have multiple bids/messages/offers.

For example, put this at the bottom of your models.py:

.. code-block:: python

    class Bid(models.Model):
        player = models.ForeignKey(Player)
        resource = models.StringField()
        offer = models.CurrencyField()

Now, you can use the Django ORM to create/update/delete bids.
For example, to create a bid for a player:

.. code-block:: python

    Bid.objects.create(player=player, resource='pipeline', offer=500)

To list all bids for a player:

.. code-block:: python

    bids = Bid.objects.filter(player=player)


If you want to use the model in your pages or tests,
you should do ``from .models import Bid``.

To export data in extra models, you can use :ref:`custom-export`.

Foreign key to group
~~~~~~~~~~~~~~~~~~~~

If you need to find all bids in a group, add a foreign key to Group:

.. code-block:: python

    class Bid(models.Model):
        player = models.ForeignKey(Player)
        group = models.ForeignKey(Group)
        # etc...

When you create the model, set the group:

.. code-block:: python

    Bid.objects.create(player=player, group=player.group, offer=500)

That way, you can also query by group:

.. code-block:: python

    bids = Bid.objects.filter(player=player)

About foreign keys
~~~~~~~~~~~~~~~~~~

The first argument to ``ForeignKey`` should be the model the bid belongs to
e.g. ``Player`` or ``Group``.

To link the model to 2 separate players
(e.g. representing a link between 2 players in a network game),
use 2 separate ForeignKeys to Player:

.. code-block:: python

    class Contract(models.Model):
        proposer = models.ForeignKey(Player, related_name='proposers')
        responder = models.ForeignKey(Player, related_name='responders')
        offer = models.CurrencyField()
        # etc...

.. _django-orm:

Django ORM
~~~~~~~~~~

Here are some examples of using the Django ORM.

Create:

.. code-block:: python

    Bid.objects.create(player=player, resource='pipeline', offer=500)

Query & sort:

.. code-block:: python

    bids = Bid.objects.filter(player=player).exclude(offer=0).order_by('offer')

Get a unique record (e.g. when you know there is exactly 1 accepted bid):

.. code-block:: python

    bid = Bid.objects.get(group=group, is_accepted=True)

Update:

.. code-block:: python

    Bid.objects.filter(player=player).update(is_accepted=False)

    # OR:
    for bid in Bid.objects.filter(player=player):
        bid.is_accepted=False
        # must be saved manually
        bid.save()

Delete:

.. code-block:: python

    bids = Bid.objects.filter(player=player, offer=0).delete()


.. _migrations:

Modifying an existing database
------------------------------

This section is more advanced and is for people who are comfortable with troubleshooting.

If your database already contains data and you want to update the structure
without running ``resetdb`` (which will delete existing data), you can use Django's migrations feature.
Below is a quick summary; for full info see the Django docs `here <https://docs.djangoproject.com/en/2.2/topics/migrations/#workflow>`__.

First, add an empty file ``otree_core_migrations/__init__.py``
in your project top-level folder.

Then, add the following line to settings.py::

    MIGRATION_MODULES = {'otree': 'otree_core_migrations'}

Then run::

    python manage.py makemigrations otree

Then run ``python manage.py makemigrations my_app_name`` (substituting your app's name),
for each app you are working on. This will create a ``migrations`` folder in your app,
which you should add to your git repo, commit, and push to your server.

Instead of using ``otree resetdb`` on the server, run ``python manage.py migrate`` (or ``otree migrate``).
If using Heroku, you would do ``heroku run otree migrate``.
This will update your database tables.

If you make further modifications to your apps or upgrade otree, you can run
``python manage.py makemigrations``. You don't need to specify the app names in this command;
migrations will be updated for every app that has a ``migrations`` folder.
Then commit, push, and run ``python manage.py migrate`` again as described above.

More info `here <https://docs.djangoproject.com/en/2.2/topics/migrations/#workflow>`__

Currency
--------

To customize the name "points" to something else like "tokens" or "credits",
set ``POINTS_CUSTOM_NAME``, e.g. ``POINTS_CUSTOM_NAME = 'tokens'``.

You can change the number of decimal places in real world currency amounts
with the setting ``REAL_WORLD_CURRENCY_DECIMAL_PLACES``.
If the extra decimal places show up but are always 0,
then you should reset the database.
