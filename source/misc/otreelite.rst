oTree alternative implementation
================================

As of December 2020, there is an alternative implementation of oTree that runs as a self-contained framework,
not dependent on Django.

Advantages
``````````

Simpler codebase
----------------

If you are someone who wants to be able to read oTree's source code, it is currently quite hard sometimes.
To understand how certain parts of oTree work, you have to go far up the chain into Django.
This codebase is simpler and more self-contained.

Easier to extend
----------------

Django is quite a heavyweight framework and imposes a lot of constraints.
It can be hard to add custom functionality unless you really know how Django works.
In contrast, this implementation is smaller and uses more modern components such as Starlette.

Lightweight
-----------

It is also considerably more lightweight, which you will notice during deployment,
running commands, etc (for example it doesn't require Redis or a second dyno).
I also expect it to eventually run much faster, once I start performance tuning it.

Installation
------------

run::

    pip install "otree>=5.0.0a1"

(Note: this does not mean it will actually be version 5 of oTree, but rather I wanted to give it a version number
that is clearly distinct from that of the stable releases.)

Compatibility
`````````````
This new implementation is generally compatible with existing oTree apps. However, here are some differences:

Templates
---------

The template system uses `Ibis <http://www.dmulholl.com/docs/ibis/master/index.html>`__,
which at first glance looks the same as Django templates, but there are some differences, including:

-   Method calls in templates require parentheses, as they do in Python code, e.g. ``{{ player.in_all_rounds() }}``
-	``{{ forloop.counter }}`` is replaced with ``{{ loop.count }}``
-	The set of available tags & filters is different. For example no ``|floatformat``. Though writing custom filters and tags is easier than in Django.
-   With Django, if you ever tried to pass HTML or certain characters to your template, you would notice it gets autoescaped,
    e.g. ``<script>alert('XSS');</script>`` becomes ``&lt;script&gt;alert(&apos;XSS&apos;);&lt;/script&gt;``,
    which you need to use ``mark_safe`` or the ``|safe`` filter to undo.
    Ibis does not do this. If you want to escape special characters, you should use the triple braces ``{{{ }}}``.

Forms
-----

In templates, if you use ``{{ form.my_field.errors }}``, you should wrap it inside an ``if``::

    {% if form.my_field.errors %}
        {{ form.my_field.errors }}
    {% endif %}

This is because in wtforms (which oTree now uses), ``.errors`` is a list of strings,
and displaying it when there are no errors will output ``[]`` which looks a bit weird.

Older oTree formats
-------------------

Since this is an experimental version of oTree, I did not see any need to implement support for certain features found in older oTree
projects, such as:

-   views.py instead of pages.py
-   FIELD_choices defined in pages.py rather than models.py.
-   ``widgets.Slider``, ``widgets.CheckboxInput``

Bootstrap
---------

Since bootstrap 5 beta just got released, I included it in this package.
Certain things are different from bootstrap 4; consult the bootstrap migration docs.
In my experience the main things that differed are:

-   ``data-*`` attributes are renamed to ``data-bs-*``
-   ``form-group`` no longer exists

oTree features
--------------

The following oTree features are not supported yet:
-   ``ExtraModel``
-   and translation with {% blocktrans %}.

``custom_export`` still works, though if you use any Django QuerySet syntax like ``Player.objects.filter()``,
it will not work; see below.

Django (for advanced use cases)
-------------------------------

This new implementation does not use Django or Channels in any way.
So, it will not run any code you got from Django documentation, such as Django views, ModelForms, ORM, etc.
Here is a quick guide to how each component has been replaced.

-   **Django views** are replaced with `Starlette endpoints <https://www.starlette.io/endpoints/>`__,
    which are similar in that they are classes with a `get()` and `post()` method that returns a Response object.
    You can implement them as regular sync or async.
    However, the details are different, e.g. ``self.request`` is different from a Django request object.
-   **Channels consumers** are also replaced with Starlette endpoints. They are pretty similar, except there is no notion of
    groups or a Channel layer (you would need to implement one yourself; you can see how oTree does it in ``otree.channels.utils``).
-   **Django URLs** have been replaced with `Starlette routes <https://www.starlette.io/routing/>`__.
    You can define custom routes for websockets & views by creating
    ``asgi_routes.py`` in your project root, and oTree will look for a var called ``routes``.
-   **Django ORM / QuerySet** is replaced by SQLAlchemy. SQLAlchemy has a very different syntax and a steeper learning curve
    (and also the documentation is not as friendly). However, it is a better fit for oTree since it is based on the
    "identity map"/"unit of work" model.
-   **Django forms** are replaced with `wtforms <https://wtforms.readthedocs.io/>`__, which are quite similar.
-   **oTree shell** and **Management commands**: you can run a script (or launch a Jupyter notebook etc)
    by putting this at the top: ``from otree.main import setup; setup()``
