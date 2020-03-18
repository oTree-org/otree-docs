REST
====

.. note::

    This section describes a feature that is not yet publicly released.
    It will be in oTree 2.6.

oTree has a small REST API that enables external programs
(such as other websites) to communicate with oTree, in particular:

-   Create sessions
-   Add participant vars

REST Setup
----------

Create an environment variable (i.e. Heroku config var) ``OTREE_REST_KEY``.
Set it to some secret value. This is the "password" to prevent unwanted API access.

Then simply make an JSON-encoded request to one of the below endpoint URLs,
including the secret key in an HTTP header.

The below examples use the Python Requests library (``pip3 install requests``),
but you can make HTTP requests using any programming language,
even JavaScript code in an oTree template
(but don't expose the secret key to non-admin users).

Setup code:

.. code-block:: python

    import requests

    SERVER_URL = 'https://your-otree-server.herokuapp.com'
    REST_KEY = 'your_secret_rest_key'

"Create sessions" REST endpoint
-------------------------------

POST URL: ``/api/v1/sessions/``

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

    import requests

    def post_session(**payload):
        return requests.post(SERVER_URL + '/api/v1/sessions/', json=payload,
            headers={'otree-rest-key': REST_KEY}
        )

    resp = post_session(session_config_name='trust', room_name='econ101', num_participants=4, modified_session_config_fields=dict(num_apples=10, abc=[1, 2, 3]))
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
-------------------------------

POST URL: ``/api/v1/participant_vars/``

This endpoint lets you set a participant's vars, i.e. ``self.participant.vars``.
The main purpose is to allow other sites/apps to pass information about a participant to oTree.
For example, if the user does a survey on Qualtrics that then links to oTree,
you can pass their survey data (like gender, age, etc) into oTree as participant vars.
(Qualtrics supports REST APIs with their `web service <https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/advanced-elements/web-service/>`__
feature.)

The POST request should be made server-side.
You can do it on the last page of your survey, presumably before you display them their oTree link.

Example
~~~~~~~

.. code-block:: python

    import requests

    def post_vars(**payload):
        return requests.post(SERVER_URL + '/api/v1/participant_vars/', json=payload,
            headers={'otree-rest-key': REST_KEY}
        )

    resp = post_vars(room_name='qualtrics_study', participant_label='albert_e', vars=dict(age=25, is_male=True, x=[3,6,9]))
    resp.raise_for_status() # ensure it succeeded

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

Demo & testing
~~~~~~~~~~~~~~

For convenience during development, you can generate fake vars to simulate
data that, in a real session, will come from the REST API.

In your session config, add the parameter ``mock_exogenous_data=True``
(We call it **exogenous** data because it originates outside oTree.)

Then define a function with the same name (``mock_exogenous_data``)
in your project's utils.py (if you are using a text editor, you may need to create that module).

Here's an example:

.. code-block:: python

    def mock_exogenous_data(session):
        participants = session.get_participants()
        for pp in participants:
            pp.vars.update(age=20, is_male=True) # or make it random

You can also set participant labels here.

When you run a session in demo mode, or using bots, ``mock_exogenous_data()``
will automatically be run after ``creating_session``. However, it will not be run
if the session created in a room.

If you have multiple session configs that require different exogenous data,
you can branch like this:

.. code-block:: python

    def mock_exogenous_data(session):
        if session.config['name'] == 'whatever':
            ...
        if 'xyz' in session.config['app_sequence']:
            ...
