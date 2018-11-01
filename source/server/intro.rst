.. _server:

Server setup
============

If you are just testing your app on your personal computer, you can use
``otree devserver``. You don't need a full server setup.

However, when you want to share your app with an audience,
you must use a web server.

Choose which option you need:

**You want to launch your app to users on the internet**

Use :ref:`Heroku <heroku>`.

**You want the easiest setup**

Again, we recommend :ref:`Heroku <heroku>`.

**You want to use your own computer as a server on your local network**

e.g. running a lab study or field study.
Follow these steps:

1.   :ref:`Conventional installation <server-windows>` (macOS instructions not available yet)
2.   Set up your PC as an :ref:`ad-hoc server <server-adhoc>`


**You want to set up a dedicated Linux server**

:ref:`Ubuntu Linux <server-ubuntu>` instructions.

**You want to see other options**

See :ref:`community` for some virtual machines created by oTree users,
such as the
`oTree Virtual Machine Manager <otree-virtual-machine-manager.readthedocs.io/>`__.

**Next steps**
After setting up your server, see :ref:`server_final_steps`.

..  Consider removing the toctree because I think it's better for people to read
    through the instructions above, rather than jumping into a page they don't
    understand. Or, add info to the individual pages above, so incoming visitors
    don't bark up the wrong tree

.. toctree::
    :maxdepth: 2

    heroku.rst
    server-windows.rst
    adhoc.rst
    ubuntu.rst
    dockerhub.rst
    next_steps.rst
    git.rst
