Admin
=====

oTree comes with an admin interface, so that experimenters can manage
sessions, monitor the progress of live sessions, and export data after
sessions.

Open your browser to the root url of your web application. If you're
developing locally, this will be *http://127.0.0.1:8000/*.


Lab Experiments
---------------

Creating sessions
~~~~~~~~~~~~~~~~~

Create a session in the admin. [TODO: more info]


Opening links
~~~~~~~~~~~~~

To launch a session, each participant must open their link. There are 2
options for how to open URLs.

Lab
^^^

In the admin interface, go to the "global data" section, and copy the
"lab link". This is a permanent URL that will last as long as you use
the same server [TODO: finish]

Each workstation has a permanent URL that, when clicked, will route the
participant to the currently active session.

choose an active session from the dropdown. Then, copy

Unique URLs
^^^^^^^^^^^

If you are running your experiment in a lab, you should deploy the links
to the target workstations using whatever means is available to you. If
you have a tool that can push distinct URLs to each PC in the lab, you
can use that. Or you can set up a unique email account for each
workstation, and then send the unique links to PCs using a mail merge.
Then open the link on each PC.

Participant labels
^^^^^^^^^^^^^^^^^^

oTree uses a unique code to identify each participant. However, you can
assign each participant a "label" that can be any convenient way to
identify them to you, such as:

-  Name
-  Computer workstation number
-  Email address
-  ID number

This label will be displayed in places where participants are listed,
like the oTree admin interface or the payments page.

You can assign each participant a label by adding a parameter to each
start link. For example, if you want to assign a participant the label
"WORKSTATION\_1", you would take the start link for that participant:

::

    http://[participant's start link]

And change it to:

::

    http://[participant's start link]?participant_label=WORKSTATION_1

Outside of oTree, you can create a script that adds a unique
``participant_label`` to each start link as indicated above. Then, when
the link is opened, the oTree server will register that participant
label for that participant.

Monitor sessions
~~~~~~~~~~~~~~~~

While your session is ongoing, you can monitor the live progress in the
admin interface. The admin tables update live, highlighting changes as
they occur. The most useful table to monitor is "Session participants",
which gives you a summary of all the participants' progress. You can
also click the "participants" table of each app to see the details of
all the data being entered in your subsessions.

Authenticaton
-------------

When you first install oTree, The entire admin interface is accessible
without a password. However, when you are ready to launch your oTree
app, you should password protect the admin so that visitors and
participants cannot access sensitive data.

If you are launching an experiment and want visitors to only be able to
play your app if you provided them with a start link, set the
environment variable ``OTREE_AUTH_LEVEL`` to ``EXPERIMENT``.

If you would like to put your site online in public demo mode where
anybody can play a demo version of your game, set ``OTREE_AUTH_LEVEL``
to ``DEMO``. This will allow people to play in demo mode, but not access
the full admin interface.

Online experiments
------------------

Experiments can be launched to participants playing over the internet,
in a similar way to how experiments are launched the lab. Login to the
admin, create a session, then distribute the links to participants via
email or a website.

In a lab, you usually can start all participants at the same time, but
this is often not possible online, because some participants might click
your link hours after other participants. If your game requires players
to play in groups, you may want to set the ``group_by_arrival_time`` key
in session type dictionary to ``True``. This will group players in the
order in which they arrive to your site, rather than randomly, so that
players who arrive around the same time play with each other.

Kiosk Mode
----------

During an experiment, subjects are expected to stay on the given
pages/game, instead of browsing irrelevant websites or using other
applications. Kiosk mode locks down the oTree pages on a web browser
thus allows the subjects to focus. Here we provide some guidelines to
initiate Kiosk mode with different browsers/on various systems. In
general, Kiosk mode is rather user-friendly so one can easily search
online how to use it on specific platforms.

iOS (iPhone/iPad)
~~~~~~~~~~~~~~~~~

1. Go to Setting – Accessibility – Guided Access
2. Turn on Guided Access and set a passcode for your Kiosk mode
3. Open your web browser and enter your URL
4. Triple-click home button to initiate Kiosk mode
5. Circle areas on the screen to disable (e.g. URL bar) and activate

Android
~~~~~~~

There are several apps for using Kiosk mode on Android, for instance:
`Kiosk Browser
Lockdown <https://play.google.com/store/apps/details?id=com.procoit.kioskbrowser&hl=en>`__.

.. image:: _static/admin/android.png
    :align: center
    :scale: 100 %


oTree comes with an admin interface, so that experimenters can manage
sessions, monitor the progress of live sessions, and export data after
sessions.

Open your browser to the root url of your web application. If you're
developing locally, this will be http://127.0.0.1:8000/.

Lab Experiments
---------------

Creating sessions
~~~~~~~~~~~~~~~~~

Create a session in the admin. [TODO: more info]

Opening links
~~~~~~~~~~~~~

To launch a session, each participant must open their link. There are 2
options for how to open URLs.

Lab
^^^

In the admin interface, go to the "global data" section, and copy the
"lab link". This is a permanent URL that will last as long as you use
the same server [TODO: finish]

Each workstation has a permanent URL that, when clicked, will route the
participant to the currently active session.

choose an active session from the dropdown. Then, copy

Unique URLs
^^^^^^^^^^^

If you are running your experiment in a lab, you should deploy the links
to the target workstations using whatever means is available to you. If
you have a tool that can push distinct URLs to each PC in the lab, you
can use that. Or you can set up a unique email account for each
workstation, and then send the unique links to PCs using a mail merge.
Then open the link on each PC.

Participant labels
^^^^^^^^^^^^^^^^^^

oTree uses a unique code to identify each participant. However, you can
assign each participant a "label" that can be any convenient way to
identify them to you, such as:

-  Name
-  Computer workstation number
-  Email address
-  ID number

This label will be displayed in places where participants are listed,
like the oTree admin interface or the payments page.

You can assign each participant a label by adding a parameter to each
start link. For example, if you want to assign a participant the label
"WORKSTATION\_1", you would take the start link for that participant:

::

    http://[participant's start link]

And change it to:

::

    http://[participant's start link]?participant_label=WORKSTATION_1

Outside of oTree, you can create a script that adds a unique
``participant_label`` to each start link as indicated above. Then, when
the link is opened, the oTree server will register that participant
label for that participant.

Monitor sessions
~~~~~~~~~~~~~~~~

While your session is ongoing, you can monitor the live progress in the
admin interface. The admin tables update live, highlighting changes as
they occur. The most useful table to monitor is "Session participants",
which gives you a summary of all the participants' progress. You can
also click the "participants" table of each app to see the details of
all the data being entered in your subsessions.

Authenticaton
-------------

When you first install oTree, The entire admin interface is accessible
without a password. However, when you are ready to launch your oTree
app, you should password protect the admin so that visitors and
participants cannot access sensitive data.

If you are launching an experiment and want visitors to only be able to
play your app if you provided them with a start link, set the
environment variable ``OTREE_AUTH_LEVEL`` to ``EXPERIMENT``.

If you would like to put your site online in public demo mode where
anybody can play a demo version of your game, set ``OTREE_AUTH_LEVEL``
to ``DEMO``. This will allow people to play in demo mode, but not access
the full admin interface.

Online experiments
------------------

Experiments can be launched to participants playing over the internet,
in a similar way to how experiments are launched the lab. Login to the
admin, create a session, then distribute the links to participants via
email or a website.

In a lab, you usually can start all participants at the same time, but
this is often not possible online, because some participants might click
your link hours after other participants. If your game requires players
to play in groups, you may want to set the ``group_by_arrival_time`` key
in session type dictionary to ``True``. This will group players in the
order in which they arrive to your site, rather than randomly, so that
players who arrive around the same time play with each other.

Kiosk Mode
----------

During an experiment, subjects are expected to stay on the given
pages/game, instead of browsing irrelevant websites or using other
applications. Kiosk mode locks down the oTree pages on a web browser
thus allows the subjects to focus. Here we provide some guidelines to
initiate Kiosk mode with different browsers/on various systems. In
general, Kiosk mode is rather user-friendly so one can easily search
online how to use it on specific platforms.

iOS (iPhone/iPad)
~~~~~~~~~~~~~~~~~

1. Go to Setting – Accessibility – Guided Access
2. Turn on Guided Access and set a passcode for your Kiosk mode
3. Open your web browser and enter your URL
4. Triple-click home button to initiate Kiosk mode
5. Circle areas on the screen to disable (e.g. URL bar) and activate

Android
~~~~~~~

There are several apps for using Kiosk mode on Android, for instance:
`Kiosk Browser
Lockdown <https://play.google.com/store/apps/details?id=com.procoit.kioskbrowser&hl=en>`__.

.. figure:: _static/admin//VJ72fKv.png
   :alt:

For iOS and Android tablets, Kiosk mode will continue to function after
normal restart. However, if subjects enter Android safe mode, the app
can be disabled.

Chrome on PC
~~~~~~~~~~~~

1. Go to Setting – Users – Add new user
2. Create a new user with a desktop shortcut
3. Right-click the shortcut and select “Properties”
4. In the “Target” filed, add to the end either
   ``--kiosk "http://www.your-otree-server.com"`` or
   ``--chrome-frame  --kiosk "http://www.your-otree-server.com"``
5. Disable hotkeys (see
   `here <http://superuser.com/questions/727072/what-windows-shortcuts-should-be-blocked-on-a-kiosk-mode-pc>`__)
6. Open the shortcut to activate Kiosk mode

IE on PC
~~~~~~~~

IE on PC See `here <http://support2.microsoft.com/kb/154780>`__

Mac
~~~

There are several apps for using Kiosk mode on Mac, for instance:
`eCrisper <http://ecrisper.com/>`__. Mac keyboard shortcuts should be
disabled.

Payment PDF
-----------

At the end of your session, you can open and print a page that lists all
the participants and how much they should be paid.

.. figure:: _static/admin/nSMlWcY.png
   :alt:

Export Data
-----------

You can download your raw data in text format (CSV) so that you can view
and analyze it with a program like Excel, Stata, or R.

Autogenerated documentation
---------------------------

Each model field you define can also have a ``doc=`` argument. Any
string you add here will be included in the autogenerated documentation
file, which can be downloaded through the data export page in the admin.

Debug Info
----------

Any application can be run so that that debug information is displayed
on the bottom of all screens. The debug information consists of the ID
in group, the group, the player, the participant label, and the session
code. The session code and participant label are two randomly generated
alphanumeric codes uniquely identifying the session and participant. The
ID in group identifes the role of the player (e.g., in a principal-agent
game, principals might have the ID in group 1, while agents have 2).

.. figure:: _static/admin/DZsyhQf.png
   :alt:

Progress-Monitor
----------------

The progress monitor allows the researcher to monitor the progress of an
experiment. It features a display that can be **filtered** and
**sorted**, for example by computer name or group. The experimenter can
see the progress of all participants, including their current action and
taken decisions. Updates are shown as they happen **in real time** and
cells that change are highlighted in yellow. Because the progress
monitor is web-based, **multiple collaborators can simultaneously open
it on several devices on premises or at remote locations**.

.. figure:: _static/admin/0nYKnDp.png
   :alt:

Session Interface
-----------------

The session interface is an optional feature convenient in some
experiments. In many experimental settings, in addition to monitoring,
**an experimenter needs to receive instructions or provide input for the
experiment**. The session interface can instruct an experimenter on what
to do next and show text to be read aloud. The session interface can
also request input from the experimenter at a specific point in the
session. For example, in an Ellsberg experiment, the experimenter might
roll an opaque urn prior to the session; the session interface will
remind the experimenter to show the urn to the participants, tell the
experimenter when all participants have selected their bets, and
instruct her to draw a ball from the urn. It will then ask the drawn
color, so that oTree can calculate participants' payoff's.

For iOS and Android tablets, Kiosk mode will continue to function after
normal restart. However, if subjects enter Android safe mode, the app
can be disabled.

Chrome on PC
~~~~~~~~~~~~

1. Go to Setting – Users – Add new user
2. Create a new user with a desktop shortcut
3. Right-click the shortcut and select “Properties”
4. In the “Target” filed, add to the end either
   ``--kiosk "http://www.your-otree-server.com"`` or
   ``--chrome-frame  --kiosk "http://www.your-otree-server.com"``
5. Disable hotkeys (see
   `here <http://superuser.com/questions/727072/what-windows-shortcuts-should-be-blocked-on-a-kiosk-mode-pc>`__)
6. Open the shortcut to activate Kiosk mode

IE on PC
~~~~~~~~

IE on PC See `here <http://support2.microsoft.com/kb/154780>`__

Mac
~~~

There are several apps for using Kiosk mode on Mac, for instance:
`eCrisper <http://ecrisper.com/>`__. Mac keyboard shortcuts should be
disabled.

Payment PDF
-----------

At the end of your session, you can open and print a page that lists all
the participants and how much they should be paid.

.. figure:: _static/admin/nSMlWcY.png
   :alt:

Export Data
-----------

You can download your raw data in text format (CSV) so that you can view
and analyze it with a program like Excel, Stata, or R.

Autogenerated documentation
---------------------------

Each model field you define can also have a ``doc=`` argument. Any
string you add here will be included in the autogenerated documentation
file, which can be downloaded through the data export page in the admin.

Debug Info
----------

Any application can be run so that that debug information is displayed
on the bottom of all screens. The debug information consists of the ID
in group, the group, the player, the participant label, and the session
code. The session code and participant label are two randomly generated
alphanumeric codes uniquely identifying the session and participant. The
ID in group identifes the role of the player (e.g., in a principal-agent
game, principals might have the ID in group 1, while agents have 2).

.. figure:: _static/admin/DZsyhQf.png
   :alt:

Progress-Monitor
----------------

The progress monitor allows the researcher to monitor the progress of an
experiment. It features a display that can be **filtered** and
**sorted**, for example by computer name or group. The experimenter can
see the progress of all participants, including their current action and
taken decisions. Updates are shown as they happen **in real time** and
cells that change are highlighted in yellow. Because the progress
monitor is web-based, **multiple collaborators can simultaneously open
it on several devices on premises or at remote locations**.

.. figure:: _static/admin/0nYKnDp.png
   :alt:

Session Interface
-----------------

The session interface is an optional feature convenient in some
experiments. In many experimental settings, in addition to monitoring,
**an experimenter needs to receive instructions or provide input for the
experiment**. The session interface can instruct an experimenter on what
to do next and show text to be read aloud. The session interface can
also request input from the experimenter at a specific point in the
session. For example, in an Ellsberg experiment, the experimenter might
roll an opaque urn prior to the session; the session interface will
remind the experimenter to show the urn to the participants, tell the
experimenter when all participants have selected their bets, and
instruct her to draw a ball from the urn. It will then ask the drawn
color, so that oTree can calculate participants' payoff's.
