:orphan:

.. _mturknostudio:

MTurk Studio setup (without Studio)
===================================

If you are not using oTree Studio, here are the steps to set up Mechanical Turk
integration.

Installation
------------

If you want to use oTree with MTurk,
you need to install ``otree[mturk]`` instead of just ``otree``.

In your ``requirements_base.txt``, you should also change ``otree`` to ``otree[mturk]``.

Next, copy the following lines (exactly as is) to your ``settings.py``.
``environ.get('AWS_ACCESS_KEY_ID')`` means that it will look up the value of the key
``AWS_ACCESS_KEY_ID`` from your environment variable (Heroku config vars).

.. code-block:: python

    AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

Preview template
----------------

Save the following to ``_templates/global/MTurkPreview.html``.
This is the "preview" workers will see before they accept the HIT.
You can modify the text as you wish:

.. code-block:: html

    {% extends "otree/MTurkPreview.html" %}
    {% load otree %}

    {% block title %}Please read this before clicking "Accept"{% endblock %}

    {% block content %}
        <p>
            This HIT is an academic experiment on decision making.
        </p>

        <p>
            It will require you to interact with other workers in real time.
            Some other workers may be waiting until you have completed a given task,
            before they can proceed.
            So, please be mindful of other participants and complete all tasks in a timely fashion.
            Please only accept ths HIT only if you can commit to completing it.
        </p>

        <p>
            After completing this HIT, you will receive your reward plus a bonus payment
            that is based on how you play the experiment.
        </p>
    {% endblock %}

Session config
--------------

In ``SESSION_CONFIG_DEFAULTS``, add an entry called `mturk_hit_settings` whose value is:

.. code-block:: python

    {
        'keywords': 'bonus, study',
        'title': 'Title for your experiment',
        'description': 'Description for your experiment',
        'frame_height': 500,
        'preview_template': 'global/MTurkPreview.html',
        'minutes_allotted_per_assignment': 60,
        'expiration_hours': 7*24, # 7 days
        #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
        'qualification_requirements': []
    },
