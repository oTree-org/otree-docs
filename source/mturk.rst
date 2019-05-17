Mechanical Turk
===============

Overview
--------

oTree provides integration with Amazon Mechanical Turk (MTurk):

-   From oTree's admin interface, you publish your game to MTurk.
-   Workers on Mechanical Turk play your app as an MTurk HIT.
-   From oTree's admin interface, you send each participant their participation fee
    and bonus (payoff).

.. warning::

    Use caution when running games on Mechanical Turk with live interaction
    between participants (i.e. wait pages). See below.

Extra steps for non-Studio users
--------------------------------

If you are not using oTree Studio, you need to additionally follow the steps
ref:`here <mturk_nostudio>`.

AWS credentials
---------------

You must create an employer account with MTurk,
and then enter your MTurk keys into oTree.

You can obtain these credentials `here <https://console.aws.amazon.com/iam/home?#security_credential>`__:

.. figure:: _static/mturk/dNhkOiA.png
   :alt: AWS key

If using Heroku, go to your App Dashboard's "settings",
and set ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.

.. warning::

    When testing with oTree, don't keep too much money in your MTurk account,
    in case something goes wrong.

Making your session work on MTurk
---------------------------------

The monetary reward paid to workers is
``self.session.config['participation_fee']``.

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

From the oTree admin interface, click on "Sessions" and then,
on the split button "Create New Session", select "For MTurk":

.. figure:: _static/mturk/create-mturk-session.png

Once you have created the session, you will see an "MTurk" tab in the session's admin page.

After publishing the HIT you can test it both as a worker and as a
requester using the links provided on the "MTurk" Tab of your session admin
panel.

.. _qualification-requirements:

Qualification requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~

oTree uses boto3 syntax for qualification requirements.
Here is an example with 2 qualification requirements:

.. code-block:: python

        [
            {
                'QualificationTypeId': "3AWO4KN9YO3JRSN25G0KTXS4AQW9I6",
                'Comparator': "DoesNotExist",
            },
            {
                'QualificationTypeId': "4AMO4KN9YO3JRSN25G0KTXS4AQW9I7",
                'Comparator': "DoesNotExist",
            },
        ]

If you are using oTree Studio, paste these requirements into your "qualification_requirements"
box. If you are not using oTree Studio, they go in your ``"qualification_requirements"``
in ``settings.py``.

Here is how you would require workers from the US.
(`00000000000000000071` is the code for a location-based qualification.)

.. code-block:: python

        [
            {
                'QualificationTypeId': "00000000000000000071",
                'Comparator': "EqualTo",
                'LocaleValues': [{'Country': "US"}]
            },
        ]

See the
`MTurk API reference <http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html>`__.
(However, note that the code examples there are in JavaScript, so you would need
to modify the syntax to make it work in Python, e.g. adding quotes around dictionary keys.)


Preventing retakes (repeat workers)
-----------------------------------

To prevent a worker from participating in your study twice,
you can grant a Qualification to each worker who participates in your study,
and then prevent people who already have this qualification from participating in your studies.

This technique is described
`here <http://turkrequesters.blogspot.kr/2014/08/how-to-block-past-workers-from-doing.html?spref=tw>`__.

First, login to your MTurk requester account and create a qualification.
(If you are testing with the MTurk sandbox, you need to create the qualification
in the sandbox as well.)
Then, paste the qualification's ID into ``grant_qualification_id``.
Then, add an entry to ``qualification_requirements``:

.. code-block:: python

        {
            'QualificationTypeId': "YOUR_QUALIFICATION_ID_HERE",
            'Comparator': "DoesNotExist",
        },


Multiplayer games
-----------------

Games that involve synchronous interaction between participants (i.e.
wait pages) are difficult on Mechanical Turk,
because some participants
drop out or delay starting the game until some time after
accepting the assignment. This causes other participants to be stuck on a wait page,
which can upset your MTurk workers, who then give you negative reviews.

To mitigate this, see the recommendations in :ref:`wait-page-stuck`.
Also, there are some discussions on the
`oTree mailing list <https://groups.google.com/forum/#!forum/otree>`__ on this
subject.

Another issue is with group sizes. When you create a session with N participants
for MTurk, oTree actually creates (N x 2) participants, because spares are needed
in case some MTurk workers start but then return the assignment. This may conflict
with some people's grouping code.

Managing your HITs
------------------

oTree provides the ability to approve/reject assignments,
send bonuses, and expire HITs early.
If you want to do anything beyond this
(e.g. extend expiration date, interact with workers,
send custom bonuses, etc), you will need to install the
`MTurk command-line tools <https://aws.amazon.com/cli/>`__
or use the 3rd party
`Manage HITs Individually <https://manage-hits-individually.s3.amazonaws.com/v4.0/index.html#/credentials>`__
tool.
