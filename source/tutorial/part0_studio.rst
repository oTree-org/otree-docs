Part 0: Simple survey (for oTree Studio users)
==============================================

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

.. code-block:: html+django

    Please enter the following information.

    {% formfields %}

    {% next_button %}


Page 2
~~~~~~

Now we define ``Results``.

Set the template's title to something like ``Results`` and set the content to:

.. code-block:: html+django

    <p>Your name is {{ player.name }} and your age is {{ player.age }}.</p>

    {% next_button %}


Define the session config
-------------------------

In the sidebar, go to "Session Configs" and set the following properties:

-   name: my_simple_survey
-   num_demo_participants: 1
-   app_sequence: my_simple_survey


Download and run
----------------

Download the *.otreezip file.
Open your command line (see :ref:`install` for more info).
Make sure you have your command line to the same folder where you downloaded the
*.otreezip file.

Then enter:

    otree runzip

Then open your browser to ``http://localhost:8000`` to try out the survey.

If there are any problems,
you can ask a question on the oTree
`discussion group <https://groups.google.com/forum/#!forum/otree>`__.
