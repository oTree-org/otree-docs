*Self* and object model
=======================

In oTree code, you will see the variable ``self`` in many places.
In Python, ``self`` refers to the object whose class you are
currently in.

For example, in this example, ``self`` refers to a ``Player`` object:

.. code-block:: python

    class Player(object):

        def my_method(self):
            return self.my_field

In the next example, however, ``self`` refers to a ``Group`` object:

.. code-block:: python

    class Group(object):

        def my_method(self):
            return self.my_field


``self`` is conceptually similar to the word "me". You refer to yourself
as "me", but others refer to you by your name. And when your friend says
the word "me", it has a different meaning from when you say the word
"me".

oTree's different objects are all connected, as illustrated by this
diagram.


.. figure:: _static/object_model_and_self/foFSxix.jpg
    :align: center


Player, group, subsession, and session are in a simple hierarchy,
'session' being at the top and 'player' being at the bottom. Then, the
'page' has an pointer to all 4 of these objects.

For example, if you are in a method on the ``Player`` class, you can
access the player's payoff with ``self.payoff`` (because ``self`` is the
player). But if you are inside a ``Page`` class in ``views.py``, the
equivalent expression is ``self.player.payoff``,
which traverses the pointer from 'page' to 'player'.

Here are some code examples to illustrate:

.. code-block:: python

    class Session(...) # this class is defined in oTree-core
        def example(self):

            # current session object
            self

            # parent objects
            self.config

            # child objects
            self.get_subsessions()
            self.get_participants()

    class Participant(...) # this class is defined in oTree-core
        def example(self):

            # current participant object
            self

            # parent objects
            self.session

            # child objects
            self.get_players()

in your ``models.py``

.. code-block:: python

    class Subsession(otree.models.Subsession):
        def example(self):

            # current subsession object
            self

            # parent objects
            self.session

            # child objects
            self.get_groups()
            self.get_players()

            # accessing previous Subsession objects
            self.in_previous_rounds()
            self.in_all_rounds()

    class Group(otree.models.Group):
        def example(self):

            # current group object
            self

            # parent objects
            self.session
            self.subsession

            # child objects
            self.get_players()

    class Player(otree.models.Player):

        def example(self):

            # current player object
            self

            # method you defined on the current object
            self.my_custom_method()

            # parent objects
            self.session
            self.subsession
            self.group
            self.participant

            self.session.config

            # accessing previous player objects
            self.in_previous_rounds()
            self.in_all_rounds() # equivalent to self.in_previous_rounds() + [self]

in your ``views.py``

.. code-block:: python

    class MyPage(Page):
        def example(self):

            # current page object
            self

            # parent objects
            self.session
            self.subsession
            self.group
            self.player

            # example of chaining lookups
            self.player.participant
            self.session.config

You can follow pointers in a transitive manner. For example, if you are
in the Page class, you can access the participant as
``self.player.participant``. If you are in the Player class, you can
access the session config as ``self.session.config``.

.. note::

    Prior to oTree-core 0.3.11, ``self.session.config`` was known as ``self.session.session_type``.


