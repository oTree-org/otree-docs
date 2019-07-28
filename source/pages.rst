.. _pages:

Pages
=====

Each page that your participants see is defined by a ``Page`` class.

Your ``page_sequence`` variable that gives the order of the pages. For example:

.. code-block:: python

    page_sequence = [Start, Offer, Accept, Results]

If your game has multiple rounds, this sequence will be repeated (see :ref:`rounds`).

A ``Page`` can have any of the following methods and attributes.

.. _is_displayed:

is_displayed()
~~~~~~~~~~~~~~

You can define this function to return ``True`` if the page should be shown,
and False if the page should be skipped.
If omitted, the page will be shown.

For example, to only show the page to P2 in each group:

.. code-block:: python

    class Page1(Page):
        def is_displayed(self):
            return self.player.id_in_group == 2

Or only show the page in round 1:

.. code-block:: python

    class Page1(Page):
        def is_displayed(self):
            return self.round_number == 1

If you need to repeat the same rule for many pages, see :ref:`here <skip_many>`.
Or try out :ref:`app_after_this_page`.


.. _vars_for_template:

vars_for_template()
~~~~~~~~~~~~~~~~~~~

Use this to pass variables to the template. Example:

.. code-block:: python

    class Page1(Page):
        def vars_for_template(self):
            return dict(
                a=1 + 1,
                b=self.player.num_apples * 10
            )

.. note::

    The documentation now uses ``dict()`` instead of ``{}`` in code examples.
    More info `here <https://groups.google.com/forum/#!topic/otree/gSggNVict6g>`__.

Then in the template you can access ``a`` and ``b`` like this:

.. code-block:: html+django

    Variables {{ a }} and {{ b }} ...

oTree automatically passes the following objects to the template:
``player``, ``group``, ``subsession``, ``participant``, ``session``, and ``Constants``.
You can access them in the template like this: ``{{ Constants.blah }}`` or ``{{ player.blah }}``.

If you need to pass the same variables to many pages,
see :ref:`here <vars_for_many_templates>`.

If the user refreshes the page, ``vars_for_template`` gets re-executed.
Keep this in mind before generating random values in ``vars_for_template``.

.. _before_next_page:

before_next_page()
~~~~~~~~~~~~~~~~~~

Here you define any code that should be executed
after form validation, before the player proceeds to the next page.

If the page is skipped with ``is_displayed``,
then ``before_next_page`` will be skipped as well.

Example:

.. code-block:: python

    class Page1(Page):
        def before_next_page(self):
            self.player.tripled_apples = self.player.num_apples * 3

template_name
~~~~~~~~~~~~~

Each Page should have a file in ``templates/`` with the same name.
For example, if your app has this page in ``my_app/pages.py``:

.. code-block:: python

    class Page1(Page):
        pass

Then you should create a file ``my_app/templates/my_app/Page1.html``,
(note that my_app is repeated).
See :ref:`templates` for info on how to write an HTML template.

If the template needs to have a different name from your
page class (e.g. you are sharing the same template for multiple pages),
set ``template_name``. Example:

.. code-block:: python

    class Page1(Page):
        template_name = 'app_name/MyPage.html'

timeout_seconds
~~~~~~~~~~~~~~~

See :ref:`timeouts`

Wait pages
~~~~~~~~~~

See :ref:`wait_pages`

Randomizing page sequence
~~~~~~~~~~~~~~~~~~~~~~~~~

You can randomize the order of pages using rounds.
An example is `here <https://github.com/oTree-org/otree-snippets/tree/master/random_page_order>`__.

.. _app_after_this_page:

app_after_this_page
~~~~~~~~~~~~~~~~~~~

To skip entire apps, you can define ``app_after_this_page``.
For example, to skip to the next app, you would do:

.. code-block:: python

    class MyPage(Page):
        def app_after_this_page(self, upcoming_apps):
            if self.player.whatever:
                return upcoming_apps[0]

``upcoming_apps`` is the remainder of the ``app_sequence`` (a list of strings).
Therefore, to skip to the last app, you would return ``upcoming_apps[-1]``.
Or you could just return a hardcoded string
(as long as that string is in ``upcoming_apps``):

.. code-block:: python

    class MyPage(Page):
        def app_after_this_page(self, upcoming_apps):
            print('upcoming_apps is', upcoming_apps)
            if self.player.whatever:
                return "public_goods"

If this function doesn't return anything,
the player proceeds to the next page as usual.