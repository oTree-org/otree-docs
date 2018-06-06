.. _chat:

Chat
====

You can add a chat room to your page so that participants can communicate with each other.
`Live demo here <http://otree-demo.herokuapp.com/demo/prisoner_chat/>`__
(open the start links and click through to the "Your Choice" page).

.. note::

    Note for people who previously used the ``otreechat`` add-on:

    In November 2017, the ``otreechat`` add-on was merged into otree.
    Now, you no longer need to install ``otreechat`` separately,
    and you don't need ``{% load otreechat}`` in your templates.

Usage
-----

Basic usage
~~~~~~~~~~~

Wherever you want a chatbox in your template, use:

.. code-block:: html+django

    {% chat %}

This will make a chat room among players in the same Group,
where each player's nickname is displayed as
"Player 1", "Player 2", etc. (based on the player's ``id_in_group``).

Customizing the nickname and chat room members
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can pass optional parameters ``channel`` and/or ``nickname`` like this:

.. code-block:: html+django

    {% chat nickname="abc" channel="123" %}

Nickname
''''''''

``nickname`` is the nickname that will be displayed for that user in the chat.
A typical usage would be ``{% chat nickname=player.role %}``.

Channel
'''''''

``channel`` is the chat room's name, meaning that if 2 players
have the same ``channel``, they can chat with each other.
``channel`` is not displayed in the user interface; it's just used internally.
Its default value is ``group.id``, meaning all players in the group can chat together.
You can use ``channel`` to instead scope the chat to the current page
or sub-division of a group, etc. (see examples below).
Regardless of the value of the ``channel`` argument,
the chat will at least be scoped to players in the same session and the same app.

Example: chat by role
`````````````````````

Here's an example where instead of communication within a group,
we have communication between groups based on role,
e.g. all buyers can talk with each other,
and all sellers can talk with each other.


.. code-block:: python

    class Player(BasePlayer):

        def role(self):
            if self.id_in_group == 1:
                return 'Seller'
            else:
                return 'Buyer'

        def chat_nickname(self):
            return 'Group {} {}'.format(self.group.id_in_subsession, self.role())

Then in the template:

.. code-block:: html+django

    {% chat nickname=player.chat_nickname channel=player.role %}

Example: chat across rounds
```````````````````````````

If you need players to chat with players who are currently in a different round
of the game, you can do:

.. code-block:: html+django

    {% chat channel=group.id_in_subsession %}

Example: chat between all groups in all rounds
``````````````````````````````````````````````

If you want everyone in the session to freely chat with each other, just do:

.. code-block:: html+django

    {% chat channel=1 %}

(The number 1 is not significant; all that matters is that it's the same for everyone.)

Styling
~~~~~~~

.. note::

    The CSS classes for the elements changed in August 2017.
    They were renamed to a more consistent BEM style.

To customize the style, just include some CSS after the ``{% chat %}`` element,
e.g.:

.. code-block:: html+django

    {% chat %}

    <style>
        .otree-chat__messages {
            height: 400px;
        }
        .otree-chat__nickname {
            color: #0000FF;
            font-weight: bold;
        }
    </style>

You can also customize the appearance by putting it inside a ``<div>``
and styling that parent ``<div>``. For example, to set the width:

.. code-block:: html+django

    <div style="width: 400px">
        {% chat %}
    </div>

Multiple chats on a page
~~~~~~~~~~~~~~~~~~~~~~~~

You can have multiple ``{% chat %}`` boxes on each page,
so that a player can be in multiple channels simultaneously.

For example, this code enables 1:1 chat with every other player in the group.

.. code-block:: python

    class Player(BasePlayer):

        def chat_nickname(self):
            return 'Player {}'.format(self.id_in_group)

        def chat_configs(self):
            configs = []
            for other in self.get_others_in_group():
                if other.id_in_group < self.id_in_group:
                    lower_id, higher_id = other.id_in_group, self.id_in_group
                else:
                    lower_id, higher_id = self.id_in_group, other.id_in_group
                configs.append({
                    # make a name for the channel that is the same for all
                    # channel members. That's why we order it (lower, higher)
                    'channel': '{}-{}-{}'.format(self.group.id, lower_id, higher_id),
                    'label': 'Chat with {}'.format(other.chat_nickname())
                })
            return configs

.. code-block:: html+django

    {% for config in player.chat_configs %}
        <h4>{{ config.label }}</h4>
        {% chat nickname=player.chat_nickname channel=config.channel %}
    {% endfor %}


Exporting CSV of chat logs
--------------------------

The chat logs download link will appear on oTree's regular data export page.
