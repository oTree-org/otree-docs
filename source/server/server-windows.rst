.. _server-windows:

Windows Server (advanced)
=========================

If you are just testing your app on your personal computer, you can use
``otree zipserver`` or ``otree devserver``. You don't need a full server setup as described below,
which is necessary for sharing your app with an audience.

This section is for people who are experienced with setting up web servers.
If you would like an easier and quicker way, we recommend using
:ref:`Heroku <heroku>`.

.. _why-server:

Why do I need to install server software?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

oTree's development setup (``devserver``)
is not designed for running actual studies.


Database (Postgres)
-------------------

If you want, you can use Postgres as your production database.
Install Postgres and psycopg2, create a new database and set the ``DATABASE_URL`` env var, for example:
to ``postgres://postgres@localhost/django_db``

However, in principle, oTree 3.0+ should do fine with its default SQLite in production,
since the server is now is single threaded.

resetdb
~~~~~~~

If all the above steps went well, you should be able to run ``otree resetdb``.

.. _redis-windows:

Install Redis
-------------

You should download and run `Redis for Windows <https://github.com/MSOpenTech/redis/releases>`__.

Redis should be running on port 6379. You can test with ``redis-cli ping``,
which should output ``PONG``.

Set your ``REDIS_URL`` env var to ``redis://localhost:6379`` in the same place where you set ``DATABASE_URL``.

Run the production server
-------------------------

Run::

    otree prodserver 80

See :ref:`here <prodserver>` for full instructions.
The steps are essentially the same as on Linux.

Set environment variables
-------------------------

You should set ``OTREE_ADMIN_PASSWORD``, ``OTREE_PRODUCTION``, and ``OTREE_AUTH_LEVEL``.

Allow other computers to connect
--------------------------------

See instructions :ref:`here <server-adhoc>`.
