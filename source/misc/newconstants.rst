.. _newconstants:

2022 Constants format change
============================

Super short version
-------------------

To ensure your code is following the latest format, run this::

    pip3 install -U otree
    otree upcase_constants


Details
-------

As of January 2022, there is a new format for constants.

It changes from this:

.. code-block:: python

    class Constants(BaseConstants):
        name_in_url = 'public_goods'
        players_per_group = 3
        num_rounds = 1
        xyz = 42

To this:

.. code-block:: python

    class C(BaseConstants):
        NAME_IN_URL = 'public_goods'
        PLAYERS_PER_GROUP = 3
        NUM_ROUNDS = 1
        XYZ = 42

Then to reference a constant, do ``C.NUM_ROUNDS`` or ``C.XYZ``.

If you want to update your existing projects to the new format,
run the commands at the top of this page.

Starting with oTree 5.7, newly created apps use this new all-caps format.

Using the new constants format is not mandatory, but is recommended so that you can be consistent with the documentation
and latest code samples. The previous format will continue to work fine.

The purpose of the change is to harmonize oTree's code style,
especially in preparation for upcoming features.
(Also, if you have prior experience in Python,
you know that ALL_CAPS is the convention for defining constants.)

If you are running an old version of oTree and try to run a project written with the new format,
you will get the error ``Constants class is missing`` when trying to start the server.

For oTree Studio users
----------------------

Your code has already been updated.

If you haven't updated oTree recently, just run::

    pip3 install -U otree
