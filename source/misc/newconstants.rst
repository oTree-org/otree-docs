.. _newconstants:

2022 Constants format change
============================

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
run ``otree upcase_constants`` (requires oTree 5.4 (September 2021) or higher).

It's not mandatory, but is recommended so that you can be consistent with the documentation
and latest code samples. The previous format will continue to work fine.

The purpose of the change is to harmonize oTree's code style,
especially in preparation for upcoming features.
(Also, if you have prior experience in Python,
you know that ALL_CAPS is the convention for defining constants.)

If you use oTree Studio, your code has already been automatically upgraded to the new format.
If you haven't upgraded oTree recently, run ``pip3 install -U otree``.