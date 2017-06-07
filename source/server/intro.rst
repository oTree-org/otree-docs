Server setup
============

If you are just testing your app on your personal computer, you can use
``otree runserver``. You don't need a full server setup.

However, when you want to share your app with an audience,
you must use a web server.

If you want to deploy on the internet, :ref:`Heroku <heroku>` is the simplest option,
and we recommend it for most people.

You can also use your own Windows/Mac computer as a temporary server,
as long as you only need the app to be accessed by devices on the local network,
Instructions for Windows are :ref:`here <server-windows>`.

Because oTree is based on Django,
you can use any server or database supported by Django.
Docker and Ubuntu instructions are available below for more advanced deployments,
or for people who do not wish to use a cloud server.

.. toctree::
    :maxdepth: 2

    heroku.rst
    docker.rst
    ubuntu.rst
    windows.rst
    next_steps.rst
    git.rst
