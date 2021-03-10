.. _otreelite:

oTree Lite
==========

As of December 2020, there is an alternative implementation of oTree that runs as a self-contained framework,
not dependent on Django.

Advantages:

-   Simpler error messages
-   Fewer dependencies such as Twisted that cause installation problems for some people
-   Compatible with more versions of Python
-   No need for Redis or second dyno
-   I also expect it to eventually run much faster, once I start performance tuning it.

oTree Lite's codebase is simpler and more self-contained.
For the curious people who want to delve into oTree's internal source code,
you will have an easier time navigating oTree Lite.

.. _lite_vs_mainline:

How can I ensure I stay on oTree 3.x?
-------------------------------------

To ensure that you don't install oTree Lite, you can specify ``<5`` when you upgrade::

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

-   Tags: ``{% if %}``, ``{% for %}``, ``{% block %}``
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
``{{ form.my_field.errors }}`` to ``{% formfield_errors 'my_field' %}``.

Older oTree formats
~~~~~~~~~~~~~~~~~~~

oTree Lite does not implement support for certain features found in older oTree
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
-   If you try to access a Player/Group/Subsession field whose value is still ``None``,
    oTree will raise an error.
-   Translating an app to multiple languages works differently. See :ref:`i18n`.

Django
~~~~~~

This new implementation does not use Django or Channels in any way.
So, it will not run any code you got from Django documentation, such as Django views, ModelForms, ORM, etc.
