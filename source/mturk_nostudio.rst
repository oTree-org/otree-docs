:orphan:

.. _mturknostudio:

MTurk Studio setup (without Studio)
===================================

If you are not using oTree Studio, here are the extra steps to set up Mechanical Turk
integration.

Installation
------------

If you want to use oTree with MTurk,
you need to install ``otree[mturk]`` instead of just ``otree``.

In your ``requirements_base.txt``, you should also change ``otree`` to ``otree[mturk]``.

Preview template
----------------

Create an file (empty for now) called ``_templates/global/mturk_template.html``.

Session config
--------------

In ``SESSION_CONFIG_DEFAULTS``, add an entry called `mturk_hit_settings` whose value is:

.. code-block:: python

    dict(
        keywords='bonus, study',
        title='Title for your experiment',
        description='Description for your experiment',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=60,
        expiration_hours=7 * 24,
        qualification_requirements=[]
        # grant_qualification_id='YOUR_QUALIFICATION_ID_HERE', # to prevent retakes
    )
