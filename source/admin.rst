Admin
=====

oTree's admin interface lets you create, monitor,
and export data from sessions.

Open your browser to *http://localhost:8000/* or whatever you server's URL is.

.. _AUTH_LEVEL:

Password protection
-------------------

When you first install oTree, The entire admin interface is accessible
without a password. However, when you are ready to deploy to your audience,
you should password protect the admin.

If you are launching an experiment and want visitors to only be able to
play your app if you provided them with a start link, set the
environment variable ``OTREE_AUTH_LEVEL`` to ``STUDY``.

To put your site online in public demo mode where
anybody can play a demo version of your game
(but not access the full admin interface), set ``OTREE_AUTH_LEVEL``
to ``DEMO``.

If you don't want any password protection at all,
leave this variable unset/blank.

Start links
-----------

There are multiple types of start links you can use.

Rooms
~~~~~

In most cases where you are doing a study, the best
way to set up URLs is to make a :ref:`room <rooms>`.

.. _single_use_links:

Single-use links
~~~~~~~~~~~~~~~~

If a room is not suited for your needs,
you can use oTree's single-use links.
Every time you create a session, you will need to re-distribute URLs
to each participant.

Session-wide link
~~~~~~~~~~~~~~~~~

The session-wide link lets you provide
the same start link to all participants in the session.
Note: this may result in the same participant playing twice, unless you use the
``participant_label`` parameter in the URL (see :ref:`participant_label`).

Before using the session-wide link, consider using a
:ref:`room <rooms>`, because you can also use a room without a
participant label file to allow everyone to play with the same URL.
The advantage of using a room is that the URL is simpler to type
(doesn't contain a randomly generated code),
and you can reuse it across sessions.

.. _participant_label:

Participant labels
------------------

Whether or not you're using a :ref:`room <rooms>`,
you can append a ``participant_label`` parameter to each participant's start
URL to identify them, e.g. by name, ID number, or computer workstation.
For example::

    http://localhost:8000/room/my_room_name/?participant_label=John

oTree will record this participant label. It
will be used to identify that participant in the
oTree admin interface and the payments page, etc.
You can also access it from your code as ``self.participant.label``.

Arrival order
-------------

oTree will assign the first person who arrives to be P1, the second to be P2, etc.,
unless you are using single-use links.

.. _edit_config:

Configure sessions
------------------

You can make your session configurable,
so that you can adjust the game's parameters in the admin interface,
without needing to edit the source code:

.. image:: _static/admin/edit-config.png
    :align: center


For example, let's say you are making a public goods game,
whose payoff function depends on
an "multiplier" parameter that is a numeric constant,
like 1.5 or 2. The usual approach would be to define it in ``Constants``,
e.g. ``Constants.multiplier``

However, to make your custom parameter configurable, instead of adding it to
``Constants``, add it to your config in :ref:`SESSION_CONFIGS`. For example:

.. code-block:: python

    dict(
        name='my_session_config',
        display_name='My Session Config',
        num_demo_participants=2,
        app_sequence=['my_app_1', 'my_app_2'],
        multiplier=1.5
    ),

Then, when you create a session in the admin interface
and select this session config, the ``multiplier`` parameter will
be listed, and you can change it to a number other than 1.5.
If you want to explain the meaning of the variable to the person creating
the session, you can add a ``'doc'`` parameter to the session config dict, e.g.:

.. code-block:: python

    dict(
        name='my_session_config',
        display_name='My Session Config',
        num_demo_participants=2,
        app_sequence=['my_app_1', 'my_app_2'],
        multiplier=1.5,
        doc="""
        Edit the 'multiplier' parameter to change the factor by which
        contributions to the group are multiplied.
        """
    ),

Then in your app's code, you can do ``self.session.config['multiplier']``
to retrieve the current session's multiplier.

Notes:

-   For a field to be configurable, its value must be a simple data type
    (number, boolean, or string).
-   On the "Demo" section of the admin, sessions are not configurable.
    It's only available when creating a session in "Sessions" or "Rooms".

Also see :ref:`session_config_treatments`.

.. _admin_report:

Customizing the admin interface (admin reports)
-----------------------------------------------

You can add a custom tab to a session's admin page with any content you want;
for example:

-   A chart/graph with the game's results
-   A custom payments page that is different from oTree's built-in one

Here is a screenshot:

.. image:: _static/admin/admin-report.png
    :align: center

Here is a trivial example, where we add an admin report that
displays a sorted list of payoffs for a given round.

First, define a method ``vars_for_admin_report`` on the Subsession.
This works the same way as :ref:`vars_for_template`.
For example:

.. code-block:: python

    class Subsession(BaseSubsession):
        def vars_for_admin_report(self):
            payoffs = sorted([p.payoff for p in self.get_players()])
            return dict(payoffs=payoffs)

Then create an includable template ``admin_report.html``
in your app, and display whatever variables were passed in ``vars_for_admin_report``:

.. code-block:: html+django

    {% load otree %}

    <p>Here is the sorted list of payoffs in round {{ subsession.round_number }}</p>

    <ul>
        {% for payoff in payoffs %}
            <li>{{ payoff }}</li>
        {% endfor %}
    </ul>

Notes:

-   ``subsession``, ``session``, and ``Constants`` are passed to the template
    automatically.
-   ``AdminReport.html`` does not need to use ``{% block %}`` or ``{% extends %}``  etc.
    The above example is valid as the full contents of ``AdminReport.html``.

If one or more apps in your session have an ``AdminReport.html``,
your admin page will have a "Reports" tab. Use the menu to select the app
and the round number, to see the report for that subsession.

Tip: if you are displaying the same chart in the admin report and participant pages,
you can reuse ``AdminReport.html`` in the participant template with an ``{% include %}``,
and pass the variables like this:

.. code-block:: python

    class Results(Page):

        def vars_for_template(self):
            return self.subsession.vars_for_admin_report()


If you're generating a chart with JavaScript,
remember to use the :ref:`|json <json>` filter.


Kiosk Mode
----------

During a lab study you may want to restrict participants from doing things like:

-   Closing the browser window
-   Clicking the "back" button
-   Viewing the URL in the address bar

You can restrict these things with "kiosk mode", a setting available in
most web browsers.
Consult your web browser's documentation for information on how to enable
kiosk mode.


Monitor sessions
----------------

The admin interface lets you monitor the live progress of your sessions.

Payments page
-------------

At the end of your session, you can open and print a page that lists all
the participants and how much they should be paid.

.. figure:: _static/admin/nSMlWcY.png
   :alt:


Export Data
-----------

In the admin interface, click on "Data"
(try http://localhost:8000/export/)
to download your data as CSV or Excel.

Autogenerated documentation
---------------------------

If you add a ``doc=`` argument to your model fields like this:

.. code-block:: python

    class Player(BasePlayer):
        contribution = models.IntegerField(doc="how much this player contributed")

It will be included in a "documentation"
file that is available on the "Data Export" page.

Debug Info
----------

When oTree runs in ``DEBUG`` mode (i.e. when the environment variable
``OTREE_PRODUCTION`` is not set), debug information is displayed
on the bottom of all screens.
