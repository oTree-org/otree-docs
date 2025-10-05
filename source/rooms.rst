.. _rooms:

Rooms
=====

oTree lets you configure "rooms", which provide:

-   Links that you can assign to participants or lab computers,
    which stay constant across sessions
-   A "waiting room" that lets you see which participants are currently waiting to start a session.
-   Short links that are easy for participants to type, good for quick live demos.

Here is a screenshot:

.. figure:: _static/admin/room-combined.png
    :align: center

Creating rooms
--------------

You can create multiple rooms -- say, for for different classes you teach,
or different labs you manage.

If using oTree Studio
~~~~~~~~~~~~~~~~~~~~~

In the sidebar, go to "Settings" and then add a room at the bottom.

If using PyCharm
~~~~~~~~~~~~~~~~

Go to your ``settings.py`` and set ``ROOMS``.

For example:

.. code-block:: python

    ROOMS = [
        dict(
            name='econ101',
            display_name='Econ 101 class',
            participant_label_file='_rooms/econ101.txt',
            use_secure_urls=True
        ),
        dict(
            name='econ_lab',
            display_name='Experimental Economics Lab'
        ),
    ]

If you are using participant labels (see below),
you need a ``participant_label_file`` which is a relative (or absolute) path to a
text file with the participant labels.

Configuring a room
------------------

Participant labels
~~~~~~~~~~~~~~~~~~

This is the "guest list" for the room.
It should contain one participant label per line. For example::

        LAB1
        LAB2
        LAB3
        LAB4
        LAB5
        LAB6
        LAB7
        LAB8
        LAB9
        LAB10

If you don't specify participant labels, then anyone can join
as long as they know the room-wide URL.
See :ref:`no-participant-labels`.

use_secure_urls (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~

This setting provides extra security on top of the ``participant_label_file``.
For example, without secure URLs, your start URLs would look something
like this::

    http://localhost:8000/room/econ101/?participant_label=Student1
    http://localhost:8000/room/econ101/?participant_label=Student2

If Student1 is mischievous,
he might change his URL's participant_label from "Student1" to "Student2",
so that he can impersonate Student2.
However, if you use ``use_secure_urls``,
each URL gets a unique code like this::

    http://localhost:8000/room/econ101/?participant_label=Student1&hash=29cd655f
    http://localhost:8000/room/econ101/?participant_label=Student2&hash=46d9f31d

Then, Student1 can't impersonate Student2 without the secret code.

Using rooms
-----------

In the admin interface, click "Rooms" in the header bar,
and click the room you created.
Scroll down to the section with the participant URLs.

If you have a participant_label_file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the room's admin page, monitor which participants are present,
and when you are ready, create a session for the desired number of people.

You can either use the participant-specific URLs, or the room-wide URL.

The participant-specific URLs already contain the participant label.
For example::

    http://localhost:8000/room/econ101/?participant_label=Student2

The room-wide URL does not contain it::

    http://localhost:8000/room/econ101/

So, if you use room-wide URLs, participants will be required to enter their participant label:

.. figure:: _static/admin/room-combined.png
    :align: center

.. _no-participant-labels:

If you don't have a participant_label_file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just have each participant open the room-wide URL.
Then, in the room's admin page, check how many people are present,
and create a session for the desired number of people.

Although this option is simple, it is less reliable than using participant labels,
because someone could play twice by opening the URL in 2 different browsers.

Reusing for multiple sessions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Room URLs are designed to be reused across sessions.
In a lab, you can set them as the browser's home page
(using either room-wide or participant-specific URLs).

In classroom experiments, you can give each student their URL that they can use
through the semester.

What if not all participants show up?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're doing a lab experiment and the number of participants is unpredictable,
you can consider using the room-wide URL, and asking participants to manually enter their
participant label. Participants are only counted as present after they enter their participant label.

Or, you can open the browsers to participant-specific URLs,
but before creating the session, close the browsers on unattended computers.

Participants can join after the session has been created, as long as there are spots remaining.

Pre-assigning participants to labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

oTree assigns participants based on arrival time, e.g. the first person to arrive is participant 1.
However, in some situations this may be undesirable, for example:

-   You want your participant labels to line up with the oTree IDs,
    in a fixed order, e.g. so that LAB29 will always be participant 29.
-   You want Alice/Bob/Charlie to always be participants 1/2/3,
    so that they get grouped to play together.

Just assign those participant labels in ``creating_session``:

.. code-block:: python

    def creating_session(subsession):
        labels = ['alice', 'bob', 'charlie']
        for player, label in zip(subsession.get_players(), labels):
            player.participant.label = label

If someone opens a start link with ``participant_label=alice``,
oTree checks if any participant in the session already has that label.
(This is necessary so that clicking a start link twice assigns back to the same participant.)

Passing data about a participant into oTree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`participant_vars_rest`.

.. _welcome-page:

Room welcome pages (consent forms, etc)
---------------------------------------

.. note::

    To use this, you must install :ref:`v60` (``pip install otree --upgrade --pre``)

When you use a Room, oTree will show a Welcome page
that asks the user to confirm to start.

This page is customizable.
This means you can put a consent form or questionnaire or any other content.

Technical details
~~~~~~~~~~~~~~~~~

In ``settings.py``, add ``welcome_page`` in your room definition:

.. code-block:: python

    ROOMS = [
        dict(
            name='my_room',
            display_name="My Room",
            welcome_page="_templates/RoomWelcomePage.html",
        ),
    ]

The welcome page is raw HTML. It doesn't use oTree's template system with ``{{ formfields }}``,
etc.

The job of your welcome page is
(1) to optionally validate the user (have them enter any info, check their response),
and (2) when they submit, send them to the room by adding ``welcome_page_ok=1`` to the URL.

Simple case: button only, no form fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you only need the participant to click to start the experiment
(without any form fields),
all you need to do is add ``welcome_page_ok=1`` to the URL query string,
then reload the page.

.. code-block:: html+django

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Welcome</title>
    </head>
    <body>
        <h2>
            Welcome
        </h2>
        <div>
            <form>
                <button type="submit">Start</button>
            </form>
        </div>

        <script>
            const urlParams = new URLSearchParams(window.location.search);

            document.querySelector('form').addEventListener('submit', function(e) {
                e.preventDefault();
                urlParams.set('welcome_page_ok', '1');
                window.location.href = window.location.pathname + '?' + urlParams.toString();
            });
        </script>
    </body>
    </html>


Consent form / quiz, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~

You can add any form fields you want (dropdowns, checkboxes, etc.)
and check the user's inputs using JavaScript and HTML attributes such as
``required``, ``min``, ``max``, etc.

.. code-block:: html+django

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Welcome</title>
    </head>
    <body>
        <h2>Consent Form</h2>
                
        <form>
            <p>This is a research study by the University of Antarctica...</p>
            <label>
                My age: <input type="number" id="age" min="1" max="120" required>
            </label>
            <br><br>

            <label>
                <input type="checkbox" id="consent" required>
                I consent to participate in this study
            </label>
            <br><br>
            <button type="submit">Continue</button>
        </form>
        
        <div id="not-eligible" style="display: none;">
            <p>You are not eligible to participate in this study. Participants must be 18 or older.</p>
        </div>


        <script>
            let urlParams = new URLSearchParams(window.location.search);
            let ageInput = document.getElementById('age');
            let notEligibleDiv = document.getElementById('not-eligible');
            let form = document.querySelector('form');
            
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                let age = parseInt(ageInput.value);
                
                if (age < 18) {
                    notEligibleDiv.style.display = 'block';
                    form.style.display = 'none';
                    return;
                }
                
                urlParams.set('welcome_page_ok', '1');
                window.location.href = window.location.pathname + '?' + urlParams.toString();
            });
        </script>
    </body>
    </html>

Any parameters in the start link (e.g. ``?participant_label=Alice``)
can be accessed from your JS code like this:

.. code-block:: javascript

    urlParams = new URLSearchParams(window.location.search);

This means you can send participants start links with custom parameters,
then use that to customize the content of your welcome page.

Custom welcome page + manual entry of participant label
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your app has a ``participant_label_file`` and you want users to enter their labels manually,
then you need to validate that it's correct.
This can be done with an AJAX POST request as below.
If the validation fails, the server will send back JSON like
``{"errors": {"participant_label": "Invalid participant label"}}``.
Display a message to your user and ask them to re-enter.

Once it succeeds, the server will return ``{"status": "ok"}``.
in that case, you should append ``welcome_page_ok=1`` to the URL and reload.

.. code-block:: html+django

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Welcome</title>
    </head>
    <body>
        <h2>
            Welcome
        </h2>
        <div>
            <p>Click the button to start.</p>
            <form style="display: flex; flex-direction: column; gap: 10px; align-items: flex-start;">
                <p id="label_error" style="display: none; color: red;">This participant label was not found</p>
                <label for="participant_label">Participant label:</label>
                <input type="text" name="participant_label" id="participant_label"/>
                <button type="submit">Start</button>
            </form>
        </div>

        <script>

            let labelErrorEle = document.getElementById('label_error');

            document.querySelector('form').addEventListener('submit', async function(e) {
                e.preventDefault();

                // Add form data to query parameters
                const form = document.querySelector('form');
                const formData = new FormData(form);
                const jsonData = Object.fromEntries(formData.entries());

                const response = await fetch(window.location.pathname, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(jsonData)
                });

                const data = await response.json();
                if (data.status === 'ok') {
                    // Validation passed, add welcome_page_ok=1 and reload page
                    const urlParams = new URLSearchParams(formData);
                    urlParams.set('welcome_page_ok', '1');
                    window.location.href = window.location.pathname + '?' + urlParams.toString();
                } else if (data.errors.participant_label) {
                    labelErrorEle.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
