.. _heroku:

Server setup (basic/Heroku)
===========================

If you are just testing your app on your personal computer, you can use
``otree runserver``. You don't need a full server setup.

However, when you want to share your app with an audience,
you must deploy to a web server.

Heroku is the simplest option, and we recommend it for most people.

However, because oTree is based on Django,
you can use any server or database supported by Django.
Ubuntu and Windows instructions are available below for more advanced deployments,
or for people who do not wish to use a cloud server.


.. toctree::
    :maxdepth: 2

    heroku.rst
    ubuntu.rst
    windows.rst