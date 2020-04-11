.. _live:

Live pages
==========

.. note::

    These features are only available in :ref:`oTree 2.6 <v26>`,
    currently in beta.

You can make pages that communicate with the server continuously
and update in real time, enabling continuous time games.

Sending data to the server
--------------------------

In your template's JavaScript code,
you can call the function ``liveSend()``.
Use it whenever you want to send code to the server.
For example, to submit a bid of 99 on behalf of the user, call:

.. code-block:: javascript

    liveSend(99);

On your ``Group``, define a method that will receive this message.
Its arguments are the ``id_in_group`` of the sender and whatever data
was sent.

.. code-block:: python

    class Group(BaseGroup):

        def your_live_method(self, id_in_group, payload):
            print('received a bid from', id_in_group, ':', payload)

On your ``Page`` class, set ``live_method`` to route the messages to that method:

.. code-block:: python

    class MyPage(Page):
        live_method = 'your_live_method'

(Note, ``live_method`` on ``WaitPage`` is not yet supported.)

Sending data to the page
------------------------

To send data back, you should return a dictionary whose keys are the IDs of the players
to receive the message.
For example, here is a method that simply sends "thanks"
to whoever sends a message.

.. code-block:: python

    def your_live_method(self, id_in_group, payload):
        return {id_in_group: 'thanks'}

To send to multiple players, just use their ``id_in_group``.
For example, this forwards every message to players 2 and 3:

.. code-block:: python

    def your_live_method(self, id_in_group, payload):
        return {2: payload, 3: payload}

To broadcast it to the whole group, use ``0``
(special case since it is not an actual ``id_in_group``).

.. code-block:: python

    def your_live_method(self, id_in_group, payload):
        return {0: payload}

In your JavaScript, define a function ``liveRecv``.
This will be automatically called each time a message is received from the server.

.. code-block:: javascript

    function liveRecv(payload) {
        console.log('received a message!', payload);
        // your code goes here
    }

Example: auction
----------------

.. code-block:: python

    class Group(BaseGroup):
        highest_bidder = models.IntegerField()
        highest_bid = models.CurrencyField(initial=0)

        def live_auction(self, id_in_group, bid):
            if bid > self.highest_bid:
                self.highest_bid = bid
                self.highest_bidder = id_in_group
                broadcast = dict(id_in_group=id_in_group, bid=bid)
                return {0: broadcast}

.. code-block:: python

    class Auction(Page):
        live_method = 'live_auction'

.. code-block:: html+django

  <table id="history" class="table">
    <tr>
      <th>Player</th>
      <th>Bid</th>
    </tr>
  </table>
  <input id="inputbox" type="number">
  <button type="button" id="sendbutton">Send</button>

  <script>

      let history = document.getElementById('history');
      let inputbox = document.getElementById('inputbox');
      let sendbutton = document.getElementById('sendbutton');

      function liveRecv(payload) {
          history.innerHTML += '<tr><td>' + payload.id_in_group + '</td><td>' + payload.bid + '</td></tr>';
      }

      sendbutton.onclick = function () {
          liveSend(parseInt(inputbox.value));
      };

  </script>

Payload
-------

The payloads that you send and receive can be any data type (as long as it is JSON serializable).
For example these are all valid:

.. code-block:: javascript

        liveSend(99);
        liveSend('hello world');
        liveSend([4, 5, 6]);
        liveSend({'type': 'bid', 'value': 10.5});

The most versatile type of payload is a dict,
since it allows you to include multiple pieces of metadata:

.. code-block:: javascript

    liveSend({'type': 'offer', 'value': 99.9, 'to': 3})
    liveSend({'type': 'response', 'accepted': true, 'to': 3})

Then you can use ``if`` statements to process different types of messages:

.. code-block:: python

    def your_live_method(self, id_in_group, payload):
        t = payload['type']
        if t == 'offer':
            other_player = payload['to']
            msg = {
                'from': id_in_group,
                'offer': payload['offer'],
                'value': payload['value']
            }
            return {other_player: msg}
        if t == 'response':
            # etc
            ...

You don't even have to call it ``payload``;
it just needs to be the method's last argument:

.. code-block:: python

    def your_live_method(self, id_in_group, bid):
        print(bid)

History
-------

By default, participants will not see messages that were sent before they arrived at the page.
(And data will not be re-sent if they refresh the page.)
If you want to save history, you should store it in the database.
When a player loads the page, your JavaScript can call something like ``liveSend({'type': 'connect'})``,
and you can configure your live_method to retrieve the history of the game from the database.

If you need to store each individual bid/message that is sent,
you can use an :ref:`extra model <aux-models>`.

Keeping users on the page
-------------------------

Let's say you require 10 messages to be sent before the users can proceed
to the next page.

First, you should omit the ``{% next_button %}``.
(Or use JS to hide it until the task is complete.)

When the task is completed, you send a message:

.. code-block:: python

    class Group(BaseGroup):
        num_messages = models.IntegerField()
        game_finished = models.BooleanField()

        def your_live_method(self, id_in_group, payload):
            self.num_messages += 1
            if self.num_messages >= 10:
                self.game_finished = True
                msg = {'game_finished': True}
                return {0: msg}

Then in the template, automatically submit the page via JavaScript:

.. code-block:: javascript

    function liveRecv(message) {
        console.log('received', message);
        if (message['game_finished']) {
            document.querySelector("form").submit();
        }
        // handle other types of messages here..
    }

For security, you should use :ref:`error_message <error_message>`:

.. code-block:: javascript

    class MyPage(Page):
        live_method = 'live_method'

        def error_message(self, values):
            if not self.group.game_finished:
                return 'you need to stay until 10 messages are sent'

By the way, using a similar technique, you could implement a pseudo
wait page, e.g. one that lets you proceed after a certain timeout,
even if not all players have arrived.

Misc notes
----------

-   On Heroku, you need to turn on your 2nd dyno.
-   live methods are executed in a single thread, so you don't need to worry about race conditions.

Bots
----

To test live methods with bots, define ``call_live_method``.
(If using a a text editor, it should be a top-level function in ``tests.py``.)
This function should simulate the sequence of calls to your ``live_method``.
The argument ``method`` is the instance method on your group,
i.e. ``method = group.your_live_method``.
For example:

.. code-block:: python

    def call_live_method(method, **kwargs):
        method(1, {"offer": 50})
        method(2, {"accepted": False})
        method(1, {"offer": 60})
        method(2, {"accepted": True})

``kwargs`` contains at least the following parameters.
You can check them to return different data conditionally:

-   ``case`` as described in :ref:`cases`.
-   ``page_class``: the current page class, e.g. ``pages.MyPage``.
-   ``round_number``

``call_live_method`` will be automatically executed when the fastest bot in the group
arrives on a page with ``live_method``.
(Other bots may be on previous pages at that point, unless you restrict this with a WaitPage.)