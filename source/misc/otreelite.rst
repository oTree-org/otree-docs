.. _otreelite:

oTree Lite
==========

As of December 2020, there is an alternative implementation of oTree that runs as a self-contained framework,
not dependent on Django.

Advantages
----------

Simpler codebase
~~~~~~~~~~~~~~~~

If you are someone who wants to be able to read oTree's source code, it is currently quite hard sometimes.
To understand how certain parts of oTree work, you have to go far up the chain into Django.
This codebase is simpler and more self-contained.

Easier to extend
~~~~~~~~~~~~~~~~

Django is quite a heavyweight framework and imposes a lot of constraints.
It can be hard to add custom functionality unless you really know how Django works.
In contrast, this implementation is smaller and uses more modern components such as Starlette.

Lightweight
~~~~~~~~~~~

It is also considerably more lightweight, which you will notice during deployment,
running commands, etc (for example it doesn't require Redis or a second dyno).
I also expect it to eventually run much faster, once I start performance tuning it.

Installation
------------

run::

    pip install "otree>=5.0.0a1"

(Note: this does not mean it will actually be version 5 of oTree, but rather I wanted to give it a version number
that is clearly distinct from that of the mainline releases.)

Compatibility
-------------

This alternative implementation is generally compatible with existing oTree apps.
However, you will probably see small things that changed, especially in how forms and templates are rendered.
This is somewhat inevitable as oTree has undergone a "brain transplant".

Here are the most important differences:

Templates
~~~~~~~~~

The template system is basically compatible with Django templates,
except that only the basic tags & filters have been implemented:

-   Tags: ``if``, ``for``, ``block``, ``extends``, ``with``, ``default``,
-   Filters: ``json``, ``escape``, ``c``

There is no ``floatformat`` filter, but there are new rounding filters that replace it.
For example::

    {{ pi|floatformat:0 }} -> {{ pi|to0 }}
    {{ pi|floatformat:1 }} -> {{ pi|to1 }}
    {{ pi|floatformat:2 }} -> {{ pi|to2 }}

The ``|safe`` filter and ``mark_safe`` are not needed anymore, because the new template system does not
autoescape content. However, if you want to escape content (e.g. displaying an untrusted string to a different
player), you should use the ``|escape`` filter.

You can also implement your own tags & filters; more on this later.

.. note::

    If you are using PyCharm with Django highlighting, it will flag some of the new syntax as a syntax error,
    so you may want to turn off Django highlighting.

Forms
~~~~~

In templates, if you are doing manual form rendering, you should change
``{{ form.my_field.errors }}`` to::

    {% if form.my_field.errors %}
        {{ form.my_field.errors.0 }}
    {% endif %}

This is because in wtforms (which oTree now uses), ``.errors`` is a list of strings,
and displaying it when there are no errors will output ``[]`` which looks a bit weird.

Older oTree formats
~~~~~~~~~~~~~~~~~~~

Since this is an experimental version of oTree, I did not see any need to implement support for certain features found in older oTree
projects, such as:

-   views.py instead of pages.py
-   FIELD_choices defined in pages.py rather than models.py.
-   ``widgets.Slider``, ``widgets.CheckboxInput``

Bootstrap
~~~~~~~~~

Since bootstrap 5 beta just got released, I included it in this package.
Certain things are different from bootstrap 4; consult the bootstrap migration docs.
In my experience the main things that differed are:

-   ``data-*`` attributes are renamed to ``data-bs-*``
-   ``form-group`` no longer exists

Known issues
~~~~~~~~~~~~

The following oTree features are not supported yet:

-   ``ExtraModel``

``custom_export`` still works, though if you use any Django QuerySet syntax like ``Player.objects.filter()``,
it will not work; see below.


Django (for advanced use cases)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
-   **Translating** an app to multiple languages works differently. See :ref:`i18n`.
