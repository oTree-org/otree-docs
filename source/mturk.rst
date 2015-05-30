Amazon Mechanical Turk
======================

Overview
--------

oTree provides integration with Amazon Mechanical Turk (MTurk).

You can publish your game to MTurk directly from
oTree's admin interface. Then, workers on mechanical Turk can accept and
play your app as an MTurk HIT and get paid a participation fee as well
as bonuses they earned by playing your game.

AWS credentials
---------------

To publish to MTurk, you must have an employer account with MTurk, which currently
requires a U.S. address and bank account.

oTree requires that you set the following env vars:

- ``AWS_ACCESS_KEY_ID``
- ``AWS_SECRET_ACCESS_KEY``

You can obtain these credentials `here <https://console.aws.amazon.com/iam/home?#security_credential>`__:

.. figure:: _static/mturk/dNhkOiA.png
   :alt: AWS key

   AWS key

On Heroku you would set these env vars like this:

.. code-block:: bash

    $ heroku config:set AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
    $ heroku config:set AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY

Making your session work on MTurk
---------------------------------

You should look in ``settings.py`` for all settings related to
Mechanical Turk (do a search for "mturk"). You can edit the properties
of the HIT such as the title and keywords, as well as the qualifications
required to participate. The monetary reward paid to workers is the
``participation_fee`` for your ``session_type``.

When you publish your HIT to MTurk, it will be visible to workers. When
a worker clicks on the link to take part in the HIT, they will see the
MTurk interface, with your app loaded inside a frame (as an
``ExternalQuestion``). Initially, they will be in preview mode, and will
see the ``preview_template`` you specify in ``settings.py``. After they
accept the HIT, they will see the first page of your session, and be
able to play your session while it is embedded inside a frame in the
MTurk worker interface.

The only modification you should make to your app for it to work on AMT
is to add a ``{% next_button %}`` to the final page that your
participants see. When the participant clicks this button, they will be
directed back to the mechanical Turk website and their work will be
submitted.

After workers have completed the session, you can click on the
"payments" Tab for your session. Here, you will be able to approve
submissions, and also pay the bonuses that workers earned in your game.

Testing your hit in sandbox
---------------------------

The Mechanical Turk Developer Sandbox is a simulated environment that
lets you test your app prior to publication in
the marketplace. This environment is available for both
`worker <https://workersandbox.mturk.com/mturk/welcome>`__ and
`requester <https://requester.mturk.com/developer/sandbox>`__.

After publishing the HIT you can test it both as a worker and as a
requester using the links provided on "MTurk" Tab of your session admin
panel.

Multiplayer games
-----------------

Games that involve synchronous interaction between participants (i.e.
wait pages) can be tricky on mechanical Turk. First, you should set
``group_by_arrival_time`` as ``True`` so that participants are assigned
to groups in the order in which they arrive, to minimize unnecessary
waiting time.

However, there is still the issue that if one participant drops out then
other participants might be stuck on a wait page. One way to mitigate
this attrition problem is to use a "lock-in" task. In other words,
before your multiplayer game, you can have a subsession that is a
single-player app and takes some effort to complete. The idea is that a
participant takes the effort to complete this initial task, they are
less likely to drop out after that point. Then, the first few
participants to finish the lock in task will be assigned to the same
group in the next subsession, which is the multiplayer game.

An upcoming feature in oTree that has not yet been implemented is the
ability to auto-submit pages if the participant drops out or does not
complete the page in time. This should enable the gameplay to proceed
even if there is attrition.

