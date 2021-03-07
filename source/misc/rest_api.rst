.. _rest:

REST
====

oTree has a REST API that enables external programs
(such as other websites) to communicate with oTree:

A REST API is just a URL on your server that is designed to be accessed by programs,
rather than being opened manually in a web browser.

Simply make a request to one of the below URLs.

"Create sessions" REST endpoint
-------------------------------

POST URL: ``/api/sessions/``

Here are some examples of how the "create sessions" endpoint can be used:

-   Other websites can create oTree sessions automatically
-   You can make a fancier alternative to oTree's :ref:`edit_config` interface
    (e.g. with sliders and visual widgets)
-   Process that will create new oTree sessions on some fixed schedule
-   Command line script to create customized sessions
    (if ``otree create_session`` is not sufficient)

Example
~~~~~~~

.. code-block:: python

    import requests  # pip3 install requests

    def create_session(**payload):
        resp = requests.post(SERVER_URL + '/api/sessions/', json=payload)
        return resp.json()

    data = create_session(session_config_name='trust', room_name='econ101', num_participants=4, modified_session_config_fields=dict(num_apples=10, abc=[1, 2, 3]))
    print(data)


.. note::

    *"Where should I put this code?"*

    This code does not need to go inside your oTree project folder.
    Since the point of the REST API is to allow external programs and servers to communicate with oTree
    across the internet, you should put this code in that other program.
    That also means you should use whatever language that other server uses.
    The examples on this page use Python,
    but it's simple to make HTTP requests using any programming language,
    or tools like webhooks or cURL.


Parameters
~~~~~~~~~~

-   ``session_config_name`` (required)
-   ``num_participants`` (required)
-   ``modified_session_config_fields``: an optional dict of session config parameters,
    as discussed in :ref:`edit_config`.
-   ``room_name`` if you want to create the session in a room.

"Get session data" endpoint
---------------------------

.. note::

    New beta feature as of March 2021.

GET URL: ``/api/sessions/``

This API retrieves data about a session and its participants.
It's useful if you want to integrate oTree with MTurk or any other online platform
to automate payments and participant recruitment.
`Here is a how-to guide <https://1drv.ms/w/s!AkzFB3_uPYH5gYd3IEj8oDFylx2Sjg?e=M4q3lJ>`__ on how to do this.

Example
~~~~~~~

.. code-block:: python

    def get_session(**payload):
        resp = requests.get(SERVER_URL + '/api/sessions/', json=payload)
        return resp.json()

    data = get_session(code='vfyqlw1q')
    # to only return data about some participants, pass participant_labels:
    # data = get_session(code='vfyqlw1q', participant_labels=['Alice'])

    print(data)

Example output
~~~~~~~~~~~~~~

.. code-block:: python

    {'num_participants': 3,
     'room_url': 'http://localhost:8000/room/econ101',
     'session_url': 'http://localhost:8000/join/bfzza6vhbx',
     'REAL_WORLD_CURRENCY_CODE': 'USD',
     'config': {'app_sequence': ['public_goods_simple'],
                'display_name': 'public_goods_simple',
                'doc': '',
                'mturk_hit_settings': {'description': 'Description for your '
                                                      'experiment',
                                       'expiration_hours': 168,
                                       'frame_height': 500,
                                       'keywords': 'bonus, study',
                                       'minutes_allotted_per_assignment': 60,
                                       'qualification_requirements': [],
                                       'template': 'global/mturk_template.html',
                                       'title': 'Title for your experiment'},
                'name': 'public_goods_simple',
                'num_demo_participants': 3,
                'participation_fee': 5.0,
                'real_world_currency_per_point': 1.0},
     'participants': [{'code': '3iscjiet',
                       'id_in_session': 1,
                       'label': 'Alice',
                       'payoff_in_real_world_currency': 13.0},
                      {'code': 'n76h05bp',
                       'id_in_session': 2,
                       'label': 'Bob',
                       'payoff_in_real_world_currency': 0.0},
                      {'code': 'fmjenzca',
                       'id_in_session': 3,
                       'label': None,
                       'payoff_in_real_world_currency': 7.0}],
     }

"Session configs" REST endpoint
-------------------------------

.. note::

    New beta feature as of March 2021.

GET URL: ``/api/session_configs/``

This endpoint simply returns the list of all your session configs, as dicts
with all their properties, e.g. ``participation_fee``, etc.

Example
~~~~~~~

.. code-block:: python

    def get_configs():
        resp = requests.get(SERVER_URL + '/api/session_configs/')
        return resp.json()

    configs = get_configs()


.. _participant_vars_rest:

"Participant vars" REST endpoint
--------------------------------

POST URL: ``/api/participant_vars/``

This endpoint lets you set ``participant.vars``.
The main purpose is to allow other sites/apps to pass information about a participant to oTree,
via web services / webhooks.
For example, if the user does a survey on Qualtrics that then links to oTree,
you can pass their survey data (like gender, age, etc) into oTree as participant vars.
(Qualtrics allows making POST requests through their `web service <https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/advanced-elements/web-service/>`__
feature.)

Example
~~~~~~~

.. code-block:: python

    import requests

    def set_participant_vars(**payload):
        resp = requests.post(SERVER_URL + '/api/participant_vars/', json=payload)
        return resp

    resp = set_participant_vars(room_name='qualtrics_study', participant_label='albert_e', vars=dict(age=25, is_male=True, x=[3,6,9]))
    print(resp.text)

Parameters
~~~~~~~~~~

-   ``room_name`` (required)
-   ``participant_label`` (required)
-   ``vars`` (required): a dict of participant vars to add. Values can be any JSON-serializable data type,
    even nested dicts/lists.

This feature requires you to use a Room.
Participants are uniquely identified with the combination of room name & participant label.
So you will need to give participants a link with a ``participant_label``,
although this does not need to come from a ``participant_label_file``.

.. _session_vars_rest:

"Session vars" REST endpoint
----------------------------

POST URL: ``/api/session_vars/``

This endpoint lets you set ``session.vars``.
One use is experimenter input.
For example, if the experimenter does a lottery drawing in the middle of the experiment,
they can input the result by running a script like the one below.

Example
~~~~~~~

.. code-block:: python

    def set_session_vars(**payload):
        return requests.post(SERVER_URL + "/api/session_vars/", json=payload)

    resp = set_session_vars(
        room_name="my_room",
        vars=dict(dice_roll=4),
    )

Parameters
~~~~~~~~~~

-   ``room_name`` (required)
-   ``vars`` (required): a dict of session vars to add.

This feature requires you to use a Room.

Note
~~~~

If you are using this for experimenter input during an experiment,
you may also want to use :ref:`error_message <error_message>`:

.. code-block:: python

    def error_message(player, values):
        session = player.session

        if 'dice_roll' not in session.vars:
            return 'You must wait until the dice roll before proceeding'


Authentication
--------------

If you have set your auth level to DEMO or STUDY,
you must authenticate your REST API requests.

Create an env var (i.e. Heroku config var) ``OTREE_REST_KEY``
on the server. Set it to some secret value.

When you make a request, add that key as an HTTP header called ``otree-rest-key``.
For example:

.. code-block:: python

    import requests

    REST_KEY = 'your_key'

    def create_session(**payload):
        resp = requests.post(SERVER_URL + '/api/sessions/', json=payload,
            headers={'otree-rest-key': REST_KEY}
        )
        return resp

    resp = create_session(session_config_name='trust', room_name='econ101', num_participants=4, modified_session_config_fields=dict(num_apples=10, abc=[1, 2, 3]))
    print(resp.text) # returns the session code


Demo & testing
--------------

For convenience during development, you can generate fake vars to simulate
data that, in a real session, will come from the REST API.

In your session config, add the parameter ``mock_exogenous_data=True``
(We call it **exogenous** data because it originates outside oTree.)

Then define a function with the same name (``mock_exogenous_data``)
in your project's shared_out.py (if you are using a text editor,
you may need to create that file).

Here's an example:

.. code-block:: python

    def mock_exogenous_data(session):
        participants = session.get_participants()
        for pp in participants:
            pp.vars.update(age=20, is_male=True) # or make it random

You can also set participant labels here.

When you run a session in demo mode, or using bots, ``mock_exogenous_data()``
will automatically be run after ``creating_session``. However, it will not be run
if the session is created in a room.

If you have multiple session configs that require different exogenous data,
you can branch like this:

.. code-block:: python

    def mock_exogenous_data(session):
        if session.config['name'] == 'whatever':
            ...
        if 'xyz' in session.config['app_sequence']:
            ...
