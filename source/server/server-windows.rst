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

Install Postgres and psycopg2, create a new database and set the ``DATABASE_URL`` env var, for example:
to ``postgres://postgres@localhost/django_db``

resetdb
~~~~~~~

If all the above steps went well, you should be able to run ``otree resetdb``.

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
