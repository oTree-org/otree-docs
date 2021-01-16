.. _pages:

Pages
=====

Each page that your participants see is defined by a ``Page``.

Your ``page_sequence`` gives the order of the pages.

If your game has multiple rounds, this sequence will be repeated (see :ref:`rounds`).

A ``Page`` can have any of the following methods and attributes.

.. _is_displayed:

is_displayed()
~~~~~~~~~~~~~~

You can define this method to return ``True`` if the page should be shown,
and False if the page should be skipped.
If omitted, the page will be shown.

For example, to only show the page to P2 in each group:

.. code-block:: python

    def is_displayed(self):
        player = self.player
        return player.id_in_group == 2

Or only show the page in round 1:

.. code-block:: python

    def is_displayed(self):
        return self.round_number == 1

If you need to repeat the same rule for many pages, use :ref:`app_after_this_page`.

.. _vars_for_template:

vars_for_template()
~~~~~~~~~~~~~~~~~~~

Use this to pass variables to the template. Example:

.. code-block:: python

    def vars_for_template(self):
        player = self.player
        a = player.num_apples * 10
        return dict(
            a=a,
            b=1 + 1,
        )

Then in the template you can access ``a`` and ``b`` like this:

.. code-block:: html

    Variables {{ a }} and {{ b }} ...

oTree automatically passes the following objects to the template:
``player``, ``group``, ``subsession``, ``participant``, ``session``, and ``Constants``.
You can access them in the template like this: ``{{ Constants.blah }}`` or ``{{ player.blah }}``.

If you need to pass the same variables to many pages,
see :ref:`here <vars_for_many_templates>`.

If the user refreshes the page, ``vars_for_template`` gets re-executed.

.. _before_next_page:

before_next_page()
~~~~~~~~~~~~~~~~~~

Here you define any code that should be executed
after form validation, before the player proceeds to the next page.

If the page is skipped with ``is_displayed``,
then ``before_next_page`` will be skipped as well.

Example:

.. code-block:: python

    def before_next_page(self):
        player = self.player
        player.tripled_apples = player.num_apples * 3


timeout_seconds
~~~~~~~~~~~~~~~

See :ref:`timeouts`

Wait pages
~~~~~~~~~~

See :ref:`wait_pages`

Randomizing page sequence
~~~~~~~~~~~~~~~~~~~~~~~~~

You can randomize the order of pages using rounds.
An example is `here <https://www.otreehub.com/projects/otree-snippets/>`__.

.. _app_after_this_page:

app_after_this_page
~~~~~~~~~~~~~~~~~~~

To skip entire apps, you can define ``app_after_this_page``.
For example, to skip to the next app, you would do:

.. code-block:: python

    def app_after_this_page(self, upcoming_apps):
        player = self.player
        if player.whatever:
            return upcoming_apps[0]

``upcoming_apps`` is the remainder of the ``app_sequence`` (a list of strings).
Therefore, to skip to the last app, you would return ``upcoming_apps[-1]``.
Or you could just return a hardcoded string
(as long as that string is in ``upcoming_apps``):

.. code-block:: python

    def app_after_this_page(self, upcoming_apps):
        player = self.player
        print('upcoming_apps is', upcoming_apps)
        if player.whatever:
            return "public_goods"

If this method doesn't return anything,
the player proceeds to the next page as usual.