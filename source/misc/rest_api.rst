.. _rest:

REST
====

.. note::

    These features are new in oTree 3.0 (July 2020).

oTree has a small REST API that enables external programs
(such as other websites) to communicate with oTree, in particular:

-   Create sessions
-   Add participant vars
-   Add session vars

A REST API is just a URL on your server that is designed to be accessed by programs,
rather than being opened manually in a web browser.

Simply make a request to one of the below URLs.

Where do I put this code?
-------------------------

This code does not need to go inside your oTree project folder.
Since the point of the REST API is to allow external programs and servers to communicate with oTree
across the internet, you should put this code in that other program.
That also means you should use whatever language that other server uses.
The examples on this page use Python,
but it's simple to make HTTP requests using any programming language,
or tools like webhooks or cURL.


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
        resp.raise_for_status() # ensure it succeeded
        return resp

    resp = create_session(session_config_name='trust', room_name='econ101', num_participants=4, modified_session_config_fields=dict(num_apples=10, abc=[1, 2, 3]))
    print(resp.text) # returns the session code

Parameters
~~~~~~~~~~

-   ``session_config_name`` (required)
-   ``num_participants`` (required)
-   ``modified_session_config_fields``: an optional dict of session config parameters,
    as discussed in :ref:`edit_config`.
-   ``room_name`` if you want to create the session in a room.


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
        resp.raise_for_status() # ensure it succeeded
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

.. note::

    New in oTree 3.0.6

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

    def error_message(self, values):
        if 'dice_roll' not in self.session.vars:
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
        resp.raise_for_status() # ensure it succeeded
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
