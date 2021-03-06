.. _otreelite:

oTree Lite
==========

As of December 2020, there is an alternative implementation of oTree that runs as a self-contained framework,
not dependent on Django.

It is smaller, which makes it easier to install, deploy, and use. For example:

-   Simpler error messages
-   Fewer dependencies such as Twisted that cause installation problems for some people
-   Compatible with more versions of Python
-   No need for Redis or second dyno
-   I also expect it to eventually run much faster, once I start performance tuning it.

oTree Lite's codebase is simpler and more self-contained.
For the curious people who want to delve into oTree's internal source code,
you will have an easier time navigating oTree Lite.


Installation
------------

run::

    pip install -U "otree>=5a"


.. _lite_vs_mainline:

Should I install oTree Lite, or oTree 3.x?
------------------------------------------

oTree 3.x and oTree Lite each have unique advantages, so I will be actively maintaining
both. You can try either version and switch back and forth between them, since they
have the same features and are compatible with the same code format.

Reasons in favor of using oTree Lite:

-   You are a first-time oTree user
-   Your apps were developed in the past 1 or 2 years, or using oTree Studio
    (so they likely already use the latest format)
-   Or, you want some of the features of oTree Lite,
    and don't mind running ``otree update_my_code`` to update your older apps.

Reasons in favor of using oTree 3.x (mainline version):

-   You have existing apps that are rather complex and want to guarantee compatibility
-   Your apps use features from the Django documentation,
    or addons you got from someone else.

How can I ensure I stay on oTree 3.x?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To ensure that you don't install oTree Lite, specify ``<5`` when you upgrade::

    pip3 install -U "otree<5"

For Heroku, use one of the following formats in your ``requirements.txt``
(replace 3.3.7 with whatever 3.x version you want)::

    otree<5
    # or:
    otree>=3.3.7,<5
    # or:
    otree==3.3.7


Compatibility
-------------

This alternative implementation is generally compatible with existing oTree apps.
However, you will probably see small things that changed, especially in how forms and templates are rendered.
This is somewhat inevitable as oTree has undergone a "brain transplant".
Please send any feedback to chris@otree.org.

Here are the most important differences:

Templates
~~~~~~~~~

The template system is basically compatible with Django templates,
except that only the basic tags & filters have been implemented:

-   Tags: ``{% if %}``, ``{% for %}``, ``{% block %}``, ``{% extends %}``, ``{% with %}``
-   Filters: ``{{ x|json }}``, ``{{ x|escape }}``, ``{{ x|c }}``, ``{{ x|default }}``

There is no ``floatformat`` filter, but there are new rounding filters that replace it.
For example:

.. code-block:: html+django

    {{ pi|floatformat:0 }} -> {{ pi|to0 }}
    {{ pi|floatformat:1 }} -> {{ pi|to1 }}
    {{ pi|floatformat:2 }} -> {{ pi|to2 }}

The ``|safe`` filter and ``mark_safe`` are not needed anymore, because the new template system does not
autoescape content. However, if you want to escape content (e.g. displaying an untrusted string to a different
player), you should use the ``|escape`` filter.

Method calls must be at the end of the expression, and not followed by more dots.
For example, if you have a Player method called ``other_player()``,
you can do:

.. code-block:: html+django

    Your partner is {{ player.other_player }}

But you cannot do:

.. code-block:: html+django

    Your partner's decision was {{ player.other_player.decision }}

Forms
~~~~~

In templates, if you are doing manual form rendering, you should change
``{{ form.my_field.errors }}`` to:

.. code-block:: html+django

    {% if form.my_field.errors %}
        {{ form.my_field.errors.0 }}
    {% endif %}

This is because in ``.errors`` is now a list of strings,
and displaying it when there are no errors will output ``[]`` which looks a bit weird.

Older oTree formats
~~~~~~~~~~~~~~~~~~~

Since this is an experimental version of oTree, it does not implement support for certain features found in older oTree
projects. To check you should run ``otree update_my_code``,
which will tell you the changes you need to make before your code can run on oTree Lite.
(It will also fix a few things automatically.)

A few common issues:

-   The ``Slider`` widget is unavailable.
    You should instead use :ref:`raw_html` (which has been the recommended solution anyway)

Bootstrap
~~~~~~~~~

Since bootstrap 5 beta just got released, I included it in this package.
Certain things are different from bootstrap 4; consult the bootstrap migration docs.
In my experience the main things that differed are:

-   ``data-*`` attributes are renamed to ``data-bs-*``
-   ``form-group`` no longer exists

Misc
~~~~

-   In ``get_group_matrix`` returns a matrix of integers, rather than a matrix of player objects.
    To preserve the previous behavior, you should pass ``objects=True``, like ``.get_group_matrix(objects=True)``.
-   ``ExtraModel`` is not supported yet
-   ``custom_export`` still works, though if you use any Django QuerySet syntax like ``Player.objects.filter()``,
    it will not work; see below.
-   If you try to access a Player/Group/Subsession field whose value is still ``None``,
    oTree will raise an error.

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
-   **Django ORM / QuerySet** is replaced by SQLAlchemy. SQLAlchemy has a very different syntax and a steeper learning curve
    (and also the documentation is not as friendly). However, it is a better fit for oTree since it is based on the
    "identity map"/"unit of work" model.
-   **Translating** an app to multiple languages works differently. See :ref:`i18n`.
