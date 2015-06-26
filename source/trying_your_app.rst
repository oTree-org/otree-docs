Trying your app
===============

You can launch your app on your local development machine to test it,
and then when you are satisfied, you can deploy it to a server.

Testing locally
~~~~~~~~~~~~~~~

You will be testing your app frequently during development, so that you
can see how the app looks and feels and discover bugs during
development. To test your app, run the server in the oTree launcher. You
may need to reset the database first.

Click on a session name and you will get a start link for the
experimenter, as well as the links for all the participants. You can
open all the start links in different tabs and simulate playing as
multiple participants simultaneously.

You can send the demo page link to your colleagues or publish it to a
public audience.

Debugging
~~~~~~~~~

Once you start playing your app, you will sometimes get a yellow Django
error page with lots of details. To troubleshoot this, look at the error
message and "Exception location" fields. If the exception location is
somewhere outside of your app's code (like if it points to an installed
module like Django or oTree), look through the "Traceback" section to
see if it passes through your code. Once you have found a reference to a
line of code in your app, go to that line of code and see if the error
message can help you pinpoint an error in your code. Googling the error
name or message will often take you to pages that explain the meaning of
the error and how to fix it.

Debugging with PyCharm
^^^^^^^^^^^^^^^^^^^^^^

PyCharm has an excellent debugger that you should be using continuously.
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

To test your app from an interactive Python shell, you can run this command:

.. code:: shell

   $ python otree shell

Then you can run code that inspects objects already in your database.
For example, if you already ran a "public goods game" session in your browser,
you can access the database objects in Python like this:

.. code:: python

   >>> from public_goods.models import Player
   >>> players = Player.objects.all()
   >>> ...


