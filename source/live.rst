.. _live:

Live pages
==========

Live pages communicate with the server continuously
and update in real time, enabling continuous time games.
Live pages are a great fit for games with lots of back-and-forth interaction
between users.

There are a bunch of examples `here <https://www.otreehub.com/projects/otree-more-demos/>`__.

Sending data to the server
--------------------------

In your template's JavaScript code,
call the function ``liveSend()``
whenever you want to send data to the server.
For example, to submit a bid of 99 on behalf of the user, call:

.. code-block:: javascript

    liveSend(99);

Define a function that will receive this message.
Its argument is whatever data
was sent.

.. code-block:: python


    class MyPage(Page):
        @staticmethod
        def live_method(player, data):
            print('received a bid from', player.id_in_group, ':', data)


If you are using oTree Studio, you must define a player function whose name
starts with ``live_``.
(Note, ``live_method`` on ``WaitPage`` is not yet supported.)

Sending data to the page
------------------------

To send data back, return a dict whose keys are the IDs of the players
to receive a message.
For example, here is a method that simply sends "thanks"
to whoever sends a message.

.. code-block:: python

    def live_method(player, data):
        return {player.id_in_group: 'thanks'}

To send to multiple players, use their ``id_in_group``.
For example, this forwards every message to players 2 and 3:

.. code-block:: python

    def live_method(player, data):
        return {2: data, 3: data}

To broadcast it to the whole group, use ``0``
(special case since it is not an actual ``id_in_group``).

.. code-block:: python

    def live_method(player, data):
        return {0: data}

In your JavaScript, define a function ``liveRecv``.
This will be automatically called each time a message is received from the server.

.. code-block:: javascript

    function liveRecv(data) {
        console.log('received a message!', data);
        // your code goes here
    }

Example: auction
----------------

.. code-block:: python

    class Group(BaseGroup):
        highest_bidder = models.IntegerField()
        highest_bid = models.CurrencyField(initial=0)

    class Player(BasePlayer):
        pass


.. code-block:: python

    def live_method(player, data):
        group = player.group
        my_id = player.id_in_group
        if bid > group.highest_bid:
            group.highest_bid = data
            group.highest_bidder = my_id
            response = dict(id_in_group=my_id, bid=data)
            return {0: response}

.. code-block:: html

    <table id="history" class="table">
    <tr>
      <th>Player</th>
      <th>Bid</th>
    </tr>
    </table>
    <input id="inputbox" type="number">
    <button type="button" onclick="sendValue()">Send</button>

    <script>

      let history = document.getElementById('history');
      let inputbox = document.getElementById('inputbox');

      function liveRecv(data) {
          history.innerHTML += '<tr><td>' + data.id_in_group + '</td><td>' + data.bid + '</td></tr>';
      }

      function sendValue() {
        liveSend(parseInt(inputbox.value));
      }

    </script>

(Note, in JavaScript ``data.id_in_group == data['id_in_group']``.)

Data
----

The data you send and receive can be any data type (as long as it is JSON serializable).
For example these are all valid:

.. code-block:: javascript

        liveSend(99);
        liveSend('hello world');
        liveSend([4, 5, 6]);
        liveSend({'type': 'bid', 'value': 10.5});

The most versatile type of data is a dict,
since it allows you to include multiple pieces of metadata,
in particular what type of message it is:

.. code-block:: javascript

    liveSend({'type': 'offer', 'value': 99.9, 'to': 3})
    liveSend({'type': 'response', 'accepted': true, 'to': 3})

Then you can use ``if`` statements to process different types of messages:

.. code-block:: python

    def live_method(player, data):
        t = data['type']
        if t == 'offer':
            other_player = data['to']
            response = {
                'type': 'offer',
                'from': player.id_in_group,
                'value': data['value']
            }
            return {other_player: response}
        if t == 'response':
            # etc
            ...


History
-------

By default, participants will not see messages that were sent before they arrived at the page.
(And data will not be re-sent if they refresh the page.)
If you want to save history, you should store it in the database.
When a player loads the page, your JavaScript can call something like ``liveSend({})``,
and you can configure your live_method to retrieve the history of the game from the database.

ExtraModel
----------

Live pages are often used together with an :ref:`ExtraModel <ExtraModel>`,
which allows you to store each individual message or action in the database.

Keeping users on the page
-------------------------

Let's say you require 10 messages to be sent before the users can proceed
to the next page.

First, you should omit the ``{{ next_button }}``.
(Or use JS to hide it until the task is complete.)

When the task is completed, you send a message:

.. code-block:: python

    class Group(BaseGroup):
        num_messages = models.IntegerField()
        game_finished = models.BooleanField()


    class MyPage(Page):
        def live_method(player, data):
            group = player.group
            group.num_messages += 1
            if group.num_messages >= 10:
                group.game_finished = True
                response = dict(type='game_finished')
                return {0: response}

Then in the template, automatically submit the page via JavaScript:

.. code-block:: javascript

    function liveRecv(data) {
        console.log('received', data);
        let type = data.type;
        if (type === 'game_finished') {
            document.getElementById("form").submit();
        }
        // handle other types of messages here..
    }

By the way, using a similar technique, you could implement a custom
wait page, e.g. one that lets you proceed after a certain timeout,
even if not all players have arrived.

General advice about live pages
-------------------------------

Here is some general advice (does not apply to all situations).
We recommend implementing most of your logic in Python,
and just using JavaScript to update the page's HTML, because:

-   The JavaScript language can be quite tricky to use properly
-   Your Python code runs on the server, which is centralized and reliable.
    JavaScript runs on the clients, which can get out of sync with each other,
    and data can get lost when the page is closed or reloaded.
-   Because Python code runs on the server, it is more secure and cannot be viewed or modified
    by participants.

Example: tic-tac-toe
~~~~~~~~~~~~~~~~~~~~

Let's say you are implementing a game of tic-tac-toe.
There are 2 types of messages your live_method can receive:

1.   A user marks a square, so you need to notify the other player
2.   A user loads (or reloads) the page, so you need to send them the current board layout.

For situation 1, you should use a JavaScript event handler like ``onclick``, e.g. so when the user clicks on square 3,
that move gets sent to the server:

.. code-block:: javascript

        liveSend({square: 3});

For situation 2, it's good to put some code like this in your template, which sends an empty message
to the server when the page loads:

.. code-block:: javascript

    document.addEventListener("DOMContentLoaded", (event) => {
        liveSend({});
    });

The server handles these 2 situations with an "if" statement:

.. code-block:: python

    def live_method(player, data):
        group = player.group

        if 'square' in data:
            # SITUATION 1
            square = data['square']

            # save_move should save the move into a group field.
            # for example, if player 1 modifies square 3,
            # that changes group.board from 'X O XX  O' to 'X OOXX  O'
            save_move(group, square, player.id_in_group)
            # so that we can highlight the square (and maybe say who made the move)
            news = {'square': square, 'id_in_group': player.id_in_group}
        else:
            # SITUATION 2
            news = {}
        # get_state should contain the current state of the game, for example:
        # {'board': 'X O XX  O', 'whose_turn': 2}
        payload = get_state(group)
        # .update just combines 2 dicts
        payload.update(news)
        return {0: payload}

In situation 2 (the player loads the page), the client gets a message like:

.. code-block:: javascript

    {'board': 'X OOXX  O', 'whose_turn': 2}

In situation 1, the player gets the update about the move that was just made, AND the current state.

.. code-block:: javascript

    {'board': 'X OOXX  O', 'whose_turn': 2, 'square': square, 'id_in_group': player.id_in_group}

The JavaScript code can be "dumb".
It doesn't need to keep track of whose move it is; it just trusts the info it receives from the server.
It can even redraw the board each time it receives a message.

Your code will also need to validate user input. For example, if player 1 tries to move when it is actually player 2's
turn, you need to block that. For reasons listed in the previous section, it's better to do this in your live_method than
in JavaScript code.

Summary
~~~~~~~

As illustrated above, the typical pattern for a live_method is like this::

    if the user made an action:
        state = (get the current state of the game)
        if (action is illegal/invalid):
            return
        update the models based on the move.
        news = (produce the feedback to send back to the user, or onward to other users)
    else:
        news = (nothing)
    state = (get the current state of the game)
    payload = (state combined with news)
    return payload

Note that we get the game's state twice. That's because the state changes when we update our models,
so we need to refresh it.

Troubleshooting
---------------
If you call ``liveSend`` before the page has finished loading,
you will get an error like ``liveSend is not defined``.
So, wait for ``DOMContentLoaded`` (or jQuery document.ready, etc):

.. code-block:: javascript

    window.addEventListener('DOMContentLoaded', (event) => {
        // your code goes here...
    });

Don't trigger ``liveSend`` when the user clicks the "next" button, since leaving the page might interrupt
the ``liveSend``. Instead, have the user click a regular button that triggers a ``liveSend``, and
then doing ``document.getElementById("form").submit();`` in your ``liveRecv``.
