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

.. code-block::python

    def my_method(self):
        Constants.my_list.append(1)

``Constants`` has global scope, so when you do this, your modification will "leak" to all other sessions,
until the server is restarted. Instead, if you want a variable that is the same for all players in your session,
you should set a field on the subsession, or use :ref:`session_vars`.

For the same reason, you shouldn't assign to class attributes on your models.
For example, don't do this:

.. code-block::python

    class Player(BasePlayer):

        my_list = []

        def foo(self):
            self.my_list.append(1)


