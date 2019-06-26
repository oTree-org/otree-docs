Mechanical Turk
===============

Overview
--------

oTree provides integration with Amazon Mechanical Turk (MTurk):

#.  From oTree's admin interface, you publish your game to MTurk.
#.  Workers on Mechanical Turk play your app as an MTurk HIT.
#.  From oTree's admin interface, you send each participant their participation fee
    and bonus (payoff).

.. warning::

    Use caution when running games on Mechanical Turk with live interaction
    between participants (i.e. wait pages). See below.

Extra steps for non-Studio users
--------------------------------

If you are not using oTree Studio, you need to additionally follow the steps
:ref:`here <mturknostudio>`.

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

When an oTree experiment is published on MTurk, it is embedded inside a rectangular
frame within the mturk.com interface. The first page participants see is your
``preview_template``. They will then click MTurk's "accept" button to proceed.

Unlike non-MTurk experiments, you need a ``{% next_button %}`` even on the final page that your
participants see. Clicking this button will submit the HIT and take the user back to MTurk.

In the admin interface for the session, the "Payments" tab lets you accept submitted assignments
and pay workers.

Publishing a HIT
----------------

From the oTree admin interface, click on "Sessions" and then,
on the button that says "Create New Session", select "For MTurk":

.. figure:: _static/mturk/create-mturk-session.png

The session's admin page will have an "MTurk" tab.
This is where you publish the HIT.
You can choose to first publish the HIT in the sandbox,
which lets you see how it will appear to workers.

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

Note: when you are in sandbox mode, oTree does not apply qualification requirements,
in order to make testing easier.

Preventing retakes (repeat workers)
-----------------------------------

To prevent a worker from participating twice,
you can grant a Qualification to each worker in your study,
and then block people who already have this Qualification.

This technique is described
`here <http://turkrequesters.blogspot.kr/2014/08/how-to-block-past-workers-from-doing.html?spref=tw>`__.

Login to your MTurk requester account and create a qualification.
Go to your oTree MTurk settings and paste that qualification ID into ``grant_qualification_id``.
Then, add an entry to ``qualification_requirements``:

.. code-block:: python

        {
            'QualificationTypeId': "YOUR_QUALIFICATION_ID_HERE",
            'Comparator': "DoesNotExist",
        },


Multiplayer games
-----------------

Games that involve wait pages are difficult on Mechanical Turk,
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
