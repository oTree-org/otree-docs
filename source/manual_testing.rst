Manual testing
==============

You can launch your app on your local development machine to test it,
and then when you are satisfied, you can deploy it to a server.

Debugging
~~~~~~~~~

Debugging with PyCharm
^^^^^^^^^^^^^^^^^^^^^^

PyCharm has an excellent debugger that you might want to try using.
You can insert a breakpoint into your code by clicking in the left-hand
margin on a line of code. You will see a little red dot. Then reload the
page and the debugger will pause when it hits your line of code. At this
point you can inspect the state of all the local variables, execute
print statements in the built-in intepreter, and step through the code
line by line.

More on the PyCharm debugger
`here <http://www.jetbrains.com/pycharm/webhelp/debugging.html>`__.

Debugging in the command shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To test your app from an interactive Python shell, do:

.. code-block:: shell

   $ otree shell

Then you can debug your code and inspect objects in your database.
For example, if you already ran a "public goods game" session in your browser,
you can access the database objects in Python like this:

.. code-block:: python

   >>> from public_goods.models import Player
   >>> players = Player.objects.all()
   >>> ...


