.. _rest:

REST
====

oTree has a REST API that enables external programs
(such as other websites) to communicate with oTree.

A REST API is just a URL on your server that is designed to be accessed by programs,
rather than being opened manually in a web browser.

One project that uses the REST API a lot is `oTree HR <https://github.com/oTree-org/HR>`__.

.. warning::

    As of March 2021, there have been some breaking changes to the REST API.

.. _rest-setup:

Setup
-----

.. note::

    *"Where should I put this code?"*

    This code does not need to go inside your oTree project folder.
    Since the point of the REST API is to allow external programs and servers to communicate with oTree
    across the internet, you should put this code in that other program.
    That also means you should use whatever language that other server uses.
    The examples on this page use Python,
    but it's simple to make HTTP requests using any programming language,
    or tools like webhooks or cURL.

.. code-block:: python

    import requests  # pip3 install requests
    from pprint import pprint


    GET = requests.get
    POST = requests.post

    # if using Heroku, change this to https://YOURAPP.herokuapp.com
    SERVER_URL = 'http://localhost:8000'
    REST_KEY = ''  # fill this later

    def call_api(method, *path_parts, **params) -> dict:
        path_parts = '/'.join(path_parts)
        url = f'{SERVER_URL}/api/{path_parts}/'
        resp = method(url, json=params, headers={'otree-rest-key': REST_KEY})
        if not resp.ok:
            msg = (
                f'Request to "{url}" failed '
                f'with status code {resp.status_code}: {resp.text}'
            )
            raise Exception(msg)
        return resp.json()


"oTree version" endpoint
------------------------

.. note::

    New beta feature as of March 2021.

GET URL: ``/api/otree_version/``

Example
~~~~~~~

.. code-block:: python

    data = call_api(GET, 'otree_version')
    # returns: {'version': '5.0.0'}

"Session configs" endpoint
--------------------------

.. note::

    New beta feature as of March 2021.

GET URL: ``/api/session_configs/``

Returns the list of all your session configs, as dicts with all their properties.

Example
~~~~~~~

.. code-block:: python

    data = call_api(GET, 'session_configs')
    pprint(data)

"Rooms" endpoint
----------------

.. note::

    New beta feature as of March 2021.

GET URL: ``/api/rooms/``

Example
~~~~~~~

.. code-block:: python

    data = call_api(GET, 'session_configs')
    pprint(data)

Example output (note it includes ``session_code`` if there is currently a session in the room):

.. code-block:: python

    [{'name': 'my_room',
      'session_code': 'lq3cxfn2',
      'url': 'http://localhost:8000/room/my_room'},
     {'name': 'live_demo',
      'session_code': None,
      'url': 'http://localhost:8000/room/live_demo'}]

"Create sessions" endpoint
--------------------------

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

    data = call_api(
        POST,
        'sessions',
        session_config_name='trust',
        room_name='econ101',
        num_participants=4,
        modified_session_config_fields=dict(num_apples=10, abc=[1, 2, 3]),
    )
    pprint(data)

Parameters
~~~~~~~~~~

-   ``session_config_name`` (required)
-   ``num_participants`` (required)
-   ``modified_session_config_fields``: an optional dict of session config parameters,
    as discussed in :ref:`edit_config`.
-   ``room_name`` if you want to create the session in a room.

.. _REST-session-data:

"Get session data" endpoint
---------------------------

.. note::

    New feature as of March 2021.
    In beta until we get sufficient user feedback.

GET URL: ``/api/sessions/{code}``

This API retrieves data about a session and its participants.
If ``participant_labels`` is omitted, it returns data for all participants.

Example
~~~~~~~

.. code-block:: python

    data = call_api(GET, 'sessions', 'vfyqlw1q', participant_labels=['Alice'])
    pprint(data)

.. _session_vars_rest:

"Session vars" endpoint
-----------------------

.. note::

    As of April 2021, this endpoint requires you to pass a session code as a path parameter.
    If the session is in a room, you can get the session code with the ``rooms`` endpoint.

POST URL: ``/api/session_vars/{session_code}``

This endpoint lets you set ``session.vars``.
One use is experimenter input.
For example, if the experimenter does a lottery drawing in the middle of the experiment,
they can input the result by running a script like the one below.

Example
~~~~~~~

.. code-block:: python

    call_api(POST, 'session_vars', 'vfyqlw1q', vars=dict(dice_roll=4))


"Participant vars" endpoint
---------------------------

POST URL: ``/api/participant_vars/{participant_code}``

Pass information about a participant to oTree, via web services / webhooks.

Example
~~~~~~~

.. code-block:: python

    call_api(POST, 'participant_vars', 'vfyqlw1q', vars=dict(birth_year='1995', gender='F'))

.. _participant_vars_rest:

"Participant vars for room" endpoint
------------------------------------

POST URL: ``/api/participant_vars/``

Similar to the other "participant vars" endpoint, but this one can be used when you don't have
the participant's code. Instead, you identify the participant by the room name and their participant label.

Example
~~~~~~~

.. code-block:: python

    call_api(
        POST,
        'participant_vars',
        room_name='qualtrics_study',
        participant_label='albert_e',
        vars=dict(age=25, is_male=True, x=[3, 6, 9]),
    )


Parameters
~~~~~~~~~~

-   ``room_name`` (required)
-   ``participant_label`` (required)
-   ``vars`` (required): a dict of participant vars to add. Values can be any JSON-serializable data type,
    even nested dicts/lists.

You will need to give participants a link with a ``participant_label``,
although this does not need to come from a ``participant_label_file``.

Authentication
--------------

If you have set your auth level to DEMO or STUDY,
you must authenticate your REST API requests.

Create an env var (i.e. Heroku config var) ``OTREE_REST_KEY``
on the server. Set it to some secret value.

When you make a request, add that key as an HTTP header called ``otree-rest-key``.
If following the :ref:`setup example <rest-setup>` above, you would set the ``REST_KEY`` variable.

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
