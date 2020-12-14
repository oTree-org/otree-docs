:orphan:

.. _mturknostudio:

MTurk setup (without Studio)
============================

If you are not using oTree Studio, here are the extra steps to set up Mechanical Turk
integration.

.. note::

    As of October 2019, oTree is using a new MTurk format.
    If you ran studies previously, see `here <https://github.com/oTree-org/otree-docs/blob/master/source/misc/mturk_newformat.rst>`__.


Installation
------------

In your ``requirements.txt`` or ``requirements_base.txt`` (not both), you should change ``otree`` to ``otree[mturk]``.

Preview template
----------------

Create an file (empty for now) called ``_templates/global/mturk_template.html``.

Session config
--------------

In ``SESSION_CONFIG_DEFAULTS``, add:

.. code-block:: python

    mturk_hit_settings=dict(
        keywords='bonus, study',
        title='Title for your experiment',
        description='Description for your experiment',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=60,
        expiration_hours=7 * 24,
        qualification_requirements=[]
        # grant_qualification_id='YOUR_QUALIFICATION_ID_HERE', # to prevent retakes
    ),
