Advanced features
=================

These are advanced features that are mostly unsupported in oTree Studio.

.. _ExtraModel:

ExtraModel
----------

An ExtraModel is useful when you need to store dozens or hundreds of data points about a single player.
For example, a list of bids, or a list of stimuli and reaction times.
They are frequently used together with :ref:`live`.

There are a bunch of examples `here <https://www.otreehub.com/projects/otree-more-demos/>`__.

An ExtraModel should link to another model:

.. code-block:: python

    class Bid(ExtraModel):
        player = models.Link(Player)
        amount = models.CurrencyField()

Each time the user makes a bid, you store it in the database:

.. code-block:: python

    Bid.create(player=player, amount=500)

Later, you can retrieve the list of a player's bids:

.. code-block:: python

    bids = Bid.filter(player=player)

An ExtraModel can have multiple links:

.. code-block:: python

    class Offer(ExtraModel):
        sender = models.Link(Player)
        receiver = models.Link(Player)
        group = models.Link(Group)
        amount = models.CurrencyField()
        accepted = models.BooleanField()

Then you can query it in various ways:

.. code-block:: python

    this_group_offers = Offer.filter(group=group)
    offers_i_accepted = Offer.filter(receiver=player, accepted=True)

For more complex filters and sorting, you should use list operations:

.. code-block:: python

    offers_over_500 = [o for o in Offer.filter(group=group) if o.amount > 500]

See the example psychology games such as the Stroop task,
which show how to generate ExtraModel data from each row of a CSV spreadsheet.

To export your ExtraModel data to CSV/Excel, use :ref:`custom-export`.

.. _read_csv:

Reading CSV files
-----------------

.. note::

    This feature is in beta (new in oTree 5.8.2)

To read a CSV file (which can be produced by Excel or any other spreadsheet app),
you can use ``read_csv()``. For example, if you have a CSV file like this::

    name,price,is_organic
    Apple,0.99,TRUE
    Mango,3.79,FALSE
    
``read_csv()`` will output a list of dicts, like:

.. code-block:: python

    [dict(name='Apple', price=0.99, is_organic=True), 
     dict(name='Mango', price=3.79, is_organic=False)]

You call the function like this:

.. code-block:: python

    rows = read_csv('my_app/my_data.csv', Product)

The second argument is a class that specifies the datatype of each column:

.. code-block:: python

    class Product(ExtraModel):
        name = models.StringField()
        price = models.FloatField()
        is_organic = models.BooleanField()

(Without this info, it would be ambiguous whether ``TRUE`` is supposed to be a bool,
or the string ``'TRUE'``, etc.)

``read_csv()`` does not actually create any instances of that class. 
If you want that, you must use ``.create()`` additionally:

.. code-block:: python

    rows = read_csv('my_app/my_data.csv', Product)
    for row in rows:
        Product.create(
            name=row['name'], 
            price=row['price'], 
            is_organic=row['is_organic'], 
            # any other args:
            player=player,
        )

The model can be an ``ExtraModel``, ``Player``, ``Group``, or ``Subsession``.
It's fine if it also contains other fields; they will be ignored by ``read_csv()``.


Templates
---------

template_name
~~~~~~~~~~~~~

If the template needs to have a different name from your
page class (e.g. you are sharing the same template for multiple pages),
set ``template_name``. Example:

.. code-block:: python

    class Page1(Page):
        template_name = 'app_name/MyPage.html'

.. _base-template:

CSS/JS and base templates
~~~~~~~~~~~~~~~~~~~~~~~~~

To include the same JS/CSS in all pages of an app, either put it in a :ref:`static file <staticfiles>`
or put it in an includable template.

.. _staticfiles:

Static files
------------

Here is how to include images (or any other static file like .css, .js, etc.) in your pages.

At the root of your oTree project, there is a ``_static/`` folder.
Put a file there, for example ``puppy.jpg``.
Then, in your template, you can get the URL to that file with
``{{ static 'puppy.jpg' }}``.

To display an image, use the ``<img>`` tag, like this:

.. code-block:: html

    <img src="{{ static 'puppy.jpg' }}"/>

Above we saved our image in ``_static/puppy.jpg``,
But actually it's better to make a subfolder with the name of your app,
and save it as ``_static/your_app_name/puppy.jpg``, to keep files organized
and prevent name conflicts.

Then your HTML code becomes:

.. code-block:: html

    <img src="{{ static 'your_app_name/puppy.jpg }}"/>

(If you prefer, you can also put static files inside your app folder,
in a subfolder called ``static/your_app_name``.)

If a static file is not updating even after you changed it,
this is because your browser cached the file. Do a full page reload
(usually Ctrl+F5)

If you have videos or high-resolution images,
it's preferable to store them somewhere online and reference them by URL
because the large file size can make uploading your
.otreezip file much slower.


Wait pages
----------

.. _customize_wait_page:

Custom wait page template
~~~~~~~~~~~~~~~~~~~~~~~~~

You can make a custom wait page template.
For example, save this to ``your_app_name/MyWaitPage.html``:

.. code-block:: html

    {{ extends 'otree/WaitPage.html' }}
    {{ block title }}{{ title_text }}{{ endblock }}
    {{ block content }}
        {{ body_text }}
        <p>
            My custom content here.
        </p>
    {{ endblock }}

Then tell your wait page to use this template:

.. code-block:: python

    class MyWaitPage(WaitPage):
        template_name = 'your_app_name/MyWaitPage.html'

Then you can use ``vars_for_template`` in the usual way.
Actually, the ``body_text`` and ``title_text`` attributes
are just shorthand for setting ``vars_for_template``;
the following 2 code snippets are equivalent:

.. code-block:: python

    class MyWaitPage(WaitPage):
        body_text = "foo"

.. code-block:: python

    class MyWaitPage(WaitPage):

        @staticmethod
        def vars_for_template(player):
            return dict(body_text="foo")

If you want to apply your custom wait page template globally,
save it to ``_templates/global/WaitPage.html``.
oTree will then automatically use it everywhere instead of the built-in wait page.


Currency
--------

To customize the name "points" to something else like "tokens" or "credits",
set ``POINTS_CUSTOM_NAME``, e.g. ``POINTS_CUSTOM_NAME = 'tokens'``.

You can change the number of decimal places in real world currency amounts
with the setting ``REAL_WORLD_CURRENCY_DECIMAL_PLACES``.
If the extra decimal places show up but are always 0,
then you should reset the database.

.. _welcome-page:

Room welcome pages
------------------

.. note::

    Beta feature as of oTree 5.12 (September 2025)

As of oTree 5.12, when you use a Room, oTree will show a Welcome page
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

Simple case: no participant label
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
            <p>Click the button to start.</p>
            <form>
                <button type="submit">Start</button>
            </form>
        </div>

        <script>
            // Populate form fields from query parameters on page load
            const urlParams = new URLSearchParams(window.location.search);

            document.querySelector('form').addEventListener('submit', function(e) {
                e.preventDefault();
                urlParams.set('welcome_page_ok', '1');
                window.location.href = window.location.pathname + '?' + urlParams.toString();
            });
        </script>
    </body>
    </html>

Manual entry of participant label
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Other use cases: consent form / quiz, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add any form fields you want (dropdowns, checkboxes, etc.)
and check the user's inputs using JavaScript that does not call the server.

Any parameters in the start link (e.g. ``?participant_label=Alice``)
can be accessed from your JS code like this:

.. code-block:: javascript

    urlParams = new URLSearchParams(window.location.search);

This means you can send participants start links with custom parameters,
then use that to customize the content of your welcome page.
