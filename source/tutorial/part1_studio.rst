.. _tutorial-studio:

Part 1: Simple survey (for oTree Studio users)
==============================================

(A video of this tutorial is on
`YouTube <https://www.youtube.com/channel/UCR9BIa4PqQJt1bjXoe7ffPg/videos>`__
)

Let's create a simple survey -- on the first page, we ask the participant
for their name and age, then on the next page, display this info back to them.

Player model
------------

In the sidebar, go to the Player model.
Let's add 2 fields:

-   ``name`` (``StringField``, meaning text characters)
-   ``age`` (``IntegerField``)


Pages
-----

This survey has 2 pages:

-  Page 1: players enter their name and age
-  Page 2: players see the data they entered on the previous page

So, create 2 pages in your ``page_sequence``: ``Survey`` and ``Results``.

Page 1
~~~~~~

First let's define ``Survey``. This page contains a form, so set ``form_model``
to ``player`` and for ``form_fields``, select ``name`` and ``age``.

Then, set the template's title to ``Enter your information``, and set the content to:

.. code-block:: html+djang0

    Please enter the following information.

    {% formfields %}

    {% next_button %}


Page 2
~~~~~~

Now we define ``Results``.

Set the template's ``title`` block to ``Results`` and set the ``content`` block to:

.. code-block:: html+djang0

    <p>Your name is {{ player.name }} and your age is {{ player.age }}.</p>

    {% next_button %}


Define the session config
-------------------------

In the sidebar, go to "Session Configs", create a session config, and add your survey app to the ``app_sequence``.


Download and run
----------------

Download the otreezip file and follow the instructions on how to install
oTree and run the otreezip file.

If there are any problems,
you can ask a question on the oTree
`discussion group <https://groups.google.com/forum/#!forum/otree>`__.
