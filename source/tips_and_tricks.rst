Tips and tricks
===============

Don't make multiple copies of your app
--------------------------------------

If possible, you should avoid copying an app's folder to make a slightly different version, because then you have
duplicated code that is harder to maintain.

If you need multiple rounds, set ``num_rounds``. If you need slightly different versions (e.g. different treatments),
then you should use the techniques described in :ref:`treatments`, such as making 2 session configs that have a different
``'treatment'`` parameter, and then checking for ``self.session.config['treatment']`` in your app's code.

Don't modify values in ``Constants``
------------------------------------

As its name implies, ``Constants`` is for values that don't change -- they are the same for all participants
across all sessions. So, you shouldn't do something like this:

.. code-block:: python

    def my_method(self):
        Constants.my_list.append(1)

``Constants`` has global scope, so when you do this, your modification will "leak" to all other sessions,
until the server is restarted. Instead, if you want a variable that is the same for all players in your session,
you should set a field on the subsession, or use :ref:`session_vars`.

In Player/Group/Subsession, use fields instead of class attributes
------------------------------------------------------------------

For the same reason as with Constants above,
you shouldn't assign to class attributes on your models.
For example, don't do this:

.. code-block::python

    class Player(BasePlayer):


        my_list = [] # wrong

        def foo(self):
            self.my_list.append(1)

Or this:

.. code-block::python

    class Player(BasePlayer):

        my_int = 0 # wrong

        def foo(self):
            self.my_int += 1

The problem with the above is that the current value of ``my_int`` will be shared by all player instances.
Instead you should do this:

.. code-block::python

    class Player(BasePlayer):

        my_int = models.IntegerField(initial=1) # right

        def foo(self):
            self.my_int += 1

Only generate random values inside methods
------------------------------------------

If you want a field whose initial value is random,
you might initially try this incorrect approach:

.. code-block:: python

    class Player(BasePlayer):

        factor = models.FloatField(initial=random.random()) # wrong

Python loads this code only once each time you run the ``otree`` command (e.g. ``resetdb`` or ``runserver``, etc.).
So ``random.random()`` is just evaluated once globally, not for each new session or player.
That means every player will end up with the same "random" value,
until you restart the server.

Instead, you should generate the random variables in :ref:`before_session_starts`.

For the same reason, this will not work either:

.. code-block:: python

    class Constants(BaseConstants):
        factor = random.random() # wrong

